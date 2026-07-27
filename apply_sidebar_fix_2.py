import glob

old_text_3 = """            <div class="px-4 py-3 text-textMuted flex items-center gap-3 rounded-xl cursor-not-allowed opacity-60 transition-opacity hover:opacity-100 group" title="Coming Soon">
                <i data-lucide="message-square" class="w-5 h-5"></i>
                <span class="font-medium">Messages</span>
                <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-gray-100 text-gray-500 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
            </div>"""

new_text_3 = """            <a href="{{ url_for('hospital_messages') }}" class="px-4 py-3 text-textMuted flex items-center gap-3 rounded-xl hover:bg-gray-50 hover:text-gray-900 transition-all">
                <i data-lucide="message-square" class="w-5 h-5"></i>
                <span class="font-medium">Messages</span>
            </a>"""

old_text_4 = """                <div class="px-3 py-2 text-textMuted flex items-center gap-3 rounded-xl cursor-not-allowed opacity-60 group">
                    <i data-lucide="message-square" class="w-5 h-5"></i>
                    <span class="font-medium">Messages</span>
                    <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-gray-100 text-gray-500 px-2 py-0.5 rounded">Soon</span>
                </div>"""

new_text_4 = """                <a href="{{ url_for('hospital_messages') }}" class="px-3 py-2 text-textMuted flex items-center gap-3 rounded-xl hover:bg-gray-50 hover:text-gray-900 transition-all">
                    <i data-lucide="message-square" class="w-5 h-5"></i>
                    <span class="font-medium">Messages</span>
                </a>"""

for filepath in glob.glob('templates/hospital-*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    if old_text_3 in content:
        content = content.replace(old_text_3, new_text_3)
    if old_text_4 in content:
        content = content.replace(old_text_4, new_text_4)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
