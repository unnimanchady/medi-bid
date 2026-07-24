import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_route = """@app.route("/patient/compare-hospitals")
def patient_compare_hospitals():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    requests = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).all()
    request_ids = [r.id for r in requests]
    
    proposals = TreatmentProposal.query.filter(
        TreatmentProposal.treatment_request_id.in_(request_ids),
        TreatmentProposal.status == 'submitted'
    ).order_by(TreatmentProposal.created_at.desc()).limit(3).all()
    
    # Pad to ensure 3 proposals for the hardcoded layout if necessary
    p1_id = proposals[0].id if len(proposals) > 0 else 0
    p2_id = proposals[1].id if len(proposals) > 1 else 0
    p3_id = proposals[2].id if len(proposals) > 2 else 0
    
    return render_template("patient-compare-hospitals.html", p1_id=p1_id, p2_id=p2_id, p3_id=p3_id)"""

new_route = """@app.route("/patient/compare-hospitals")
def patient_compare_hospitals():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    req_id = request.args.get('request_id', type=int)
    prop_ids = request.args.get('proposal_ids')
    
    if req_id:
        target_req = TreatmentRequest.query.filter_by(id=req_id).first()
        if not target_req or target_req.patient_profile_id not in profile_ids:
            target_req = None
    else:
        # Fallback to the latest request that has submitted proposals
        all_reqs = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).order_by(TreatmentRequest.created_at.desc()).all()
        target_req = None
        for r in all_reqs:
            props = TreatmentProposal.query.filter_by(treatment_request_id=r.id, status='submitted').count()
            if props > 0:
                target_req = r
                break
                
    compare_items = []
    if target_req:
        q = TreatmentProposal.query.filter_by(treatment_request_id=target_req.id, status='submitted')
        if prop_ids:
            id_list = [int(i.strip()) for i in prop_ids.split(',') if i.strip().isdigit()]
            if id_list:
                q = q.filter(TreatmentProposal.id.in_(id_list))
                
        proposals = q.limit(3).all()
        for p in proposals:
            h = Hospital.query.get(p.hospital_id)
            if h:
                compare_items.append({'proposal': p, 'hospital': h})
                
    return render_template("patient-compare-hospitals.html", compare_items=compare_items, target_req=target_req)"""

if old_route in content:
    content = content.replace(old_route, new_route)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated patient_compare_hospitals route in app.py successfully.")
else:
    print("Could not find the exact old_route in app.py.")
