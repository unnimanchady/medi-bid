with open('templates/patient-hospital-responses.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("response.submitted_at.strftime('%b %d, %Y')", "(response.submitted_at.strftime('%b %d, %Y') if response.submitted_at else 'Unknown')")
with open('templates/patient-hospital-responses.html', 'w', encoding='utf-8') as f:
    f.write(c)
