import os
import re

files = [
    'patient-dashboard.html',
    'patient-request-details.html',
    'patient-hospital-responses.html',
    'patient-treatment-proposal-details.html',
    'patient-hospital-profile.html',
    'patient-secure-messages.html',
    'patient-medical-documents.html',
    'patient-notifications.html',
    'patient-profile-settings.html',
    'patient-support.html',
    'patient-support-ticket.html',
    'patient-compare-hospitals.html'
]

# Read patient-layout.html
with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    layout = f.read()

# We need to revert the jinja user safe checks back to normal first
layout = layout.replace("{% if user %}", "")
layout = layout.replace("{% else %}", "")
layout = layout.replace("{% endif %}", "")
layout = layout.replace("""                        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-softBlue border border-blue-100 flex items-center justify-center text-secondary font-extrabold text-[12px] sm:text-[13px] uppercase shadow-sm">
                            G
                        </div>
                        <div class="hidden sm:flex flex-col text-left">
                            <span class="text-[13px] font-bold text-textMain leading-none">Guest</span>
                        </div>""", "")
layout = layout.replace("""                            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-extrabold text-[14px] uppercase shadow-sm">
                                G
                            </div>
                            <div class="flex flex-col min-w-0">
                                <p class="text-[14px] font-bold text-textMain truncate">Guest User</p>
                                <p class="text-[12px] text-textMuted truncate">guest@medibid.com</p>
                            </div>""", "")

# Split layout into top, bottom, scripts
content_split = layout.split('{% block content %}')
top_part = content_split[0]

# Replace {% block page_styles %}
top_part = top_part.replace("{% block page_styles %}{% endblock %}", "")
# Remove {% block title %}...{% endblock %} - wait, we just want standard <title>Patient Dashboard | MediBid</title>
top_part = re.sub(r'\{% block title %\}.*?\{% endblock %\}', 'Patient Dashboard | MediBid', top_part)

after_content = content_split[1]
bottom_split = after_content.split('{% endblock %}')
bottom_part = bottom_split[0].strip() # Should be empty normally, wait, what is after block content?
# The endblock for content is: {% block content %}\n...\n{% endblock %}
# So bottom_split[0] is just the stuff inside the block (which is nothing in the layout file)

after_content_endblock = bottom_split[1]
# Now we have <!-- FOOTER --> and then scripts.
# Then {% block page_scripts %}{% endblock %}

scripts_split = after_content_endblock.split('{% block page_scripts %}')
bottom_part = scripts_split[0]
footer_scripts = scripts_split[1].split('{% endblock %}')[1] if '{% endblock %}' in scripts_split[1] else scripts_split[1]

# Now, apply to each file
for fn in files:
    try:
        with open('templates/' + fn, 'r', encoding='utf-8') as f:
            t = f.read()
    except FileNotFoundError:
        continue
        
    if '{% extends' not in t:
        print(f'{fn} already standalone.')
        continue

    # Extract content
    try:
        main_content = t.split('{% block content %}')[1].split('{% endblock %}')[0].strip()
    except IndexError:
        main_content = ""
        
    try:
        if '{% block page_scripts %}' in t:
            custom_scripts = t.split('{% block page_scripts %}')[1].split('{% endblock %}')[0].strip()
        else:
            custom_scripts = ""
    except IndexError:
        custom_scripts = ""
        
    new_t = top_part + "\n" + main_content + "\n" + bottom_part + "\n" + custom_scripts + "\n" + footer_scripts
    
    # Remove any stray newlines left by replace
    new_t = new_t.replace('\n\n\n\n', '\n\n')
    
    with open('templates/' + fn, 'w', encoding='utf-8') as f:
        f.write(new_t)
    print(f'Restored {fn}')
