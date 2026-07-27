from app import app, db
from models import User, TreatmentRequest, Hospital, MessageThread, Message, PatientProfile, TreatmentProposal, HospitalUser

with app.test_client() as client:
    with app.app_context():
        # Get Sijo
        sijo = User.query.filter_by(id=2).first()
        req = TreatmentRequest.query.filter_by(reference_id='TR-R5PDRXK8WW').first()
        mayo = Hospital.query.filter((Hospital.legal_name.ilike('%Mayo%')) | (Hospital.display_name.ilike('%Mayo%'))).first()
        cleveland = Hospital.query.filter((Hospital.legal_name.ilike('%Cleveland%')) | (Hospital.display_name.ilike('%Cleveland%'))).first()
        
        mayo_user = HospitalUser.query.filter_by(hospital_id=mayo.id).first()
        cleveland_user = HospitalUser.query.filter_by(hospital_id=cleveland.id).first()
        
        # Ensure thread exists
        mayo_thread = MessageThread.query.filter_by(treatment_request_id=req.id, hospital_id=mayo.id).first()
        if not mayo_thread:
            mayo_thread = MessageThread(treatment_request_id=req.id, hospital_id=mayo.id)
            db.session.add(mayo_thread)
            db.session.commit()
            # Send Sijo's initial message
            db.session.add(Message(
                thread_id=mayo_thread.id,
                sender_type='patient',
                sender_user_id=sijo.id,
                message_body='Hello Mayo'
            ))
            db.session.commit()
            
        mayo_thread_id = mayo_thread.id
        
    print("=== TEST 1: Hospital (Mayo) Reads & Replies ===")
    
    with client.session_transaction() as sess:
        sess['hospital_user_id'] = mayo_user.id
        
    # Read thread
    resp = client.get(f'/hospital/messages/{mayo_thread_id}', follow_redirects=True)
    print('Patient message visible to Mayo:', 'Hello Mayo' in resp.text)
    
    # Reply
    reply_text = 'Hello Sijo, we have received your message.'
    resp = client.post(f'/hospital/messages/{mayo_thread_id}/send', data={
        'message_body': reply_text
    }, follow_redirects=True)
    
    print('Hospital reply persisted and visible:', reply_text in resp.text)
    
    print("\n=== TEST 2: Patient (Sijo) Sees Shared Conversation ===")
    
    with client.session_transaction() as sess:
        # Clear hospital user, set patient user
        if 'hospital_user_id' in sess:
            del sess['hospital_user_id']
        sess['registration_user_id'] = sijo.id
        
    resp = client.get(f'/patient/secure-messages?thread_id={mayo_thread_id}', follow_redirects=True)
    
    print('Patient sees their own message:', 'Hello Mayo' in resp.text)
    print('Patient sees hospital reply in same thread:', reply_text in resp.text)
    
    print("\n=== TEST 3: Isolation (Cleveland Clinic blocked) ===")
    
    with client.session_transaction() as sess:
        # Clear patient user, set cleveland hospital user
        if 'registration_user_id' in sess:
            del sess['registration_user_id']
        sess['hospital_user_id'] = cleveland_user.id
        
    resp = client.get(f'/hospital/messages/{mayo_thread_id}', follow_redirects=True)
    print('Cleveland blocked from reading Mayo thread:', resp.status_code == 403)
    
    resp = client.post(f'/hospital/messages/{mayo_thread_id}/send', data={
        'message_body': 'I am a hacker.'
    })
    print('Cleveland blocked from replying to Mayo thread:', resp.status_code == 403)
