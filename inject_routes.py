import os
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# PATIENT SECURE MESSAGES
patient_inbox_code = '''
@app.route("/patient/secure-messages")
def patient_secure_messages():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    # Get all threads for the patient's requests
    threads = MessageThread.query.join(TreatmentRequest).filter(
        TreatmentRequest.patient_profile_id.in_(profile_ids)
    ).order_by(MessageThread.updated_at.desc()).all()
    
    # Calculate unread counts for each thread (where patient hasn't read hospital's message)
    unread_counts = {}
    for t in threads:
        unread_counts[t.id] = Message.query.filter_by(
            thread_id=t.id, sender_type='hospital', is_read=False
        ).count()
        
    return render_template("patient-secure-messages.html", user=user, threads=threads, unread_counts=unread_counts)

@app.route("/patient/secure-messages/<int:thread_id>")
def patient_message_thread(thread_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    thread = MessageThread.query.get_or_404(thread_id)
    
    # Authorization: check if the thread belongs to one of the patient's profiles
    user = User.query.get(user_id)
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    if thread.treatment_request.patient_profile_id not in profile_ids:
        from flask import abort
        abort(403)
        
    # Mark hospital messages as read
    unread_msgs = Message.query.filter_by(thread_id=thread.id, sender_type='hospital', is_read=False).all()
    for msg in unread_msgs:
        msg.is_read = True
    if unread_msgs:
        db.session.commit()
        
    messages = Message.query.filter_by(thread_id=thread.id).order_by(Message.created_at.asc()).all()
    
    return render_template("patient-message-thread.html", user=user, thread=thread, messages=messages)

@app.route("/patient/secure-messages/<int:thread_id>/send", methods=["POST"])
def patient_send_message(thread_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    thread = MessageThread.query.get_or_404(thread_id)
    
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    if thread.treatment_request.patient_profile_id not in profile_ids:
        from flask import abort
        abort(403)
        
    message_body = request.form.get('message_body', '').strip()
    if not message_body:
        return redirect(url_for('patient_message_thread', thread_id=thread.id))
        
    if len(message_body) > 5000:
        message_body = message_body[:5000]
        
    new_msg = Message(
        thread_id=thread.id,
        sender_type='patient',
        sender_user_id=user_id,
        message_body=message_body
    )
    thread.updated_at = datetime.utcnow()
    db.session.add(new_msg)
    db.session.commit()
    
    return redirect(url_for('patient_message_thread', thread_id=thread.id))

@app.route("/patient/secure-messages/start/<int:hospital_id>/<reference_id>", methods=["POST"])
def patient_start_message(hospital_id, reference_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    if req.patient_profile_id not in profile_ids:
        from flask import abort
        abort(403)
        
    hospital = Hospital.query.get_or_404(hospital_id)
    
    # Verify the hospital submitted a valid proposal
    proposal = TreatmentProposal.query.filter_by(
        treatment_request_id=req.id, 
        hospital_id=hospital.id,
        status='submitted'
    ).first()
    
    if not proposal:
        from flask import abort
        abort(403)
        
    # Get or create thread
    thread = MessageThread.query.filter_by(treatment_request_id=req.id, hospital_id=hospital.id).first()
    if not thread:
        thread = MessageThread(treatment_request_id=req.id, hospital_id=hospital.id)
        db.session.add(thread)
        db.session.commit()
        
    return redirect(url_for('patient_message_thread', thread_id=thread.id))

'''

# HOSPITAL SECURE MESSAGES
hospital_inbox_code = '''
@app.route("/hospital/messages")
def hospital_messages():
    hospital_user_id = session.get('hospital_user_id')
    if not hospital_user_id:
        return redirect(url_for('hospital_login'))
        
    hospital_user = HospitalUser.query.get(hospital_user_id)
    
    threads = MessageThread.query.filter_by(hospital_id=hospital_user.hospital_id).order_by(MessageThread.updated_at.desc()).all()
    
    unread_counts = {}
    for t in threads:
        unread_counts[t.id] = Message.query.filter_by(
            thread_id=t.id, sender_type='patient', is_read=False
        ).count()
        
    return render_template("hospital-messages.html", user=hospital_user, threads=threads, unread_counts=unread_counts)

@app.route("/hospital/messages/<int:thread_id>")
def hospital_message_thread(thread_id):
    hospital_user_id = session.get('hospital_user_id')
    if not hospital_user_id:
        return redirect(url_for('hospital_login'))
        
    hospital_user = HospitalUser.query.get(hospital_user_id)
    thread = MessageThread.query.get_or_404(thread_id)
    
    if thread.hospital_id != hospital_user.hospital_id:
        from flask import abort
        abort(403)
        
    # Mark patient messages as read
    unread_msgs = Message.query.filter_by(thread_id=thread.id, sender_type='patient', is_read=False).all()
    for msg in unread_msgs:
        msg.is_read = True
    if unread_msgs:
        db.session.commit()
        
    messages = Message.query.filter_by(thread_id=thread.id).order_by(Message.created_at.asc()).all()
    
    return render_template("hospital-message-thread.html", user=hospital_user, thread=thread, messages=messages)

@app.route("/hospital/messages/<int:thread_id>/send", methods=["POST"])
def hospital_send_message(thread_id):
    hospital_user_id = session.get('hospital_user_id')
    if not hospital_user_id:
        return redirect(url_for('hospital_login'))
        
    hospital_user = HospitalUser.query.get(hospital_user_id)
    thread = MessageThread.query.get_or_404(thread_id)
    
    if thread.hospital_id != hospital_user.hospital_id:
        from flask import abort
        abort(403)
        
    message_body = request.form.get('message_body', '').strip()
    if not message_body:
        return redirect(url_for('hospital_message_thread', thread_id=thread.id))
        
    if len(message_body) > 5000:
        message_body = message_body[:5000]
        
    new_msg = Message(
        thread_id=thread.id,
        sender_type='hospital',
        sender_hospital_id=hospital_user.hospital_id,
        message_body=message_body
    )
    thread.updated_at = datetime.utcnow()
    db.session.add(new_msg)
    db.session.commit()
    
    return redirect(url_for('hospital_message_thread', thread_id=thread.id))
'''

# REPLACE PATIENT MESSAGES
old_patient_messages = """@app.route("/patient/secure-messages")
def patient_secure_messages():
    return render_template("patient-secure-messages.html")"""

content = content.replace(old_patient_messages, patient_inbox_code)

# APPEND HOSPITAL MESSAGES before end
# We can find hospital_dashboard and insert before it
content = content.replace("@app.route(\"/hospital/dashboard\")", hospital_inbox_code + "\n\n@app.route(\"/hospital/dashboard\")")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected routes!")
