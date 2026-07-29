import os
import glob

template_dir = r"f:\projects\medi-bid\templates"
html_files = glob.glob(os.path.join(template_dir, "*.html"))

replacements = [
    ("MediBid For Hospitals", "TreatAnywhere for Hospitals"),
    ("MediBid for Hospitals", "TreatAnywhere for Hospitals"),
    ("MediBid", "TreatAnywhere")
]

files_changed = []

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        files_changed.append(os.path.basename(file_path))

print("Changed files:")
for f in files_changed:
    print(f)
