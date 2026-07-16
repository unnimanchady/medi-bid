import os
import glob
import re

templates_dir = "templates"

# Fix patient-dashboard.html
dash_path = os.path.join(templates_dir, 'patient-dashboard.html')
with open(dash_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("{{ patient.first_name | default('') }}", "[patient.first_name | default('')]")

with open(dash_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Fix onsubmit quotes in all html files
for filepath in glob.glob(os.path.join(templates_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace window.location.href="{{ url_for(...) }}"; with window.location.href='{{ url_for(...) }}'; inside onsubmit
    # Actually, let's just replace all occurrences of: window.location.href="{{ url_for
    # with: window.location.href='{{ url_for
    # and the trailing }}" with }}'
    
    original = content
    content = re.sub(r'window\.location\.href="\{\{\s*url_for\((.*?)\)\s*\}\}"', r"window.location.href='{{ url_for(\1) }}'", content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed quotes in {filepath}")

print("Fixes applied.")
