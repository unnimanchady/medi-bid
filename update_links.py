import os
import re

for filepath in ['templates/patient-compare-hospitals.html', 'templates/patient-treatment-proposal-details.html']:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace url_for('patient_hospital_profile') with url_for('patient_hospital_profile', hospital_id=proposal.hospital_id, proposal_id=proposal.id)
    content = re.sub(
        r"url_for\('patient_hospital_profile'\)",
        r"url_for('patient_hospital_profile', hospital_id=proposal.hospital_id, proposal_id=proposal.id)",
        content
    )
    # Also handle the fallback one I might have added earlier like url_for('patient_hospital_profile', proposal_id=1) 
    content = re.sub(
        r"url_for\('patient_hospital_profile', proposal_id=1\)",
        r"url_for('patient_hospital_profile', hospital_id=proposal.hospital_id, proposal_id=proposal.id)",
        content
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done linking.')
