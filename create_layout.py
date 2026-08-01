import re

with open('templates/hospital-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract everything before <main ...>
head_match = re.search(r'(.*?<main[^>]*>)', content, re.DOTALL)
head_content = head_match.group(1) if head_match else ''

# Extract everything after </main>
tail_match = re.search(r'(</main>.*)', content, re.DOTALL)
tail_content = tail_match.group(1) if tail_match else ''

# Create hospital-layout.html
layout_content = head_content + '''
            {% block content %}{% endblock %}
''' + tail_content

# We need to replace the static title with a block
layout_content = re.sub(r'<title>.*?</title>', r'<title>{% block title %}Hospital Portal | TreatAnywhere{% endblock %}</title>', layout_content)

# Inject page_styles block and page_scripts block
layout_content = layout_content.replace('</head>', '    {% block page_styles %}{% endblock %}\n</head>')
layout_content = layout_content.replace('</body>', '    {% block page_scripts %}{% endblock %}\n</body>')

# Remove dashboard specific active states if any and use jinja variables
layout_content = layout_content.replace('''<h2 class="text-[16px] font-bold text-primary">Hospital Dashboard</h2>''', '''<h2 class="text-[16px] font-bold text-primary">{{ page_title | default("Hospital Portal") }}</h2>''')

with open('templates/hospital-layout.html', 'w', encoding='utf-8') as f:
    f.write(layout_content)

print("hospital-layout.html created")
