import re

with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    r"{{ url_for(\'patient_requests\') }}",
    "{{ url_for('patient_requests') }}"
)

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(c)
