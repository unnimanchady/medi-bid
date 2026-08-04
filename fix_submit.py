import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''@app.route("/hospital/treatment-requests/<string:reference_id>/proposal/submit", methods=['POST'])
def hospital_proposal_submit(reference_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        abort(403)
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403, description="This treatment request is no longer active.")
        
    proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first_or_404()
    if proposal.status == 'submitted':
        flash("Proposal already submitted.", "info")
        return redirect(url_for('hospital_proposal_view', reference_id=reference_id))
        
    # Validation logic
    if not proposal.proposed_treatment or not proposal.treatment_plan:
        flash("Treatment details are required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if not proposal.currency or proposal.estimated_cost_min is None or proposal.estimated_cost_max is None:
        flash("Valid cost estimates are required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if proposal.estimated_cost_min <= 0 or proposal.estimated_cost_max < proposal.estimated_cost_min:
        flash("Invalid cost ranges.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if not proposal.valid_until:
        flash("Validity date is required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    today = datetime.now(timezone.utc).date()
    try:
        max_date = today.replace(year=today.year + 1)
    except ValueError:
        max_date = today.replace(year=today.year + 1, month=2, day=28)
        
    if proposal.valid_until < today:
        flash("Validity date cannot be in the past.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if proposal.valid_until > max_date:
        flash("Validity date cannot be more than 1 year from today.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    proposal.status = "submitted"
    proposal.submitted_at = datetime.now(timezone.utc)
    db.session.commit()
    
    flash("Proposal submitted successfully.", "success")
    return redirect(url_for('hospital_proposal_view', reference_id=reference_id))'''

new_func = '''@app.route("/hospital/treatment-requests/<string:reference_id>/proposal/submit", methods=['POST'])
def hospital_proposal_submit(reference_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        if is_ajax: return jsonify({"status": "error", "message": "Not logged in"}), 401
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        if is_ajax: return jsonify({"status": "error", "message": "Forbidden"}), 403
        abort(403)
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        if is_ajax: return jsonify({"status": "error", "message": "Request no longer active"}), 400
        abort(403, description="This treatment request is no longer active.")
        
    proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first_or_404()
    if proposal.status == 'submitted':
        if is_ajax: return jsonify({"status": "success", "redirect_url": url_for('hospital_proposal_view', reference_id=reference_id)})
        flash("Proposal already submitted.", "info")
        return redirect(url_for('hospital_proposal_view', reference_id=reference_id))
        
    # Validation logic
    if not proposal.proposed_treatment or not proposal.treatment_plan:
        if is_ajax: return jsonify({"status": "error", "message": "Treatment details are required."}), 400
        flash("Treatment details are required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if not proposal.currency or proposal.estimated_cost_min is None or proposal.estimated_cost_max is None:
        if is_ajax: return jsonify({"status": "error", "message": "Valid cost estimates are required."}), 400
        flash("Valid cost estimates are required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if proposal.estimated_cost_min <= 0 or proposal.estimated_cost_max < proposal.estimated_cost_min:
        if is_ajax: return jsonify({"status": "error", "message": "Invalid cost ranges."}), 400
        flash("Invalid cost ranges.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if not proposal.valid_until:
        if is_ajax: return jsonify({"status": "error", "message": "Validity date is required."}), 400
        flash("Validity date is required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    today = datetime.now(timezone.utc).date()
    try:
        max_date = today.replace(year=today.year + 1)
    except ValueError:
        max_date = today.replace(year=today.year + 1, month=2, day=28)
        
    if proposal.valid_until < today:
        if is_ajax: return jsonify({"status": "error", "message": "Validity date cannot be in the past."}), 400
        flash("Validity date cannot be in the past.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if proposal.valid_until > max_date:
        if is_ajax: return jsonify({"status": "error", "message": "Validity date cannot be more than 1 year from today."}), 400
        flash("Validity date cannot be more than 1 year from today.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    try:
        proposal.status = "submitted"
        proposal.submitted_at = datetime.now(timezone.utc)
        db.session.commit()
        
        # Add Notification Trigger
        try:
            create_notification(
                recipient_type='patient',
                recipient_user_id=req.patient_id,
                title="New Proposal Received",
                message=f"{hospital.legal_name} has submitted a new proposal for your request.",
                notification_type='proposal',
                reference_type='TreatmentProposal',
                reference_id=proposal.id,
                target_url=url_for('patient_treatment_proposal_details', proposal_id=proposal.id)
            )
        except Exception as e:
            print("Failed to create notification:", str(e))
            
    except Exception as e:
        db.session.rollback()
        if is_ajax: return jsonify({"status": "error", "message": "Database error: " + str(e)}), 500
        flash("Database error: " + str(e), "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
    
    if is_ajax:
        return jsonify({"status": "success", "redirect_url": url_for('hospital_proposal_view', reference_id=reference_id)})
        
    flash("Proposal submitted successfully.", "success")
    return redirect(url_for('hospital_proposal_view', reference_id=reference_id))'''

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Could not find old_func")
