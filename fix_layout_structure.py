with open('original_dashboard.html', 'r', encoding='utf-16') as f:
    orig = f.read()

# Get everything up to <!-- DASHBOARD MAIN CONTENT -->
top = orig.split('<!-- DASHBOARD MAIN CONTENT -->')[0]

# Add the <main> tag that was stripped earlier, it was on the very next line in orig
main_tag = '<main class="flex-grow p-4 sm:p-6 lg:p-8 flex flex-col gap-8 max-w-[1400px] w-full mx-auto">'
top = top + '\n' + main_tag + '\n' + '    {% block content %}{% endblock %}\n'

# Replace the title
import re
top = re.sub(r'<title>.*?</title>', '<title>{% block title %}Patient Dashboard | MediBid{% endblock %}</title>', top)

# Inject page_styles
top = top.replace('</title>', '</title>\n    {% block page_styles %}{% endblock %}')

# Update log out link
old_logout = '<button disabled class="w-full flex items-center gap-3 px-4 py-2.5 text-[14px] font-medium text-gray-400 bg-transparent cursor-not-allowed transition-colors text-left"><i data-lucide="log-out" class="w-4 h-4"></i> Log Out</button>'
new_logout = '<a href="{{ url_for(\'patient_logout\') }}" class="flex items-center gap-2.5 px-4 py-2.5 text-[14px] font-semibold text-red-600 hover:bg-red-50 transition-colors w-full text-left"><i data-lucide="log-out" class="w-4 h-4"></i> Log Out</a>'
top = top.replace(old_logout, new_logout)
# Also fix sidebar logout link
old_sidebar_logout = '<button disabled class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-textMain font-semibold text-[15px] opacity-50 cursor-not-allowed transition-all text-left">'
new_sidebar_logout = '<a href="{{ url_for(\'patient_logout\') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-red-600 font-semibold text-[15px] hover:bg-red-50 transition-all w-full text-left">'
top = top.replace(old_sidebar_logout, new_sidebar_logout)

# Re-apply user safe checks
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
top = top.replace(old_btn, new_btn)
top = top.replace(old_dropdown, new_dropdown)


# Get everything from <!-- FOOTER --> to the end from orig
footer_parts = orig.split('<!-- FOOTER -->')
bottom = '<!-- FOOTER -->' + footer_parts[1]

# Inject block page_scripts
bottom = bottom.replace('</body>', '    {% block page_scripts %}{% endblock %}\n</body>')

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(top + '\n' + bottom)

print("patient-layout.html structure perfectly restored!")
