import os
import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Global CSS fix
    if 'overflow-x: hidden;' not in content:
        css_addition = """
        html, body {
            max-width: 100%;
            overflow-x: hidden;
        }"""
        content = re.sub(r'(</style>)', r'\n' + css_addition + r'\n    \1', content)

    # 2. Header
    content = content.replace('px-6 lg:px-12 sticky top-0', 'px-3 sm:px-6 lg:px-12 sticky top-0')
    content = content.replace('<div class="flex items-center gap-6">', '<div class="flex items-center gap-2 sm:gap-6">')
    content = content.replace('w-8 h-8 sm:w-10 sm:h-10', 'w-6 h-6 sm:w-10 sm:h-10')
    content = content.replace('text-[20px] font-extrabold leading-none', 'text-[18px] sm:text-[20px] font-extrabold leading-none')
    content = content.replace('gap-4 sm:gap-6', 'gap-2 sm:gap-6')
    content = content.replace('px-5 sm:px-6 py-2.5 rounded-full text-[14px]', 'px-3 py-1.5 sm:px-6 sm:py-2.5 rounded-full text-[13px] sm:text-[14px]')

    # 3. Main wrapper
    content = content.replace('py-10 sm:py-14', 'py-4 sm:py-14')
    
    # 4. Mobile back link
    content = content.replace('mb-8 self-start', 'mb-4 sm:mb-8 self-start')

    # 5. Illustration container
    content = content.replace('mb-8 opacity-0 animate-fade-in', 'mb-4 sm:mb-8 opacity-0 animate-fade-in')
    content = content.replace('w-[110px] sm:w-[140px] md:w-[170px] h-[110px] sm:h-[140px] md:h-[170px] mb-5', 'w-[80px] sm:w-[140px] md:w-[170px] h-[80px] sm:h-[140px] md:h-[170px] mb-3 sm:mb-5')

    # 6. Heading
    content = content.replace('<div class="text-center mb-10">', '<div class="text-center mb-6 sm:mb-10">')
    content = content.replace('text-[32px] sm:text-[38px] font-extrabold text-primary leading-tight tracking-tight mb-3', 'text-[24px] sm:text-[38px] font-extrabold text-primary leading-tight tracking-tight mb-1 sm:mb-3')
    content = content.replace('text-[15px] sm:text-[16px] text-gray-500 font-medium', 'text-[14px] sm:text-[16px] text-gray-500 font-medium')

    # 7. Progress Indicator
    content = content.replace('mb-10 sm:mb-12', 'mb-6 sm:mb-12')
    content = content.replace('mb-8 pb-6 relative z-10 px-2 sm:px-4', 'mb-4 sm:mb-8 pb-6 relative z-10 px-2 sm:px-4')
    
    # 8. Registration card padding
    content = content.replace('p-8 sm:p-10 relative', 'p-5 sm:p-10 relative')
    content = content.replace('p-6 sm:p-10 md:p-12 relative', 'p-5 sm:p-10 md:p-12 relative')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Processed {filepath}")

if __name__ == "__main__":
    files = glob.glob('f:/projects/medi-bid/templates/patient-registration-*.html')
    for f in files:
        fix_file(f)
