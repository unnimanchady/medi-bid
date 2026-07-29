import os
import re

template_dir = r'f:\projects\medi-bid\templates'
count = 0

for root, _, files in os.walk(template_dir):
    for file in files:
        if not file.endswith('.html'):
            continue
        filepath = os.path.join(root, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig = content
        
        def repl(m):
            cls = m.group(1)
            treat_c = 'text-white' if 'text-white' in cls else 'text-primary'
            cls = re.sub(r'\btext-(primary|white|textMain)\b', '', cls).replace('  ', ' ').strip()
            return f'<span class="{cls}"><span class="{treat_c}">Treat</span><span class="text-secondary">Anywhere</span></span>'
            
        content = re.sub(r'<span class="([^"]*tracking-tight[^"]*)">MediBid</span>', repl, content)
        
        if content != orig:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            
print(f'Updated {count} files.')
