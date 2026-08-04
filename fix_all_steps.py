import glob
import re

def fix_buttons(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace `rounded-full` with `rounded-xl` for buttons only.
    # We can match `<a ... rounded-full` and `<button ... rounded-full` in the bottom buttons area.
    
    # A simple regex for button classes
    def replace_button_class(match):
        cls = match.group(0)
        cls = cls.replace('rounded-full', 'rounded-xl')
        cls = cls.replace('sm:py-4', 'sm:py-3.5')
        cls = cls.replace('py-4', 'py-3.5')
        return cls

    # We match the class attribute of button or a tag
    content = re.sub(r'class="[^"]*rounded-full[^"]*transition-all[^"]*"', replace_button_class, content)

    # For adding the login link
    if 'Already have an account' not in content:
        login_html = '''
                    <div class="mt-4 text-center pb-2">
                        <span class="text-[14px] font-medium text-gray-500">Already have an account?</span>
                        <a href="{{ url_for('patient_login') }}" class="text-[14px] font-bold text-[#2563EB] hover:text-blue-800 transition-colors ml-1">Sign In</a>
                    </div>
                </form>'''
        content = re.sub(r'</form>', login_html, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {filepath}")

files = glob.glob('f:/projects/medi-bid/templates/patient-registration-step*.html')
for f in files:
    if 'step1.html' not in f:
        fix_buttons(f)
