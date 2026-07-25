import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

new_routes = """@app.route("/patient/secure-messages")
def patient_secure_messages():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    
    threads = []
    active_thread = None
    
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    if profiles:
        profile_ids = [p.id for p in profiles]
        requests = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).all()
        if requests:
            request_ids = [r.id for r in requests]
            from models import MessageThread, Message
            
            # Subquery to order threads by their most recent message, or creation date
            threads = MessageThread.query.filter(MessageThread.treatment_request_id.in_(request_ids)).order_by(MessageThread.updated_at.desc()).all()
            
            thread_id = request.args.get('thread_id', type=int)
            if thread_id:
                # Security: Verify the requested thread is actually in the patient's authorized threads
                active_thread = next((t for t in threads if t.id == thread_id), None)
                if not active_thread:
                    flash("Unauthorized access or thread not found.", "error")
                    return redirect(url_for('patient_secure_messages'))

    return render_template("patient-secure-messages.html", user=user, threads=threads, active_thread=active_thread)

@app.route("/patient/secure-messages/start", methods=["POST"])
def patient_secure_messages_start():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    treatment_request_id = request.form.get('treatment_request_id', type=int)
    hospital_id = request.form.get('hospital_id', type=int)
    
    if not treatment_request_id or not hospital_id:
        flash("Invalid request parameters.", "error")
        return redirect(url_for('patient_hospital_responses'))
        
    # Authorization check
    req = TreatmentRequest.query.get(treatment_request_id)
    if not req:
        abort(404)
        
    profile = PatientProfile.query.filter_by(id=req.patient_profile_id, user_id=user_id).first()
    if not profile:
        abort(403) # Not authorized
        
    # Verify hospital actually submitted a proposal for this request (V1 rule)
    proposal = TreatmentProposal.query.filter_by(treatment_request_id=treatment_request_id, hospital_id=hospital_id).first()
    if not proposal:
        flash("Hospital has not submitted a proposal for this request.", "error")
        return redirect(url_for('patient_hospital_responses'))
        
    from models import MessageThread
    
    # Check if thread exists
    thread = MessageThread.query.filter_by(treatment_request_id=treatment_request_id, hospital_id=hospital_id).first()
    
    if not thread:
        thread = MessageThread(treatment_request_id=treatment_request_id, hospital_id=hospital_id)
        db.session.add(thread)
        db.session.commit()
        
    return redirect(url_for('patient_secure_messages', thread_id=thread.id))

@app.route("/patient/secure-messages/<int:thread_id>/send", methods=["POST"])
def patient_secure_messages_send(thread_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    message_body = request.form.get('message_body', '').strip()
    if not message_body:
        return redirect(url_for('patient_secure_messages', thread_id=thread_id))
        
    from models import MessageThread, Message
    thread = MessageThread.query.get_or_404(thread_id)
    
    # Authorization Check
    req = thread.treatment_request
    profile = PatientProfile.query.filter_by(id=req.patient_profile_id, user_id=user_id).first()
    if not profile:
        abort(403)
        
    msg = Message(
        thread_id=thread_id,
        sender_type='patient',
        sender_user_id=user_id,
        message_body=message_body
    )
    
    # Update thread's updated_at timestamp to bubble it up
    from datetime import datetime
    thread.updated_at = datetime.utcnow()
    
    db.session.add(msg)
    db.session.commit()
    
    return redirect(url_for('patient_secure_messages', thread_id=thread_id))
"""

c = re.sub(
    r'@app\.route\("/patient/secure-messages"\)\ndef patient_secure_messages\(\):.*?return render_template\("patient-secure-messages\.html", user=user, threads=threads\)',
    new_routes,
    c,
    flags=re.DOTALL
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
