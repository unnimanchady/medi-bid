import os
import re

app_py = 'app.py'

with open(app_py, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update admin_dashboard
old_dashboard = """@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    pending_count = Hospital.query.filter_by(verification_status="pending_verification").count()
    verified_count = Hospital.query.filter_by(verification_status="verified").count()
    total_count = Hospital.query.count()
    
    return render_template(
        "admin-dashboard.html",
        pending_count=pending_count,
        verified_count=verified_count,
        total_count=total_count
    )"""

new_dashboard = """@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    total_patients = User.query.filter_by(role='patient').count()
    total_hospitals = Hospital.query.count()
    active_requests = TreatmentRequest.query.filter(TreatmentRequest.status.in_(['Active', 'Pending'])).count()
    submitted_proposals = TreatmentProposal.query.filter_by(status='submitted').count()
    pending_count = Hospital.query.filter_by(verification_status="pending_verification").count()
    
    # Recent activity
    recent_requests = TreatmentRequest.query.order_by(TreatmentRequest.created_at.desc()).limit(5).all()
    recent_hospitals = Hospital.query.order_by(Hospital.created_at.desc()).limit(5).all()
    
    recent_activity = []
    for r in recent_requests:
        recent_activity.append({
            'type': 'request',
            'title': f'New Treatment Request ({r.reference_id})',
            'time': r.created_at,
            'url': url_for('admin_treatment_request_detail', reference_id=r.reference_id)
        })
    for h in recent_hospitals:
        recent_activity.append({
            'type': 'hospital',
            'title': f'Hospital Registration ({h.hospital_name})',
            'time': h.created_at,
            'url': url_for('admin_application_review', hospital_id=h.id)
        })
        
    recent_activity.sort(key=lambda x: x['time'], reverse=True)
    recent_activity = recent_activity[:5]
    
    return render_template(
        "admin-dashboard.html",
        total_patients=total_patients,
        total_hospitals=total_hospitals,
        active_requests=active_requests,
        submitted_proposals=submitted_proposals,
        pending_count=pending_count,
        recent_activity=recent_activity
    )"""

content = content.replace(old_dashboard, new_dashboard)

# 2. Update admin_application_review to handle POST for admin_notes
old_review = """@app.route("/admin/hospitals/applications/<int:hospital_id>/review")
@admin_required
def admin_application_review(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    error = request.args.get('error')
    return render_template("admin-application-review.html", hospital=hospital, error=error)"""

new_review = """@app.route("/admin/hospitals/applications/<int:hospital_id>/review", methods=["GET", "POST"])
@admin_required
def admin_application_review(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    error = request.args.get('error')
    
    if request.method == "POST":
        notes = request.form.get("admin_notes", "").strip()
        hospital.admin_notes = notes
        db.session.commit()
        flash("Admin notes saved.", "success")
        return redirect(url_for("admin_application_review", hospital_id=hospital.id))
        
    return render_template("admin-application-review.html", hospital=hospital, error=error)"""

content = content.replace(old_review, new_review)

# 3. Update admin_treatment_requests filters
old_requests = """@app.route("/admin/treatment-requests")
@admin_required
def admin_treatment_requests():
    status_filter = request.args.get('status')
    search_query = request.args.get('q')
    
    query = TreatmentRequest.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if search_query:
        query = query.join(PatientProfile).filter(
            (TreatmentRequest.reference_id.ilike(f"%{search_query}%")) |
            (PatientProfile.first_name.ilike(f"%{search_query}%")) |
            (PatientProfile.last_name.ilike(f"%{search_query}%"))
        )
        
    requests_list = query.order_by(TreatmentRequest.created_at.desc()).all()
    
    for req in requests_list:
        req.response_count = TreatmentProposal.query.filter_by(treatment_request_id=req.id, status='submitted').count()
        
    return render_template("admin-treatment-requests.html", requests=requests_list, current_status=status_filter, search_query=search_query)"""

new_requests = """@app.route("/admin/treatment-requests")
@admin_required
def admin_treatment_requests():
    status_filter = request.args.get('status')
    specialty_filter = request.args.get('specialty')
    country_filter = request.args.get('country')
    search_query = request.args.get('q')
    
    query = TreatmentRequest.query.join(PatientProfile)
    
    if status_filter:
        query = query.filter(TreatmentRequest.status == status_filter)
        
    if specialty_filter:
        query = query.filter(TreatmentRequest.specialty == specialty_filter)
        
    if country_filter:
        query = query.filter(PatientProfile.country_of_residence == country_filter)
        
    if search_query:
        query = query.filter(
            (TreatmentRequest.reference_id.ilike(f"%{search_query}%")) |
            (PatientProfile.first_name.ilike(f"%{search_query}%")) |
            (PatientProfile.last_name.ilike(f"%{search_query}%"))
        )
        
    requests_list = query.order_by(TreatmentRequest.created_at.desc()).all()
    
    for req in requests_list:
        req.response_count = TreatmentProposal.query.filter_by(treatment_request_id=req.id, status='submitted').count()
        
    return render_template(
        "admin-treatment-requests.html", 
        requests=requests_list, 
        current_status=status_filter, 
        current_specialty=specialty_filter,
        current_country=country_filter,
        search_query=search_query
    )"""

content = content.replace(old_requests, new_requests)

# 4. Add Patient and Proposal routes
new_admin_routes = """
@app.route("/admin/patients")
@admin_required
def admin_patients():
    search_query = request.args.get('q')
    
    query = User.query.filter_by(role='patient')
    if search_query:
        query = query.filter(
            (User.email.ilike(f"%{search_query}%")) |
            (User.first_name.ilike(f"%{search_query}%")) |
            (User.last_name.ilike(f"%{search_query}%"))
        )
        
    patients = query.order_by(User.created_at.desc()).all()
    return render_template("admin-patients.html", patients=patients, search_query=search_query)

@app.route("/admin/patients/<int:user_id>")
@admin_required
def admin_patient_detail(user_id):
    patient = User.query.filter_by(id=user_id, role='patient').first_or_404()
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    
    profile_ids = [p.id for p in profiles]
    requests = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).order_by(TreatmentRequest.created_at.desc()).all()
    
    for req in requests:
        req.response_count = TreatmentProposal.query.filter_by(treatment_request_id=req.id, status='submitted').count()
        
    return render_template("admin-patient-detail.html", patient=patient, profiles=profiles, requests=requests)

@app.route("/admin/proposals")
@admin_required
def admin_proposals():
    hospital_id = request.args.get('hospital_id')
    status_filter = request.args.get('status')
    
    query = TreatmentProposal.query.join(TreatmentRequest)
    
    if hospital_id:
        query = query.filter(TreatmentProposal.hospital_id == hospital_id)
        
    if status_filter:
        query = query.filter(TreatmentProposal.status == status_filter)
        
    proposals = query.order_by(TreatmentProposal.created_at.desc()).all()
    
    hospitals = Hospital.query.order_by(Hospital.hospital_name.asc()).all()
    
    return render_template("admin-proposals.html", proposals=proposals, hospitals=hospitals, current_status=status_filter, current_hospital=hospital_id)
"""

if 'def admin_patients(' not in content:
    content = content.replace('# =========================================================\n# DEVELOPMENT SERVER', new_admin_routes + '\n\n# =========================================================\n# DEVELOPMENT SERVER')


with open(app_py, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with new Admin Portal routes.")
