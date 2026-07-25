import re

with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    r"{{ url_for(\'patient_requests\', context=\'responses\') }}",
    r"{{ url_for('patient_requests', context='responses') }}"
)

c = c.replace(
    r"{{ url_for(\'patient_compare_hospitals\', request_id=request.id) if request and request.reference_id else url_for(\'patient_compare_hospitals\') }}",
    r"{{ url_for('patient_compare_hospitals', request_id=request.id) if request and request.reference_id else url_for('patient_compare_hospitals') }}"
)

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(c)
