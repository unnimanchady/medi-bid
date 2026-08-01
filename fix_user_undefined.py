import re

with open('templates/hospital-layout.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace user.first_name with admin.first_name, etc.
# But first, we need to inject {% set admin = hospital.users[0] if hospital.users else None %} at the top of the header if we are using it.
# Actually, the user says: "Remove all sidebar account-related UI that depends on 'user', including: Primary Contact, Avatar initials, User name, User email, Log Out button."
# I already removed that in the previous step. Wait, did I? Yes, I removed it from the sidebar.
# The remaining 'user' references are in the header dropdown.

dropdown_orig = '''<div class="relative">
                    <button id="profile-btn" class="flex items-center gap-2.5 focus:outline-none hover:bg-gray-50 p-1.5 sm:pr-3 rounded-full transition-colors border border-transparent hover:border-gray-200">
                        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-orange-50 border border-orange-100 flex items-center justify-center text-[#C2410C] font-extrabold text-[12px] sm:text-[13px] uppercase shadow-sm">
                            {{ user.first_name[0]|title}}{{ user.last_name[0]|title}}
                        </div>
                        <div class="hidden sm:flex flex-col text-left">
                            <span class="text-[13px] font-bold text-textMain leading-none">{{ user.first_name|title}}</span>
                        </div>
                        <i data-lucide="chevron-down" class="w-4 h-4 text-textMuted hidden sm:block"></i>
                    </button>
                    
                    <div id="profile-dropdown" class="absolute right-0 top-[110%] w-64 bg-white border border-gray-100 rounded-2xl shadow-dropdown z-50 py-2">
                        <div class="px-4 py-3 border-b border-gray-50 mb-1 flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-[#C2410C] flex items-center justify-center text-white font-extrabold text-[14px] uppercase shadow-sm">
                                {{ user.first_name[0]|title}}{{ user.last_name[0]|title}}
                            </div>
                            <div class="flex flex-col min-w-0">
                                <p class="text-[14px] font-bold text-textMain truncate">{{ user.first_name|title}} {{ user.last_name|title}}</p>
                                <p class="text-[12px] text-textMuted truncate">{{ user.email }}</p>
                            </div>
                        </div>'''

dropdown_new = '''<div class="relative">
                    {% set admin = hospital.users[0] if hospital.users else None %}
                    <button id="profile-btn" class="flex items-center gap-2.5 focus:outline-none hover:bg-gray-50 p-1.5 sm:pr-3 rounded-full transition-colors border border-transparent hover:border-gray-200">
                        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-orange-50 border border-orange-100 flex items-center justify-center text-[#C2410C] font-extrabold text-[12px] sm:text-[13px] uppercase shadow-sm">
                            {% if admin %}{{ admin.first_name[0]|title }}{{ admin.last_name[0]|title }}{% else %}A{% endif %}
                        </div>
                        <div class="hidden sm:flex flex-col text-left">
                            <span class="text-[13px] font-bold text-textMain leading-none">{% if admin %}{{ admin.first_name|title }}{% else %}Admin{% endif %}</span>
                        </div>
                        <i data-lucide="chevron-down" class="w-4 h-4 text-textMuted hidden sm:block"></i>
                    </button>
                    
                    <div id="profile-dropdown" class="absolute right-0 top-[110%] w-64 bg-white border border-gray-100 rounded-2xl shadow-dropdown z-50 py-2">
                        <div class="px-4 py-3 border-b border-gray-50 mb-1 flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-[#C2410C] flex items-center justify-center text-white font-extrabold text-[14px] uppercase shadow-sm">
                                {% if admin %}{{ admin.first_name[0]|title }}{{ admin.last_name[0]|title }}{% else %}A{% endif %}
                            </div>
                            <div class="flex flex-col min-w-0">
                                <p class="text-[14px] font-bold text-textMain truncate">{% if admin %}{{ admin.first_name|title }} {{ admin.last_name|title }}{% else %}Administrator{% endif %}</p>
                                <p class="text-[12px] text-textMuted truncate">{% if admin %}{{ admin.work_email }}{% endif %}</p>
                            </div>
                        </div>'''

content = content.replace(dropdown_orig, dropdown_new)

with open('templates/hospital-layout.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("done")
