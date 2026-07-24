import os
import re

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace patient_profile_settings
old_settings_route = """@app.route("/patient/profile/settings")
def patient_profile_settings():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    
    return render_template("patient-profile-settings.html", user=user, profiles=profiles)"""

new_settings_route = """@app.route("/patient/profile/settings", methods=["GET", "POST"])
def patient_profile_settings():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    
    # Identify the 'Self' profile to display DOB and Gender
    self_profile = next((p for p in profiles if p.relationship_type == 'Self'), None)
    
    if request.method == "POST":
        # Update User Base Fields
        user.first_name = request.form.get("first_name", user.first_name).strip().title()
        user.last_name = request.form.get("last_name", user.last_name).strip().title()
        user.phone = request.form.get("phone", user.phone).strip()
        user.country_of_residence = request.form.get("residence", user.country_of_residence).strip()
        user.preferred_language = request.form.get("language", user.preferred_language).strip()
        
        # Also sync to 'Self' profile if it exists
        if self_profile:
            self_profile.first_name = user.first_name
            self_profile.last_name = user.last_name
            self_profile.country_of_residence = user.country_of_residence
            self_profile.phone = user.phone
            
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('patient_profile_settings'))
    
    return render_template("patient-profile-settings.html", user=user, profiles=profiles, self_profile=self_profile)"""

content = content.replace(old_settings_route, new_settings_route)

# 2. Add new routes (notifications, security, add, delete)
new_routes = """
@app.route("/patient/profile/settings/notifications", methods=["POST"])
def patient_settings_notifications():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    
    user.notify_email = request.form.get("notify_email") == 'on'
    user.notify_in_app = request.form.get("notify_in_app") == 'on'
    
    db.session.commit()
    flash("Notification preferences updated.", "success")
    return redirect(url_for('patient_profile_settings'))


@app.route("/patient/profile/settings/security", methods=["POST"])
def patient_settings_security():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")
    
    from werkzeug.security import check_password_hash, generate_password_hash
    
    if not check_password_hash(user.password_hash, current_password):
        flash("Incorrect current password.", "error")
        return redirect(url_for('patient_profile_settings'))
        
    if new_password != confirm_password:
        flash("New passwords do not match.", "error")
        return redirect(url_for('patient_profile_settings'))
        
    if len(new_password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return redirect(url_for('patient_profile_settings'))
        
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    flash("Password updated successfully.", "success")
    return redirect(url_for('patient_profile_settings'))


@app.route("/patient/profile/add", methods=["GET", "POST"])
def patient_profile_add():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    error = None
    if request.method == "POST":
        relationship = request.form.get("relationship", "").strip()
        first_name = request.form.get("first-name", "").strip().title()
        last_name = request.form.get("last-name", "").strip().title()
        
        dob_str = request.form.get("dob", "").strip()
        dob = None
        if dob_str:
            from datetime import datetime
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                error = "Invalid date format."
                
        gender = request.form.get("gender", "").strip()
        nationality = request.form.get("nationality", "").strip()
        residence = request.form.get("residence", "").strip()
        city = request.form.get("city", "").strip()
        passport = request.form.get("passport", "").strip()
        
        if not relationship or relationship == "Self":
            error = "Invalid relationship type."
            
        if not first_name or not last_name or not dob or not gender or not nationality or not residence:
            error = "Please fill all required fields."
            
        if not error:
            new_profile = PatientProfile(
                user_id=user_id,
                relationship_type=relationship,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender,
                nationality=nationality,
                country_of_residence=residence,
                city=city,
                passport_number=passport
            )
            db.session.add(new_profile)
            try:
                db.session.commit()
                
                # Generate patient_id after commit
                new_profile.patient_id = f"PT{new_profile.id:06d}"
                db.session.commit()
                
                flash("Patient profile added successfully.", "success")
                return redirect(url_for("patient_profile_settings"))
            except Exception as e:
                db.session.rollback()
                error = "Could not save profile."
                
    return render_template("patient-registration-step2.html", 
        error=error, 
        is_self=False,
        default_first_name="",
        default_last_name="",
        default_residence="",
        profile=None,
        edit_mode=False
    )


@app.route("/patient/profile/delete/<int:profile_id>", methods=["POST"])
def patient_profile_delete(profile_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    profile = PatientProfile.query.filter_by(id=profile_id, user_id=user_id).first()
    if not profile:
        flash("Profile not found.", "error")
        return redirect(url_for('patient_profile_settings'))
        
    if profile.relationship_type == 'Self':
        flash("Cannot delete primary 'Self' profile.", "error")
        return redirect(url_for('patient_profile_settings'))
        
    # Check if linked to any treatment requests
    req_count = TreatmentRequest.query.filter_by(patient_profile_id=profile_id).count()
    if req_count > 0:
        flash("Cannot delete profile because it is linked to active or past treatment requests.", "error")
        return redirect(url_for('patient_profile_settings'))
        
    db.session.delete(profile)
    db.session.commit()
    
    flash("Profile deleted successfully.", "success")
    return redirect(url_for('patient_profile_settings'))

"""

if 'def patient_settings_notifications(' not in content:
    # Insert new_routes after patient_profile_settings
    content = content.replace(new_settings_route, new_settings_route + "\n\n" + new_routes)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with Sprint 3 settings routes")
