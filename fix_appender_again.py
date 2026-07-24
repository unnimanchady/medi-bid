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
    content = content.replace('unread_counts[t.id]', 'item.unread_count')
    
    # Replace t.messages.count() > 0 with item.latest_message
    content = content.replace('t.messages.count() > 0', 'item.latest_message')
    
    # Replace t.messages[-1] with item.latest_message
    content = content.replace('t.messages[-1]', 'item.latest_message')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

for tpl in [
    'templates/hospital-messages.html',
    'templates/hospital-message-thread.html'
]:
    update_template(tpl)

print("Updated templates.")
