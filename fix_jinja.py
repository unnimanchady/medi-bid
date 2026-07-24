import os
import glob
import re

html_files = glob.glob('templates/*.html')
count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace escaped single quotes in url_for inside Jinja brackets
    # Actually, we can just replace the specific string:
    target = r"{{ url_for(\'patient_notifications\') }}"
    replacement = r"{{ url_for('patient_notifications') }}"
    
    if target in content:
        new_content = content.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Fixed {filepath}")

print(f"Fixed {count} files.")
