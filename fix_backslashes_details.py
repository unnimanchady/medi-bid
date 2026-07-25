import re

with open('templates/patient-request-details.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    r"{{ request.proposals | selectattr(\'status\', \'equalto\', \'submitted\') | list | length }}",
    "{{ request.proposals | selectattr('status', 'equalto', 'submitted') | list | length }}"
)

c = c.replace(
    r"{% if (request.proposals | selectattr(\'status\', \'equalto\', \'submitted\') | list | length) == 1 %}",
    "{% if (request.proposals | selectattr('status', 'equalto', 'submitted') | list | length) == 1 %}"
)

with open('templates/patient-request-details.html', 'w', encoding='utf-8') as f:
    f.write(c)
