import os

target = '''            <div class="px-4 py-3 text-textMuted flex items-center gap-3 rounded-xl cursor-not-allowed opacity-60 transition-opacity hover:opacity-100 group" title="Coming Soon">
                <i data-lucide="file-text" class="w-5 h-5"></i>
                <span class="font-medium">Proposals</span>
                <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-gray-100 text-gray-500 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
            </div>'''

replacement = '''            <a href="{{ url_for('hospital_proposals') }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">
                <i data-lucide="file-text" class="w-5 h-5"></i>
                <span>Proposals</span>
            </a>'''

d = 'templates'
count = 0
for f in os.listdir(d):
    if f.startswith('hospital-') and f.endswith('.html'):
        p = os.path.join(d, f)
        with open(p, 'r', encoding='utf-8') as file:
            content = file.read()
        if target in content:
            content = content.replace(target, replacement)
            with open(p, 'w', encoding='utf-8') as file:
                file.write(content)
            count += 1
            print('Updated', f)

print(f'Done. Updated {count} files.')
