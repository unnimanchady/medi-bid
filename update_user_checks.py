import os

with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_btn = """                    <button id="profile-btn" class="flex items-center gap-2.5 focus:outline-none hover:bg-gray-50 p-1.5 sm:pr-3 rounded-full transition-colors border border-transparent hover:border-gray-200">
                        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-softBlue border border-blue-100 flex items-center justify-center text-secondary font-extrabold text-[12px] sm:text-[13px] uppercase shadow-sm">
                            {{ user.first_name[0]|title}}{{ user.last_name[0]|title}}
                        </div>
                        <div class="hidden sm:flex flex-col text-left">
                            <span class="text-[13px] font-bold text-textMain leading-none">{{ user.first_name|title}}</span>
                        </div>
                        <i data-lucide="chevron-down" class="w-4 h-4 text-textMuted hidden sm:block"></i>
                    </button>"""

new_btn = """                    <button id="profile-btn" class="flex items-center gap-2.5 focus:outline-none hover:bg-gray-50 p-1.5 sm:pr-3 rounded-full transition-colors border border-transparent hover:border-gray-200">
                        {% if user %}
                        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-softBlue border border-blue-100 flex items-center justify-center text-secondary font-extrabold text-[12px] sm:text-[13px] uppercase shadow-sm">
                            {{ user.first_name[0]|title}}{{ user.last_name[0]|title}}
                        </div>
                        <div class="hidden sm:flex flex-col text-left">
                            <span class="text-[13px] font-bold text-textMain leading-none">{{ user.first_name|title}}</span>
                        </div>
                        {% else %}
                        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-softBlue border border-blue-100 flex items-center justify-center text-secondary font-extrabold text-[12px] sm:text-[13px] uppercase shadow-sm">
                            G
                        </div>
                        <div class="hidden sm:flex flex-col text-left">
                            <span class="text-[13px] font-bold text-textMain leading-none">Guest</span>
                        </div>
                        {% endif %}
                        <i data-lucide="chevron-down" class="w-4 h-4 text-textMuted hidden sm:block"></i>
                    </button>"""
                    
old_dropdown = """                        <div class="px-4 py-3 border-b border-gray-50 mb-1 flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-extrabold text-[14px] uppercase shadow-sm">
                                {{ user.first_name[0]|title}}{{ user.last_name[0]|title}}
                            </div>
                            <div class="flex flex-col min-w-0">
                                <p class="text-[14px] font-bold text-textMain truncate">{{ user.first_name|title}} {{ user.last_name|title}}</p>
                                <p class="text-[12px] text-textMuted truncate">{{ user.email }}</p>
                            </div>
                        </div>"""

new_dropdown = """                        <div class="px-4 py-3 border-b border-gray-50 mb-1 flex items-center gap-3">
                            {% if user %}
                            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-extrabold text-[14px] uppercase shadow-sm">
                                {{ user.first_name[0]|title}}{{ user.last_name[0]|title}}
                            </div>
                            <div class="flex flex-col min-w-0">
                                <p class="text-[14px] font-bold text-textMain truncate">{{ user.first_name|title}} {{ user.last_name|title}}</p>
                                <p class="text-[12px] text-textMuted truncate">{{ user.email }}</p>
                            </div>
                            {% else %}
                            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-extrabold text-[14px] uppercase shadow-sm">
                                G
                            </div>
                            <div class="flex flex-col min-w-0">
                                <p class="text-[14px] font-bold text-textMain truncate">Guest User</p>
                                <p class="text-[12px] text-textMuted truncate">guest@medibid.com</p>
                            </div>
                            {% endif %}
                        </div>"""

content = content.replace(old_btn, new_btn)
content = content.replace(old_dropdown, new_dropdown)

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated patient-layout.html with safe user checks.")
