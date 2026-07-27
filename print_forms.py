import re

def extract_form(filepath):
    content = open(filepath, 'r', encoding='utf-8').read()
    match = re.search(r'<form[^>]*>.*?name="message_body".*?</form>', content, re.DOTALL)
    if match:
        print(filepath)
        print(match.group(0))
        print('-'*50)

extract_form('templates/patient-secure-messages.html')
extract_form('templates/hospital-message-thread.html')
