import os

scripts = [
    "create_patient_medical_docs_template.py",
    "update_sidebars.py",
    "create_patient_notifications_html.py",
    "inject_notifications_header.py",
    "update_profile_template.py",
    "create_support_template.py",
    "create_ticket_template.py"
]

for script in scripts:
    print(f"Running {script}...")
    os.system(f"venv\\Scripts\\python {script}")

print("Done rebuilding templates.")
