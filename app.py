from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from config import Config
from models import db, User, PatientProfile
from werkzeug.security import generate_password_hash
from datetime import datetime
import re

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


# =========================================================
# PUBLIC PAGES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# PATIENT REGISTRATION
# =========================================================

@app.route("/patient/register/step-1", methods=["GET", "POST"])
def patient_registration_step1():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        country_code = request.form.get("country-code", "").strip()
        mobile = request.form.get("mobile", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm-password", "")
        
        full_phone = None
        if country_code and mobile:
            clean_mobile = re.sub(r"[^\d]", "", mobile)
            if clean_mobile:
                full_phone = f"{country_code} {clean_mobile}"
        
        if not email or not password or not mobile:
            error = "Email, phone number, and password are required."
        elif not full_phone:
            error = "Please enter a valid phone number format."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>\-_]", password):
            error = "Password does not meet the security requirements."
        else:
            existing_email = User.query.filter_by(email=email).first()
            existing_phone = User.query.filter_by(phone=full_phone).first()
            
            if existing_email:
                error = "An account with this email already exists."
            elif existing_phone:
                error = "An account with this phone number already exists."
            else:
                try:
                    hashed_pw = generate_password_hash(password)
                    new_user = User(email=email, phone=full_phone, password_hash=hashed_pw, role="patient")
                    db.session.add(new_user)
                    db.session.commit()
                    
                    # Store user ID in session securely
                    session['registration_user_id'] = new_user.id
                    
                    return redirect(url_for("patient_registration_step2"))
                except Exception as e:
                    db.session.rollback()
                    error = "An error occurred during registration. Please try again."

    return render_template("patient-registration-step1.html", error=error)


@app.route("/patient/register/step-2", methods=["GET", "POST"])
def patient_registration_step2():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    if not user:
        session.pop('registration_user_id', None)
        return redirect(url_for('patient_registration_step1'))

    error = None
    if request.method == "POST":
        first_name = request.form.get("first-name", "").strip()
        last_name = request.form.get("last-name", "").strip()
        dob_str = request.form.get("dob", "").strip()
        gender = request.form.get("gender", "").strip().lower()
        nationality = request.form.get("nationality", "").strip()
        residence = request.form.get("residence", "").strip()
        city = request.form.get("city", "").strip()
        passport = request.form.get("passport", "").strip()
        
        if not first_name or not last_name or not dob_str or not gender or not nationality or not residence or not city:
            error = "Please fill out all required fields."
        elif gender not in ["male", "female", "other"]:
            error = "Please select a valid gender."
        elif len(first_name) > 100 or len(last_name) > 100 or len(nationality) > 100 or len(residence) > 100 or len(city) > 100 or len(passport) > 100:
            error = "One or more fields exceed the maximum length limit."
        else:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                if dob >= datetime.now().date():
                    error = "Date of birth cannot be in the future or today."
            except ValueError:
                error = "Invalid date format for Date of Birth."
            
            if not error:
                try:
                    # Check for existing profile
                    profile = PatientProfile.query.filter_by(user_id=user_id).first()
                    if profile:
                        error = "A profile for this account already exists."
                    else:
                        new_profile = PatientProfile(
                            user_id=user_id,
                            first_name=first_name,
                            last_name=last_name,
                            date_of_birth=dob,
                            gender=gender,
                            nationality=nationality,
                            country_of_residence=residence,
                            city=city,
                            passport_number=passport if passport else None
                        )
                        db.session.add(new_profile)
                        db.session.commit()
                        return redirect(url_for("patient_registration_step3"))
                except Exception as e:
                    db.session.rollback()
                    error = "An error occurred while saving your profile. Please try again."

    return render_template("patient-registration-step2.html", error=error)


@app.route("/patient/register/step-3")
def patient_registration_step3():
    return render_template("patient-registration-step3.html")


@app.route("/patient/register/step-4")
def patient_registration_step4():
    return render_template("patient-registration-step4.html")


@app.route("/patient/register/step-5")
def patient_registration_step5():
    return render_template("patient-registration-step5.html")


@app.route("/patient/register/success")
def patient_registration_success():
    return render_template("patient-registration-success.html")


# =========================================================
# PATIENT DASHBOARD
# =========================================================

@app.route("/patient/dashboard")
def patient_dashboard():
    return render_template("patient-dashboard.html")


@app.route("/patient/requests/details")
def patient_request_details():
    return render_template("patient-request-details.html")


# =========================================================
# HOSPITAL RESPONSES & PROPOSALS
# =========================================================

@app.route("/patient/hospital-responses")
def patient_hospital_responses():
    return render_template("patient-hospital-responses.html")


@app.route("/patient/hospital-profile")
def patient_hospital_profile():
    return render_template("patient-hospital-profile.html")


@app.route("/patient/compare-hospitals")
def patient_compare_hospitals():
    return render_template("patient-compare-hospitals.html")


@app.route("/patient/treatment-proposal")
def patient_treatment_proposal_details():
    return render_template("patient-treatment-proposal-details.html")


# =========================================================
# SECURE MESSAGES
# =========================================================

@app.route("/patient/messages")
def patient_secure_messages():
    return render_template("patient-secure-messages.html")


# =========================================================
# PATIENT PROFILE & SETTINGS
# =========================================================

@app.route("/patient/profile-settings")
def patient_profile_settings():
    return render_template("patient-profile-settings.html")


# =========================================================
# DEVELOPMENT SERVER
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)