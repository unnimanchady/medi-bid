import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

helpers_code = '''
def get_patient_sidebar_threads(profile_ids):
    threads = MessageThread.query.join(TreatmentRequest).filter(
        TreatmentRequest.patient_profile_id.in_(profile_ids)
    ).order_by(MessageThread.updated_at.desc()).all()
    
    sidebar_threads = []
    for t in threads:
        latest = t.messages.order_by(Message.created_at.desc()).first()
        unread = Message.query.filter_by(thread_id=t.id, sender_type='hospital', is_read=False).count()
        sidebar_threads.append({'thread': t, 'latest_message': latest, 'unread_count': unread})
    return sidebar_threads

def get_hospital_sidebar_threads(hospital_id):
    threads = MessageThread.query.filter_by(hospital_id=hospital_id).order_by(MessageThread.updated_at.desc()).all()
    
    sidebar_threads = []
    for t in threads:
        latest = t.messages.order_by(Message.created_at.desc()).first()
        unread = Message.query.filter_by(thread_id=t.id, sender_type='patient', is_read=False).count()
        sidebar_threads.append({'thread': t, 'latest_message': latest, 'unread_count': unread})
    return sidebar_threads

@app.route("/patient/secure-messages")
'''

content = content.replace('@app.route("/patient/secure-messages")', helpers_code)

# Replace patient_secure_messages logic
patient_inbox_logic = r'''    # Get all threads for the patient's requests.*?sidebar_threads\.append\(\{'thread': t, 'latest_message': latest, 'unread_count': unread\}\)'''
content = re.sub(patient_inbox_logic, '    sidebar_threads = get_patient_sidebar_threads(profile_ids)', content, flags=re.DOTALL)

# Replace patient_message_thread logic
patient_thread_logic = r'''    # Get all threads for the sidebar.*?\}\n    for t in threads:\n.*?\.count\(\)'''
content = re.sub(patient_thread_logic, '    sidebar_threads = get_patient_sidebar_threads(profile_ids)', content, flags=re.DOTALL)

# Replace hospital_messages logic
hospital_inbox_logic = r'''    threads = MessageThread.query.filter_by\(hospital_id=hospital_user\.hospital_id\)\.order_by\(MessageThread\.updated_at\.desc\(\)\)\.all\(\)\n\n    # Prepare sidebar data\n    sidebar_threads = \[\]\n    for t in threads:\n        latest = t\.messages\.order_by\(Message\.created_at\.desc\(\)\)\.first\(\)\n        unread = Message\.query\.filter_by\(thread_id=t\.id, sender_type='patient', is_read=False\)\.count\(\)\n        sidebar_threads\.append\(\{'thread': t, 'latest_message': latest, 'unread_count': unread\}\)'''
content = re.sub(hospital_inbox_logic, '    sidebar_threads = get_hospital_sidebar_threads(hospital_user.hospital_id)', content, flags=re.DOTALL)

# Replace hospital_message_thread logic
hospital_thread_logic = r'''    # Prepare sidebar data\n    threads = MessageThread\.query\.filter_by\(hospital_id=hospital_user\.hospital_id\)\.order_by\(MessageThread\.updated_at\.desc\(\)\)\.all\(\)\n    sidebar_threads = \[\]\n    for t in threads:\n        latest = t\.messages\.order_by\(Message\.created_at\.desc\(\)\)\.first\(\)\n        unread = Message\.query\.filter_by\(thread_id=t\.id, sender_type='patient', is_read=False\)\.count\(\)\n        sidebar_threads\.append\(\{'thread': t, 'latest_message': latest, 'unread_count': unread\}\)'''
content = re.sub(hospital_thread_logic, '    sidebar_threads = get_hospital_sidebar_threads(hospital_user.hospital_id)', content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
