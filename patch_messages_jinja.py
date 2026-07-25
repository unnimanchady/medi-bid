import re

with open('templates/patient-secure-messages.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the broken jinja block
c = c.replace(
    "{% set last_msg = thread.messages.order_by(thread.messages._klass.created_at.desc()).first() %}",
    "{% set all_msgs = thread.messages.all() %}\n                                        {% set last_msg = all_msgs[-1] if all_msgs else None %}"
)

with open('templates/patient-secure-messages.html', 'w', encoding='utf-8') as f:
    f.write(c)
