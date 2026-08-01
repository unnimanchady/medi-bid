import re

with open('templates/hospital-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the inner part of <main>
main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
if main_match:
    main_content = main_match.group(1).strip()
    
    # We should exclude the footer part if it's there, but actually patient-layout usually has a footer. 
    # Let's see if patient-layout has a footer. It doesn't matter, we can keep the footer inside the block or remove it.
    
    new_content = '''{% extends "hospital-layout.html" %}
{% set page_title = "Hospital Dashboard" %}
{% set active_page = "dashboard" %}

{% block content %}
''' + main_content + '''
{% endblock %}
'''
    with open('templates/hospital-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("hospital-dashboard.html refactored")
else:
    print("Failed to find <main> block")
