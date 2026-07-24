import re

def patch_routes():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # PATIENT LOGIN
    patient_login_guard = """@app.route("/patient/login", methods=["GET", "POST"])
def patient_login():
    if session.get('patient_authenticated'):
        return redirect(url_for('patient_dashboard'))"""
    
    content = re.sub(
        r'@app\.route\("/patient/login", methods=\["GET", "POST"\]\)\ndef patient_login\(\):\n\s*if \'registration_user_id\' in session:\n\s*return redirect\(url_for\(\'patient_dashboard\'\)\)',
        patient_login_guard,
        content
    )
    
    content = content.replace(
        "session['registration_user_id'] = user.id\n            return redirect(url_for('patient_dashboard'))",
        "session['registration_user_id'] = user.id\n            session['patient_authenticated'] = True\n            return redirect(url_for('patient_dashboard'))"
    )

    # PATIENT SUCCESS
    content = content.replace(
        "session['last_request_reference'] = reference_id\n            \n            return redirect(url_for('patient_registration_success'))",
        "session['last_request_reference'] = reference_id\n            session['patient_authenticated'] = True\n            return redirect(url_for('patient_registration_success'))"
    )
    
    # PATIENT LOGOUT (Precise)
    logout_target = """@app.route("/patient/logout")
def patient_logout():
    session.pop('registration_user_id', None)
    return redirect(url_for('patient_login'))"""

    logout_replacement = """@app.route("/patient/logout")
def patient_logout():
    session.pop('registration_user_id', None)
    session.pop('patient_authenticated', None)
    return redirect(url_for('patient_login'))"""

    content = content.replace(logout_target, logout_replacement)

    # NOW add the guard to all registration steps
    patient_funcs = [
        'def patient_registration_who():',
        'def patient_registration_step1():',
        'def patient_registration_step2():',
        'def patient_registration_step3():',
        'def patient_registration_step4():',
        'def patient_registration_step5():',
        'def patient_registration_step6():'
    ]
    
    patient_guard = """
    if session.get('patient_authenticated'):
        return redirect(url_for('patient_dashboard'))"""

    for func in patient_funcs:
        if patient_guard in content.split(func)[1][:200]:
            continue
        content = content.replace(func, func + patient_guard, 1)

    # HOSPITAL LOGIN
    hospital_login_guard = """@app.route("/hospital/login", methods=["GET", "POST"])
def hospital_login():
    if session.get('hospital_id'):
        return redirect(url_for('hospital_dashboard'))"""
        
    content = re.sub(
        r'@app\.route\("/hospital/login", methods=\["GET", "POST"\]\)\ndef hospital_login\(\):',
        hospital_login_guard,
        content
    )

    # HOSPITAL REGISTER
    hospital_register_pattern = r'existing_hospital_id = session\.get\(\'hospital_id\'\)\n\s*if existing_hospital_id:\n\s*existing_hospital = Hospital\.query\.get\(existing_hospital_id\)\n\s*if existing_hospital:\n\s*if existing_hospital\.verification_status != "incomplete":\n\s*return redirect\(url_for\(\'hospital_register_success\'\)\)\n\s*return redirect\(url_for\(\'hospital_register_info\'\)\)'
    
    hospital_register_replacement = """existing_hospital_id = session.get('hospital_id')
    if existing_hospital_id:
        return redirect(url_for('hospital_dashboard'))"""
        
    content = re.sub(hospital_register_pattern, hospital_register_replacement, content)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Guards applied via AST/Regex.")

if __name__ == '__main__':
    patch_routes()
