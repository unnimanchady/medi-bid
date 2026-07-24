import re
import glob

# 1. Update app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

def inject_sidebar_logic_patient(match):
    return '''    # Prepare sidebar data
    sidebar_threads = []
    for t in threads:
        latest = t.messages.order_by(Message.created_at.desc()).first()
        unread = Message.query.filter_by(thread_id=t.id, sender_type='hospital', is_read=False).count()
        sidebar_threads.append({'thread': t, 'latest_message': latest, 'unread_count': unread})
'''

app_content = re.sub(
    r'    # Calculate unread counts.*?\.count\(\)', 
    inject_sidebar_logic_patient, 
    app_content, 
    flags=re.DOTALL
)

app_content = app_content.replace(
    'threads=threads, unread_counts=unread_counts', 
    'sidebar_threads=sidebar_threads'
)

def inject_sidebar_logic_hospital(match):
    return '''    # Prepare sidebar data
    sidebar_threads = []
    for t in threads:
        latest = t.messages.order_by(Message.created_at.desc()).first()
        unread = Message.query.filter_by(thread_id=t.id, sender_type='patient', is_read=False).count()
        sidebar_threads.append({'thread': t, 'latest_message': latest, 'unread_count': unread})
'''

# We also need to fix hospital routes which might not have the comment yet.
# Let's find how hospital_messages is structured.
app_content = re.sub(
    r'    unread_counts = \{\}\n    for t in threads:\n        unread_counts\[t\.id\] = Message\.query\.filter_by\(\n            thread_id=t\.id, sender_type=\'patient\', is_read=False\n        \)\.count\(\)',
    inject_sidebar_logic_hospital,
    app_content,
    flags=re.DOTALL
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

# 2. Update Templates
def update_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Loop over sidebar_threads instead of threads
    content = content.replace('{% if threads %}', '{% if sidebar_threads %}')
    content = content.replace('{% for t in threads %}', '{% for item in sidebar_threads %}')
    
    # Replace references to t.id, t.hospital, t.treatment_request with item.thread.id, etc
    content = content.replace('t.id', 'item.thread.id')
    content = content.replace('t.hospital', 'item.thread.hospital')
    content = content.replace('t.treatment_request', 'item.thread.treatment_request')
    
    # Replace unread_counts[t.id]
    content = content.replace('unread_counts[item.thread.id]', 'item.unread_count')
    
    # Replace t.messages.count() > 0 with item.latest_message
    content = content.replace('t.messages.count() > 0', 'item.latest_message')
    
    # Replace t.messages[-1] with item.latest_message
    content = content.replace('t.messages[-1]', 'item.latest_message')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

for tpl in [
    'templates/patient-secure-messages.html',
    'templates/patient-message-thread.html',
    'templates/hospital-messages.html',
    'templates/hospital-message-thread.html'
]:
    update_template(tpl)

print("Updated app.py and templates.")
