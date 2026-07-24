import re

files = ['templates/patient-dashboard.html', 'templates/patient-medical-documents.html', 'templates/patient-notifications.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sidebar_pattern = re.compile(r'<a href="[^"]*"([^>]*)>(.*?)Notifications</a>')
    new_content = sidebar_pattern.sub(r'<a href="{{ url_for(\'patient_notifications\') }}"\1>\2Notifications</a>', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated sidebar in {filepath}")
