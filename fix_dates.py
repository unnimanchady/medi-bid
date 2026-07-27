import os

# 1. patient-treatment-proposal-details.html
filepath = r'f:\projects\medi-bid\templates\patient-treatment-proposal-details.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace(
    "{{ proposal.submitted_at.strftime('%B %d, %Y') }}",
    "{{ proposal.submitted_at.strftime('%B %d, %Y') if proposal.submitted_at else 'Not available' }}"
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. admin-treatment-request-detail.html
filepath = r'f:\projects\medi-bid\templates\admin-treatment-request-detail.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace(
    "{{ proposal.submitted_at.strftime('%b %d, %Y') }}",
    "{{ proposal.submitted_at.strftime('%b %d, %Y') if proposal.submitted_at else 'Not available' }}"
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. admin-proposal-view.html
filepath = r'f:\projects\medi-bid\templates\admin-proposal-view.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace(
    "{{ proposal.submitted_at.strftime('%B %d, %Y') }}",
    "{{ proposal.submitted_at.strftime('%B %d, %Y') if proposal.submitted_at else 'an unknown date' }}"
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dates safely.")
