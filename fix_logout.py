import os
import glob

templates_dir = 'templates'
patient_files = glob.glob(os.path.join(templates_dir, 'patient-*.html'))

disabled_btn = '<button disabled class="w-full flex items-center gap-3 px-4 py-2.5 text-[14px] font-medium text-gray-400 bg-transparent cursor-not-allowed transition-colors text-left"><i data-lucide="log-out" class="w-4 h-4"></i> Log Out</button>'
hash_link = '<a href="#" class="flex items-center gap-2.5 px-4 py-2.5 text-[14px] font-semibold text-red-600 hover:bg-red-50 transition-colors"><i data-lucide="log-out" class="w-4 h-4"></i> Log Out</a>'
working_link = '<a href="{{ url_for(\'patient_logout\') }}" class="flex items-center gap-2.5 px-4 py-2.5 text-[14px] font-semibold text-red-600 hover:bg-red-50 transition-colors w-full text-left"><i data-lucide="log-out" class="w-4 h-4"></i> Log Out</a>'

for file_path in patient_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    modified = False
    
    if disabled_btn in content:
        content = content.replace(disabled_btn, working_link)
        modified = True
        
    if hash_link in content:
        content = content.replace(hash_link, working_link)
        modified = True
        
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed logout link in {file_path}')
        
print("Logout fixes complete.")
