import glob

def fix_header_fixed(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change sticky to fixed w-full
    new_content = content.replace(
        'px-3 sm:px-6 lg:px-12 sticky top-0 z-50',
        'px-3 sm:px-6 lg:px-12 fixed w-full top-0 z-50'
    )
    
    # Add mt-[80px] to main to compensate for the fixed header
    # The main class might be slightly different in some files, but generally:
    # class="flex-grow flex flex-col items-center py-4 sm:py-14 px-4 sm:px-6 relative"
    if 'mt-[80px]' not in new_content:
        new_content = new_content.replace(
            '<main class="flex-grow flex flex-col items-center py-4 sm:py-14 px-4 sm:px-6 relative',
            '<main class="flex-grow flex flex-col items-center mt-[80px] py-4 sm:py-14 px-4 sm:px-6 relative'
        )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed header to fixed in {filepath}")
    else:
        print(f"No match found in {filepath}")

if __name__ == "__main__":
    files = glob.glob('f:/projects/medi-bid/templates/patient-registration-step*.html')
    for f in files:
        fix_header_fixed(f)
