import re

def patch_routes():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # PATIENT LOGIN
    patient_login_guard = """@app.route("/patient/login", methods=["GET", "POST"])
def patient_login():
    if session.get('patient_authenticated'):
        return redirect(url_for('patient_dashboard'))"""
    
    # We replace the original patient_login start
    content = re.sub(
        r'@app\.route\("/patient/login", methods=\["GET", "POST"\]\)\ndef patient_login\(\):\n\s*if \'registration_user_id\' in session:\n\s*return redirect\(url_for\(\'patient_dashboard\'\)\)',
        patient_login_guard,
        content
    )
    
    # We need to set patient_authenticated = True when login succeeds
    content = content.replace(
        "session['registration_user_id'] = user.id\n            return redirect(url_for('patient_dashboard'))",
        "session['registration_user_id'] = user.id\n            session['patient_authenticated'] = True\n            return redirect(url_for('patient_dashboard'))"
    )

    # We need to set patient_authenticated = True when step 6 succeeds
    # Let's find patient_registration_step6 success
    # It sets session['last_request_reference'] = reference_id
    content = content.replace(
        "session['last_request_reference'] = reference_id\n            \n            return redirect(url_for('patient_registration_success'))",
        "session['last_request_reference'] = reference_id\n            session['patient_authenticated'] = True\n            return redirect(url_for('patient_registration_success'))"
    )
    
    # Also in patient_logout, we clear it
    content = content.replace(
        "session.pop('registration_user_id', None)",
        "session.pop('registration_user_id', None)\n    session.pop('patient_authenticated', None)"
    )

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

    # Also there is a "/patient/register" route in the prompt, let's make sure it's covered by who or step-1.
    # We already guarded who and step1.
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Guards applied via AST/Regex.")

if __name__ == '__main__':
    patch_routes()
