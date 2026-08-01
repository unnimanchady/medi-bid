import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. hospital_proposal_edit
old_edit = '''    if not _is_hospital_eligible(hospital, req.specialty):
        if request.method == 'POST':
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        abort(403)'''
        
new_edit = '''    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        if request.method == 'POST':
            return jsonify({'status': 'error', 'message': 'This treatment request is no longer active.'}), 403
        abort(403, description="This treatment request is no longer active.")'''
        
content = content.replace(old_edit, new_edit)

# 2. hospital_proposal_review
old_review = '''    if not _is_hospital_eligible(hospital, req.specialty):
        abort(403)'''
        
new_review = '''    if req.status in ['Closed', 'Completed', 'Cancelled', 'Expired'] or req.status != 'Active':
        abort(403, description="This treatment request is no longer active.")'''

# Replace the specific occurrences carefully for review, submit, and view
content = content.replace(old_review, new_review)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py proposal authorization rules successfully!")
