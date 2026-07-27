import glob

non_active_link = """            <a href="{{ url_for('hospital_messages') }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">
                <i data-lucide="message-square" class="w-5 h-5 shrink-0"></i>
                <span>Messages</span>
            </a>"""

for filepath in glob.glob('templates/hospital-*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Check if there is an active link already (has url_for('hospital_messages') and bg-softBlue)
    has_active_link = "bg-softBlue" in content and "url_for('hospital_messages')" in content

    # Find the "Soon" messages block
    # It starts with `<div` and ends with `</div>` and contains `message-square` and `Soon`.
    # Let's find all occurrences of 'message-square'.
    import re
    # Match the div exactly by looking for the start div and end div containing message-square and Soon
    # non-greedy match of div contents
    pattern = r'<div[^>]*class="[^"]*cursor-not-allowed[^"]*"[^>]*>.*?<i[^>]*data-lucide="message-square"[^>]*>.*?Messages.*?Soon.*?</div>'
    
    matches = re.findall(pattern, content, flags=re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        if has_active_link:
            # Delete it
            content = content.replace(match, "")
        else:
            # Replace it with non-active link
            content = content.replace(match, non_active_link.strip())
            
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

