import re

with open('verify_hospital_messages.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('mayo.user_id', 'mayo.registration_user_id')
c = c.replace('cleveland.user_id', 'cleveland.registration_user_id')

with open('verify_hospital_messages.py', 'w', encoding='utf-8') as f:
    f.write(c)
