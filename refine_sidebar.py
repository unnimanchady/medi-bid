import re

with open('templates/hospital-layout.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Desktop Primary Contact & Log Out
desktop_contact = r'<!-- Primary Contact & Log Out -->.*?</div>\s*<!-- Navigation Links -->'
content = re.sub(desktop_contact, '<!-- Navigation Links -->', content, flags=re.DOTALL)

# 2. Remove Mobile Primary Contact & Log Out
mobile_contact = r'<!-- Primary Contact & Log Out \(Mobile\) -->.*?</div>\s*<!-- Drawer Navigation Links \(Mobile\) -->'
content = re.sub(mobile_contact, '<!-- Drawer Navigation Links (Mobile) -->', content, flags=re.DOTALL)

# 3. Remove Hospital Profile, Notifications, Account & Settings from Desktop Nav
# Actually, the user didn't mention removing Notifications from the sidebar, but they said "Make the sidebar navigation-focused while keeping all account-related actions exclusively in the top-right profile dropdown".
# Let's see what the sidebar currently has: Dashboard, Treatment Requests, Proposals, Messages, h-px divider, Hospital Profile, Notifications, Account & Settings.
# The user wants dropdown to have: User avatar, Administrator name, Email address, Hospital Profile, Account & Settings, Log Out.
# Notice they didn't say Notifications for the dropdown. So I will keep Notifications in the sidebar, or just remove Profile and Settings from sidebar.
# Wait, let's just remove Profile and Settings from the sidebar.

profile_desktop = r'<a href="#" class="w-full flex items-center justify-between px-4 py-3\.5 rounded-xl \{% if active_page == \'profile\' %\}bg-active-hospital text-white font-bold shadow-sm\{% else %\}text-white/80 hover:text-white hover-hospital font-medium transition-all group\{% endif %\} text-left">\s*<div class="flex items-center gap-3">\s*<i data-lucide="building" class="w-5 h-5 \{% if active_page == \'profile\' %\}text-white\{% else %\}group-hover:text-white transition-colors text-white/80\{% endif %\}"></i> Hospital Profile\s*</div>\s*</a>'
settings_desktop = r'<a href="#" class="w-full flex items-center justify-between px-4 py-3\.5 rounded-xl \{% if active_page == \'settings\' %\}bg-active-hospital text-white font-bold shadow-sm\{% else %\}text-white/80 hover:text-white hover-hospital font-medium transition-all group\{% endif %\} text-left">\s*<div class="flex items-center gap-3">\s*<i data-lucide="settings" class="w-5 h-5 \{% if active_page == \'settings\' %\}text-white\{% else %\}group-hover:text-white transition-colors text-white/80\{% endif %\}"></i> Account & Settings\s*</div>\s*</a>'

content = re.sub(profile_desktop, '', content)
content = re.sub(settings_desktop, '', content)

# 4. Modify Dropdown
dropdown_orig = '''<div class="h-[1px] bg-gray-100 my-1"></div>
                        <a href="{{ url_for('hospital_logout') }}" class="flex items-center gap-2.5 px-4 py-2.5 text-[14px] font-semibold text-red-600 hover:bg-red-50 transition-colors w-full text-left"><i data-lucide="log-out" class="w-4 h-4"></i> Log Out</a>'''

dropdown_new = '''<div class="h-[1px] bg-gray-100 my-1"></div>
                        <a href="#" class="flex items-center gap-2.5 px-4 py-2.5 text-[14px] font-semibold text-textMain hover:bg-gray-50 transition-colors w-full text-left"><i data-lucide="building" class="w-4 h-4 text-textMuted"></i> Hospital Profile</a>
                        <a href="#" class="flex items-center gap-2.5 px-4 py-2.5 text-[14px] font-semibold text-textMain hover:bg-gray-50 transition-colors w-full text-left"><i data-lucide="settings" class="w-4 h-4 text-textMuted"></i> Account & Settings</a>
                        <div class="h-[1px] bg-gray-100 my-1"></div>
                        <a href="{{ url_for('hospital_logout') }}" class="flex items-center gap-2.5 px-4 py-2.5 text-[14px] font-semibold text-red-600 hover:bg-red-50 transition-colors w-full text-left"><i data-lucide="log-out" class="w-4 h-4"></i> Log Out</a>'''

content = content.replace(dropdown_orig, dropdown_new)

with open('templates/hospital-layout.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("done")
