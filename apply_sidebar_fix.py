import glob

# Variant 1: Desktop sidebar
old_text_1 = """            <div class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl cursor-not-allowed opacity-60 group" title="Coming Soon">
                <i data-lucide="message-square" class="w-5 h-5 shrink-0"></i>
                <span>Messages</span>
                <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-500 px-2.5 py-0.5 rounded-full">Soon</span>
            </div>"""

new_text_1 = """            <a href="{{ url_for('hospital_messages') }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">
                <i data-lucide="message-square" class="w-5 h-5 shrink-0"></i>
                <span>Messages</span>
            </a>"""

# Variant 2: Mobile sidebar
old_text_2 = """                <div class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl cursor-not-allowed opacity-60 group">
                    <i data-lucide="message-square" class="w-5 h-5 shrink-0"></i>
                    <span>Messages</span>
                    <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-500 px-2.5 py-0.5 rounded-full">Soon</span>
                </div>"""

new_text_2 = """                <a href="{{ url_for('hospital_messages') }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">
                    <i data-lucide="message-square" class="w-5 h-5 shrink-0"></i>
                    <span>Messages</span>
                </a>"""

for filepath in glob.glob('templates/hospital-*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # In files where it's already an active link (like hospital-messages.html), 
    # we don't want to replace anything if it would result in duplicates.
    # Actually, hospital-messages.html doesn't have the 'Soon' blocks anymore because they were 
    # removed when it was created?
    # Let's check if the old text is present and simply replace it.
    
    if old_text_1 in content:
        content = content.replace(old_text_1, new_text_1)
    if old_text_2 in content:
        content = content.replace(old_text_2, new_text_2)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
