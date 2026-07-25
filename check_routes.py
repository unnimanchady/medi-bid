import re
with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()
for match in re.findall(r'@app\.route\([\'\"]([^\'\"]*)[\'\"]\)', c):
    if 'hospital-responses' in match or 'responses' in match:
        print(match)
