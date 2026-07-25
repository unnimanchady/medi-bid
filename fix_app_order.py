import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# First we need to extract the patient_requests route
route_block = """@app.route('/patient/requests')
def patient_requests():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('patient_registration_step1'))
        
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    if profile_ids:
        requests = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).order_by(TreatmentRequest.created_at.desc()).all()
    else:
        requests = []
        
    return render_template('patient-requests.html', user=user, requests=requests)"""

# Remove it from wherever it is
c = c.replace(route_block, '')

# And also remove if __name__ == "__main__":
main_block = """if __name__ == "__main__":
    app.run(debug=True)"""
c = c.replace(main_block, '')

# Now put them back in the correct order
c = c.strip() + '\n\n' + route_block + '\n\n' + main_block + '\n'

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
