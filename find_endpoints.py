import re
with open('old_compare.txt', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
    endpoints = re.findall(r'/patient/[a-zA-Z0-9\-\_]+', content)
    print(set(endpoints))
