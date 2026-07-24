import re

# Fix patient-message-thread.html
with open('templates/patient-message-thread.html', 'r', encoding='utf-8') as f:
    patient_html = f.read()

# 1. Remove duplicated composer
# It starts at: <!-- Composer Area (Sticky Bottom) --> and ends at </main>
patient_html = re.sub(r'<!-- Composer Area \(Sticky Bottom\).*?</main>', '', patient_html, flags=re.DOTALL)

# 2. Add id to message container
# <div class="flex-grow overflow-y-auto custom-scrollbar p-4 sm:p-6 flex flex-col relative z-10 space-y-4">
patient_html = patient_html.replace(
    '<div class="flex-grow overflow-y-auto custom-scrollbar p-4 sm:p-6 flex flex-col relative z-10 space-y-4">',
    '<div id="message-history-container" class="flex-grow overflow-y-auto custom-scrollbar p-4 sm:p-6 flex flex-col relative z-10 space-y-4">'
)

# 3. Update the script
script_replacement = '''
const chatContainer = document.getElementById('message-history-container');
if (chatContainer) {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
'''
patient_html = re.sub(
    r'const chatContainer = document\.querySelector\(\'\.overflow-y-auto\.custom-scrollbar\'\);\s*if \(chatContainer\) \{\s*chatContainer\.scrollTop = chatContainer\.scrollHeight;\s*\}',
    script_replacement.strip(),
    patient_html
)

with open('templates/patient-message-thread.html', 'w', encoding='utf-8') as f:
    f.write(patient_html)

# Fix hospital-message-thread.html
with open('templates/hospital-message-thread.html', 'r', encoding='utf-8') as f:
    hospital_html = f.read()

# 1. Add id to message container
# <div class="flex-1 overflow-y-auto custom-scrollbar p-6 bg-bgLight flex flex-col space-y-4">
hospital_html = hospital_html.replace(
    '<div class="flex-1 overflow-y-auto custom-scrollbar p-6 bg-bgLight flex flex-col space-y-4">',
    '<div id="message-history-container" class="flex-1 overflow-y-auto custom-scrollbar p-6 bg-bgLight flex flex-col space-y-4">'
)

# 2. Update the script
hospital_html = re.sub(
    r'const chatContainer = document\.querySelector\(\'\.overflow-y-auto\.custom-scrollbar\'\);\s*if \(chatContainer\) \{\s*chatContainer\.scrollTop = chatContainer\.scrollHeight;\s*\}',
    script_replacement.strip(),
    hospital_html
)

with open('templates/hospital-message-thread.html', 'w', encoding='utf-8') as f:
    f.write(hospital_html)

print("Fixed scroll scripts and containers in both templates.")
