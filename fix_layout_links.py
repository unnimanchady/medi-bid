import re

with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Restore Compare Proposals
c = re.sub(
    r'<a href=\"\{\{ url_for\(\'patient_requests\'\) \}\}\"([^\>]*?)\>\s*<i data-lucide=\"bar-chart-2\"',
    r'<a href="{{ url_for(\'patient_compare_hospitals\', request_id=request.id) if request and request.reference_id else url_for(\'patient_compare_hospitals\') }}"\1>\n                <i data-lucide="bar-chart-2"',
    c
)

# Set Hospital Responses to patient_requests with context
c = re.sub(
    r'<a href=\"\{\{ url_for\(\'patient_requests\'\) \}\}\"([^\>]*?)\>\s*<i data-lucide=\"building-2\"',
    r'<a href="{{ url_for(\'patient_requests\', context=\'responses\') }}"\1>\n                <i data-lucide="building-2"',
    c
)

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(c)
