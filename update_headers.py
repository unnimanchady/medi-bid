import glob
import re

for filepath in glob.glob('templates/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Sarah Jenkins' in content and 'profile-dropdown' in content:
        # Replace the Sarah Jenkins name and email
        content = re.sub(
            r'<p class="text-\[14px\] font-bold text-textMain truncate">Sarah Jenkins</p>\s*<p class="text-\[12px\] text-textMuted truncate">sarah\.j@example\.com</p>',
            r'<p class="text-[14px] font-bold text-textMain truncate">{{ user.first_name }} {{ user.last_name }}</p>\n                        <p class="text-[12px] text-textMuted truncate">{{ user.email }}</p>',
            content
        )
        # Replace the SJ avatar
        content = re.sub(
            r'<div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-primary flex items-center justify-center text-white font-bold text-\[13px\] sm:text-\[14px\]">SJ</div>',
            r'<div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-primary flex items-center justify-center text-white font-bold text-[13px] sm:text-[14px]">{{ user.first_name[0] }}{{ user.last_name[0] }}</div>',
            content
        )
    
    if 'patient-secure-messages.html' in filepath:
        content = content.replace('Apollo Hospitals', '{{ hospital.display_name or hospital.legal_name }}')
        content = content.replace('MB-2026-8A39C2', '{{ request.reference_id }}')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print("Done header replacements.")
