import os

for f in ['templates/patient-secure-messages.html', 'templates/patient-hospital-profile.html']:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        c = c.replace("url_for('patient_treatment_proposal_details')", "url_for('patient_treatment_proposal_details', proposal_id=1)")
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c)
print("done")
