import glob

def fix_main_scroll(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace 'relative overflow-y-auto' or just 'overflow-y-auto' in the main tag
    new_content = content.replace(
        '<main class="flex-grow flex flex-col items-center py-4 sm:py-14 px-4 sm:px-6 relative overflow-y-auto">',
        '<main class="flex-grow flex flex-col items-center py-4 sm:py-14 px-4 sm:px-6 relative">'
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed scrolling in {filepath}")
    else:
        print(f"No match found in {filepath}")

if __name__ == "__main__":
    files = glob.glob('f:/projects/medi-bid/templates/patient-registration-step*.html')
    for f in files:
        fix_main_scroll(f)
