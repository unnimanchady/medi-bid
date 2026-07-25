import json
from app import app, db
from models import TreatmentProposal

with app.app_context():
    app.config['TESTING'] = True
    client = app.test_client()
    
    # 1. Reset state
    p11 = TreatmentProposal.query.get(11)
    p11.patient_shortlisted = False
    p11.patient_notes = ""
    
    p12 = TreatmentProposal.query.get(12)
    p12.patient_shortlisted = False
    p12.patient_notes = ""
    db.session.commit()
    
    # 2. Test Shortlist Mayo (11) -> ON, Notes -> "Prefer Mayo"
    with client.session_transaction() as sess:
        sess['registration_user_id'] = 2
        
    res = client.post('/patient/treatment-proposal/11/shortlist', json={'shortlisted': True})
    print("Mayo Shortlist Status:", res.status_code, res.get_json())
    
    res = client.post('/patient/treatment-proposal/11/notes', json={'notes': 'Prefer Mayo'})
    print("Mayo Notes Status:", res.status_code, res.get_json())
    
    # 3. Test Shortlist Cleveland (12) -> OFF, Notes -> "Compare Cleveland later"
    res = client.post('/patient/treatment-proposal/12/shortlist', json={'shortlisted': False})
    print("Cleveland Shortlist Status:", res.status_code, res.get_json())
    
    res = client.post('/patient/treatment-proposal/12/notes', json={'notes': 'Compare Cleveland later'})
    print("Cleveland Notes Status:", res.status_code, res.get_json())
    
    # 4. Read back from DB to verify persistence and independence
    db.session.expire_all()
    p11 = TreatmentProposal.query.get(11)
    p12 = TreatmentProposal.query.get(12)
    
    print("\nVERIFICATION:")
    print(f"Mayo (11): Shortlisted={p11.patient_shortlisted}, Notes='{p11.patient_notes}'")
    print(f"Cleveland (12): Shortlisted={p12.patient_shortlisted}, Notes='{p12.patient_notes}'")

