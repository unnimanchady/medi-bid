import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Make sure HospitalUser is imported at the top level so it's available everywhere
if 'from models import HospitalUser' not in c and 'HospitalUser' not in c.split('\n')[0]:
    c = c.replace('from models import User, Hospital', 'from models import User, Hospital, HospitalUser')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
