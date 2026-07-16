from flask import Flask, render_template

app = Flask(__name__)


# =========================================================
# PUBLIC PAGES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# PATIENT REGISTRATION
# =========================================================

@app.route("/patient/register/step-1")
def patient_registration_step1():
    return render_template("patient-registration-step1.html")


@app.route("/patient/register/step-2")
def patient_registration_step2():
    return render_template("patient-registration-step2.html")


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