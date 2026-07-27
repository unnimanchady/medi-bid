import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

new_routes = """@app.route("/hospital/messages")
def hospital_messages():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('hospital_registration_step1'))
        
    hospital = Hospital.query.filter_by(user_id=user_id).first()
    if not hospital:
        return redirect(url_for('hospital_registration_step1'))

    from models import MessageThread, Message
    threads = MessageThread.query.filter_by(hospital_id=hospital.id).order_by(MessageThread.updated_at.desc()).all()
    
    sidebar_threads = []
    for t in threads:
        all_msgs = t.messages.all()
        sidebar_threads.append({
            'thread': t,
            'latest_message': all_msgs[-1] if all_msgs else None,
            'unread_count': 0 # For future implementation
        })

    return render_template("hospital-messages.html", hospital=hospital, sidebar_threads=sidebar_threads)

@app.route("/hospital/messages/<int:thread_id>")
def hospital_message_thread(thread_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('hospital_registration_step1'))
        
    hospital = Hospital.query.filter_by(user_id=user_id).first()
    if not hospital:
        return redirect(url_for('hospital_registration_step1'))

    from models import MessageThread, Message
    thread = MessageThread.query.get_or_404(thread_id)
    
    # Authorization Check
    if thread.hospital_id != hospital.id:
        abort(403)
        
    messages = thread.messages.all()

    return render_template("hospital-message-thread.html", hospital=hospital, thread=thread, messages=messages)

@app.route("/hospital/messages/<int:thread_id>/send", methods=["POST"])
def hospital_send_message(thread_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('hospital_registration_step1'))
        
    hospital = Hospital.query.filter_by(user_id=user_id).first()
    if not hospital:
        return redirect(url_for('hospital_registration_step1'))
        
    message_body = request.form.get('message_body', '').strip()
    if not message_body:
        return redirect(url_for('hospital_message_thread', thread_id=thread_id))

    from models import MessageThread, Message
    thread = MessageThread.query.get_or_404(thread_id)
    
    # Authorization Check
    if thread.hospital_id != hospital.id:
        abort(403)
        
    msg = Message(
        thread_id=thread_id,
        sender_type='hospital',
        sender_hospital_id=hospital.id,
        message_body=message_body
    )
    
    from datetime import datetime
    thread.updated_at = datetime.utcnow()
    
    db.session.add(msg)
    db.session.commit()
    
    return redirect(url_for('hospital_message_thread', thread_id=thread_id))
"""

# We'll place it right before the patient_secure_messages
c = re.sub(
    r'(@app\.route\("/patient/secure-messages"\))',
    new_routes + r'\n\n\1',
    c
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
