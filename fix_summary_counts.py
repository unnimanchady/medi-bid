import re

with open('templates/patient-request-details.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace Matched count from 0 to N/A
c = re.sub(
    r'<span class="text-\[11px\] text-textMuted font-bold uppercase">Matched</span>\s*<span class="text-\[16px\] font-extrabold text-primary">0</span>',
    r'<span class="text-[11px] text-textMuted font-bold uppercase">Matched</span>\n                                <span class="text-[16px] font-extrabold text-primary">--</span>',
    c
)

# Replace Responses count from 0 to actual count
c = re.sub(
    r'<span class="text-\[11px\] text-textMuted font-bold uppercase">Responses</span>\s*<span class="text-\[16px\] font-extrabold text-secondary">0</span>',
    r'<span class="text-[11px] text-textMuted font-bold uppercase">Responses</span>\n                                <span class="text-[16px] font-extrabold text-secondary">{{ request.proposals | selectattr(\'status\', \'equalto\', \'submitted\') | list | length }}</span>',
    c
)

# Fix line 160 Good news to also be explicitly accurate
c = re.sub(
    r'Good News! You have \{\{ request\.proposals\|length \}\} hospital \{% if request\.proposals\|length == 1 %\}response\{% else %\}responses\{% endif %\}',
    r'Good News! You have {{ request.proposals | selectattr(\'status\', \'equalto\', \'submitted\') | list | length }} hospital {% if (request.proposals | selectattr(\'status\', \'equalto\', \'submitted\') | list | length) == 1 %}response{% else %}responses{% endif %}',
    c
)

with open('templates/patient-request-details.html', 'w', encoding='utf-8') as f:
    f.write(c)
