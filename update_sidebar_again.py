import re

with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's use a more specific regex for the href value
old_hrefs = []
for match in re.finditer(r'<a href=\"([^\"]+)\"[^>]*class=\"([^\"]+)\"[^>]*>\s*<i data-lucide=\"building-2\"[^>]*></i>\s*Hospital Responses\s*</a>', c, re.DOTALL):
    old_hrefs.append(match.group(1))

print("Current hrefs:", old_hrefs)

c = re.sub(
    r'<a href=\"([^\"]+)\"([^>]*)class=\"([^\"]+)\"([^>]*)>\s*<i data-lucide=\"building-2\"([^>]*)></i>\s*Hospital Responses\s*</a>',
    r'<a href="{{ url_for(\'patient_requests\') }}"\2class="\3"\4>\n                <i data-lucide="building-2"\5></i> Hospital Responses\n            </a>',
    c,
    flags=re.DOTALL
)

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(c)
