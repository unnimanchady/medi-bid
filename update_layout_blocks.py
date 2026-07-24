import os

with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace <title>
if '<title>Patient Dashboard | MediBid</title>' in content:
    content = content.replace('<title>Patient Dashboard | MediBid</title>', '<title>{% block title %}Patient Dashboard | MediBid{% endblock %}</title>')

# Add block page_styles before closing </head>
if '</head>' in content:
    content = content.replace('</head>', '    {% block page_styles %}{% endblock %}\n</head>')

# Rename block scripts to block page_scripts
if '{% block scripts %}{% endblock %}' in content:
    content = content.replace('{% block scripts %}{% endblock %}', '{% block page_scripts %}{% endblock %}')
elif '</body>' in content and '{% block page_scripts %}' not in content:
    content = content.replace('</body>', '{% block page_scripts %}{% endblock %}\n</body>')

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated patient-layout.html blocks.")
