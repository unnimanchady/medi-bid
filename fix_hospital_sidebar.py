import glob

search_str = '''<div class="px-4 py-3 text-textMuted flex items-center gap-3 rounded-xl cursor-not-allowed opacity-60 transition-opacity hover:opacity-100 group" title="Coming Soon">
                    <i data-lucide="message-square" class="w-5 h-5"></i>
                    <span class="font-medium">Messages</span>
                    <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-gray-100 text-gray-500 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
                </div>'''

replace_str = '''<a href="{{ url_for('hospital_messages') }}" class="px-4 py-3 text-textMuted hover:bg-gray-50 hover:text-primary flex items-center gap-3 rounded-xl transition-colors">
                    <i data-lucide="message-square" class="w-5 h-5"></i>
                    <span class="font-medium">Messages</span>
                </a>'''

for filename in glob.glob('templates/hospital*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We strip spaces and handle formatting by using regex for flexibility
    import re
    
    pattern = re.compile(r'<div class="px-4 py-3 text-textMuted flex items-center gap-3 rounded-xl cursor-not-allowed opacity-60 transition-opacity hover:opacity-100 group" title="Coming Soon">\s*<i data-lucide="message-square" class="w-5 h-5"></i>\s*<span class="font-medium">Messages</span>\s*<span class="ml-auto text-\[10px\] font-bold uppercase tracking-wider bg-gray-100 text-gray-500 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>\s*</div>')
    
    if pattern.search(content):
        new_content = pattern.sub(replace_str, content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
