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
            current_user_id = session.get('registration_user_id')
            current_user = User.query.get(current_user_id) if current_user_id else None

            existing_email = User.query.filter_by(email=email).first()
            existing_phone = User.query.filter_by(phone=full_phone).first()
            
            if existing_email and (not current_user or existing_email.id != current_user.id):
                error = "An account with this email already exists."
            elif existing_phone and (not current_user or existing_phone.id != current_user.id):
                error = "An account with this phone number already exists."
            else:
                try:
                    hashed_pw = generate_password_hash(password)
                    if current_user:
                        current_user.email = email
                        current_user.phone = full_phone
                        current_user.password_hash = hashed_pw
                    else:
                        new_user = User(email=email, phone=full_phone, password_hash=hashed_pw, role="patient")
                        db.session.add(new_user)
                        db.session.flush()
                        current_user = new_user
                        
                    db.session.commit()
                    
                    # Store user ID in session securely
                    session['registration_user_id'] = current_user.id
                    
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
                today = datetime.now().date()
                try:
                    min_dob = today.replace(year=today.year - 120)
                except ValueError:
                    min_dob = today.replace(year=today.year - 120, month=2, day=28)
                
                if dob > today:
                    error = "Date of birth cannot be in the future."
                elif dob < min_dob:
                    error = "Please enter a valid date of birth."
            except ValueError:
                error = "Invalid date format for Date of Birth."
            
            if not error:
                try:
                    # Check for existing profile
                    profile = PatientProfile.query.filter_by(user_id=user_id).first()
                    if profile:
                        profile.first_name = first_name
                        profile.last_name = last_name
                        profile.date_of_birth = dob
                        profile.gender = gender
                        profile.nationality = nationality
                        profile.country_of_residence = residence
                        profile.city = city
                        profile.passport_number = passport if passport else None
                    else:
                        profile = PatientProfile(
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
                        db.session.add(profile)
                        
                    db.session.commit()
                    return redirect(url_for("patient_registration_step3"))
                except Exception as e:
                    db.session.rollback()
                    error = "An error occurred while saving your profile. Please try again."

    return render_template("patient-registration-step2.html", error=error)


def is_pregnancy_applicable(profile):
    if not profile or not profile.gender or not profile.date_of_birth:
        return False
    
    gender = profile.gender.strip().lower()
    if gender != 'female':
        return False
        
    today = datetime.now().date()
    dob = profile.date_of_birth
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    return 10 <= age <= 55


@app.route("/patient/register/step-3", methods=["GET", "POST"])
def patient_registration_step3():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    if not user:
        session.pop('registration_user_id', None)
        return redirect(url_for('patient_registration_step1'))

    profile = PatientProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return redirect(url_for('patient_registration_step2'))

    show_pregnancy = is_pregnancy_applicable(profile)

    if request.method == "POST":
        specialty = request.form.get("specialty", "").strip()
        if specialty:
            session['registration_specialty'] = specialty

        height_cm_str = request.form.get("height-cm", "").strip()
        weight_kg_str = request.form.get("weight-kg", "").strip()
        height_ft_str = request.form.get("height-ft", "").strip()
        height_in_str = request.form.get("height-in", "").strip()
        weight_lbs_str = request.form.get("weight-lbs", "").strip()
        
        error = None
        try:
            if height_cm_str:
                h_cm = float(height_cm_str)
                if h_cm < 30 or h_cm > 250:
                    error = "Please enter a height between 30 cm and 250 cm."
            if weight_kg_str and not error:
                w_kg = float(weight_kg_str)
                if w_kg < 1 or w_kg > 500:
                    error = "Please enter a weight between 1 kg and 500 kg."
            
            if (height_ft_str or height_in_str) and not error:
                ft = float(height_ft_str) if height_ft_str else 0
                inch = float(height_in_str) if height_in_str else 0
                total_inches = ft * 12 + inch
                if total_inches < 11.8 or total_inches > 98.4:
                    error = "Please enter a valid height between 1 ft and approximately 8 ft 2 in."
                    
            if weight_lbs_str and not error:
                w_lbs = float(weight_lbs_str)
                if w_lbs < 2 or w_lbs > 1102.3:
                    error = "Please enter a weight between 2 lbs and 1102 lbs."
        except ValueError:
            error = "Invalid number format."
            
        if error:
            return render_template("patient-registration-step3.html", show_pregnancy=show_pregnancy, error=error)

        if show_pregnancy:
            pregnancy = request.form.get("pregnancy", "").strip()
            if pregnancy in ["Yes", "No", "Not sure"]:
                profile.pregnancy_status = pregnancy
            else:
                profile.pregnancy_status = None
        else:
            profile.pregnancy_status = None
            
        session['registration_medical'] = {
            'condition': request.form.get("condition", "").strip(),
            'diagnosis': request.form.get("diagnosis", "").strip(),
            'symptoms': request.form.get("symptoms", "").strip(),
            'previous_treatments': request.form.get("previous-treatments", "").strip(),
            'medications': request.form.get("medications", "").strip(),
            'allergies': request.form.getlist("allergies"),
            'allergy_other_text': request.form.get("allergy-other-text", "").strip(),
            'blood_group': request.form.get("blood-group", "").strip(),
            'height_cm': height_cm_str,
            'weight_kg': weight_kg_str,
            'height_ft': height_ft_str,
            'height_in': height_in_str,
            'weight_lbs': weight_lbs_str,
            'emergency_name': request.form.get("emergency-name", "").strip(),
            'emergency_relationship': request.form.get("emergency-relationship", "").strip(),
            'emergency_country_code': request.form.get("emergency-country-code", "").strip(),
            'emergency_phone': request.form.get("emergency-phone", "").strip(),
        }
            
        try:
            db.session.commit()
            return redirect(url_for("patient_registration_step4"))
        except Exception as e:
            db.session.rollback()
            # If there's an error, just redirect back or render with error. The UI has no error banner, so we just pass for now.

    return render_template("patient-registration-step3.html", show_pregnancy=show_pregnancy)


@app.route("/patient/register/step-4")
def patient_registration_step4():
    specialty = session.get('registration_specialty', '')
    
    specialty_lower = specialty.lower()
    if "cardiology" in specialty_lower:
        recommendation_title = "Cardiology Recommendations"
        recommendation_text = 'Helpful documents may include <strong class="font-bold text-teal-950">ECG</strong>, <strong class="font-bold text-teal-950">Echo reports</strong>, <strong class="font-bold text-teal-950">angiograms</strong>, <strong class="font-bold text-teal-950">cardiac test results</strong> and previous cardiology reports.'
    elif "neurology" in specialty_lower:
        recommendation_title = "Neurology Recommendations"
        recommendation_text = 'Helpful documents may include <strong class="font-bold text-teal-950">MRI scans</strong>, <strong class="font-bold text-teal-950">CT scans</strong>, <strong class="font-bold text-teal-950">EEG reports</strong>, neurological assessments and previous neurology reports.'
    elif "orthopedics" in specialty_lower:
        recommendation_title = "Orthopedics Recommendations"
        recommendation_text = 'Helpful documents may include <strong class="font-bold text-teal-950">X-rays</strong>, <strong class="font-bold text-teal-950">MRI scans</strong>, <strong class="font-bold text-teal-950">CT scans</strong>, previous surgery records and orthopedic reports.'
    elif "oncology" in specialty_lower:
        recommendation_title = "Oncology Recommendations"
        recommendation_text = 'Helpful documents may include <strong class="font-bold text-teal-950">biopsy or pathology reports</strong>, <strong class="font-bold text-teal-950">PET scans</strong>, <strong class="font-bold text-teal-950">CT scans</strong>, <strong class="font-bold text-teal-950">MRI scans</strong>, previous treatment records and oncology reports.'
    elif "gastroenterology" in specialty_lower:
        recommendation_title = "Gastroenterology Recommendations"
        recommendation_text = 'Helpful documents may include <strong class="font-bold text-teal-950">endoscopy or colonoscopy reports</strong>, <strong class="font-bold text-teal-950">ultrasound scans</strong>, <strong class="font-bold text-teal-950">CT scans</strong>, laboratory reports and previous gastroenterology reports.'
    elif "ent" in specialty_lower:
        recommendation_title = "ENT Recommendations"
        recommendation_text = 'Helpful documents may include <strong class="font-bold text-teal-950">audiometry reports</strong>, imaging reports, endoscopy reports and previous ENT reports.'
    elif "general physician" in specialty_lower:
        recommendation_title = "General Medical Recommendations"
        recommendation_text = 'Helpful documents may include <strong class="font-bold text-teal-950">recent blood tests</strong>, laboratory reports, prescriptions, discharge summaries and relevant previous medical reports.'
    else:
        recommendation_title = "Medical Document Recommendations"
        recommendation_text = 'Please upload any available medical reports, test results, scans, prescriptions or previous treatment records related to your condition.'
        
    recommendation_text += ' <br><br><span class="block text-teal-900 font-semibold mt-1">These documents are recommended but not mandatory.</span>'
    
    return render_template("patient-registration-step4.html", recommendation_title=recommendation_title, recommendation_text=recommendation_text)


@app.route("/patient/register/step-5", methods=["GET", "POST"])
def patient_registration_step5():
    error = None
    
    if request.method == "POST":
        timeframe = request.form.get("timeframe")
        location = request.form.get("location")
        countries = request.form.getlist("countries")
        assistance = request.form.getlist("assistance")
        notes = request.form.get("additional_notes", "").strip()

        allowed_timeframes = ["As soon as possible", "Within 1 week", "Within 1 month", "Within 3 months", "Flexible / Not sure"]
        allowed_locations = ["Near me", "My state / region", "Anywhere in my country", "Specific countries", "Worldwide"]
        allowed_assistance = ["Visa assistance", "Accommodation assistance", "Airport pickup / transportation", "Language / interpreter assistance", "Financial assistance information", "None"]

        if timeframe not in allowed_timeframes:
            error = "Please select a valid treatment timeframe."
        elif location not in allowed_locations:
            error = "Please select a valid location preference."
        elif location == "Specific countries" and not countries:
            error = "Please select at least one country."
        elif any(a not in allowed_assistance for a in assistance):
            error = "Invalid assistance option selected."
        elif len(notes) > 1000:
            error = "Additional notes cannot exceed 1000 characters."
        
        if not error:
            if "None" in assistance and len(assistance) > 1:
                assistance = ["None"]
                
            session['registration_preferences'] = {
                'timeframe': timeframe,
                'location_preference': location,
                'specific_countries': countries if location == "Specific countries" else [],
                'assistance': assistance,
                'additional_notes': notes
            }
            return redirect(url_for('patient_registration_step6'))

    preferences = session.get('registration_preferences', {})
    return render_template("patient-registration-step5.html", error=error, preferences=preferences)


@app.route("/patient/register/step-6", methods=["GET", "POST"])
def patient_registration_step6():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profile = PatientProfile.query.filter_by(user_id=user_id).first()
    
    if not user or not profile:
        return redirect(url_for('patient_registration_step1'))
        
    preferences = session.get('registration_preferences')
    if not preferences:
        return redirect(url_for('patient_registration_step5'))
        
    medical = session.get('registration_medical', {})
    specialty = session.get('registration_specialty', '')
    
    error = None
    if request.method == "POST":
        consent_accurate = request.form.get("consent-accurate")
        consent_share = request.form.get("consent-share")
        consent_neutrality = request.form.get("consent-neutrality")
        
        if not consent_accurate or not consent_share or not consent_neutrality:
            error = "Please accept all required consent checkboxes to submit your request."
        else:
            # Validated successfully. 
            # TODO: Create the permanent TreatmentRequest database record here in the future.
            session['registration_complete'] = True
            return redirect(url_for('patient_registration_success'))
            
    return render_template(
        "patient-registration-step6.html", 
        user=user, 
        profile=profile, 
        medical=medical, 
        specialty=specialty, 
        preferences=preferences,
        error=error
    )


@app.route("/patient/register/success")
def patient_registration_success():
    return render_template("patient-registration-success.html")


# =========================================================
# PATIENT DASHBOARD
# =========================================================

@app.route("/patient/dashboard")
def patient_dashboard():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profile = PatientProfile.query.filter_by(user_id=user_id).first()
    
    if not user or not profile:
        return redirect(url_for('patient_registration_step1'))
        
    has_temporary_request = session.get('registration_complete', False)
    temporary_specialty = session.get('registration_specialty', '')
    
    return render_template(
        "patient-dashboard.html",
        user=user,
        profile=profile,
        has_temporary_request=has_temporary_request,
        temporary_specialty=temporary_specialty
    )


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