import os
import glob
import re

templates_dir = "templates"

mappings = {
    'index.html': 'home',
    'patient-registration-step1.html': 'patient_registration_step1',
    'patient-registration-step2.html': 'patient_registration_step2',
    'patient-registration-step3.html': 'patient_registration_step3',
    'patient-registration-step4.html': 'patient_registration_step4',
    'patient-registration-step5.html': 'patient_registration_step5',
    'patient-registration-success.html': 'patient_registration_success',
    'patient-dashboard.html': 'patient_dashboard',
    'patient-request-details.html': 'patient_request_details',
    'patient-hospital-responses.html': 'patient_hospital_responses',
    'patient-hospital-profile.html': 'patient_hospital_profile',
    'patient-compare-hospitals.html': 'patient_compare_hospitals',
    'patient-treatment-proposal-details.html': 'patient_treatment_proposal_details',
    'patient-proposal-details.html': 'patient_treatment_proposal_details',
    'patient-secure-messages.html': 'patient_secure_messages',
    'patient-profile-settings.html': 'patient_profile_settings'
}

files_modified = set()
total_replacements = 0

for filepath in glob.glob(os.path.join(templates_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for key, val in mappings.items():
        # href="filename.html"
        content, count = re.subn(r'href=([\'"])' + re.escape(key) + r'\1', f'href="{{{{ url_for(\'{val}\') }}}}"', content)
        total_replacements += count
        
        # action="filename.html"
        content, count = re.subn(r'action=([\'"])' + re.escape(key) + r'\1', f'action="{{{{ url_for(\'{val}\') }}}}"', content)
        total_replacements += count
        
        # window.location.href = "filename.html"
        content, count = re.subn(r'window\.location\.href\s*=\s*([\'"])' + re.escape(key) + r'\1', f'window.location.href = "{{{{ url_for(\'{val}\') }}}}"', content)
        total_replacements += count

        # window.location.assign("filename.html")
        content, count = re.subn(r'window\.location\.assign\(([\'"])' + re.escape(key) + r'\1\)', f'window.location.assign("{{{{ url_for(\'{val}\') }}}}")', content)
        total_replacements += count
        
        # location.href = "filename.html" (to be safe)
        content, count = re.subn(r'(?<!window\.)location\.href\s*=\s*([\'"])' + re.escape(key) + r'\1', f'location.href = "{{{{ url_for(\'{val}\') }}}}"', content)
        total_replacements += count
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        files_modified.add(filepath)

print(f"Files modified: {len(files_modified)}")
print(f"Total replacements: {total_replacements}")
