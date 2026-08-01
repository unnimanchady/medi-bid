import re

with open('templates/hospital-layout.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Desktop and Mobile both have identical nav anchors. We can just replace the specific links.

dashboard_orig = '''<a href="{{ url_for('hospital_dashboard') }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl bg-active-hospital text-white font-bold shadow-sm">
                <i data-lucide="layout-dashboard" class="w-5 h-5 text-white"></i> Dashboard
            </a>'''
dashboard_new = '''<a href="{{ url_for('hospital_dashboard') }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl {% if active_page == 'dashboard' %}bg-active-hospital text-white font-bold shadow-sm{% else %}text-white/80 hover:text-white hover-hospital font-medium transition-all group{% endif %}">
                <i data-lucide="layout-dashboard" class="w-5 h-5 {% if active_page == 'dashboard' %}text-white{% else %}group-hover:text-white transition-colors text-white/80{% endif %}"></i> Dashboard
            </a>'''

requests_orig = '''<a href="{{ url_for('hospital_treatment_requests') if hospital.verification_status == 'verified' else '#' }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl text-white/80 hover:text-white hover-hospital font-medium transition-all group {{ 'opacity-50 cursor-not-allowed' if hospital.verification_status != 'verified' else '' }}">
                <i data-lucide="file-text" class="w-5 h-5 group-hover:text-white transition-colors text-white/80"></i> Treatment Requests
            </a>'''
requests_new = '''<a href="{{ url_for('hospital_treatment_requests') if hospital.verification_status == 'verified' else '#' }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl {% if active_page == 'requests' %}bg-active-hospital text-white font-bold shadow-sm{% else %}text-white/80 hover:text-white hover-hospital font-medium transition-all group{% endif %} {{ 'opacity-50 cursor-not-allowed' if hospital.verification_status != 'verified' else '' }}">
                <i data-lucide="file-text" class="w-5 h-5 {% if active_page == 'requests' %}text-white{% else %}group-hover:text-white transition-colors text-white/80{% endif %}"></i> Treatment Requests
            </a>'''

proposals_orig = '''<a href="{{ url_for('hospital_proposals') }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl text-white/80 hover:text-white hover-hospital font-medium transition-all group">
                <i data-lucide="file-text" class="w-5 h-5 group-hover:text-white transition-colors text-white/80"></i> Proposals
            </a>'''
proposals_new = '''<a href="{{ url_for('hospital_proposals') }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl {% if active_page == 'proposals' %}bg-active-hospital text-white font-bold shadow-sm{% else %}text-white/80 hover:text-white hover-hospital font-medium transition-all group{% endif %}">
                <i data-lucide="file-text" class="w-5 h-5 {% if active_page == 'proposals' %}text-white{% else %}group-hover:text-white transition-colors text-white/80{% endif %}"></i> Proposals
            </a>'''

messages_orig = '''<a href="{{ url_for('hospital_messages') }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl text-white/80 hover:text-white hover-hospital font-medium transition-all group">
                <i data-lucide="message-square" class="w-5 h-5 group-hover:text-white transition-colors text-white/80"></i> Messages
            </a>'''
messages_new = '''<a href="{{ url_for('hospital_messages') }}" class="flex items-center gap-3 px-4 py-3.5 rounded-xl {% if active_page == 'messages' %}bg-active-hospital text-white font-bold shadow-sm{% else %}text-white/80 hover:text-white hover-hospital font-medium transition-all group{% endif %}">
                <i data-lucide="message-square" class="w-5 h-5 {% if active_page == 'messages' %}text-white{% else %}group-hover:text-white transition-colors text-white/80{% endif %}"></i> Messages
            </a>'''

profile_orig = '''<button disabled class="w-full flex items-center justify-between px-4 py-3.5 rounded-xl text-white/50 hover:text-white/60 bg-transparent hover:bg-white/5 transition-all cursor-not-allowed group text-left">
                <div class="flex items-center gap-3 font-medium">
                    <i data-lucide="building" class="w-5 h-5"></i> Hospital Profile
                </div>
                <span class="text-[10px] font-extrabold bg-white/20 text-white px-2 py-0.5 rounded-md uppercase">Soon</span>
            </button>'''
profile_new = '''<a href="#" class="w-full flex items-center justify-between px-4 py-3.5 rounded-xl {% if active_page == 'profile' %}bg-active-hospital text-white font-bold shadow-sm{% else %}text-white/80 hover:text-white hover-hospital font-medium transition-all group{% endif %} text-left">
                <div class="flex items-center gap-3">
                    <i data-lucide="building" class="w-5 h-5 {% if active_page == 'profile' %}text-white{% else %}group-hover:text-white transition-colors text-white/80{% endif %}"></i> Hospital Profile
                </div>
            </a>'''

notifications_orig = '''<button disabled class="w-full flex items-center justify-between px-4 py-3.5 rounded-xl text-white/50 hover:text-white/60 bg-transparent hover:bg-white/5 transition-all cursor-not-allowed group text-left">
                <div class="flex items-center gap-3 font-medium">
                    <i data-lucide="bell" class="w-5 h-5"></i> Notifications
                </div>
                <span class="text-[10px] font-extrabold bg-white/20 text-white px-2 py-0.5 rounded-md uppercase">Soon</span>
            </button>'''
notifications_new = '''<a href="#" class="w-full flex items-center justify-between px-4 py-3.5 rounded-xl {% if active_page == 'notifications' %}bg-active-hospital text-white font-bold shadow-sm{% else %}text-white/80 hover:text-white hover-hospital font-medium transition-all group{% endif %} text-left">
                <div class="flex items-center gap-3">
                    <i data-lucide="bell" class="w-5 h-5 {% if active_page == 'notifications' %}text-white{% else %}group-hover:text-white transition-colors text-white/80{% endif %}"></i> Notifications
                </div>
            </a>'''

settings_orig = '''<button disabled class="w-full flex items-center justify-between px-4 py-3.5 rounded-xl text-white/50 hover:text-white/60 bg-transparent hover:bg-white/5 transition-all cursor-not-allowed group text-left">
                <div class="flex items-center gap-3 font-medium">
                    <i data-lucide="settings" class="w-5 h-5"></i> Account & Settings
                </div>
                <span class="text-[10px] font-extrabold bg-white/20 text-white px-2 py-0.5 rounded-md uppercase">Soon</span>
            </button>'''
settings_new = '''<a href="#" class="w-full flex items-center justify-between px-4 py-3.5 rounded-xl {% if active_page == 'settings' %}bg-active-hospital text-white font-bold shadow-sm{% else %}text-white/80 hover:text-white hover-hospital font-medium transition-all group{% endif %} text-left">
                <div class="flex items-center gap-3">
                    <i data-lucide="settings" class="w-5 h-5 {% if active_page == 'settings' %}text-white{% else %}group-hover:text-white transition-colors text-white/80{% endif %}"></i> Account & Settings
                </div>
            </a>'''

content = content.replace(dashboard_orig, dashboard_new)
content = content.replace(requests_orig, requests_new)
content = content.replace(proposals_orig, proposals_new)
content = content.replace(messages_orig, messages_new)
content = content.replace(profile_orig, profile_new)
content = content.replace(notifications_orig, notifications_new)
content = content.replace(settings_orig, settings_new)

with open('templates/hospital-layout.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("done")
