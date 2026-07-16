import os
import glob
import re

templates_dir = "templates"

mappings = {
    'Dashboard': 'patient_dashboard',
    'My Requests': 'patient_hospital_responses',
    'View Requests': 'patient_hospital_responses',
    'View All History': 'patient_hospital_responses',
    'Messages': 'patient_secure_messages',
    'View Messages': 'patient_secure_messages',
    'View Responses': 'patient_hospital_responses',
    'My Profile': 'patient_profile_settings',
    'Account Settings': 'patient_profile_settings',
    'View Details': 'patient_request_details',
    'Review Proposal': 'patient_treatment_proposal_details',
    'Compare Estimates': 'patient_compare_hospitals',
    'View Hospital Profile': 'patient_hospital_profile',
    'Hospital Profile': 'patient_hospital_profile',
    'Sign In': 'patient_dashboard',
}

def replace_link(match):
    full_match = match.group(0)
    inner_text = match.group(1)
    
    # Check mappings
    for key, endpoint in mappings.items():
        if key in inner_text:
            return full_match.replace('href="#"', f'href="{{{{ url_for(\'{endpoint}\') }}}}"')
            
    return full_match

for filepath in glob.glob(os.path.join(templates_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    content = re.sub(r'<a\s+[^>]*?href="#"[^>]*>(.*?)</a>', replace_link, content, flags=re.DOTALL | re.IGNORECASE)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

print("Done")
