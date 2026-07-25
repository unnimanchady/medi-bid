import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix NameError
c = c.replace(
    'threads = MessageThread.query.filter',
    'from models import MessageThread\n            threads = MessageThread.query.filter'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
