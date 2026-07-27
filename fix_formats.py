import sys
import glob

# 1. Update admin-proposal-view.html
filepath = r'f:\projects\medi-bid\templates\admin-proposal-view.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '{{ hospital.city }}, {{ hospital.country }}',
    '{{ hospital|format_location }}'
)
content = content.replace(
    "{{ proposal.estimated_duration_value }} {{ proposal.estimated_duration_unit|default('days', true)|capitalize }}",
    "{{ proposal.estimated_duration_value|format_duration(proposal.estimated_duration_unit) }}"
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update admin-treatment-request-detail.html
filepath = r'f:\projects\medi-bid\templates\admin-treatment-request-detail.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '{{ proposal.hospital.city }}, {{ proposal.hospital.country }}',
    '{{ proposal.hospital|format_location }}'
)
content = content.replace(
    "{{ proposal.estimated_duration_value }} {{ proposal.estimated_duration_unit }}s",
    "{{ proposal.estimated_duration_value|format_duration(proposal.estimated_duration_unit) }}"
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done updating templates.")
