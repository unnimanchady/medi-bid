import os

def patch():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. patient_login guard update
    content = content.replace(
        "if 'registration_user_id' in session:\n        return redirect(url_for('patient_dashboard'))",
        "if session.get('patient_authenticated'):\n        return redirect(url_for('patient_dashboard'))"
    )

    # 2. patient_login authentication flag
    content = content.replace(
        "session['registration_user_id'] = user.id\n            return redirect(url_for('patient_dashboard'))",
        "session['registration_user_id'] = user.id\n            session['patient_authenticated'] = True\n            return redirect(url_for('patient_dashboard'))"
    )
    
    # 3. patient_logout route
    logout_code = """
@app.route("/patient/logout")
def patient_logout():
    session.pop('registration_user_id', None)
    session.pop('patient_authenticated', None)
    return redirect(url_for('patient_login'))

@app.route("/patient/register/who", methods=["GET", "POST"])"""
    content = content.replace(
        '@app.route("/patient/register/who", methods=["GET", "POST"])',
        logout_code
    )

    # 4. patient_registration_step6 authentication flag
    content = content.replace(
        "session['last_request_reference'] = reference_id\n            \n            return redirect(url_for('patient_registration_success'))",
        "session['last_request_reference'] = reference_id\n            session['patient_authenticated'] = True\n            return redirect(url_for('patient_registration_success'))"
    )
    
    # 5. Add guards to all registration steps
    steps = [
        ('def patient_registration_step1():', 'def patient_registration_step1():\n    if session.get("patient_authenticated"):\n        return redirect(url_for("patient_dashboard"))'),
        ('def patient_registration_who():', 'def patient_registration_who():\n    if session.get("patient_authenticated"):\n        return redirect(url_for("patient_dashboard"))'),
        ('def patient_registration_step2():', 'def patient_registration_step2():\n    if session.get("patient_authenticated"):\n        return redirect(url_for("patient_dashboard"))'),
        ('def patient_registration_step3():', 'def patient_registration_step3():\n    if session.get("patient_authenticated"):\n        return redirect(url_for("patient_dashboard"))'),
        ('def patient_registration_step4():', 'def patient_registration_step4():\n    if session.get("patient_authenticated"):\n        return redirect(url_for("patient_dashboard"))'),
        ('def patient_registration_step5():', 'def patient_registration_step5():\n    if session.get("patient_authenticated"):\n        return redirect(url_for("patient_dashboard"))'),
        ('def patient_registration_step6():', 'def patient_registration_step6():\n    if session.get("patient_authenticated"):\n        return redirect(url_for("patient_dashboard"))')
    ]
    for old, new in steps:
        content = content.replace(old, new, 1)
        
    # 6. hospital_login guard
    # original:
    # @app.route("/hospital/login", methods=["GET", "POST"])
    # def hospital_login():
    #     error = None
    hospital_login_new = """@app.route("/hospital/login", methods=["GET", "POST"])
def hospital_login():
    if session.get('hospital_id'):
        return redirect(url_for('hospital_dashboard'))
    error = None"""
    content = content.replace(
        '@app.route("/hospital/login", methods=["GET", "POST"])\ndef hospital_login():\n    error = None',
        hospital_login_new
    )
    
    # 7. hospital_register guard
    hospital_reg_old = """    existing_hospital_id = session.get('hospital_id')
    if existing_hospital_id:
        existing_hospital = Hospital.query.get(existing_hospital_id)
        if existing_hospital:
            if existing_hospital.verification_status != "incomplete":
                return redirect(url_for('hospital_register_success'))
            return redirect(url_for('hospital_register_info'))"""
            
    hospital_reg_new = """    existing_hospital_id = session.get('hospital_id')
    if existing_hospital_id:
        return redirect(url_for('hospital_dashboard'))"""
        
    content = content.replace(hospital_reg_old, hospital_reg_new)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done safely patching.")

if __name__ == '__main__':
    patch()
