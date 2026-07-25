import re

with open('templates/patient-requests.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(
    r'<h1 class="([^"]+)">My Requests</h1>',
    r'<h1 class="\1">{{ page_title | default(\'My Requests\') }}</h1>',
    c
)

c = re.sub(
    r'<p class="([^"]+)">Manage and track your submitted treatment requests.</p>',
    r'<p class="\1">{{ page_desc | default(\'Manage and track your submitted treatment requests.\') }}</p>',
    c
)

with open('templates/patient-requests.html', 'w', encoding='utf-8') as f:
    f.write(c)
