import re

# Fix app.py hospital login logic
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

hospital_login_new = '''@app.route("/hospital/login", methods=["GET", "POST"])
def hospital_login():
    error = None
    if request.method == "POST":
        # Clear stale sessions on new login attempt
        session.pop('hospital_id', None)
        session.pop('hospital_user_id', None)
        
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        
        if not email or not password:
            error = "Please enter both email and password."
        else:
            user = HospitalUser.query.filter_by(work_email=email).first()
            if user and check_password_hash(user.password_hash, password):
                session['hospital_id'] = user.hospital_id
                session['hospital_user_id'] = user.id
                
                hospital = Hospital.query.get(user.hospital_id)
                if hospital.verification_status == "incomplete":
                    return redirect(url_for('hospital_register_info'))
                return redirect(url_for('hospital_dashboard'))
            else:
                error = "Invalid email or password."
    else:
        existing_hospital_id = session.get('hospital_id')
        if existing_hospital_id:
            existing_hospital = Hospital.query.get(existing_hospital_id)
            if existing_hospital:
                if existing_hospital.verification_status != "incomplete":
                    return redirect(url_for('hospital_dashboard'))
                return redirect(url_for('hospital_register_info'))

    return render_template("hospital-login.html", error=error)'''

# Use regex to replace hospital_login function in app.py
app_content = re.sub(
    r'@app\.route\("/hospital/login", methods=\["GET", "POST"\]\)\ndef hospital_login\(\):.*?return render_template\("hospital-login\.html", error=error\)',
    hospital_login_new,
    app_content,
    flags=re.DOTALL
)

# Also check patient_login just in case it needs session clearing
patient_login_old = '''@app.route("/patient/login", methods=["GET", "POST"])
def patient_login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['registration_user_id'] = user.id
            return redirect(url_for('patient_dashboard'))
        else:
            error = "Invalid email or password."

    return render_template("patient-login.html", error=error)'''

patient_login_new = '''@app.route("/patient/login", methods=["GET", "POST"])
def patient_login():
    error = None
    if request.method == "POST":
        session.pop('registration_user_id', None)
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['registration_user_id'] = user.id
            return redirect(url_for('patient_dashboard'))
        else:
            error = "Invalid email or password."
    else:
        if session.get('registration_user_id'):
            return redirect(url_for('patient_dashboard'))

    return render_template("patient-login.html", error=error)'''

app_content = app_content.replace(patient_login_old, patient_login_new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

# Fix hospital-login.html to preserve email
with open('templates/hospital-login.html', 'r', encoding='utf-8') as f:
    hl_content = f.read()

hl_content = hl_content.replace(
    'class="block w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-textMain text-sm focus:bg-white focus:ring-2 focus:ring-primary focus:border-primary transition-colors outline-none"',
    'class="block w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-textMain text-sm focus:bg-white focus:ring-2 focus:ring-primary focus:border-primary transition-colors outline-none"\n                                value="{{ request.form.get(\'email\', \'\') }}"'
)

with open('templates/hospital-login.html', 'w', encoding='utf-8') as f:
    f.write(hl_content)

# Fix patient-login.html to preserve email
with open('templates/patient-login.html', 'r', encoding='utf-8') as f:
    pl_content = f.read()

pl_content = pl_content.replace(
    'class="w-full border border-gray-200 rounded-xl px-4 py-3.5 text-[15px] focus:outline-none focus:ring-2 focus:ring-secondary/20 focus:border-secondary transition-all placeholder-gray-400"',
    'class="w-full border border-gray-200 rounded-xl px-4 py-3.5 text-[15px] focus:outline-none focus:ring-2 focus:ring-secondary/20 focus:border-secondary transition-all placeholder-gray-400" value="{{ request.form.get(\'email\', \'\') }}"'
)

with open('templates/patient-login.html', 'w', encoding='utf-8') as f:
    f.write(pl_content)

print("Updated login validation.")
