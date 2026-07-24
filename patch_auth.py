import re

def apply_auth_guards():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Patient guards
    patient_funcs = [
        'def patient_login():',
        'def patient_registration_who():',
        'def patient_registration_step1():',
        'def patient_registration_step2():',
        'def patient_registration_step3():',
        'def patient_registration_step4():',
        'def patient_registration_step5():',
        'def patient_registration_step6():'
    ]
    
    patient_guard = """
    if session.get('registration_user_id'):
        return redirect(url_for('patient_dashboard'))"""

    for func in patient_funcs:
        # Check if already guarded
        if patient_guard in content.split(func)[1][:200]:
            continue
        content = content.replace(func, func + patient_guard, 1)

    # Hospital guards
    hospital_funcs = [
        'def hospital_login():',
        'def hospital_register():'
    ]
    
    hospital_guard = """
    if session.get('hospital_id'):
        return redirect(url_for('hospital_dashboard'))"""
        
    for func in hospital_funcs:
        if hospital_guard in content.split(func)[1][:200]:
            continue
        content = content.replace(func, func + hospital_guard, 1)

    # Admin guard
    admin_funcs = [
        'def admin_login():'
    ]
    
    admin_guard = """
    if session.get('admin_id'):
        user = User.query.get(session.get('admin_id'))
        if user and user.role == 'admin':
            return redirect(url_for('admin_dashboard'))"""
            
    for func in admin_funcs:
        if admin_guard in content.split(func)[1][:200]:
            continue
        content = content.replace(func, func + admin_guard, 1)

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Guards applied.")

if __name__ == '__main__':
    apply_auth_guards()
