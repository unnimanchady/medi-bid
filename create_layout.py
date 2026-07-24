import os

with open('templates/patient-dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
# Extract head, body start, sidebar, mobile drawer, main container start, and top header
layout_top = []
for i, line in enumerate(lines):
    layout_top.append(line)
    if '<!-- DASHBOARD MAIN CONTENT -->' in line:
        layout_top.pop() # remove the DASHBOARD MAIN CONTENT line
        break
        
# Extract scripts and footer
layout_bottom = []
found_scripts = False
for line in lines:
    if '<!-- MAIN DASHBOARD JS -->' in line:
        found_scripts = True
    if found_scripts:
        layout_bottom.append(line)
        
layout_content = "".join(layout_top)
layout_content += "    {% block content %}{% endblock %}\n"
layout_content += "</div>\n"
layout_content += "".join(layout_bottom).replace('</body>', '    {% block scripts %}{% endblock %}\n</body>')

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(layout_content)
    
print("patient-layout.html created successfully.")
