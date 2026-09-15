from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory, flash, abort
from functools import wraps
from flask_migrate import Migrate
from config import Config
from models import db, User, PatientProfile, TreatmentRequest, MedicalDocument, Hospital, HospitalUser, Specialty, Language, HospitalAccreditation, HospitalVerificationDocument, TreatmentProposal, CostLineItem
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import re
import uuid
import json
import uuid
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
HOSPITAL_DOCS_FOLDER = os.path.join(UPLOAD_FOLDER, 'hospital_verification')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HOSPITAL_DOCS_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

@app.template_filter('format_location')
def format_location(hospital):
    if not hospital:
        return "Unknown Location"
    parts = []
    if getattr(hospital, 'city', None) and str(hospital.city).lower() not in ('none', ''):
        parts.append(str(hospital.city).strip())
    if getattr(hospital, 'state_region', None) and str(hospital.state_region).lower() not in ('none', ''):
        parts.append(str(hospital.state_region).strip())
    if getattr(hospital, 'country', None) and str(hospital.country).lower() not in ('none', ''):
        parts.append(str(hospital.country).strip())
    return ", ".join(parts) if parts else "Unknown Location"

@app.template_filter('format_duration')
def format_duration(val, unit):
    val_str = str(val) if val is not None else ""
    unit_str = str(unit) if unit else ""
    
    if not val_str or val_str.lower() == 'none':
        return "Not specified"
        
    val_lower = val_str.lower()
    
    if any(u in val_lower for u in ['day', 'week', 'month', 'year']):
        val_str = val_str.replace("dayss", "days").replace("Dayss", "Days")
        return val_str.title()
    else:
        unit_str = unit_str.replace("dayss", "days")
        if not unit_str or unit_str.lower() == 'none':
            unit_str = "days"
        return f"{val_str} {unit_str.capitalize()}"
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
    if session.get("patient_authenticated"):
        return redirect(url_for("patient_dashboard"))
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        country_code = request.form.get("country-code", "").strip()
        mobile = request.form.get("mobile", "").strip()
        first_name = request.form.get("first-name", "").strip().title()
        last_name = request.form.get("last-name", "").strip().title()
        residence = request.form.get("residence", "").strip()
        nationality = request.form.get("nationality", "").strip()
        language = request.form.get("language", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm-password", "")
        
        full_phone = None
        if country_code and mobile:
            clean_mobile = re.sub(r"[^\d]", "", mobile)
            if clean_mobile:
                full_phone = f"{country_code} {clean_mobile}"
        
        if not email or not password or not mobile or not first_name or not last_name or not residence or not nationality or not language or not request.form.get("terms") or not request.form.get("privacy"):
            error = "All fields are required."
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
            
            if existing_email:
                error = 'An account with this email already exists. <a href="/patient/login" class="underline font-bold">Please sign in.</a>'
            elif existing_phone:
                error = 'An account with this phone number already exists. <a href="/patient/login" class="underline font-bold">Please sign in.</a>'
            else:
                try:
                    hashed_pw = generate_password_hash(password)
                    if current_user and current_user.email == email:
                        # Account data updates User only when explicitly editing Account Settings.
                        # We do not overwrite user data from the patient registration flow.
                        pass
                    else:
                        # Clear old session data to ensure complete isolation
                        for key in list(session.keys()):
                            if key in ['registration_user_id', 'active_patient_profile_id', 'new_profile_relationship', 'registration_specialty', 'registration_medical', 'registration_preferences', 'last_request_reference']:
                                session.pop(key, None)
                                
                        new_user = User(
                            email=email, 
                            phone=full_phone, 
                            password_hash=hashed_pw, 
                            role="patient",
                            first_name=first_name,
                            last_name=last_name,
                            country_of_residence=residence,
                            preferred_language=language
                        )
                        db.session.add(new_user)
                        db.session.flush()
                        current_user = new_user
                        
                    db.session.commit()
                    
                    # Store user ID in session securely
                    session['registration_user_id'] = current_user.id
                    session['registration_nationality'] = nationality
                    return redirect(url_for("patient_registration_who"))
                except Exception as e:
                    db.session.rollback()
                    error = "An error occurred during registration. Please try again."

    return render_template("patient-registration-step1.html", error=error)


@app.route("/patient/login", methods=["GET", "POST"])
def patient_login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['registration_user_id'] = user.id
            session['patient_authenticated'] = True
            session.pop('creating_new_request', None)
            return redirect(url_for('patient_dashboard'))
        else:
            error = "Invalid email or password."
            
    return render_template("patient-login.html", error=error)



@app.route("/patient/logout")
def patient_logout():
    session.pop('registration_user_id', None)
    session.pop('patient_authenticated', None)
    return redirect(url_for('patient_login'))

@app.route("/patient/request/new")
def patient_new_request():
    if not session.get("patient_authenticated"):
        return redirect(url_for("patient_login"))
    
    # Initialize a new request flow for the authenticated user
    # Keep the existing registration_user_id intact
    session['creating_new_request'] = True
    
    # Clear any old request state
    session.pop('active_patient_profile_id', None)
    session.pop('new_profile_relationship', None)
    session.pop('registration_specialty', None)
    
    return redirect(url_for('patient_registration_who'))

@app.route("/patient/register/who", methods=["GET", "POST"])
def patient_registration_who():
    if session.get("patient_authenticated") and not session.get("creating_new_request"):
        return redirect(url_for("patient_dashboard"))
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
    
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    self_profile = next((p for p in profiles if p.relationship_type == 'Self'), None)
    other_profiles = [p for p in profiles if p.relationship_type != 'Self']
    error = None
    
    if request.method == "POST":
        selected_profile_id = request.form.get("profile_id")
        
        if selected_profile_id == "new_self":
            session['new_profile_relationship'] = "Self"
            return redirect(url_for('patient_registration_step2'))
            
        elif selected_profile_id == "new_other":
            relationship = request.form.get("relationship")
            if not relationship:
                error = "Please select a relationship for the new profile."
            else:
                session['new_profile_relationship'] = relationship
                return redirect(url_for('patient_registration_step2'))
                
        else:
            profile = next((p for p in profiles if str(p.id) == str(selected_profile_id)), None)
            if profile:
                session['active_patient_profile_id'] = profile.id
                return redirect(url_for('patient_registration_step3'))
            else:
                error = "Invalid profile selected."
            
    return render_template("patient-registration-who.html", self_profile=self_profile, other_profiles=other_profiles, error=error)

@app.route("/patient/register/step-2", methods=["GET", "POST"])
def patient_registration_step2():
    if session.get("patient_authenticated") and not session.get("creating_new_request"):
        return redirect(url_for("patient_dashboard"))
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    if not user:
        session.pop('registration_user_id', None)
        return redirect(url_for('patient_registration_step1'))

    error = None
    if request.method == "POST":
        first_name = request.form.get("first-name", "").strip().title()
        last_name = request.form.get("last-name", "").strip().title()
        dob_str = request.form.get("dob", "").strip()
        gender = request.form.get("gender", "").strip().lower()
        
        # Get nationality and residence from session or user account
        nationality = session.get('registration_nationality')
        residence = None
        current_user = User.query.get(user_id)
        if current_user:
            residence = current_user.country_of_residence
            
        relationship = session.get('new_profile_relationship', 'Self')
        is_self = (relationship == 'Self')
        
        if not is_self:
            form_nationality = request.form.get("nationality", "").strip()
            form_residence = request.form.get("country_of_residence", "").strip()
            if form_nationality:
                nationality = form_nationality
            if form_residence:
                residence = form_residence
            
        city = request.form.get("city", "").strip()
        passport = request.form.get("passport", "").strip()
        
        if not first_name or not last_name or not dob_str or not gender or not city or (not is_self and (not nationality or not residence)):
            error = "Please fill out all required fields."
        elif gender not in ["male", "female", "other"]:
            error = "Please select a valid gender."
        elif len(first_name) > 100 or len(last_name) > 100 or len(city) > 100 or len(passport) > 100:
            error = "One or more fields exceed the maximum length limit."
        else:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                today = datetime.now().date()
                min_dob = datetime(1900, 1, 1).date()
                
                if dob > today:
                    error = "Date of birth cannot be in the future."
                elif dob < min_dob:
                    error = "Date of birth cannot be before 1900."
            except ValueError:
                error = "Invalid date format for Date of Birth."
            
            # Basic MVP Residence Validation
            city_lower = city.lower()
            if city_lower in ['kochi', 'cochin', 'mumbai', 'delhi', 'bangalore'] and residence != 'IN':
                error = f"{city.title()} is typically in India. Please verify your country of residence."
            elif city_lower in ['new york', 'los angeles', 'chicago'] and residence != 'US':
                error = f"{city.title()} is typically in the US. Please verify your country of residence."
            elif city_lower in ['london', 'manchester'] and residence != 'GB':
                error = f"{city.title()} is typically in the UK. Please verify your country of residence."
            elif city_lower in ['paris'] and residence != 'FR':
                error = f"{city.title()} is typically in France. Please verify your country of residence."
                
            if not error:
                try:
                    import uuid
                    new_id = f"MB-P-{uuid.uuid4().hex[:6].upper()}"
                    relationship = session.get('new_profile_relationship', 'Self')
                    
                    new_profile = PatientProfile(
                        user_id=user_id, # Keep for backwards compatibility
                        patient_id=new_id,
                        relationship_type=relationship,
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
                    
                    session.pop('new_profile_relationship', None)
                    session['active_patient_profile_id'] = new_profile.id
                    return redirect(url_for("patient_registration_step3"))
                except Exception as e:
                    db.session.rollback()
                    error = "An error occurred while saving your profile. Please try again."

    is_self = session.get('new_profile_relationship', 'Self') == 'Self'
    default_first_name = user.first_name if is_self else ''
    default_last_name = user.last_name if is_self else ''
    default_residence = user.country_of_residence if is_self else ''
    
    return render_template("patient-registration-step2.html", 
        error=error, 
        is_self=is_self,
        default_first_name=default_first_name,
        default_last_name=default_last_name,
        default_residence=default_residence
    )


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
    if session.get("patient_authenticated") and not session.get("creating_new_request"):
        return redirect(url_for("patient_dashboard"))
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    if not user:
        session.pop('registration_user_id', None)
        return redirect(url_for('patient_registration_step1'))

    active_profile_id = session.get('active_patient_profile_id')
    if active_profile_id:
        profile = PatientProfile.query.filter_by(id=active_profile_id, user_id=user_id).first()
        if not profile:
            return redirect(url_for('patient_registration_who'))
    else:
        profile = PatientProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return redirect(url_for('patient_registration_who'))

    show_pregnancy = is_pregnancy_applicable(profile)
    previous_request = TreatmentRequest.query.filter_by(patient_profile_id=profile.id).order_by(TreatmentRequest.created_at.desc()).first()
    
    error = request.args.get('error')

    if request.method == "POST":
        condition = request.form.get("condition", "").strip()
        diagnosis = request.form.get("diagnosis", "").strip()
        
        prev_treatments = request.form.get("previous-treatments", "").strip()
        no_prev_treatments = request.form.get("no-previous-treatments")
        
        medications = request.form.get("medications", "").strip()
        no_medications = request.form.get("no-medications")
        

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
            
        if not error:
            if not condition or not diagnosis:
                error = "Please fill out all required medical condition fields."
            elif not prev_treatments and not no_prev_treatments:
                error = "Please provide your previous treatments or select None."
            elif not medications and not no_medications:
                error = "Please provide your current medications or select None."
            elif not request.form.getlist("allergies"):
                has_existing_allergies = profile and (
                    (profile.allergies and profile.allergies != ['No Known Allergies']) or 
                    profile.allergy_other_text
                )
                if not has_existing_allergies:
                    error = "Please provide your allergies or select No Known Allergies."
            elif not previous_request:
                if not height_cm_str and not (height_ft_str or height_in_str):
                    error = "Please provide your height."
                elif not weight_kg_str and not weight_lbs_str:
                    error = "Please provide your weight."

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
            
        submitted_allergies = request.form.getlist("allergies")
        submitted_allergy_other = request.form.get("allergy-other-text", "").strip()
        new_allergies_text = request.form.get("new-allergies", "").strip()

        ignore_phrases = ["none", "nil", "no other", "na", "n/a", "no", "nothing"]

        if submitted_allergies:
            if "No Known Allergies" in submitted_allergies:
                final_allergies = ["No Known Allergies"]
                final_allergy_other = ""
            else:
                final_allergies = [a for a in submitted_allergies if a != "No Known Allergies"]
                if "Other" in final_allergies and submitted_allergy_other and submitted_allergy_other.lower() not in ignore_phrases:
                    final_allergy_other = submitted_allergy_other
                else:
                    final_allergy_other = ""
                    if "Other" in final_allergies:
                        final_allergies.remove("Other")
        else:
            final_allergies = profile.allergies if profile.allergies else ["No Known Allergies"]
            final_allergy_other = profile.allergy_other_text if profile.allergy_other_text else ""

        if new_allergies_text and new_allergies_text.lower() not in ignore_phrases:
            if final_allergy_other:
                final_allergy_other += ", " + new_allergies_text
            else:
                final_allergy_other = new_allergies_text
            
            if "No Known Allergies" in final_allergies:
                final_allergies.remove("No Known Allergies")
            if "Other" not in final_allergies:
                final_allergies.append("Other")

        profile.allergies = final_allergies
        profile.allergy_other_text = final_allergy_other

        # Weight Logic Update
        weight_change_type = ""
        weight_change_amount = ""
        weight_change_amount_unit = ""
        prev_weight_kg = None
        prev_weight_lbs = None
        prev_weight_date = None

        if previous_request:
            prev_weight_kg = previous_request.weight_kg
            prev_weight_lbs = previous_request.weight_lbs
            prev_weight_date = previous_request.created_at.strftime('%b %d, %Y') if previous_request.created_at else None

            if weight_kg_str and prev_weight_kg is not None:
                diff = float(weight_kg_str) - float(prev_weight_kg)
                weight_change_amount = f"+{round(abs(diff), 1)}" if diff > 0 else f"-{round(abs(diff), 1)}" if diff < 0 else "0"
                weight_change_amount_unit = "kg"
                if diff > 0:
                    weight_change_type = "Weight gain"
                elif diff < 0:
                    weight_change_type = "Weight loss"
                else:
                    weight_change_type = "No weight change"
            elif weight_lbs_str and prev_weight_lbs is not None:
                diff = float(weight_lbs_str) - float(prev_weight_lbs)
                weight_change_amount = f"+{round(abs(diff), 1)}" if diff > 0 else f"-{round(abs(diff), 1)}" if diff < 0 else "0"
                weight_change_amount_unit = "lbs"
                if diff > 0:
                    weight_change_type = "Weight gain"
                elif diff < 0:
                    weight_change_type = "Weight loss"
                else:
                    weight_change_type = "No weight change"

        session['registration_medical'] = {
            'condition': request.form.get("condition", "").strip(),
            'diagnosis': request.form.get("diagnosis", "").strip(),
            'symptoms': request.form.get("symptoms", "").strip(),
            'previous_treatments': request.form.get("previous-treatments", "").strip(),
            'medications': request.form.get("medications", "").strip(),
            'allergies': final_allergies,
            'allergy_other_text': final_allergy_other,
            'blood_group': previous_request.blood_group if previous_request else request.form.get("blood-group", "").strip(),
            'height_cm': previous_request.height_cm if previous_request else height_cm_str,
            'weight_kg': weight_kg_str,
            'height_ft': previous_request.height_ft if previous_request else height_ft_str,
            'height_in': previous_request.height_in if previous_request else height_in_str,
            'weight_lbs': weight_lbs_str,
            'weight_change_type': weight_change_type,
            'weight_change_amount': weight_change_amount,
            'weight_change_amount_unit': weight_change_amount_unit,
            'weight_change_period': "",
            'weight_change_period_unit': "",
            'current_weight': "",
            'current_weight_unit': "",
            'emergency_name': request.form.get("emergency-name", "").strip().title(),
            'emergency_relationship': request.form.get("emergency-relationship", "").strip(),
            'emergency_country_code': request.form.get("emergency-country-code", "").strip(),
            'emergency_phone': request.form.get("emergency-phone", "").strip(),
            'prev_weight_kg': prev_weight_kg,
            'prev_weight_lbs': prev_weight_lbs,
            'prev_weight_date': prev_weight_date,
        }
            
        try:
            db.session.commit()
            return redirect(url_for("patient_registration_step4"))
        except Exception as e:
            db.session.rollback()
            # If there's an error, just redirect back or render with error. The UI has no error banner, so we just pass for now.

    medical_data = session.get('registration_medical', {})
    specialty_data = session.get('registration_specialty', '')
    return render_template("patient-registration-step3.html", show_pregnancy=show_pregnancy, previous_request=previous_request, profile=profile, medical_data=medical_data, specialty_data=specialty_data)


@app.route("/patient/register/step-4")
def patient_registration_step4():
    if session.get("patient_authenticated") and not session.get("creating_new_request"):
        return redirect(url_for("patient_dashboard"))
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
    if session.get("patient_authenticated") and not session.get("creating_new_request"):
        return redirect(url_for("patient_dashboard"))
    error = request.args.get('error')
    
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


@app.route("/patient/register/upload-document", methods=["POST"])
def upload_document():
    user_id = session.get('registration_user_id')
    active_profile_id = session.get('active_patient_profile_id')
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    profile = PatientProfile.query.filter_by(id=active_profile_id, user_id=user_id).first() if active_profile_id else PatientProfile.query.filter_by(user_id=user_id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
        
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    document_type = request.form.get('document_type', 'Other Medical Document')
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        storage_filename = f"{uuid.uuid4().hex}.{ext}"
        
        file_path = os.path.join(UPLOAD_FOLDER, storage_filename)
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        new_doc = MedicalDocument(
            original_filename=original_filename,
            storage_filename=storage_filename,
            document_type=document_type,
            mime_type=file.content_type,
            file_size=file_size,
            patient_profile_id=profile.id,
            uploaded_by_id=user_id
        )
        db.session.add(new_doc)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'document_id': new_doc.id,
            'original_filename': original_filename,
            'document_type': document_type
        })
        
    return jsonify({'error': 'Invalid file type'}), 400

@app.route("/patient/document/<int:doc_id>")
def download_document(doc_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        from flask import abort
        abort(401)
        
    doc = MedicalDocument.query.get_or_404(doc_id)
    if doc.uploaded_by_id != user_id:
        from flask import abort
        abort(403)
        
    return send_from_directory(UPLOAD_FOLDER, doc.storage_filename, as_attachment=True, download_name=doc.original_filename)

@app.route("/patient/register/step-6", methods=["GET", "POST"])
def patient_registration_step6():
    if session.get("patient_authenticated") and not session.get("creating_new_request"):
        return redirect(url_for("patient_dashboard"))
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    active_profile_id = session.get('active_patient_profile_id')
    profile = None
    if active_profile_id:
        profile = PatientProfile.query.filter_by(id=active_profile_id, user_id=user_id).first()
    else:
        profile = PatientProfile.query.filter_by(user_id=user_id).first()
        
    if not profile:
        return redirect(url_for('patient_registration_who'))
    
    specialty = session.get('registration_specialty')
    medical = session.get('registration_medical')
    preferences = session.get('registration_preferences')
    
    if not medical or not preferences:
        error_msg = "Some information from your treatment request is missing. Please review the highlighted steps before submitting again."
        if not medical:
            return redirect(url_for('patient_registration_step3', error=error_msg))
        else:
            return redirect(url_for('patient_registration_step5', error=error_msg))
            
    error = None
    if request.method == "POST":
        consent_accurate = request.form.get("consent-accurate")
        consent_share = request.form.get("consent-share")
        consent_neutrality = request.form.get("consent-neutrality")
        
        if not consent_accurate or not consent_share or not consent_neutrality:
            error = "Please accept all required consent checkboxes to submit your request."
        else:
            try:
                # Parse numeric values
                def parse_float(val):
                    try:
                        return float(val) if val else None
                    except ValueError:
                        return None
                
                while True:
                    reference_id = f"TR-{uuid.uuid4().hex[:10].upper()}"
                    existing = TreatmentRequest.query.filter_by(reference_id=reference_id).first()
                    if not existing:
                        break
                
                        
                new_request = TreatmentRequest(
                    reference_id=reference_id,
                    patient_profile_id=profile.id,
                    status="Active",
                    specialty=specialty,
                    condition=medical.get('condition'),
                    diagnosis=medical.get('diagnosis'),
                    symptoms=medical.get('symptoms'),
                    previous_treatments=medical.get('previous_treatments'),
                    medications=medical.get('medications'),
                    allergies=medical.get('allergies', []) if medical.get('allergies') else None,
                    allergy_other_text=(medical.get('allergy_other_text', '') + ' ' + medical.get('new_allergies_text', '')).strip() if (medical.get('allergy_other_text') or medical.get('new_allergies_text')) else None,
                    blood_group=medical.get('blood_group'),
                    height_cm=parse_float(medical.get('height_cm')),
                    weight_kg=parse_float(medical.get('weight_kg')),
                    height_ft=parse_float(medical.get('height_ft')),
                    height_in=parse_float(medical.get('height_in')),
                    weight_lbs=parse_float(medical.get('weight_lbs')),
                    weight_change_type=medical.get('weight_change_type'),
                    weight_change_amount=medical.get('weight_change_amount'),
                    weight_change_amount_unit=medical.get('weight_change_amount_unit'),
                    weight_change_period=medical.get('weight_change_period'),
                    weight_change_period_unit=medical.get('weight_change_period_unit'),
                    current_weight=parse_float(medical.get('current_weight')),
                    current_weight_unit=medical.get('current_weight_unit'),
                    emergency_name=medical.get('emergency_name'),
                    emergency_relationship=medical.get('emergency_relationship'),
                    emergency_country_code=medical.get('emergency_country_code'),
                    emergency_phone=medical.get('emergency_phone'),
                    timeframe=preferences.get('timeframe'),
                    location_preference=preferences.get('location_preference'),
                    specific_countries=preferences.get('specific_countries'),
                    assistance_required=preferences.get('assistance'),
                    additional_notes=preferences.get('additional_notes')
                )
                
                db.session.add(new_request)
                
                pending_docs = MedicalDocument.query.filter_by(
                    patient_profile_id=profile.id,
                    uploaded_by_id=user_id,
                    treatment_request_id=None
                ).all()
                for doc in pending_docs:
                    doc.treatment_request = new_request
                    
                db.session.commit()
                
                session.pop('registration_specialty', None)
                session.pop('registration_medical', None)
                session.pop('registration_preferences', None)
                session.pop('creating_new_request', None)
                
                session['patient_authenticated'] = True
                session['last_request_reference'] = reference_id
                
                return redirect(url_for('patient_registration_success'))
            except Exception as e:
                db.session.rollback()
                error = "An error occurred while saving your request. Please try again."
            
    pending_docs = MedicalDocument.query.filter_by(
        patient_profile_id=profile.id,
        uploaded_by_id=user_id,
        treatment_request_id=None
    ).all()

    return render_template(
        "patient-registration-step6.html", 
        user=user, 
        profile=profile, 
        medical=medical, 
        specialty=specialty, 
        preferences=preferences,
        pending_docs=pending_docs,
        error=error
    )


@app.route("/patient/register/success")
def patient_registration_success():
    reference_id = session.get('last_request_reference')
    if not reference_id:
        return redirect(url_for('patient_dashboard'))
    return render_template("patient-registration-success.html", reference_id=reference_id)


# =========================================================
# PATIENT DASHBOARD
# =========================================================

@app.route("/patient/dashboard")
def patient_dashboard():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    if not user or not profiles:
        return redirect(url_for('patient_registration_step1'))
        
    profile_ids = [p.id for p in profiles]
    profile = next((p for p in profiles if p.relationship_type == 'Self'), None)
    if not profile and profiles:
        profile = profiles[0]
        
    active_requests = TreatmentRequest.query.filter(
        TreatmentRequest.patient_profile_id.in_(profile_ids)
    ).order_by(TreatmentRequest.created_at.desc()).all()
    
    total_responses = 0
    shortlisted_hospitals_count = 0
    for req in active_requests:
        req.response_count = TreatmentProposal.query.filter_by(
            treatment_request_id=req.id,
            status='submitted'
        ).count()
        total_responses += req.response_count
        shortlisted_hospitals_count += TreatmentProposal.query.filter_by(
            treatment_request_id=req.id,
            status='submitted',
            patient_shortlisted=True
        ).count()

    from models import MessageThread, Message

    recent_responses = []
    recent_messages = []
    unread_messages_count = 0
    
    for req in active_requests:
        # Get recent responses
        proposals = TreatmentProposal.query.filter_by(
            treatment_request_id=req.id,
            status='submitted'
        ).order_by(TreatmentProposal.submitted_at.desc()).all()
        recent_responses.extend(proposals)
        
        # Get recent messages
        threads = MessageThread.query.filter_by(treatment_request_id=req.id).all()
        for thread in threads:
            latest_msg = thread.messages.order_by(Message.created_at.desc()).first()
            if latest_msg:
                recent_messages.append({
                    'thread': thread,
                    'latest_message': latest_msg
                })
            
            # Count unread messages from hospital
            unread_count = thread.messages.filter_by(sender_type='hospital', is_read=False).count()
            unread_messages_count += unread_count

    # Sort and limit
    recent_responses.sort(key=lambda x: x.submitted_at or x.created_at, reverse=True)
    recent_responses = recent_responses[:5]
    
    recent_messages.sort(key=lambda x: x['latest_message'].created_at, reverse=True)
    recent_messages = recent_messages[:5]

    return render_template(
        "patient-dashboard.html",
        user=user,
        profile=profile,
        active_requests=active_requests,
        profiles=profiles,
        total_responses=total_responses,
        shortlisted_hospitals_count=shortlisted_hospitals_count,
        recent_responses=recent_responses,
        recent_messages=recent_messages,
        unread_messages_count=unread_messages_count
    )


@app.route("/patient/requests/details/<string:reference_id>")
def patient_request_details(reference_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    
    profile = PatientProfile.query.filter_by(id=req.patient_profile_id, user_id=user_id).first()
    
    if not profile:
        from flask import abort
        abort(403)
        
    user = User.query.get(user_id)
    
    previous_request = TreatmentRequest.query.filter(
        TreatmentRequest.patient_profile_id == req.patient_profile_id,
        TreatmentRequest.created_at < req.created_at
    ).order_by(TreatmentRequest.created_at.desc()).first()
    
    return render_template("patient-request-details.html", request=req, profile=profile, user=user, previous_request=previous_request)


# =========================================================
# HOSPITAL RESPONSES & PROPOSALS
# =========================================================

@app.route("/patient/hospital-responses")
@app.route("/patient/requests/<string:reference_id>/responses")
def patient_hospital_responses(reference_id=None):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    
    if not user or not profiles:
        return redirect(url_for('patient_registration_step1'))
        
    profile_ids = [p.id for p in profiles]
    
    req_reference_id = reference_id or request.args.get('reference_id')
    
    if req_reference_id:
        req = TreatmentRequest.query.filter_by(reference_id=req_reference_id).first()
        if not req or req.patient_profile_id not in profile_ids:
            return redirect(url_for('patient_dashboard'))
    else:
        req = TreatmentRequest.query.filter(
            TreatmentRequest.patient_profile_id.in_(profile_ids)
        ).order_by(TreatmentRequest.created_at.desc()).first()
    
    profile = PatientProfile.query.get(req.patient_profile_id) if req else None
    
    if req:
        responses = TreatmentProposal.query.filter_by(
            treatment_request_id=req.id,
            status='submitted'
        ).order_by(TreatmentProposal.submitted_at.desc()).all()
    else:
        responses = []

    return render_template(
        "patient-hospital-responses.html", 
        request=req, 
        profile=profile, 
        user=user, 
        responses=responses
    )


@app.route("/patient/treatment-proposal/<int:proposal_id>/hospital")
def patient_hospital_profile_by_proposal(proposal_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    proposal = TreatmentProposal.query.get(proposal_id)
    if not proposal:
        flash("Treatment proposal not found.", "error")
        return redirect(url_for('patient_dashboard'))
        
    # Authorization: Ensure this proposal belongs to a request owned by this patient
    target_request = TreatmentRequest.query.get(proposal.treatment_request_id)
    if not target_request:
        flash("Treatment request not found.", "error")
        return redirect(url_for('patient_dashboard'))
        
    patient_profile = PatientProfile.query.get(target_request.patient_profile_id)
    if not patient_profile or patient_profile.user_id != user_id:
        flash("Unauthorized access.", "error")
        return redirect(url_for('patient_dashboard'))
        
    hospital = Hospital.query.get(proposal.hospital_id)
    if not hospital:
        flash("Hospital profile not found.", "error")
        return redirect(url_for('patient_dashboard'))
        
    return render_template("patient-hospital-profile.html", proposal=proposal, hospital=hospital, target_req=target_request)


@app.route("/patient/compare-hospitals")
def patient_compare_hospitals():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('patient_registration_step1'))
        
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    req_id = request.args.get('request_id', type=int)
    prop_ids = request.args.get('proposal_ids')
    
    if req_id:
        target_req = TreatmentRequest.query.filter_by(id=req_id).first()
        if not target_req or target_req.patient_profile_id not in profile_ids:
            target_req = None
    else:
        # Fallback to the latest request that has submitted proposals
        all_reqs = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).order_by(TreatmentRequest.created_at.desc()).all()
        target_req = None
        for r in all_reqs:
            props = TreatmentProposal.query.filter_by(treatment_request_id=r.id, status='submitted').count()
            if props > 0:
                target_req = r
                break
                
    compare_items = []
    if target_req:
        q = TreatmentProposal.query.filter_by(treatment_request_id=target_req.id, status='submitted')
        if prop_ids:
            id_list = [int(i.strip()) for i in prop_ids.split(',') if i.strip().isdigit()]
            if id_list:
                q = q.filter(TreatmentProposal.id.in_(id_list))
                
        proposals = q.limit(3).all()
        for p in proposals:
            h = Hospital.query.get(p.hospital_id)
            if h:
                compare_items.append({'proposal': p, 'hospital': h})
                
    return render_template("patient-compare-hospitals.html", compare_items=compare_items, target_req=target_req, user=user)


@app.route("/patient/treatment-proposal/<int:proposal_id>")
def patient_treatment_proposal_details(proposal_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    if not user or not profiles:
        return redirect(url_for('patient_registration_step1'))
        
    profile_ids = [p.id for p in profiles]
    
    proposal = TreatmentProposal.query.get_or_404(proposal_id)
    req = TreatmentRequest.query.get(proposal.treatment_request_id)
    
    # Security: Ensure request belongs to user and proposal is submitted
    if not req or req.patient_profile_id not in profile_ids or proposal.status != 'submitted':
        from flask import abort
        abort(403)
        
    profile = PatientProfile.query.get(req.patient_profile_id)
    hospital = Hospital.query.get(proposal.hospital_id)
    
    return render_template("patient-treatment-proposal-details.html", proposal=proposal, request=req, profile=profile, hospital=hospital, user=user)


# =========================================================
# SECURE MESSAGES
# =========================================================

@app.route("/hospital/messages")
def hospital_messages():
    hospital_user_id = session.get('hospital_user_id')
    if not hospital_user_id:
        return redirect(url_for('hospital_login'))
        
    from models import HospitalUser
    hospital_user = HospitalUser.query.get(hospital_user_id)
    if not hospital_user:
        return redirect(url_for('hospital_login'))
    hospital = hospital_user.hospital

    from models import MessageThread, HospitalUser, Message
    threads = MessageThread.query.filter_by(hospital_id=hospital.id).order_by(MessageThread.updated_at.desc()).all()
    
    sidebar_threads = []
    for t in threads:
        all_msgs = t.messages.all()
        sidebar_threads.append({
            'thread': t,
            'latest_message': all_msgs[-1] if all_msgs else None,
            'unread_count': 0 # For future implementation
        })

    return render_template("hospital-messages.html", hospital=hospital, sidebar_threads=sidebar_threads)

@app.route("/hospital/messages/<int:thread_id>")
def hospital_message_thread(thread_id):
    hospital_user_id = session.get('hospital_user_id')
    if not hospital_user_id:
        return redirect(url_for('hospital_login'))
        
    from models import HospitalUser
    hospital_user = HospitalUser.query.get(hospital_user_id)
    if not hospital_user:
        return redirect(url_for('hospital_login'))
    hospital = hospital_user.hospital

    from models import MessageThread, HospitalUser, Message
    thread = MessageThread.query.get_or_404(thread_id)
    
    # Authorization Check
    if thread.hospital_id != hospital.id:
        abort(403)
        
    messages = thread.messages.all()

    return render_template("hospital-message-thread.html", hospital=hospital, thread=thread, messages=messages)

@app.route("/hospital/messages/<int:thread_id>/send", methods=["POST"])
def hospital_send_message(thread_id):
    hospital_user_id = session.get('hospital_user_id')
    if not hospital_user_id:
        return redirect(url_for('hospital_login'))
        
    hospital_user = HospitalUser.query.get(hospital_user_id)
    if not hospital_user:
        return redirect(url_for('hospital_login'))
    hospital = hospital_user.hospital
        
    message_body = request.form.get('message_body', '').strip()
    if not message_body:
        return redirect(url_for('hospital_message_thread', thread_id=thread_id))

    from models import MessageThread, Message
    thread = MessageThread.query.get_or_404(thread_id)
    
    # Authorization Check
    if thread.hospital_id != hospital.id:
        abort(403)
        
    msg = Message(
        thread_id=thread_id,
        sender_type='hospital',
        sender_hospital_id=hospital.id,
        message_body=message_body
    )
    
    from datetime import datetime
    thread.updated_at = datetime.utcnow()
    
    db.session.add(msg)
    db.session.commit()
    
    return redirect(url_for('hospital_message_thread', thread_id=thread_id))


@app.route("/patient/secure-messages")
def patient_secure_messages():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    
    threads = []
    active_thread = None
    
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    if profiles:
        profile_ids = [p.id for p in profiles]
        requests = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).all()
        if requests:
            request_ids = [r.id for r in requests]
            from models import MessageThread, Message
            
            # Subquery to order threads by their most recent message, or creation date
            threads = MessageThread.query.filter(MessageThread.treatment_request_id.in_(request_ids)).order_by(MessageThread.updated_at.desc()).all()
            
            thread_id = request.args.get('thread_id', type=int)
            if thread_id:
                # Security: Verify the requested thread is actually in the patient's authorized threads
                active_thread = next((t for t in threads if t.id == thread_id), None)
                if not active_thread:
                    flash("Unauthorized access or thread not found.", "error")
                    return redirect(url_for('patient_secure_messages'))

    return render_template("patient-secure-messages.html", user=user, threads=threads, active_thread=active_thread)

@app.route("/patient/secure-messages/start", methods=["POST"])
def patient_secure_messages_start():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    treatment_request_id = request.form.get('treatment_request_id', type=int)
    hospital_id = request.form.get('hospital_id', type=int)
    
    if not treatment_request_id or not hospital_id:
        flash("Invalid request parameters.", "error")
        return redirect(url_for('patient_hospital_responses'))
        
    # Authorization check
    req = TreatmentRequest.query.get(treatment_request_id)
    if not req:
        abort(404)
        
    profile = PatientProfile.query.filter_by(id=req.patient_profile_id, user_id=user_id).first()
    if not profile:
        abort(403) # Not authorized
        
    # Verify hospital actually submitted a proposal for this request (V1 rule)
    proposal = TreatmentProposal.query.filter_by(treatment_request_id=treatment_request_id, hospital_id=hospital_id).first()
    if not proposal:
        flash("Hospital has not submitted a proposal for this request.", "error")
        return redirect(url_for('patient_hospital_responses'))
        
    from models import MessageThread
    
    # Check if thread exists
    thread = MessageThread.query.filter_by(treatment_request_id=treatment_request_id, hospital_id=hospital_id).first()
    
    if not thread:
        thread = MessageThread(treatment_request_id=treatment_request_id, hospital_id=hospital_id)
        db.session.add(thread)
        db.session.commit()
        
    return redirect(url_for('patient_secure_messages', thread_id=thread.id))

@app.route("/patient/secure-messages/<int:thread_id>/send", methods=["POST"])
def patient_secure_messages_send(thread_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    message_body = request.form.get('message_body', '').strip()
    if not message_body:
        return redirect(url_for('patient_secure_messages', thread_id=thread_id))
        
    from models import MessageThread, Message
    thread = MessageThread.query.get_or_404(thread_id)
    
    # Authorization Check
    req = thread.treatment_request
    profile = PatientProfile.query.filter_by(id=req.patient_profile_id, user_id=user_id).first()
    if not profile:
        abort(403)
        
    msg = Message(
        thread_id=thread_id,
        sender_type='patient',
        sender_user_id=user_id,
        message_body=message_body
    )
    
    # Update thread's updated_at timestamp to bubble it up
    from datetime import datetime
    thread.updated_at = datetime.utcnow()
    
    db.session.add(msg)
    db.session.commit()
    
    return redirect(url_for('patient_secure_messages', thread_id=thread_id))



@app.route("/patient/profile-settings")
def patient_profile_settings():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    
    return render_template("patient-profile-settings.html", user=user, profiles=profiles)


@app.route("/patient/profile/edit/<int:profile_id>", methods=["GET", "POST"])
def patient_profile_edit(profile_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    profile = PatientProfile.query.filter_by(id=profile_id, user_id=user_id).first()
    if not profile:
        return redirect(url_for('patient_profile_settings'))
        
    error = None
    if request.method == "POST":
        # Ensure we only update PatientProfile fields, never the User model
        profile.first_name = request.form.get("first-name", "").strip().title()
        profile.last_name = request.form.get("last-name", "").strip().title()
        
        dob_str = request.form.get("dob", "").strip()
        if dob_str:
            try:
                profile.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                error = "Invalid date format."
                
        profile.gender = request.form.get("gender", profile.gender).strip()
        profile.nationality = request.form.get("nationality", profile.nationality).strip()
        profile.country_of_residence = request.form.get("residence", profile.country_of_residence).strip()
        profile.city = request.form.get("city", profile.city).strip()
        profile.passport_number = request.form.get("passport", profile.passport_number).strip()
        
        if not error:
            try:
                db.session.commit()
                return redirect(url_for("patient_profile_settings"))
            except Exception as e:
                db.session.rollback()
                error = "Could not save changes."
                
    return render_template("patient-registration-step2.html", 
        error=error, 
        is_self=(profile.relationship_type == 'Self'),
        default_first_name=profile.first_name,
        default_last_name=profile.last_name,
        default_residence=profile.country_of_residence,
        profile=profile,
        edit_mode=True
    )


# =========================================================
# HOSPITAL PORTAL ROUTES
# =========================================================

@app.route("/hospital/register", methods=["GET", "POST"])
def hospital_register():
    # If user is already in a session, redirect appropriately
    existing_hospital_id = session.get('hospital_id')
    if existing_hospital_id:
        return redirect(url_for('hospital_dashboard'))

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        work_email = request.form.get("work_email", "").strip().lower()
        phone_country_code = request.form.get("phone_country_code", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        error = None
        
        # Validation
        if not all([first_name, last_name, work_email, password, confirm_password]):
            error = "Please fill in all required fields."
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", work_email):
            error = "Please enter a valid email address."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif len(password) < 8:
            error = "Password must be at least 8 characters long."
        else:
            # Check for duplicate email
            existing_user = HospitalUser.query.filter_by(work_email=work_email).first()
            if existing_user:
                error = "An account with this email already exists."
                
        if error:
            return render_template("hospital-registration-step1.html", error=error)
            
        try:
            # Create Hospital
            new_hospital = Hospital(
                verification_status="incomplete"
            )
            db.session.add(new_hospital)
            db.session.flush() # Get the new hospital ID
            
            # Create HospitalUser
            new_user = HospitalUser(
                hospital_id=new_hospital.id,
                first_name=first_name,
                last_name=last_name,
                work_email=work_email,
                phone_country_code=phone_country_code,
                phone_number=phone_number,
                password_hash=generate_password_hash(password),
                role="hospital_admin"
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Store in session securely
            session['hospital_id'] = new_hospital.id
            session['hospital_user_id'] = new_user.id
            
            return redirect(url_for('hospital_register_info'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.exception("Hospital registration failed")
            error = "An error occurred during registration. Please try again."
            return render_template("hospital-registration-step1.html", error=error)

    return render_template("hospital-registration-step1.html")

@app.route("/hospital/register/information", methods=["GET", "POST"])
def hospital_register_info():
    hospital_id = session.get('hospital_id')
    hospital_user_id = session.get('hospital_user_id')
    
    if not hospital_id or not hospital_user_id:
        return redirect(url_for('hospital_register'))
        
    user = HospitalUser.query.filter_by(id=hospital_user_id, hospital_id=hospital_id).first()
    if not user:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    if hospital.verification_status != "incomplete":
        return redirect(url_for('hospital_register_success'))

    error = None

    if request.method == "POST":
        legal_name = request.form.get("legal_name", "").strip()
        display_name = request.form.get("display_name", "").strip()
        hospital_type = request.form.get("hospital_type", "").strip()
        year_established = request.form.get("year_established", "").strip()
        country = request.form.get("country", "").strip()
        state_region = request.form.get("state_region", "").strip()
        city = request.form.get("city", "").strip()
        address = request.form.get("address", "").strip()
        postal_code = request.form.get("postal_code", "").strip()
        website = request.form.get("website", "").strip()
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
            
        description = request.form.get("description", "").strip()
        
        # Required Field Validation
        if not all([legal_name, hospital_type, country, state_region, city, address]):
            error = "Please fill in all required fields."
        else:
            # Year Validation
            if year_established:
                try:
                    year_val = int(year_established)
                    current_year = datetime.now().year
                    if year_val > current_year or year_val < 1000:
                        error = "Please enter a valid establishment year."
                except ValueError:
                    error = "Year must be a number."

            if not error:
                try:
                    hospital.legal_name = legal_name
                    hospital.display_name = display_name if display_name else None
                    hospital.hospital_type = hospital_type
                    hospital.year_established = int(year_established) if year_established else None
                    hospital.country = country
                    hospital.state_region = state_region
                    hospital.city = city
                    hospital.address = address
                    hospital.postal_code = postal_code if postal_code else None
                    hospital.website = website if website else None
                    hospital.description = description if description else None
                    
                    db.session.commit()
                    return redirect(url_for('hospital_register_capabilities'))
                except Exception as e:
                    db.session.rollback()
                    error = "An error occurred while saving your information. Please try again."

    # For GET requests or validation failures, render the form passing back any existing data
    form_data = request.form if request.method == "POST" else {}
    return render_template("hospital-registration-step2.html", error=error, form_data=form_data)

@app.route("/hospital/register/capabilities", methods=["GET", "POST"])
def hospital_register_capabilities():
    hospital_id = session.get('hospital_id')
    hospital_user_id = session.get('hospital_user_id')
    
    if not hospital_id or not hospital_user_id:
        return redirect(url_for('hospital_register'))
        
    user = HospitalUser.query.filter_by(id=hospital_user_id, hospital_id=hospital_id).first()
    if not user:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    if hospital.verification_status != "incomplete":
        return redirect(url_for('hospital_register_success'))

    error = None
    all_specialties = Specialty.query.order_by(Specialty.name).all()

    if request.method == "POST":
        selected_specialty_ids = request.form.getlist("specialties")
        other_specialty = request.form.get("other_specialty", "").strip()
        treatments_json = request.form.get("treatments", "[]")
        centers_json = request.form.get("centers_of_excellence", "[]")
        international = request.form.get("international_patients", "")
        
        # Validation
        if not selected_specialty_ids and not other_specialty:
            error = "Please select at least one medical specialty."
            
        if not error:
            try:
                # Update specialties relationship only if new valid specialties are provided
                if selected_specialty_ids:
                    hospital.specialties = [] # Clear existing
                    specialties_to_add = Specialty.query.filter(Specialty.id.in_(selected_specialty_ids)).all()
                    hospital.specialties.extend(specialties_to_add)
                
                hospital.other_specialty = other_specialty if other_specialty else None
                
                # Parse JSON arrays safely
                try:
                    treatments_list = json.loads(treatments_json)
                    hospital.treatments = [str(t).strip() for t in treatments_list if str(t).strip()]
                except Exception:
                    hospital.treatments = []
                    
                try:
                    centers_list = json.loads(centers_json)
                    hospital.centers_of_excellence = [str(c).strip() for c in centers_list if str(c).strip()]
                except Exception:
                    hospital.centers_of_excellence = []
                    
                hospital.international_patient_experience = international if international else None
                
                db.session.commit()
                return redirect(url_for('hospital_register_facilities'))
            except Exception as e:
                db.session.rollback()
                error = "An error occurred while saving capabilities. Please try again."

    # Pre-fill for GET or validation error
    selected_ids = [str(s.id) for s in hospital.specialties]
    
    return render_template(
        "hospital-registration-step3.html",
        error=error,
        all_specialties=all_specialties,
        hospital=hospital,
        selected_ids=selected_ids
    )

@app.route("/hospital/register/facilities", methods=["GET", "POST"])
def hospital_register_facilities():
    hospital_id = session.get('hospital_id')
    hospital_user_id = session.get('hospital_user_id')
    
    if not hospital_id or not hospital_user_id:
        return redirect(url_for('hospital_register'))
        
    user = HospitalUser.query.filter_by(id=hospital_user_id, hospital_id=hospital_id).first()
    if not user:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    if hospital.verification_status != "incomplete":
        return redirect(url_for('hospital_register_success'))

    error = None
    all_languages = Language.query.order_by(Language.name).all()

    if request.method == "POST":
        core_facilities = request.form.getlist("core_facilities")
        has_inpatient = request.form.get("has_inpatient_rooms") == "Yes"
        inpatient_rooms = request.form.getlist("inpatient_rooms") if has_inpatient else []
        international_services = request.form.getlist("international_services")
        selected_language_ids = request.form.getlist("languages")
        other_languages = request.form.get("other_languages", "").strip()
        food_and_dietary = request.form.getlist("food_and_dietary")
        other_dietary = request.form.get("other_dietary", "").strip()
        accessibility = request.form.getlist("accessibility")
        
        # Validation
        if not selected_language_ids and not other_languages:
            error = "Please select at least one communication language."
            
        if not error:
            try:
                hospital.core_facilities = core_facilities
                hospital.has_inpatient_rooms = has_inpatient
                hospital.inpatient_rooms = inpatient_rooms
                
                # Check mutually exclusive "none" for international services
                if "none" in international_services:
                    hospital.international_services_offered = ["none"]
                else:
                    hospital.international_services_offered = international_services
                    
                # Update languages relationship
                hospital.languages = []
                if selected_language_ids:
                    languages_to_add = Language.query.filter(Language.id.in_(selected_language_ids)).all()
                    hospital.languages.extend(languages_to_add)
                
                hospital.other_languages = other_languages if other_languages else None
                hospital.food_and_dietary = food_and_dietary
                hospital.other_dietary = other_dietary if other_dietary else None
                hospital.accessibility = accessibility
                
                db.session.commit()
                return redirect(url_for('hospital_register_verification'))
            except Exception as e:
                db.session.rollback()
                error = "An error occurred while saving facilities. Please try again."

    # Pre-fill for GET or validation error
    selected_language_ids = [str(l.id) for l in hospital.languages]
    
    return render_template(
        "hospital-registration-step4.html",
        error=error,
        all_languages=all_languages,
        hospital=hospital,
        selected_language_ids=selected_language_ids
    )

@app.route("/hospital/register/verification", methods=["GET", "POST"])
def hospital_register_verification():
    hospital_id = session.get('hospital_id')
    hospital_user_id = session.get('hospital_user_id')
    
    if not hospital_id or not hospital_user_id:
        return redirect(url_for('hospital_register'))
        
    user = HospitalUser.query.filter_by(id=hospital_user_id, hospital_id=hospital_id).first()
    if not user:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    if hospital.verification_status != "incomplete":
        return redirect(url_for('hospital_register_success'))

    error = None

    if request.method == "POST":
        legal_name = request.form.get("legal_name", "").strip()
        registration_license_number = request.form.get("registration_license_number", "").strip()
        licensing_authority = request.form.get("licensing_authority", "").strip()
        registration_country = request.form.get("registration_country", "").strip()
        
        issue_date_str = request.form.get("license_issue_date")
        expiry_date_str = request.form.get("license_expiry_date")
        
        has_accreditations = request.form.get("has_accreditations") == "Yes"
        
        # Parse Dates
        issue_date = None
        expiry_date = None
        
        if issue_date_str:
            try:
                issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d").date()
            except ValueError:
                error = "Invalid Issue Date format."
                
        if expiry_date_str:
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            except ValueError:
                error = "Invalid Expiry Date format."

        # Validation
        if not legal_name or not registration_license_number or not licensing_authority or not registration_country:
            error = "Please fill all required legal registration fields."
            
        if not error and issue_date and expiry_date and expiry_date < issue_date:
            error = "Expiry Date cannot be earlier than Issue Date."
            
        # File Validation
        files_to_save = []
        if not error:
            # Main registration doc (Required if not already uploaded)
            main_doc_existing = HospitalVerificationDocument.query.filter_by(
                hospital_id=hospital.id, document_category="Hospital Registration / Operating License"
            ).first()
            
            main_doc_file = request.files.get("doc_registration")
            
            if not main_doc_existing and (not main_doc_file or main_doc_file.filename == ""):
                error = "Hospital Registration / Operating License document is required."
            
            # Check all uploaded files for size and extension
            for file_key in request.files:
                file = request.files[file_key]
                if file and file.filename != "":
                    if not allowed_file(file.filename):
                        error = f"Invalid file type for {file.filename}. Only PDF, JPG, JPEG, and PNG are allowed."
                        break
                    
                    # Size check (10MB)
                    file.seek(0, os.SEEK_END)
                    size = file.tell()
                    file.seek(0)
                    if size > 10 * 1024 * 1024:
                        error = f"File {file.filename} exceeds the 10MB limit."
                        break
                        
                    # Map to category
                    category = "Other Supporting Document"
                    if file_key == "doc_registration":
                        category = "Hospital Registration / Operating License"
                    elif file_key == "doc_accreditation":
                        category = "Accreditation Certificate"
                    elif file_key == "doc_gov":
                        category = "Government Registration Certificate"
                    elif file_key == "doc_tax":
                        category = "Tax / Business Registration Document"
                        
                    files_to_save.append((file, category, size))

        if not error:
            try:
                hospital.legal_name = legal_name # Canonical update
                hospital.registration_country = registration_country
                hospital.registration_license_number = registration_license_number
                hospital.licensing_authority = licensing_authority
                hospital.license_issue_date = issue_date
                hospital.license_expiry_date = expiry_date
                hospital.has_accreditations = has_accreditations
                
                # Accreditations
                # Clear existing to handle dynamic list
                for acc in hospital.accreditations:
                    db.session.delete(acc)
                
                if has_accreditations:
                    acc_names = request.form.getlist("acc_name[]")
                    acc_nums = request.form.getlist("acc_number[]")
                    acc_dates = request.form.getlist("acc_valid_until[]")
                    
                    for i in range(len(acc_names)):
                        name = acc_names[i].strip()
                        if name:
                            valid_until = None
                            if i < len(acc_dates) and acc_dates[i]:
                                try:
                                    valid_until = datetime.strptime(acc_dates[i], "%Y-%m-%d").date()
                                except ValueError:
                                    pass
                            
                            new_acc = HospitalAccreditation(
                                hospital_id=hospital.id,
                                name=name,
                                certificate_number=acc_nums[i].strip() if i < len(acc_nums) else None,
                                valid_until=valid_until
                            )
                            db.session.add(new_acc)

                # Save files
                for file_obj, category, size in files_to_save:
                    # If it's a replacement for a singular category like registration, delete old one
                    if category == "Hospital Registration / Operating License":
                        old_doc = HospitalVerificationDocument.query.filter_by(
                            hospital_id=hospital.id, document_category=category
                        ).first()
                        if old_doc:
                            db.session.delete(old_doc)
                            # Actual file deletion would go here if needed, skipping for brevity
                    
                    original_filename = secure_filename(file_obj.filename)
                    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
                    storage_filename = f"{uuid.uuid4().hex}.{ext}"
                    
                    save_path = os.path.join(HOSPITAL_DOCS_FOLDER, storage_filename)
                    file_obj.save(save_path)
                    
                    new_doc = HospitalVerificationDocument(
                        hospital_id=hospital.id,
                        uploaded_by_id=user.id,
                        original_filename=original_filename,
                        storage_filename=storage_filename,
                        document_category=category,
                        mime_type=file_obj.mimetype,
                        file_size=size
                    )
                    db.session.add(new_doc)

                db.session.commit()
                return redirect(url_for('hospital_register_review'))
            except Exception as e:
                db.session.rollback()
                error = "An error occurred while saving verification details. Please try again."
                print(f"Error: {e}")

    return render_template(
        "hospital-registration-step5.html",
        error=error,
        hospital=hospital
    )

@app.route("/hospital/document/remove/<int:doc_id>", methods=["POST"])
def hospital_remove_document(doc_id):
    hospital_id = session.get('hospital_id')
    if not hospital_id:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
        
    doc = HospitalVerificationDocument.query.get(doc_id)
    if not doc or doc.hospital_id != hospital_id:
        return jsonify({"success": False, "error": "Document not found"}), 404
        
    hospital = Hospital.query.get(hospital_id)
    if hospital and hospital.verification_status != "incomplete":
        return jsonify({"success": False, "error": "Cannot modify submitted registration"}), 403
        
    try:
        # Delete file
        file_path = os.path.join(HOSPITAL_DOCS_FOLDER, doc.storage_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        db.session.delete(doc)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/hospital/register/review", methods=["GET", "POST"])
def hospital_register_review():
    hospital_id = session.get('hospital_id')
    hospital_user_id = session.get('hospital_user_id')
    
    if not hospital_id or not hospital_user_id:
        return redirect(url_for('hospital_register'))
        
    user = HospitalUser.query.filter_by(id=hospital_user_id, hospital_id=hospital_id).first()
    if not user:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    if hospital.verification_status != "incomplete":
        return redirect(url_for('hospital_register_success'))

    error = None

    if request.method == "POST":
        declaration = request.form.get("declaration")
        if declaration != "on":
            error = "You must agree to the declaration before submitting."
        else:
            try:
                hospital.verification_status = "pending_verification"
                db.session.commit()
                return redirect(url_for('hospital_register_success'))
            except Exception as e:
                db.session.rollback()
                error = "An error occurred while submitting your registration. Please try again."

    return render_template("hospital-registration-step6.html", hospital=hospital, user=user, error=error)

@app.route("/hospital/register/success")
def hospital_register_success():
    hospital_id = session.get('hospital_id')
    hospital_user_id = session.get('hospital_user_id')
    
    if not hospital_id or not hospital_user_id:
        return redirect(url_for('hospital_register'))
        
    return render_template("hospital-registration-success.html")

@app.route("/hospital/login", methods=["GET", "POST"])
def hospital_login():
    existing_hospital_id = session.get('hospital_id')
    if existing_hospital_id:
        existing_hospital = Hospital.query.get(existing_hospital_id)
        if existing_hospital:
            if existing_hospital.verification_status != "incomplete":
                return redirect(url_for('hospital_dashboard'))
            return redirect(url_for('hospital_register_info'))
            
    error = None
    if request.method == "POST":
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
                
    return render_template("hospital-login.html", error=error)

@app.route("/hospital/dashboard")
def hospital_dashboard():
    hospital_id = session.get('hospital_id')
    hospital_user_id = session.get('hospital_user_id')
    
    if not hospital_id or not hospital_user_id:
        return redirect(url_for('hospital_register'))
        
    user = HospitalUser.query.filter_by(id=hospital_user_id, hospital_id=hospital_id).first()
    if not user:
        session.clear()
        return redirect(url_for('hospital_register'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_register'))

    if hospital.verification_status == "incomplete":
        return redirect(url_for('hospital_register_info'))
        
    eligible_requests_count = 0
    submitted_proposals_count = 0
    if hospital and hospital.verification_status == 'verified':
        eligible_requests_count = get_visible_treatment_requests(hospital).count()
        submitted_proposals_count = TreatmentProposal.query.filter_by(hospital_id=hospital.id, status='submitted').count()
                
    return render_template("hospital-dashboard.html", hospital=hospital, user=user, eligible_requests_count=eligible_requests_count, submitted_proposals_count=submitted_proposals_count)

@app.route("/hospital/profile")
def hospital_profile():
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_login'))
        
    return render_template("hospital-profile.html", hospital=hospital)

@app.route("/hospital/settings")
def hospital_settings():
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        session.clear()
        return redirect(url_for('hospital_login'))
        
    return render_template("hospital-settings.html", hospital=hospital)

def get_visible_treatment_requests(hospital):
    """
    Returns a SQLAlchemy query for all treatment requests that the given hospital is allowed to view.
    MVP Logic: All verified hospitals can view all active/open requests.
    """
    if not hospital or hospital.verification_status != 'verified':
        return TreatmentRequest.query.filter(False)
        
    return TreatmentRequest.query.filter(
        TreatmentRequest.status.notin_(['Closed', 'Completed', 'Cancelled', 'Expired']),
        TreatmentRequest.status == 'Active'
    )

def _is_hospital_eligible(hospital, request_specialty):
    if not request_specialty:
        return False
    hospital_specialties = [s.name.lower() for s in hospital.specialties]
    req_spec_lower = request_specialty.lower()
    for hs in hospital_specialties:
        if req_spec_lower in hs or hs in req_spec_lower:
            return True
    return False

@app.route("/hospital/treatment-requests")
def hospital_treatment_requests():
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        return redirect(url_for('hospital_dashboard'))
        
    # UI Filters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    country_filter = request.args.get('country', '').strip()
    sort_order = request.args.get('sort', 'newest')

    query = get_visible_treatment_requests(hospital)
    
    if search_query:
        query = query.filter(db.or_(
            TreatmentRequest.reference_id.ilike(f"%{search_query}%"),
            TreatmentRequest.specialty.ilike(f"%{search_query}%"),
            TreatmentRequest.primary_diagnosis.ilike(f"%{search_query}%")
        ))
        
    if category_filter:
        query = query.filter(TreatmentRequest.specialty.ilike(f"%{category_filter}%"))
        
    if country_filter:
        # Need to join PatientProfile to search by country
        from models import PatientProfile
        query = query.join(PatientProfile).filter(PatientProfile.country.ilike(f"%{country_filter}%"))
        
    if sort_order == 'oldest':
        query = query.order_by(TreatmentRequest.created_at.asc())
    else:
        query = query.order_by(TreatmentRequest.created_at.desc())

    paginated_requests = query.paginate(page=page, per_page=20, error_out=False)
    
    # Pre-fetch hospital proposals to determine button states
    from models import TreatmentProposal
    proposals = TreatmentProposal.query.filter_by(hospital_id=hospital.id).all()
    hospital_proposals = {p.treatment_request_id: p for p in proposals}
            
    return render_template(
        "hospital-treatment-requests.html", 
        requests=paginated_requests, 
        hospital=hospital,
        hospital_proposals=hospital_proposals,
        search=search_query,
        category=category_filter,
        country=country_filter,
        sort=sort_order
    )

@app.route("/hospital/treatment-requests/<string:reference_id>")
def hospital_treatment_request_detail(reference_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        return redirect(url_for('hospital_dashboard'))
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403, description="This treatment request is no longer active.")
        
    from models import TreatmentProposal
    existing_proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first()
        
    return render_template("hospital-treatment-request-detail.html", req=req, hospital=hospital, existing_proposal=existing_proposal)

@app.route("/hospital/treatment-requests/document/<int:doc_id>")
def hospital_treatment_request_document(doc_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        abort(403)
        
    doc = MedicalDocument.query.get_or_404(doc_id)
    
    # Check if doc has a treatment_request, if not check patient_profile's active request
    req = doc.treatment_request
    if not req:
        req = TreatmentRequest.query.filter_by(patient_profile_id=doc.patient_profile_id, status='Active').first()
        if not req:
            abort(403)
            
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403)
        
    return send_from_directory(UPLOAD_FOLDER, doc.storage_filename)

@app.route("/hospital/treatment-requests/document/<int:doc_id>/download")
def hospital_treatment_request_document_download(doc_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        abort(403)
        
    doc = MedicalDocument.query.get_or_404(doc_id)
    
    req = doc.treatment_request
    if not req:
        req = TreatmentRequest.query.filter_by(patient_profile_id=doc.patient_profile_id, status='Active').first()
        if not req:
            abort(403)
            
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403, description="This treatment request is no longer active.")
        
    return send_from_directory(UPLOAD_FOLDER, doc.storage_filename, as_attachment=True, download_name=doc.original_filename)

@app.route("/hospital/proposals")
def hospital_proposals():
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        abort(403)
        
    proposals = TreatmentProposal.query.filter_by(hospital_id=hospital.id).order_by(TreatmentProposal.created_at.desc()).all()
    
    today = datetime.now(timezone.utc).date()
    for prop in proposals:
        if prop.status == 'submitted' and prop.valid_until and prop.valid_until < today:
            prop.display_status = 'Expired'
        elif prop.status == 'submitted':
            prop.display_status = 'Submitted'
        else:
            prop.display_status = 'Draft'
            
    return render_template("hospital-proposals.html", hospital=hospital, proposals=proposals)

@app.route("/hospital/treatment-requests/<string:reference_id>/proposal/edit", methods=['GET', 'POST'])
def hospital_proposal_edit(reference_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        if request.method == 'POST':
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        if request.method == 'POST':
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        abort(403)
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        if request.method == 'POST':
            return jsonify({'status': 'error', 'message': 'This treatment request is no longer active.'}), 403
        abort(403, description="This treatment request is no longer active.")

    proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first()
    
    if proposal and proposal.status == 'submitted':
        return redirect(url_for('hospital_proposal_view', reference_id=reference_id))

    if request.method == 'POST':
        data = request.json
        if not proposal:
            proposal = TreatmentProposal(treatment_request_id=req.id, hospital_id=hospital.id)
            db.session.add(proposal)
            
        proposal.proposed_treatment = data.get('proposed_treatment')
        proposal.treatment_plan = data.get('treatment_plan')
        proposal.specialty = data.get('specialty')
        proposal.lead_doctor = data.get('lead_doctor')
        
        try:
            proposal.estimated_duration_value = int(data.get('estimated_duration_value')) if data.get('estimated_duration_value') else None
        except ValueError:
            proposal.estimated_duration_value = None
            
        proposal.estimated_duration_unit = data.get('estimated_duration_unit')
        
        try:
            proposal.hospital_stay_nights = int(data.get('hospital_stay_nights')) if data.get('hospital_stay_nights') else None
            proposal.recovery_stay_days = int(data.get('recovery_stay_days')) if data.get('recovery_stay_days') else None
        except ValueError:
            pass
            
        proposal.currency = data.get('currency')
        try:
            proposal.estimated_cost_min = float(data.get('estimated_cost_min')) if data.get('estimated_cost_min') else None
            proposal.estimated_cost_max = float(data.get('estimated_cost_max')) if data.get('estimated_cost_max') else None
        except ValueError:
            pass
            
        proposal.inclusions = data.get('inclusions')
        proposal.exclusions = data.get('exclusions')
        proposal.requirements = data.get('requirements')
        proposal.additional_notes = data.get('additional_notes')
        
        valid_until_str = data.get('valid_until')
        if not valid_until_str:
            return jsonify({'status': 'error', 'message': 'Proposal Validity Date is required.'}), 400
            
        try:
            parsed_date = datetime.strptime(valid_until_str, '%Y-%m-%d').date()
            today = datetime.now(timezone.utc).date()
            try:
                max_date = today.replace(year=today.year + 1)
            except ValueError:
                max_date = today.replace(year=today.year + 1, month=2, day=28)
                
            if parsed_date < today:
                return jsonify({'status': 'error', 'message': 'Proposal Validity Date cannot be in the past.'}), 400
            if parsed_date > max_date:
                return jsonify({'status': 'error', 'message': 'Proposal Validity Date cannot be more than 1 year from today.'}), 400
                
            proposal.valid_until = parsed_date
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid Proposal Validity Date format.'}), 400
                
        # Line items
        # First clear old
        if proposal.id:
            CostLineItem.query.filter_by(proposal_id=proposal.id).delete()
        else:
            db.session.flush() # get ID
            
        line_items = data.get('line_items', [])
        for item in line_items:
            try:
                amt = float(item.get('amount', 0))
                desc = item.get('description', '').strip()
                if desc and amt > 0:
                    li = CostLineItem(proposal_id=proposal.id, description=desc, amount=amt)
                    db.session.add(li)
            except ValueError:
                continue
                
        db.session.commit()
        return jsonify({'status': 'success', 'proposal_id': proposal.id})

    # GET
    if not proposal:
        proposal = TreatmentProposal(
            treatment_request_id=req.id, 
            hospital_id=hospital.id,
            specialty=req.specialty
        )
        
    return render_template("hospital-proposal-edit.html", req=req, hospital=hospital, proposal=proposal)

@app.route("/hospital/treatment-requests/<string:reference_id>/proposal/review")
def hospital_proposal_review(reference_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        abort(403)
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403, description="This treatment request is no longer active.")
        
    proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first_or_404()
    if proposal.status == 'submitted':
        return redirect(url_for('hospital_proposal_view', reference_id=reference_id))
        
    today = datetime.now(timezone.utc).date()
    try:
        max_date = today.replace(year=today.year + 1)
    except ValueError:
        max_date = today.replace(year=today.year + 1, month=2, day=28)
        
    if not proposal.valid_until or proposal.valid_until < today or proposal.valid_until > max_date:
        flash("Please provide a valid Proposal Validity Date before reviewing.", "error")
        return redirect(url_for('hospital_proposal_edit', reference_id=reference_id))
        
    return render_template("hospital-proposal-review.html", req=req, hospital=hospital, proposal=proposal)

@app.route("/hospital/treatment-requests/<string:reference_id>/proposal/submit", methods=['POST'])
def hospital_proposal_submit(reference_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        if is_ajax: return jsonify({"status": "error", "message": "Not logged in"}), 401
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        if is_ajax: return jsonify({"status": "error", "message": "Forbidden"}), 403
        abort(403)
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        if is_ajax: return jsonify({"status": "error", "message": "Request no longer active"}), 400
        abort(403, description="This treatment request is no longer active.")
        
    proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first_or_404()
    if proposal.status == 'submitted':
        if is_ajax: return jsonify({"status": "success", "redirect_url": url_for('hospital_proposal_view', reference_id=reference_id)})
        flash("Proposal already submitted.", "info")
        return redirect(url_for('hospital_proposal_view', reference_id=reference_id))
        
    # Validation logic
    if not proposal.proposed_treatment or not proposal.treatment_plan:
        if is_ajax: return jsonify({"status": "error", "message": "Treatment details are required."}), 400
        flash("Treatment details are required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if not proposal.currency or proposal.estimated_cost_min is None or proposal.estimated_cost_max is None:
        if is_ajax: return jsonify({"status": "error", "message": "Valid cost estimates are required."}), 400
        flash("Valid cost estimates are required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if proposal.estimated_cost_min <= 0 or proposal.estimated_cost_max < proposal.estimated_cost_min:
        if is_ajax: return jsonify({"status": "error", "message": "Invalid cost ranges."}), 400
        flash("Invalid cost ranges.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if not proposal.valid_until:
        if is_ajax: return jsonify({"status": "error", "message": "Validity date is required."}), 400
        flash("Validity date is required.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    today = datetime.now(timezone.utc).date()
    try:
        max_date = today.replace(year=today.year + 1)
    except ValueError:
        max_date = today.replace(year=today.year + 1, month=2, day=28)
        
    if proposal.valid_until < today:
        if is_ajax: return jsonify({"status": "error", "message": "Validity date cannot be in the past."}), 400
        flash("Validity date cannot be in the past.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    if proposal.valid_until > max_date:
        if is_ajax: return jsonify({"status": "error", "message": "Validity date cannot be more than 1 year from today."}), 400
        flash("Validity date cannot be more than 1 year from today.", "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
        
    try:
        proposal.status = "submitted"
        proposal.submitted_at = datetime.now(timezone.utc)
        db.session.commit()
        
        # Add Notification Trigger
        try:
            create_notification(
                recipient_type='patient',
                recipient_user_id=req.patient_id,
                title="New Proposal Received",
                message=f"{hospital.legal_name} has submitted a new proposal for your request.",
                notification_type='proposal',
                reference_type='TreatmentProposal',
                reference_id=proposal.id,
                target_url=url_for('patient_treatment_proposal_details', proposal_id=proposal.id)
            )
        except Exception as e:
            print("Failed to create notification:", str(e))
            
    except Exception as e:
        db.session.rollback()
        if is_ajax: return jsonify({"status": "error", "message": "Database error: " + str(e)}), 500
        flash("Database error: " + str(e), "error")
        return redirect(url_for('hospital_proposal_review', reference_id=reference_id))
    
    if is_ajax:
        return jsonify({"status": "success", "redirect_url": url_for('hospital_proposal_view', reference_id=reference_id)})
        
    flash("Proposal submitted successfully.", "success")
    return redirect(url_for('hospital_proposal_view', reference_id=reference_id))

@app.route("/hospital/treatment-requests/<string:reference_id>/proposal/view")
def hospital_proposal_view(reference_id):
    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return redirect(url_for('hospital_login'))
        
    hospital = Hospital.query.get(hospital_id)
    if not hospital or hospital.verification_status != 'verified':
        abort(403)
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403, description="This treatment request is no longer active.")
        
    proposal = TreatmentProposal.query.filter_by(hospital_id=hospital.id, treatment_request_id=req.id).first_or_404()
    
    return render_template("hospital-proposal-review.html", req=req, hospital=hospital, proposal=proposal, is_view_only=True)

@app.route("/hospital/logout")
def hospital_logout():
    session.pop('hospital_id', None)
    session.pop('hospital_user_id', None)
    return redirect(url_for('home'))

# =========================================================
# ADMIN PORTAL ROUTES
# =========================================================

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_id = session.get('admin_id')
        if not admin_id:
            return redirect(url_for('admin_login'))
            
        user = User.query.get(admin_id)
        if not user or user.role != 'admin':
            session.pop('admin_id', None)
            return redirect(url_for('admin_login'))
            
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get('admin_id'):
        user = User.query.get(session.get('admin_id'))
        if user and user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
            
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        
        user = User.query.filter_by(email=email).first()
        if user and user.role == 'admin' and check_password_hash(user.password_hash, password):
            session['admin_id'] = user.id
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid email or password."
            
    return render_template("admin-login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    total_patients = User.query.filter_by(role='patient').count()
    total_hospitals = Hospital.query.count()
    active_requests = TreatmentRequest.query.filter(TreatmentRequest.status.in_(['Active', 'Pending'])).count()
    submitted_proposals = TreatmentProposal.query.filter_by(status='submitted').count()
    pending_count = Hospital.query.filter_by(verification_status="pending_verification").count()
    
    # Recent activity
    recent_requests = TreatmentRequest.query.order_by(TreatmentRequest.created_at.desc()).limit(5).all()
    recent_hospitals = Hospital.query.order_by(Hospital.created_at.desc()).limit(5).all()
    
    recent_activity = []
    for r in recent_requests:
        recent_activity.append({
            'type': 'request',
            'title': f'New Treatment Request ({r.reference_id})',
            'time': r.created_at,
            'url': url_for('admin_treatment_request_detail', reference_id=r.reference_id)
        })
    for h in recent_hospitals:
        recent_activity.append({
            'type': 'hospital',
            'title': f'Hospital Registration ({h.legal_name})',
            'time': h.created_at,
            'url': url_for('admin_application_review', hospital_id=h.id)
        })
        
    recent_activity.sort(key=lambda x: x['time'], reverse=True)
    recent_activity = recent_activity[:5]
    
    return render_template(
        "admin-dashboard.html",
        total_patients=total_patients,
        total_hospitals=total_hospitals,
        active_requests=active_requests,
        submitted_proposals=submitted_proposals,
        pending_count=pending_count,
        recent_activity=recent_activity
    )

@app.route("/admin/hospitals/applications")
@admin_required
def admin_applications():
    status = request.args.get('status', 'pending_verification')
    if status not in ['pending_verification', 'verified', 'rejected']:
        status = 'pending_verification'
        
    applications = Hospital.query.filter_by(verification_status=status).order_by(Hospital.updated_at.desc()).all()
    
    pending_count = Hospital.query.filter_by(verification_status='pending_verification').count()
    verified_count = Hospital.query.filter_by(verification_status='verified').count()
    rejected_count = Hospital.query.filter_by(verification_status='rejected').count()
    
    return render_template(
        "admin-applications.html", 
        applications=applications,
        current_status=status,
        pending_count=pending_count,
        verified_count=verified_count,
        rejected_count=rejected_count
    )

@app.route("/admin/hospitals/applications/<int:hospital_id>/review", methods=["GET", "POST"])
@admin_required
def admin_application_review(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    error = request.args.get('error')
    
    if request.method == "POST":
        notes = request.form.get("admin_notes", "").strip()
        hospital.admin_notes = notes
        db.session.commit()
        flash("Admin notes saved.", "success")
        return redirect(url_for("admin_application_review", hospital_id=hospital.id))
        
    return render_template("admin-application-review.html", hospital=hospital, error=error)

@app.route("/admin/hospitals/applications/document/<int:doc_id>")
@admin_required
def admin_application_document(doc_id):
    doc = HospitalVerificationDocument.query.get_or_404(doc_id)
    return send_from_directory(HOSPITAL_DOCS_FOLDER, doc.storage_filename)

@app.route("/admin/hospitals/applications/<int:hospital_id>/approve", methods=["POST"])
@admin_required
def admin_application_approve(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    if hospital.verification_status != 'pending_verification':
        return redirect(url_for('admin_application_review', hospital_id=hospital.id, error="Application is not pending verification."))
        
    hospital.verification_status = 'verified'
    hospital.reviewed_at = datetime.now(timezone.utc)
    hospital.reviewed_by_id = session.get('admin_id')
    db.session.commit()
    return redirect(url_for('admin_applications', status='verified'))

@app.route("/admin/hospitals/applications/<int:hospital_id>/reject", methods=["POST"])
@admin_required
def admin_application_reject(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    if hospital.verification_status != 'pending_verification':
        return redirect(url_for('admin_application_review', hospital_id=hospital.id, error="Application is not pending verification."))
        
    reason = request.form.get('rejection_reason', '').strip()
    if not reason:
        return redirect(url_for('admin_application_review', hospital_id=hospital.id, error="Rejection reason is required."))
        
    if len(reason) > 2000:
        return redirect(url_for('admin_application_review', hospital_id=hospital.id, error="Rejection reason is too long."))
        
    hospital.verification_status = 'rejected'
    hospital.rejection_reason = reason
    hospital.reviewed_at = datetime.now(timezone.utc)
    hospital.reviewed_by_id = session.get('admin_id')
    db.session.commit()
    return redirect(url_for('admin_applications', status='rejected'))

@app.route("/admin/treatment-requests")
@admin_required
def admin_treatment_requests():
    status_filter = request.args.get('status')
    specialty_filter = request.args.get('specialty')
    country_filter = request.args.get('country')
    search_query = request.args.get('q')
    
    query = TreatmentRequest.query.join(PatientProfile)
    
    if status_filter:
        query = query.filter(TreatmentRequest.status == status_filter)
        
    if specialty_filter:
        query = query.filter(TreatmentRequest.specialty == specialty_filter)
        
    if country_filter:
        query = query.filter(PatientProfile.country_of_residence == country_filter)
        
    if search_query:
        query = query.filter(
            (TreatmentRequest.reference_id.ilike(f"%{search_query}%")) |
            (PatientProfile.first_name.ilike(f"%{search_query}%")) |
            (PatientProfile.last_name.ilike(f"%{search_query}%"))
        )
        
    requests_list = query.order_by(TreatmentRequest.created_at.desc()).all()
    
    verified_hospitals_count = Hospital.query.filter_by(verification_status='verified').count()
    for req in requests_list:
        req.response_count = TreatmentProposal.query.filter_by(treatment_request_id=req.id, status='submitted').count()
        req.matched_count = verified_hospitals_count
        
    return render_template(
        "admin-treatment-requests.html", 
        requests=requests_list, 
        current_status=status_filter, 
        current_specialty=specialty_filter,
        current_country=country_filter,
        search_query=search_query
    )

@app.route("/admin/treatment-requests/<string:reference_id>")
@admin_required
def admin_treatment_request_detail(reference_id):
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    patient = req.patient_profile
    proposals = TreatmentProposal.query.filter_by(treatment_request_id=req.id).all()
    
    verified_hospitals = Hospital.query.filter_by(verification_status='verified').all()
    
    proposals_by_hospital = {p.hospital_id: p for p in proposals}
    
    hospital_matches = []
    for h in verified_hospitals:
        prop = proposals_by_hospital.get(h.id)
        hospital_matches.append({
            'hospital': h,
            'proposal': prop
        })
        
    docs = MedicalDocument.query.filter_by(treatment_request_id=req.id).all()
    
    from datetime import date
    today = date.today()
    if patient.date_of_birth:
        age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))
    else:
        age = None
    patient.age = age
    
    return render_template("admin-treatment-request-detail.html", 
                           req=req, 
                           patient=patient, 
                           proposals=proposals, 
                           docs=docs, 
                           hospital_matches=hospital_matches,
                           total_matched=len(verified_hospitals))

@app.route("/admin/treatment-requests/<string:reference_id>/proposal/<int:proposal_id>")
@admin_required
def admin_proposal_view(reference_id, proposal_id):
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    proposal = TreatmentProposal.query.filter_by(id=proposal_id, treatment_request_id=req.id, status='submitted').first_or_404()
    hospital = proposal.hospital
    
    return render_template("admin-proposal-view.html", req=req, proposal=proposal, hospital=hospital, is_view_only=True)


@app.route("/admin/patients")
@admin_required
def admin_patients():
    search_query = request.args.get('q')
    
    query = User.query.filter_by(role='patient')
    if search_query:
        query = query.filter(
            (User.email.ilike(f"%{search_query}%")) |
            (User.first_name.ilike(f"%{search_query}%")) |
            (User.last_name.ilike(f"%{search_query}%"))
        )
        
    patients = query.order_by(User.created_at.desc()).all()
    return render_template("admin-patients.html", patients=patients, search_query=search_query)

@app.route("/admin/patients/<int:user_id>")
@admin_required
def admin_patient_detail(user_id):
    patient = User.query.filter_by(id=user_id, role='patient').first_or_404()
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    
    profile_ids = [p.id for p in profiles]
    requests = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).order_by(TreatmentRequest.created_at.desc()).all()
    
    for req in requests:
        req.response_count = TreatmentProposal.query.filter_by(treatment_request_id=req.id, status='submitted').count()
        
    return render_template("admin-patient-detail.html", patient=patient, profiles=profiles, requests=requests)

@app.route("/admin/proposals")
@admin_required
def admin_proposals():
    q = request.args.get('q', '').strip()
    
    query = TreatmentProposal.query.join(TreatmentRequest).join(Hospital).filter(TreatmentProposal.status == 'submitted')
    
    if q:
        query = query.filter(
            db.or_(
                TreatmentRequest.reference_id.ilike(f'%{q}%'),
                Hospital.legal_name.ilike(f'%{q}%')
            )
        )
        
    proposals = query.order_by(TreatmentProposal.submitted_at.desc().nullslast(), TreatmentProposal.created_at.desc()).all()
    
    return render_template("admin-proposals.html", proposals=proposals, q=q)


# =========================================================
# DEVELOPMENT SERVER
# =========================================================


# =========================================================
# PATIENT MEDICAL DOCUMENTS
# =========================================================

@app.route("/patient/medical-documents")
def patient_medical_documents():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    docs = MedicalDocument.query.filter(MedicalDocument.patient_profile_id.in_(profile_ids)).order_by(MedicalDocument.uploaded_at.desc()).all()
    
    return render_template("patient-medical-documents.html", docs=docs, profiles=profiles)

@app.route("/patient/document/upload", methods=["POST"])
def patient_medical_documents_upload():
    user_id = session.get('registration_user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    document_type = request.form.get('document_type', 'Other')
    title = request.form.get('title')
    description = request.form.get('description')
    profile_id = request.form.get('patient_profile_id')
    treatment_request_id = request.form.get('treatment_request_id')
    
    if not profile_id:
        return jsonify({'error': 'Patient Profile is required'}), 400
        
    # Verify profile belongs to user
    profile = PatientProfile.query.filter_by(id=profile_id, user_id=user_id).first()
    if not profile:
        return jsonify({'error': 'Invalid Patient Profile'}), 400
        
    # Verify treatment request if provided
    if treatment_request_id:
        req = TreatmentRequest.query.filter_by(id=treatment_request_id, patient_profile_id=profile_id).first()
        if not req:
            return jsonify({'error': 'Invalid Treatment Request for this profile'}), 400
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        storage_filename = f"{uuid.uuid4().hex}.{ext}"
        
        file_path = os.path.join(UPLOAD_FOLDER, storage_filename)
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        new_doc = MedicalDocument(
            original_filename=original_filename,
            storage_filename=storage_filename,
            document_type=document_type,
            title=title,
            description=description,
            mime_type=file.content_type,
            file_size=file_size,
            patient_profile_id=profile_id,
            treatment_request_id=treatment_request_id if treatment_request_id else None,
            uploaded_by_id=user_id
        )
        db.session.add(new_doc)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Document uploaded successfully!'})
        
    return jsonify({'error': 'Invalid file type'}), 400

@app.route("/patient/document/<int:doc_id>/delete", methods=["POST"])
def patient_medical_document_delete(doc_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    doc = MedicalDocument.query.get_or_404(doc_id)
    
    if doc.uploaded_by_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        file_path = os.path.join(UPLOAD_FOLDER, doc.storage_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        db.session.delete(doc)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/patient/document/<int:doc_id>/view")
def view_document(doc_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        from flask import abort
        abort(401)
        
    doc = MedicalDocument.query.get_or_404(doc_id)
    if doc.uploaded_by_id != user_id:
        from flask import abort
        abort(403)
        
    return send_from_directory(UPLOAD_FOLDER, doc.storage_filename, as_attachment=False)



# =========================================================
# NOTIFICATION ENGINE HELPER
# =========================================================

def create_notification(recipient_type, recipient_user_id, title, message, notification_type, reference_type=None, reference_id=None, target_url=None):
    from models import db, Notification
    from datetime import datetime, timezone
    
    if not recipient_type or not recipient_user_id or not title or not message or not notification_type:
        return None
        
    try:
        new_notif = Notification(
            recipient_type=recipient_type,
            recipient_user_id=recipient_user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            reference_type=reference_type,
            reference_id=reference_id,
            target_url=target_url,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(new_notif)
        db.session.commit()
        return new_notif
    except Exception as e:
        db.session.rollback()
        print(f"Failed to create notification: {str(e)}")
        return None


# =========================================================
# NOTIFICATION ROUTES
# =========================================================

@app.route("/api/notifications")
def api_get_notifications():
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    notifications = Notification.query.filter_by(
        recipient_type='patient', 
        recipient_user_id=user_id
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    unread_count = Notification.query.filter_by(
        recipient_type='patient', 
        recipient_user_id=user_id,
        is_read=False
    ).count()
    
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat(),
            'target_url': n.target_url
        })
        
    return jsonify({
        'notifications': data,
        'unread_count': unread_count
    })

@app.route("/api/notifications/<int:notif_id>/read", methods=['POST'])
def api_mark_notification_read(notif_id):
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    notif = Notification.query.filter_by(
        id=notif_id,
        recipient_type='patient',
        recipient_user_id=user_id
    ).first()
    
    if notif:
        notif.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route("/api/notifications/read-all", methods=['POST'])
def api_mark_all_notifications_read():
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    Notification.query.filter_by(
        recipient_type='patient',
        recipient_user_id=user_id,
        is_read=False
    ).update({'is_read': True})
    
    db.session.commit()
    return jsonify({'success': True})

@app.route("/patient/notifications")
def patient_notifications():
    user_id = session.get("registration_user_id")
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    # We will fetch from client side or pass to template
    notifications = Notification.query.filter_by(
        recipient_type='patient', 
        recipient_user_id=user_id
    ).order_by(Notification.created_at.desc()).all()
    
    unread_count = sum(1 for n in notifications if not n.is_read)
    
    return render_template("patient-notifications.html", notifications=notifications, unread_count=unread_count)



# =========================================================
# SUPPORT MODULE
# =========================================================

@app.route("/patient/support")
def patient_support():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    tickets = SupportTicket.query.filter_by(user_id=user_id).order_by(SupportTicket.updated_at.desc()).all()
    
    return render_template("patient-support.html", user=user, tickets=tickets)


@app.route("/patient/support/submit", methods=["POST"])
def patient_support_submit():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    subject = request.form.get("subject", "").strip()
    category = request.form.get("category", "").strip()
    message = request.form.get("message", "").strip()
    
    if not subject or not category or not message:
        flash("All fields are required.", "error")
        return redirect(url_for('patient_support') + '#contact')
        
    import random
    import string
    
    # Generate unique ticket number
    while True:
        ticket_number = 'TKT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not SupportTicket.query.filter_by(ticket_number=ticket_number).first():
            break
            
    attachment = request.files.get("attachment")
    attachment_filename = None
    if attachment and attachment.filename:
        # In a real app we'd save it properly. For V1 MVP, just store the filename
        attachment_filename = attachment.filename
        
    new_ticket = SupportTicket(
        ticket_number=ticket_number,
        user_id=user_id,
        subject=subject,
        category=category,
        message=message,
        attachment_filename=attachment_filename,
        status="Open"
    )
    db.session.add(new_ticket)
    db.session.commit()
    
    flash(f"Support ticket {ticket_number} created successfully.", "success")
    return redirect(url_for('patient_support') + '#tickets')


@app.route("/patient/support/ticket/<string:ticket_number>", methods=["GET", "POST"])
def patient_support_ticket_detail(ticket_number):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    ticket = SupportTicket.query.filter_by(ticket_number=ticket_number).first_or_404()
    
    # IDOR Prevention
    if ticket.user_id != user_id:
        from flask import abort
        abort(403)
        
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if not message:
            flash("Message cannot be empty.", "error")
            return redirect(url_for('patient_support_ticket_detail', ticket_number=ticket.ticket_number))
            
        new_msg = SupportTicketMessage(
            ticket_id=ticket.id,
            sender_type="patient",
            message=message
        )
        ticket.updated_at = datetime.now(timezone.utc)
        db.session.add(new_msg)
        db.session.commit()
        
        return redirect(url_for('patient_support_ticket_detail', ticket_number=ticket.ticket_number))
        
    return render_template("patient-support-ticket.html", ticket=ticket)



@app.route("/patient/request/<reference_id>/add-document", methods=["POST"])
def patient_request_add_document(reference_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    
    # Check authorization
    if req.patient_profile.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    document_type = request.form.get('document_type', 'Other Medical Document')
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        storage_filename = f"{uuid.uuid4().hex}.{ext}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_filename)
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        new_doc = MedicalDocument(
            original_filename=original_filename,
            storage_filename=storage_filename,
            document_type=document_type,
            mime_type=file.content_type,
            file_size=file_size,
            patient_profile_id=req.patient_profile_id,
            treatment_request_id=req.id,
            uploaded_by_id=user_id
        )
        db.session.add(new_doc)
        db.session.commit()
        
        return jsonify({'success': True})
        
    return jsonify({'error': 'Invalid file type'}), 400



@app.route("/patient/treatment-proposal/<int:proposal_id>/shortlist", methods=['POST'])
def patient_proposal_shortlist(proposal_id):
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    proposal = TreatmentProposal.query.get_or_404(proposal_id)
    if proposal.treatment_request.patient_profile.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    proposal.patient_shortlisted = data.get('shortlisted', False)
    db.session.commit()
    
    return jsonify({'success': True, 'shortlisted': proposal.patient_shortlisted})

@app.route("/patient/treatment-proposal/<int:proposal_id>/notes", methods=['POST'])
def patient_proposal_notes(proposal_id):
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    proposal = TreatmentProposal.query.get_or_404(proposal_id)
    if proposal.treatment_request.patient_profile.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    proposal.patient_notes = data.get('notes', '')
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/patient/requests')
def patient_requests():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('patient_registration_step1'))
        
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    context = request.args.get('context')
    
    if profile_ids:
        requests_query = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).order_by(TreatmentRequest.created_at.desc()).all()
        
        processed_requests = []
        for req in requests_query:
            proposals = [p for p in req.proposals if p.status == 'submitted']
            if context == 'responses' and not proposals:
                continue # Skip requests with no responses for the Hospital Responses page
                
            if proposals:
                latest_proposal_time = max((p.submitted_at for p in proposals if p.submitted_at), default=req.created_at)
                req._latest_response_time = latest_proposal_time
            else:
                req._latest_response_time = None
                
            processed_requests.append(req)

        requests = sorted(
            processed_requests,
            key=lambda r: (r._latest_response_time is not None, r._latest_response_time or r.created_at),
            reverse=True
        )
    else:
        requests = []
    if context == 'responses':
        page_title = "Requests with Hospital Responses"
        page_desc = "Select a treatment request to review estimates and proposals submitted by hospitals."
    else:
        page_title = "My Requests"
        page_desc = "Manage and track your submitted treatment requests."
        
    return render_template('patient-requests.html', user=user, requests=requests, page_title=page_title, page_desc=page_desc)

if __name__ == "__main__":
    app.run(debug=True)
