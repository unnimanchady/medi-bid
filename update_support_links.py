import os
import glob
import re

target_dir = 'templates'
files = glob.glob(os.path.join(target_dir, 'patient-*.html'))

# Pattern for Desktop sidebar button
pattern_desktop = re.compile(
    r'<button disabled title="Feature coming soon" class="[^"]*w-full flex items-center justify-between px-4 py-3 rounded-xl text-white/50 hover:text-white/60 bg-transparent hover:bg-white/5 transition-all cursor-not-allowed group text-left">\s*<div class="flex items-center gap-3 font-medium">\s*<i data-lucide="help-circle" class="w-5 h-5"></i> Help & Support\s*</div>\s*<span class="[^"]*">Soon</span>\s*</button>',
    re.MULTILINE
)

replacement_desktop = """<a href="{{ url_for('patient_support') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all group">
                <i data-lucide="help-circle" class="w-5 h-5 group-hover:text-white transition-colors"></i> Help & Support
            </a>"""

# Pattern for Footer link <a href="#">Help & Support</a>
pattern_footer = re.compile(r'<a href="#" class="([^"]*)">Help & Support</a>')
replacement_footer = r'<a href="{{ url_for(' + "'patient_support'" + r') }}" class="\1">Help & Support</a>'



for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    content = pattern_desktop.sub(replacement_desktop, content)
    content = pattern_footer.sub(replacement_footer, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
