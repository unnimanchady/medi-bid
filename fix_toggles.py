import re

def fix_patient_reg():
    with open('f:/projects/medi-bid/templates/patient-registration-step1.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix HTML aria-label
    content = content.replace('aria-label="Toggle password visibility"', 'aria-label="Show password"')

    # Fix JS
    js_target = "button.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');"
    if js_target not in content:
        content = content.replace(
            "button.setAttribute('aria-pressed', isPassword ? 'true' : 'false');",
            "button.setAttribute('aria-pressed', isPassword ? 'true' : 'false');\n            button.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');"
        )

    with open('f:/projects/medi-bid/templates/patient-registration-step1.html', 'w', encoding='utf-8') as f:
        f.write(content)


def fix_hospital_reg():
    with open('f:/projects/medi-bid/templates/hospital-registration-step1.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix HTML aria-label
    content = content.replace('data-target="password">', 'data-target="password" aria-label="Show password">')
    content = content.replace('data-target="confirm_password">', 'data-target="confirm_password" aria-label="Show password">')

    # The JS in hospital reg uses two icon elements instead of setting data-lucide
    # Let's inspect the JS first... Actually, I can just replace the JS using regex if needed, or let's look at the JS.
    pass

fix_patient_reg()
fix_hospital_reg()
