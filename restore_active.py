import re

active_link = '''<a href="{{ url_for('hospital_messages') }}" class="px-4 py-3 bg-softBlue text-secondary flex items-center gap-3 rounded-xl">
                <i data-lucide="message-square" class="w-5 h-5 shrink-0"></i>
                <span class="font-bold">Messages</span>
            </a>'''

for filepath in ['templates/hospital-messages.html', 'templates/hospital-message-thread.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(
        r'<a href="{{ url_for\(\'hospital_messages\'\) }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">.*?</a>',
        active_link,
        content,
        flags=re.DOTALL
    )
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Restored active state in {filepath}')
