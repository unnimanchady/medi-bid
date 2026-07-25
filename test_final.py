import json
from app import app, db
from models import TreatmentProposal

with app.app_context():
    app.config['TESTING'] = True
    client = app.test_client()
    
    with client.session_transaction() as sess:
        sess['registration_user_id'] = 2

    print("--- 9. Both Shortlisted Simultaneously ---")
    client.post('/patient/treatment-proposal/11/shortlist', json={'shortlisted': True})
    client.post('/patient/treatment-proposal/12/shortlist', json={'shortlisted': True})
    
    db.session.expire_all()
    p11 = TreatmentProposal.query.get(11)
    p12 = TreatmentProposal.query.get(12)
    print(f"Mayo (11) Shortlisted: {p11.patient_shortlisted}")
    print(f"Cleveland (12) Shortlisted: {p12.patient_shortlisted}")
    
    print("\n--- 10. Notes Remain ---")
    client.post('/patient/treatment-proposal/11/notes', json={'notes': 'Prefer Mayo'})
    client.post('/patient/treatment-proposal/12/notes', json={'notes': 'let me check'})
    
    db.session.expire_all()
    p11 = TreatmentProposal.query.get(11)
    p12 = TreatmentProposal.query.get(12)
    print(f"Mayo (11) Notes: '{p11.patient_notes}'")
    print(f"Cleveland (12) Notes: '{p12.patient_notes}'")

    print("\n--- 11. Unshortlist Cleveland Only ---")
    client.post('/patient/treatment-proposal/12/shortlist', json={'shortlisted': False})
    
    db.session.expire_all()
    p11 = TreatmentProposal.query.get(11)
    p12 = TreatmentProposal.query.get(12)
    print(f"Mayo (11) Shortlisted: {p11.patient_shortlisted}")
    print(f"Cleveland (12) Shortlisted: {p12.patient_shortlisted}")
