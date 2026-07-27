import glob, re

replacement_link = '''<a href="{{ url_for('hospital_messages') }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">
                <i data-lucide="message-square" class="w-5 h-5 shrink-0"></i>
                <span>Messages</span>
            </a>'''

for filepath in glob.glob('templates/hospital-*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace the div that contains 'message-square' and 'Soon' / 'Messages'
    new_content = re.sub(
        r'<div[^>]*>.*?<i[^>]*message-square[^>]*>.*?Messages.*?</div>',
        replacement_link,
        content,
        flags=re.DOTALL
    )
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')
