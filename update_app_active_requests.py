import os
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. hospital_treatment_requests
old_list = '''@app.route("/hospital/treatment-requests")
def hospital_treatment_requests():
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        return redirect(url_for('hospital_dashboard'))
        
    all_active_requests = TreatmentRequest.query.filter_by(status='Active').order_by(TreatmentRequest.created_at.desc()).all()
    
    eligible_requests = []
    for req in all_active_requests:
        if _is_hospital_eligible(hospital, req.specialty):
            eligible_requests.append(req)
            
    return render_template("hospital-treatment-requests.html", requests=eligible_requests, hospital=hospital)'''

new_list = '''@app.route("/hospital/treatment-requests")
def hospital_treatment_requests():
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        return redirect(url_for('hospital_dashboard'))
        
    # UI Filters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    country_filter = request.args.get('country', '').strip()
    sort_order = request.args.get('sort', 'newest')

    query = TreatmentRequest.query.filter(
        TreatmentRequest.status.notin_(['Closed', 'Completed', 'Cancelled', 'Expired']),
        TreatmentRequest.status == 'Active'
    )
    
    if search_query:
        query = query.filter(db.or_(
            TreatmentRequest.reference_id.ilike(f"%{search_query}%"),
            TreatmentRequest.specialty.ilike(f"%{search_query}%"),
            TreatmentRequest.primary_diagnosis.ilike(f"%{search_query}%")
        ))
        
    if category_filter:
        query = query.filter(TreatmentRequest.specialty.ilike(f"%{category_filter}%"))
        
    if country_filter:
        # Need to join PatientProfile to search by country
        from models import PatientProfile
        query = query.join(PatientProfile).filter(PatientProfile.country.ilike(f"%{country_filter}%"))
        
    if sort_order == 'oldest':
        query = query.order_by(TreatmentRequest.created_at.asc())
    else:
        query = query.order_by(TreatmentRequest.created_at.desc())

    paginated_requests = query.paginate(page=page, per_page=20, error_out=False)
    
    # Pre-fetch hospital proposals to determine button states
    from models import TreatmentProposal
    proposals = TreatmentProposal.query.filter_by(hospital_id=hospital.id).all()
    hospital_proposals = {p.treatment_request_id: p for p in proposals}
            
    return render_template(
        "hospital-treatment-requests.html", 
        requests=paginated_requests, 
        hospital=hospital,
        hospital_proposals=hospital_proposals,
        search=search_query,
        category=category_filter,
        country=country_filter,
        sort=sort_order
    )'''

content = content.replace(old_list, new_list)

# 2. hospital_treatment_request_detail
old_detail = '''@app.route("/hospital/treatment-requests/<string:reference_id>")
def hospital_treatment_request_detail(reference_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        return redirect(url_for('hospital_dashboard'))
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    
    if not _is_hospital_eligible(hospital, req.specialty):
        abort(403, description="You are not authorized to view this treatment request.")
        
    return render_template("hospital-treatment-request-detail.html", req=req, hospital=hospital)'''

new_detail = '''@app.route("/hospital/treatment-requests/<string:reference_id>")
def hospital_treatment_request_detail(reference_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        return redirect(url_for('hospital_dashboard'))
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403, description="This treatment request is no longer active.")
        
    from models import TreatmentProposal
    existing_proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first()
        
    return render_template("hospital-treatment-request-detail.html", req=req, hospital=hospital, existing_proposal=existing_proposal)'''

content = content.replace(old_detail, new_detail)

# 3. document routes
old_doc_1 = '''    if not _is_hospital_eligible(hospital, req.specialty):
        abort(403)
        
    return send_from_directory(UPLOAD_FOLDER, doc.storage_filename)'''

new_doc_1 = '''    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403)
        
    return send_from_directory(UPLOAD_FOLDER, doc.storage_filename)'''

content = content.replace(old_doc_1, new_doc_1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py successfully!")
