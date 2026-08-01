import os
import re

def refactor_file(filepath, active_page, page_title):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract inner main part
    main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
    if not main_match:
        print(f"No <main> tag found in {filepath}")
        return
        
    main_content = main_match.group(1).strip()
    
    # Remove custom headers because layout handles it
    header_match = re.search(r'<header.*?</header>', main_content, re.DOTALL)
    if header_match:
        header_content = header_match.group(0)
        main_content = main_content.replace(header_content, '')
        
        # If there's a back button in the header, we want to inject it at the top of the content
        if 'Back' in header_content or 'back' in header_content:
            # Try to extract the link
            back_link_match = re.search(r'<a href="([^"]+)".*?>.*?</a>', header_content, re.DOTALL)
            if back_link_match:
                # Add a back button block
                top_bar = f'''
                <div class="mb-4">
                    <a href="{back_link_match.group(1)}" class="inline-flex items-center gap-2 text-textMuted hover:text-[#C2410C] font-semibold transition-colors text-[14px]">
                        <i data-lucide="arrow-left" class="w-4 h-4"></i> Back
                    </a>
                </div>
                '''
                main_content = top_bar + main_content
                
    # Theme adjustments (Blue/Accent to Orange)
    main_content = main_content.replace('text-accent', 'text-[#C2410C]')
    main_content = main_content.replace('bg-accent', 'bg-[#C2410C]')
    main_content = main_content.replace('border-accent', 'border-[#C2410C]')
    main_content = main_content.replace('ring-blue-50', 'ring-orange-50')
    main_content = main_content.replace('hover:bg-blue-600', 'hover:bg-[#EA580C]')
    main_content = main_content.replace('hover:text-blue-700', 'hover:text-[#C2410C]')
    main_content = main_content.replace('hover:bg-blue-50', 'hover:bg-orange-50')
    main_content = main_content.replace('bg-blue-50', 'bg-orange-50')
    main_content = main_content.replace('text-blue-800', 'text-[#9A3412]')
    main_content = main_content.replace('border-blue-100', 'border-orange-100')
    main_content = main_content.replace('bg-gradient-to-r from-accent to-blue-700', 'bg-[#C2410C]')
    main_content = main_content.replace('text-blue-600', 'text-[#C2410C]')
    
    # Extract scripts
    script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    scripts = ''
    if script_match:
        script_code = script_match.group(1)
        # Remove lucide icon initialization if present as layout handles it
        script_code = script_code.replace('lucide.createIcons();', '')
        scripts = f'''\n{{% block page_scripts %}}\n<script>{script_code}</script>\n{{% endblock %}}'''
        
    new_content = f'''{{% extends "hospital-layout.html" %}}
{{% set page_title = "{page_title}" %}}
{{% set active_page = "{active_page}" %}}

{{% block content %}}
{main_content}
{{% endblock %}}
{scripts}'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Refactored {filepath}")

refactor_file('templates/hospital-proposal-edit.html', 'proposals', 'Edit Proposal')
refactor_file('templates/hospital-proposal-review.html', 'proposals', 'Review Proposal')
refactor_file('templates/hospital-treatment-request-detail.html', 'requests', 'Request Details')
