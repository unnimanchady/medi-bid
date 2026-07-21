import re

with open('templates/patient-profile-settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire <main> block
main_pattern = re.compile(r'<main.*?</main>', re.DOTALL)

new_main = """<main class="flex-grow w-full max-w-[1100px] mx-auto py-6 sm:py-8 px-4 sm:px-6 flex flex-col gap-6">
    <nav class="flex items-center text-[13px] text-textMuted font-medium truncate gap-2" aria-label="Breadcrumb">
        <a href="{{ url_for('patient_dashboard') }}" class="hover:text-primary transition-colors hidden sm:inline">Dashboard</a>
        <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300 hidden sm:inline"></i>
        <span class="text-textMain font-bold">Profile & Settings</span>
    </nav>
    <div class="flex flex-col gap-2 mb-2">
        <h1 class="text-[26px] sm:text-[30px] font-extrabold text-primary tracking-tight">Profile & Settings</h1>
        <p class="text-[14px] text-textMuted max-w-2xl">Manage your account information and linked patient profiles.</p>
    </div>
    
    <div class="flex flex-col gap-8">
        
        <!-- Account Contact Info -->
        <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8">
            <h2 class="text-[20px] font-extrabold text-primary mb-4">Account Contact Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-gray-50 border border-gray-100 p-5 rounded-2xl">
                    <label class="text-[12px] font-bold text-textMuted uppercase tracking-wider mb-2 block">Email Address</label>
                    <span class="text-[15.5px] font-medium text-textMain">{{ user.email }}</span>
                </div>
                <div class="bg-gray-50 border border-gray-100 p-5 rounded-2xl">
                    <label class="text-[12px] font-bold text-textMuted uppercase tracking-wider mb-2 block">Phone Number</label>
                    <span class="text-[15.5px] font-medium text-textMain">{{ user.phone }}</span>
                </div>
            </div>
        </div>
        
        <!-- Linked Patient Profiles -->
        <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8">
            <h2 class="text-[20px] font-extrabold text-primary mb-4">Linked Patient Profiles</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {% for profile in profiles %}
                <div class="border border-gray-200 rounded-2xl p-5 hover:border-secondary transition-colors relative flex flex-col gap-2">
                    <div class="flex items-center justify-between">
                        <h3 class="text-[16px] font-bold text-textMain">{{ profile.first_name|title }} {{ profile.last_name|title }}</h3>
                        <span class="bg-blue-50 text-secondary text-[12px] font-bold px-2 py-1 rounded-md">{{ profile.relationship_type }}</span>
                    </div>
                    <p class="text-[13px] text-gray-500">Born: {{ profile.date_of_birth.strftime('%b %d, %Y') if profile.date_of_birth else 'N/A' }} | Gender: {{ profile.gender|title }}</p>
                    <div class="mt-4 flex gap-3">
                        <a href="{{ url_for('patient_profile_edit', profile_id=profile.id) }}" class="text-[13px] font-bold text-white bg-secondary hover:bg-blue-600 px-4 py-2 rounded-lg transition-colors text-center w-full">Edit Profile</a>
                    </div>
                </div>
                {% else %}
                <p class="text-[14px] text-gray-500">No patient profiles linked yet.</p>
                {% endfor %}
            </div>
        </div>

    </div>
</main>"""

content = main_pattern.sub(new_main, content)

with open('templates/patient-profile-settings.html', 'w', encoding='utf-8') as f:
    f.write(content)
