import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block starting with <div class="relative w-[80px] sm:w-[140px]... flex-shrink-0">
    # containing an svg, up to the matching </div>
    pattern_svg_container = r'<div class="relative\s+w-\[80px\][^>]*animate-float-subtle[^>]*>.*?</div>'
    
    # We also want to reduce the margin on the parent div containing the text message.
    # The parent has class="flex flex-col items-center justify-center mb-4 sm:mb-8 opacity-0 animate-fade-in text-center"
    
    # First, replace the margin
    content = content.replace('mb-4 sm:mb-8 opacity-0 animate-fade-in', 'mb-2 sm:mb-4 opacity-0 animate-fade-in')
    
    # Second, remove the svg container
    new_content = re.sub(pattern_svg_container, '', content, flags=re.DOTALL)
    
    # Remove any extra blank lines left behind (optional but clean)
    new_content = re.sub(r'\n\s*\n\s*<p class="text-\[12px\]', r'\n            <p class="text-[12px]', new_content)
    
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
