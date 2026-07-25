from app import app, db
from models import User, TreatmentRequest, Hospital, MessageThread, Message, PatientProfile, TreatmentProposal
import traceback

with app.test_client() as client:
    with app.app_context():
        sijo = User.query.filter_by(id=2).first()
        req = TreatmentRequest.query.filter_by(reference_id='TR-R5PDRXK8WW').first()
        mayo = Hospital.query.filter((Hospital.legal_name.ilike('%Mayo%')) | (Hospital.display_name.ilike('%Mayo%'))).first()
        cleveland = Hospital.query.filter((Hospital.legal_name.ilike('%Cleveland%')) | (Hospital.display_name.ilike('%Cleveland%'))).first()
        
    with client.session_transaction() as sess:
        sess['registration_user_id'] = sijo.id

    print("=== TEST 1: Creation & Persistence ===")
    
    resp = client.post('/patient/secure-messages/start', data={
        'treatment_request_id': req.id,
        'hospital_id': mayo.id
    }, follow_redirects=True)
    
    if 'Mayo Clinic' not in resp.text and 'Mayo' not in resp.text:
        print("FAILED Started Mayo Thread. Response:")
        print(resp.text[:500])
    else:
        print("Started Mayo Thread: True")
        
    with app.app_context():
        mayo_thread = MessageThread.query.filter_by(treatment_request_id=req.id, hospital_id=mayo.id).first()
        mayo_thread_id = mayo_thread.id
        
    resp = client.post(f'/patient/secure-messages/{mayo_thread_id}/send', data={
        'message_body': 'Hello Mayo'
    }, follow_redirects=True)
    
    if 'Hello Mayo' not in resp.text:
        print("FAILED Message Persisted. Response:")
        print(resp.text[:500])
    else:
        print("Message Persisted: True")
        
    print("\n=== TEST 2: Isolation ===")
    
    resp = client.post('/patient/secure-messages/start', data={
        'treatment_request_id': req.id,
        'hospital_id': cleveland.id
    }, follow_redirects=True)
    
    if 'Cleveland' not in resp.text:
        print("FAILED Started Cleveland Thread. Response:")
    else:
        print("Started Cleveland Thread: True")
        
    print('Isolation check (Hello Mayo NOT in Cleveland thread):', 'Hello Mayo' not in resp.text)
    
    print("\n=== TEST 3: Authorization (Direct ID Manipulation) ===")
    
    with app.app_context():
        other_profile = PatientProfile.query.filter(PatientProfile.user_id != sijo.id).first()
        other_req = TreatmentRequest.query.filter_by(patient_profile_id=other_profile.id).first()
        if other_req:
            t = MessageThread.query.filter_by(treatment_request_id=other_req.id, hospital_id=mayo.id).first()
            if not t:
                t = MessageThread(treatment_request_id=other_req.id, hospital_id=mayo.id)
                db.session.add(t)
                db.session.commit()
            unauth_thread_id = t.id
            
            resp = client.get(f'/patient/secure-messages?thread_id={unauth_thread_id}', follow_redirects=True)
            print('Unauthorized Thread Access Blocked:', 'Unauthorized access' in resp.text)
            
            resp = client.post(f'/patient/secure-messages/{unauth_thread_id}/send', data={
                'message_body': 'Hacking attempt'
            })
            print('Unauthorized Send Blocked Status:', resp.status_code == 403)
