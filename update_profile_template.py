import os

file_path = 'templates/patient-profile-settings.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    
# Extract header and footer
header_part = content.split('<!-- MAIN CONTENT -->')[0]
footer_part = content.split('</main>')[1]

new_main = """
    <!-- MAIN CONTENT -->
    <main class="flex-grow w-full max-w-[1100px] mx-auto py-6 sm:py-8 px-4 sm:px-6 flex flex-col gap-6">
        <nav class="flex items-center text-[13px] text-textMuted font-medium truncate gap-2" aria-label="Breadcrumb">
            <a href="{{ url_for('patient_dashboard') }}" class="hover:text-primary transition-colors hidden sm:inline">Dashboard</a>
            <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300 hidden sm:inline"></i>
            <span class="text-textMain font-bold">Profile & Settings</span>
        </nav>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center mb-2">
            <div>
                <h1 class="text-[26px] sm:text-[30px] font-extrabold text-primary tracking-tight">Profile & Settings</h1>
                <p class="text-[14px] text-textMuted mt-1">Manage your account information, linked profiles, and security.</p>
            </div>
            
            {% set fields_filled = 0 %}
            {% if user.first_name %}{% set fields_filled = fields_filled + 1 %}{% endif %}
            {% if user.last_name %}{% set fields_filled = fields_filled + 1 %}{% endif %}
            {% if user.email %}{% set fields_filled = fields_filled + 1 %}{% endif %}
            {% if user.phone %}{% set fields_filled = fields_filled + 1 %}{% endif %}
            {% if user.country_of_residence %}{% set fields_filled = fields_filled + 1 %}{% endif %}
            {% if user.preferred_language %}{% set fields_filled = fields_filled + 1 %}{% endif %}
            {% set completion = (fields_filled / 6 * 100) | int %}
            
            <div class="bg-white px-5 py-3 rounded-2xl border border-gray-100 shadow-sm flex flex-col gap-2 min-w-[200px]">
                <div class="flex justify-between items-center text-[13px] font-bold">
                    <span class="text-textMuted">Profile Completion</span>
                    <span class="text-secondary">{{ completion }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-2">
                    <div class="bg-secondary h-2 rounded-full transition-all duration-1000" style="width: {{ completion }}%"></div>
                </div>
            </div>
        </div>
        
        <!-- FLash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="p-4 rounded-xl text-[14px] font-bold {% if category == 'error' %}bg-red-50 text-red-600{% else %}bg-green-50 text-green-600{% endif %}">
                  {{ message }}
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <div class="flex flex-col md:flex-row gap-8">
            <!-- TABS SIDEBAR -->
            <aside class="w-full md:w-64 flex-shrink-0">
                <div class="bg-white rounded-[20px] p-2 border border-gray-100 shadow-sm flex flex-row md:flex-col gap-1 overflow-x-auto custom-scrollbar sticky top-[100px]">
                    <button onclick="switchTab('tab-profile')" id="btn-tab-profile" class="tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-[14px] transition-colors bg-softBlue text-secondary whitespace-nowrap">
                        <i data-lucide="user" class="w-4 h-4"></i> Account Profile
                    </button>
                    <button onclick="switchTab('tab-patients')" id="btn-tab-patients" class="tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-[14px] text-textMuted hover:bg-gray-50 hover:text-primary transition-colors whitespace-nowrap">
                        <i data-lucide="users" class="w-4 h-4"></i> Patient Profiles
                    </button>
                    <button onclick="switchTab('tab-notifications')" id="btn-tab-notifications" class="tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-[14px] text-textMuted hover:bg-gray-50 hover:text-primary transition-colors whitespace-nowrap">
                        <i data-lucide="bell" class="w-4 h-4"></i> Notifications
                    </button>
                    <button onclick="switchTab('tab-security')" id="btn-tab-security" class="tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-[14px] text-textMuted hover:bg-gray-50 hover:text-primary transition-colors whitespace-nowrap">
                        <i data-lucide="shield" class="w-4 h-4"></i> Security
                    </button>
                </div>
            </aside>
            
            <!-- TABS CONTENT -->
            <div class="flex-grow w-full min-w-0">
                
                <!-- TAB: ACCOUNT PROFILE -->
                <div id="tab-profile" class="tab-content block animate-fade-in">
                    <form method="POST" action="{{ url_for('patient_profile_settings') }}" class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8 flex flex-col gap-6">
                        <h2 class="text-[20px] font-extrabold text-primary mb-2">Account Information</h2>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">First Name</label>
                                <input type="text" name="first_name" value="{{ user.first_name }}" required class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Last Name</label>
                                <input type="text" name="last_name" value="{{ user.last_name }}" required class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>
                            
                            <div class="flex flex-col gap-2 sm:col-span-2">
                                <label class="text-[13px] font-bold text-textMain">Email Address <span class="text-[11px] text-textMuted font-normal ml-2">(Read-only)</span></label>
                                <input type="email" value="{{ user.email }}" disabled class="w-full border border-gray-200 bg-gray-100 text-gray-500 cursor-not-allowed rounded-xl px-4 py-3 text-[14px]">
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Mobile Number</label>
                                <input type="text" name="phone" value="{{ user.phone or '' }}" class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Country of Residence</label>
                                <input type="text" name="residence" value="{{ user.country_of_residence }}" required class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Preferred Language</label>
                                <select name="language" class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all appearance-none">
                                    <option value="English" {% if user.preferred_language == 'English' %}selected{% endif %}>English</option>
                                    <option value="Spanish" {% if user.preferred_language == 'Spanish' %}selected{% endif %}>Spanish</option>
                                    <option value="French" {% if user.preferred_language == 'French' %}selected{% endif %}>French</option>
                                    <option value="German" {% if user.preferred_language == 'German' %}selected{% endif %}>German</option>
                                    <option value="Arabic" {% if user.preferred_language == 'Arabic' %}selected{% endif %}>Arabic</option>
                                </select>
                            </div>
                            
                            {% if self_profile %}
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Date of Birth <span class="text-[11px] text-textMuted font-normal ml-2">(Fetched from 'Self' profile)</span></label>
                                <input type="text" value="{{ self_profile.date_of_birth.strftime('%b %d, %Y') if self_profile.date_of_birth else 'Not Set' }}" disabled class="w-full border border-gray-200 bg-gray-100 text-gray-500 cursor-not-allowed rounded-xl px-4 py-3 text-[14px]">
                            </div>
                            {% endif %}
                        </div>
                        
                        <div class="mt-4 pt-6 border-t border-gray-100 flex justify-end">
                            <button type="submit" class="bg-secondary text-white font-bold px-8 py-3 rounded-xl hover:bg-blue-600 transition-colors shadow-sm flex items-center gap-2">
                                <i data-lucide="save" class="w-4 h-4"></i> Save Changes
                            </button>
                        </div>
                    </form>
                </div>
                
                <!-- TAB: PATIENT PROFILES -->
                <div id="tab-patients" class="tab-content hidden animate-fade-in">
                    <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8 flex flex-col gap-6">
                        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-2">
                            <h2 class="text-[20px] font-extrabold text-primary">Linked Patient Profiles</h2>
                            <a href="{{ url_for('patient_profile_add') }}" class="bg-softBlue text-secondary font-bold px-5 py-2.5 rounded-xl hover:bg-blue-100 transition-colors shadow-sm flex items-center gap-2 text-[14px] self-start sm:self-auto">
                                <i data-lucide="plus" class="w-4 h-4"></i> Add New Profile
                            </a>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {% for profile in profiles %}
                            <div class="border border-gray-200 rounded-2xl p-5 hover:border-secondary transition-colors relative flex flex-col gap-3 group">
                                <div class="flex items-start justify-between gap-2">
                                    <div>
                                        <h3 class="text-[16px] font-bold text-textMain">{{ profile.first_name|title }} {{ profile.last_name|title }}</h3>
                                        <p class="text-[13px] text-gray-500 mt-1">Born: {{ profile.date_of_birth.strftime('%b %d, %Y') if profile.date_of_birth else 'N/A' }} | {{ profile.gender|title }}</p>
                                    </div>
                                    <span class="bg-blue-50 text-secondary text-[12px] font-bold px-2.5 py-1 rounded-md">{{ profile.relationship_type }}</span>
                                </div>
                                
                                <div class="mt-3 pt-3 border-t border-gray-100 flex gap-2">
                                    <a href="{{ url_for('patient_profile_edit', profile_id=profile.id) }}" class="flex-1 text-[13px] font-bold text-secondary bg-softBlue hover:bg-blue-100 px-4 py-2 rounded-lg transition-colors text-center flex items-center justify-center gap-2"><i data-lucide="edit-2" class="w-3.5 h-3.5"></i> Edit</a>
                                    
                                    {% if profile.relationship_type != 'Self' %}
                                    <form method="POST" action="{{ url_for('patient_profile_delete', profile_id=profile.id) }}" class="flex-1" onsubmit="return confirm('Are you sure you want to delete this profile?');">
                                        <button type="submit" class="w-full text-[13px] font-bold text-red-600 bg-red-50 hover:bg-red-100 px-4 py-2 rounded-lg transition-colors text-center flex items-center justify-center gap-2"><i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Delete</button>
                                    </form>
                                    {% endif %}
                                </div>
                            </div>
                            {% else %}
                            <div class="col-span-full py-8 text-center bg-gray-50 rounded-2xl border border-gray-100">
                                <p class="text-[14px] text-gray-500">No patient profiles linked yet.</p>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>

                <!-- TAB: NOTIFICATIONS -->
                <div id="tab-notifications" class="tab-content hidden animate-fade-in">
                    <form method="POST" action="{{ url_for('patient_settings_notifications') }}" class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8 flex flex-col gap-6">
                        <h2 class="text-[20px] font-extrabold text-primary mb-2">Notification Preferences</h2>
                        
                        <div class="flex flex-col gap-4">
                            <label class="flex items-center justify-between p-4 border border-gray-100 rounded-2xl cursor-pointer hover:bg-gray-50 transition-colors">
                                <div class="flex flex-col gap-1">
                                    <span class="text-[15px] font-bold text-textMain flex items-center gap-2"><i data-lucide="mail" class="w-4 h-4 text-secondary"></i> Email Notifications</span>
                                    <span class="text-[13px] text-textMuted">Receive updates about proposals and messages via email.</span>
                                </div>
                                <div class="relative inline-block w-12 h-6 rounded-full bg-gray-200">
                                    <input type="checkbox" name="notify_email" class="peer sr-only" {% if user.notify_email %}checked{% endif %}>
                                    <span class="absolute inset-y-0 left-0 w-6 h-6 bg-white border border-gray-300 rounded-full shadow transition-transform peer-checked:translate-x-6 peer-checked:bg-secondary peer-checked:border-secondary"></span>
                                </div>
                            </label>

                            <label class="flex items-center justify-between p-4 border border-gray-100 rounded-2xl cursor-pointer hover:bg-gray-50 transition-colors">
                                <div class="flex flex-col gap-1">
                                    <span class="text-[15px] font-bold text-textMain flex items-center gap-2"><i data-lucide="bell" class="w-4 h-4 text-secondary"></i> In-App Notifications</span>
                                    <span class="text-[13px] text-textMuted">Receive alerts within the MediBid portal.</span>
                                </div>
                                <div class="relative inline-block w-12 h-6 rounded-full bg-gray-200">
                                    <input type="checkbox" name="notify_in_app" class="peer sr-only" {% if user.notify_in_app %}checked{% endif %}>
                                    <span class="absolute inset-y-0 left-0 w-6 h-6 bg-white border border-gray-300 rounded-full shadow transition-transform peer-checked:translate-x-6 peer-checked:bg-secondary peer-checked:border-secondary"></span>
                                </div>
                            </label>
                        </div>
                        
                        <div class="mt-4 pt-6 border-t border-gray-100 flex justify-end">
                            <button type="submit" class="bg-secondary text-white font-bold px-8 py-3 rounded-xl hover:bg-blue-600 transition-colors shadow-sm flex items-center gap-2">
                                <i data-lucide="save" class="w-4 h-4"></i> Save Preferences
                            </button>
                        </div>
                    </form>
                </div>

                <!-- TAB: SECURITY -->
                <div id="tab-security" class="tab-content hidden animate-fade-in">
                    <form method="POST" action="{{ url_for('patient_settings_security') }}" class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8 flex flex-col gap-6">
                        <h2 class="text-[20px] font-extrabold text-primary mb-2">Change Password</h2>
                        
                        <div class="grid grid-cols-1 gap-6 max-w-lg">
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Current Password</label>
                                <input type="password" name="current_password" required class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">New Password</label>
                                <input type="password" name="new_password" required minlength="6" class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>

                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Confirm New Password</label>
                                <input type="password" name="confirm_password" required minlength="6" class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>
                        </div>
                        
                        <div class="mt-4 pt-6 border-t border-gray-100 flex justify-start">
                            <button type="submit" class="bg-primary text-white font-bold px-8 py-3 rounded-xl hover:bg-blue-900 transition-colors shadow-sm flex items-center gap-2">
                                <i data-lucide="shield-check" class="w-4 h-4"></i> Update Password
                            </button>
                        </div>
                    </form>
                </div>
                
            </div>
        </div>
    </main>
    
    <script>
        function switchTab(tabId) {
            // Hide all contents
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('block'));
            
            // Show target content
            document.getElementById(tabId).classList.remove('hidden');
            document.getElementById(tabId).classList.add('block');
            
            // Reset all buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.className = 'tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-[14px] text-textMuted hover:bg-gray-50 hover:text-primary transition-colors whitespace-nowrap';
            });
            
            // Highlight active button
            const activeBtn = document.getElementById('btn-' + tabId);
            activeBtn.className = 'tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-[14px] transition-colors bg-softBlue text-secondary whitespace-nowrap';
            
            // Update URL hash without jumping
            history.pushState(null, null, '#' + tabId.replace('tab-', ''));
        }
        
        // Handle direct links to tabs
        document.addEventListener('DOMContentLoaded', () => {
            const hash = window.location.hash;
            if (hash && ['#profile', '#patients', '#notifications', '#security'].includes(hash)) {
                switchTab('tab-' + hash.replace('#', ''));
            }
        });
    </script>
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(header_part + new_main + footer_part)

print("Updated templates/patient-profile-settings.html")
