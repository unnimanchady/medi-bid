with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Desktop sidebar link
c = c.replace(
    "else url_for('patient_hospital_responses')",
    "else url_for('patient_requests')"
)

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(c)
