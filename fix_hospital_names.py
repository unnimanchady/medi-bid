with open('templates/patient-compare-hospitals.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the titles
old_title_1 = '<h3 class="text-[15px] font-bold text-textMain leading-tight truncate" title="{{ item.hospital.name }}">{{ item.hospital.name }}</h3>'
new_title_1 = '<h3 class="text-[15px] font-bold text-textMain leading-tight truncate" title="{{ item.hospital.display_name or item.hospital.legal_name or \'Hospital name not available\' }}">{{ item.hospital.display_name or item.hospital.legal_name or \'Hospital name not available\' }}</h3>'
content = content.replace(old_title_1, new_title_1)

old_title_2 = '<div class="w-5 h-5 rounded {{ bg_colors[loop.index0 % 3] }} text-white flex items-center justify-center text-[10px] font-bold shadow-sm">{{ loop.index }}</div> {{ item.hospital.name }}'
new_title_2 = '<div class="w-5 h-5 rounded {{ bg_colors[loop.index0 % 3] }} text-white flex items-center justify-center text-[10px] font-bold shadow-sm">{{ loop.index }}</div> {{ item.hospital.display_name or item.hospital.legal_name or \'Hospital name not available\' }}'
content = content.replace(old_title_2, new_title_2)

with open('templates/patient-compare-hospitals.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated hospital names in patient-compare-hospitals.html")
