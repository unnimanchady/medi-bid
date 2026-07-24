import os, re

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
    'patient-support-ticket.html'
]

# We know the layout already includes all these common scripts.
COMMON_JS_MARKERS = [
    "lucide.createIcons()",
    "// Mobile Menu Toggle",
    "// Profile Dropdown Toggle",
    "// Notification Logic",
    "function toggleNotifDropdown",
    "const notifDropdown"
]

def clean_script_tag(script_content):
    """If the script ONLY contains layout stuff, we return empty string.
       If it contains custom page stuff (e.g. Chat UI logic), we keep it."""
    # A simple heuristic: remove the exact common blocks.
    # But since it's hard, we will just look for custom keywords.
    # If it contains "lucide.createIcons()" and not much else, it's common.
    lines = script_content.split('\n')
    is_custom = False
    for line in lines:
        if line.strip() == '' or line.strip() == '<script>' or line.strip() == '</script>':
            continue
        
        is_common_line = False
        for marker in COMMON_JS_MARKERS:
            if marker in line:
                is_common_line = True
                break
                
        # We assume if there are significant lines NOT in common markers, it's a custom script.
        # Actually, let's just use regex to extract scripts.
        pass

def migrate(filename):
    with open('templates/' + filename, 'r', encoding='utf-8') as f:
        content = f.read()

    if '{% extends' in content:
        print(f'{filename} already migrated.')
        return

    # Split by </header>
    if '</header>' not in content:
        print(f'Error: </header> not found in {filename}')
        return
        
    parts = content.split('</header>')
    after_header = parts[1]
    
    end_marker = None
    # Prioritize finding the end of the <main> block or FOOTER.
    if '<!-- FOOTER -->' in after_header:
        end_marker = '<!-- FOOTER -->'
    elif '<!-- MAIN DASHBOARD JS -->' in after_header:
        end_marker = '<!-- MAIN DASHBOARD JS -->'
    elif '<!-- Scripts -->' in after_header:
        end_marker = '<!-- Scripts -->'
    elif '<!-- MAIN SCRIPTS -->' in after_header:
        end_marker = '<!-- MAIN SCRIPTS -->'
    elif '<script>' in after_header:
        end_marker = '<script>'
        
    if not end_marker:
        print(f'Error: Could not find end marker in {filename}')
        return
        
    content_parts = after_header.split(end_marker)
    main_content = content_parts[0].strip()
    
    # We now have the script part:
    script_part = end_marker + content_parts[1]
    
    # Extract page specific scripts.
    # E.g. in patient-hospital-responses.html there is no custom JS.
    # In patient-secure-messages.html there is a LOT of custom JS (chat logic).
    # To be perfectly safe, I will just extract all <script>...</script> blocks from script_part
    # and if they contain specific page logic, include them. 
    # Actually, we can just grab all scripts that do NOT contain "lucide.createIcons()".
    # Wait, what if they mixed them? Let's just output the whole script part to a comment block and I'll review it.
    
    custom_scripts = []
    script_blocks = re.findall(r'<script.*?>.*?</script>', script_part, re.DOTALL)
    for block in script_blocks:
        if 'lucide.createIcons()' in block and 'function toggleNotifDropdown' in block:
            # This is the massive common block. Ignore it.
            continue
        elif 'function toggleNotifDropdown' in block or 'async function fetchNotifications' in block:
            # Common notification block. Ignore it.
            continue
        else:
            # Must be custom! Keep it.
            custom_scripts.append(block)
    
    new_html = '{% extends "patient-layout.html" %}\n\n'
    new_html += '{% block title %}' + filename.replace('.html', '').replace('-', ' ').title() + ' | MediBid{% endblock %}\n\n'
    new_html += '{% block content %}\n'
    new_html += main_content + '\n{% endblock %}\n\n'
    
    if custom_scripts:
        new_html += '{% block page_scripts %}\n'
        new_html += '\n'.join(custom_scripts)
        new_html += '\n{% endblock %}\n'
    
    with open('templates/' + filename, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print(f'Migrated {filename}')

for fn in files:
    migrate(fn)
