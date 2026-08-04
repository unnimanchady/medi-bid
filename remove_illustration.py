import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace the whole 1.5. HEALTHCARE ILLUSTRATION block up to Trust Message
    # with just the Trust Message block.
    
    # We can use regex to match from <!-- 1.5. HEALTHCARE ILLUSTRATION to <!-- Trust Message -->
    pattern = r'(<!-- 1\.5\. HEALTHCARE ILLUSTRATION & TRUST MESSAGE -->\s*<div class="[^"]*mb-4 sm:mb-8[^"]*">)\s*<!-- Subtle floating illustration -->\s*<div class="relative[^>]*>.*?</div>\s*(<!-- Trust Message -->)'
    
    new_content = re.sub(pattern, r'<!-- 1.5. TRUST MESSAGE -->\n        <div class="flex flex-col items-center justify-center mb-2 sm:mb-4 opacity-0 animate-fade-in text-center">\n            \2', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Processed {filepath}")
    else:
        print(f"No match found in {filepath}")

if __name__ == "__main__":
    files = glob.glob('f:/projects/medi-bid/templates/patient-registration-step*.html')
    for f in files:
        fix_file(f)
