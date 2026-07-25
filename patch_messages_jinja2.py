import re

with open('templates/patient-secure-messages.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('active_(thread.hospital.display_name or thread.hospital.legal_name)', '(active_thread.hospital.display_name or active_thread.hospital.legal_name)')

with open('templates/patient-secure-messages.html', 'w', encoding='utf-8') as f:
    f.write(c)
