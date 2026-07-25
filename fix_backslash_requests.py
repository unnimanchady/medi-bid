import re

with open('templates/patient-requests.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    r"{{ page_title | default(\'My Requests\') }}",
    r"{{ page_title | default('My Requests') }}"
)

c = c.replace(
    r"{{ page_desc | default(\'Manage and track your submitted treatment requests.\') }}",
    r"{{ page_desc | default('Manage and track your submitted treatment requests.') }}"
)

with open('templates/patient-requests.html', 'w', encoding='utf-8') as f:
    f.write(c)
