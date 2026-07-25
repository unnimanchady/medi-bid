import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# I will replace the patient_secure_messages route
new_route = """def patient_secure_messages():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    
    threads = []
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    if profiles:
        profile_ids = [p.id for p in profiles]
        requests = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).all()
        if requests:
            request_ids = [r.id for r in requests]
            threads = MessageThread.query.filter(MessageThread.treatment_request_id.in_(request_ids)).all()
        
    return render_template("patient-secure-messages.html", user=user, threads=threads)"""

c = re.sub(r'def patient_secure_messages\(\):.*?(?=\n\n\n@app.route)', new_route, c, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
