import re

# 1. Update app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()
    
old_route = """@app.route("/patient/compare-hospitals")
def patient_compare_hospitals():
    return render_template("patient-compare-hospitals.html")"""

new_route = """@app.route("/patient/compare-hospitals")
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

app_code = app_code.replace(old_route, new_route)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

# 2. Update patient-compare-hospitals.html
with open('templates/patient-compare-hospitals.html', 'r', encoding='utf-8') as f:
    html_code = f.read()

# Replace the three instances with the three different proposal IDs
parts = html_code.split("url_for('patient_treatment_proposal_details')")
if len(parts) == 4:
    new_html = parts[0] + "url_for('patient_treatment_proposal_details', proposal_id=p1_id)" + parts[1] + "url_for('patient_treatment_proposal_details', proposal_id=p2_id)" + parts[2] + "url_for('patient_treatment_proposal_details', proposal_id=p3_id)" + parts[3]
    with open('templates/patient-compare-hospitals.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Fixed patient-compare-hospitals.html successfully.")
else:
    print(f"Error: Found {len(parts) - 1} instances of url_for in the template, expected 3.")
