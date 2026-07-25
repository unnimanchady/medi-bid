with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    '@app.route("/patient/hospital-responses")\ndef patient_hospital_responses():',
    '@app.route("/patient/hospital-responses")\n@app.route("/patient/requests/<string:reference_id>/responses")\ndef patient_hospital_responses(reference_id=None):'
)

c = c.replace(
    "req_reference_id = request.args.get('reference_id')",
    "req_reference_id = reference_id or request.args.get('reference_id')"
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
