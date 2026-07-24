import os
import glob
import re

inactive_nav_link = """            <a href="{{ url_for('patient_medical_documents') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all group mt-1">
                <i data-lucide="folder" class="w-5 h-5 group-hover:text-white transition-colors"></i> Medical Documents
            </a>"""

doc_btn_pattern = r'<button disabled[^>]*>\s*<div[^>]*>\s*<i data-lucide="folder"[^>]*></i>\s*Medical Documents\s*</div>\s*<span[^>]*>Soon</span>\s*</button>'

count = 0
for filepath in glob.glob('templates/patient-*.html'):
    if 'patient-medical-documents.html' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'data-lucide="folder"' in content and 'Medical Documents' in content:
        new_content = re.sub(doc_btn_pattern, inactive_nav_link, content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Updated {filepath}")

print(f"Total files updated: {count}")
