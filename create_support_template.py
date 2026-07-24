import os

source = 'templates/patient-profile-settings.html'
dest = 'templates/patient-support.html'

with open(source, 'r', encoding='utf-8') as f:
    content = f.read()
    
# We want the header and sidebar from patient-profile-settings.html, but the main content replaced.
# Let's extract everything before <!-- MAIN CONTENT AREA -->
header_part = content.split('<!-- MAIN CONTENT AREA -->')[0]

# And the footer part which is just closing tags.
footer_part = content.split('</main>')[1]

# However, patient-profile-settings.html has the main content block.
# Let's rebuild the main content block.

new_main = """
    <!-- MAIN CONTENT AREA -->
    <div class="flex-grow flex flex-col min-w-0 bg-bgLight relative">
        
        <!-- TOP HEADER -->
        <header class="bg-white border-b border-gray-200 h-[70px] lg:h-[80px] flex items-center justify-between px-4 sm:px-6 lg:px-8 sticky top-0 z-30 shadow-sm">
            <div class="flex items-center gap-4">
                <button id="mobile-menu-btn" class="p-2 -ml-2 text-textMuted hover:text-primary hover:bg-gray-50 rounded-xl md:hidden transition-colors">
                    <i data-lucide="menu" class="w-6 h-6"></i>
                </button>
                <h1 class="text-[20px] sm:text-[24px] font-extrabold text-primary tracking-tight hidden sm:block">Help & Support</h1>
                <h1 class="text-[20px] font-extrabold text-primary tracking-tight sm:hidden">Support</h1>
            </div>
            
            <div class="flex items-center gap-3 sm:gap-5">
                <div class="relative group">
                    <button class="p-2 sm:p-2.5 text-textMuted hover:text-primary hover:bg-gray-50 rounded-full transition-all relative">
                        <i data-lucide="bell" class="w-5 h-5 sm:w-6 sm:h-6"></i>
                        <span class="absolute top-1 sm:top-1.5 right-1 sm:right-1.5 w-2 sm:w-2.5 h-2 sm:w-2.5 bg-red-500 rounded-full border-2 border-white"></span>
                    </button>
                </div>
                
                <div class="h-8 w-px bg-gray-200 hidden sm:block"></div>
                
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 sm:w-11 sm:h-11 rounded-full bg-secondary/10 flex items-center justify-center border border-secondary/20 shadow-inner">
                        <span class="text-secondary font-bold text-[14px] sm:text-[16px]">{{ user.first_name[0] }}{{ user.last_name[0] }}</span>
                    </div>
                    <div class="hidden md:flex flex-col">
                        <span class="text-[14px] font-bold text-textMain leading-tight">{{ user.first_name }} {{ user.last_name }}</span>
                        <span class="text-[12px] text-textMuted font-medium">Patient</span>
                    </div>
                </div>
            </div>
        </header>

        <main class="flex-grow w-full max-w-[1100px] mx-auto py-6 sm:py-8 px-4 sm:px-6 flex flex-col gap-6">
            
            <nav class="flex items-center text-[13px] text-textMuted font-medium truncate gap-2" aria-label="Breadcrumb">
                <a href="{{ url_for('patient_dashboard') }}" class="hover:text-primary transition-colors hidden sm:inline">Dashboard</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300 hidden sm:inline"></i>
                <span class="text-textMain font-bold">Help & Support</span>
            </nav>
            
            <!-- EMERGENCY NOTICE -->
            <div class="bg-red-50 border border-red-200 rounded-[20px] p-5 shadow-sm flex items-start gap-4">
                <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0 text-red-600">
                    <i data-lucide="alert-triangle" class="w-5 h-5"></i>
                </div>
                <div>
                    <h3 class="text-[16px] font-extrabold text-red-800">MediBid is NOT an emergency medical service.</h3>
                    <p class="text-[14px] text-red-700 mt-1 font-medium">If you require emergency treatment, contact your local emergency services immediately.</p>
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

            <div class="flex flex-col md:flex-row gap-8 mt-2">
                <!-- TABS SIDEBAR -->
                <aside class="w-full md:w-64 flex-shrink-0">
                    <div class="bg-white rounded-[20px] p-2 border border-gray-100 shadow-sm flex flex-row md:flex-col gap-1 overflow-x-auto custom-scrollbar sticky top-[100px]">
                        <button onclick="switchTab('tab-faq')" id="btn-tab-faq" class="tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-[14px] transition-colors bg-softBlue text-secondary whitespace-nowrap">
                            <i data-lucide="help-circle" class="w-4 h-4"></i> Help Center
                        </button>
                        <button onclick="switchTab('tab-contact')" id="btn-tab-contact" class="tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-[14px] text-textMuted hover:bg-gray-50 hover:text-primary transition-colors whitespace-nowrap">
                            <i data-lucide="mail" class="w-4 h-4"></i> Contact Support
                        </button>
                        <button onclick="switchTab('tab-tickets')" id="btn-tab-tickets" class="tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-[14px] text-textMuted hover:bg-gray-50 hover:text-primary transition-colors whitespace-nowrap">
                            <i data-lucide="ticket" class="w-4 h-4"></i> My Tickets
                        </button>
                    </div>
                </aside>
                
                <!-- TABS CONTENT -->
                <div class="flex-grow w-full min-w-0">
                    
                    <!-- TAB: FAQ -->
                    <div id="tab-faq" class="tab-content block animate-fade-in">
                        <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8 flex flex-col gap-6">
                            <h2 class="text-[20px] font-extrabold text-primary mb-2">Frequently Asked Questions</h2>
                            
                            <div class="flex flex-col gap-4">
                                <!-- FAQ 1 -->
                                <div class="border border-gray-100 rounded-2xl overflow-hidden group">
                                    <button class="w-full text-left px-5 py-4 font-bold text-[15px] text-textMain bg-gray-50 group-hover:bg-softBlue transition-colors flex justify-between items-center" onclick="this.nextElementSibling.classList.toggle('hidden')">
                                        How MediBid Works
                                        <i data-lucide="chevron-down" class="w-4 h-4 text-textMuted"></i>
                                    </button>
                                    <div class="p-5 text-[14px] text-textMuted hidden bg-white">
                                        MediBid connects you directly with top hospitals worldwide. Simply submit a treatment request detailing your medical needs, and registered hospitals will securely review it and reply with comprehensive proposals. You can compare options and message hospitals directly.
                                    </div>
                                </div>
                                
                                <!-- FAQ 2 -->
                                <div class="border border-gray-100 rounded-2xl overflow-hidden group">
                                    <button class="w-full text-left px-5 py-4 font-bold text-[15px] text-textMain bg-gray-50 group-hover:bg-softBlue transition-colors flex justify-between items-center" onclick="this.nextElementSibling.classList.toggle('hidden')">
                                        How to upload medical reports
                                    </button>
                                    <div class="p-5 text-[14px] text-textMuted hidden bg-white">
                                        Navigate to the "Medical Documents" section from the sidebar. You can upload PDFs or image files (up to 10MB) related to your treatment requests. These are encrypted and shared securely.
                                    </div>
                                </div>
                                
                                <!-- FAQ 3 -->
                                <div class="border border-gray-100 rounded-2xl overflow-hidden group">
                                    <button class="w-full text-left px-5 py-4 font-bold text-[15px] text-textMain bg-gray-50 group-hover:bg-softBlue transition-colors flex justify-between items-center" onclick="this.nextElementSibling.classList.toggle('hidden')">
                                        How hospitals respond
                                    </button>
                                    <div class="p-5 text-[14px] text-textMuted hidden bg-white">
                                        Hospitals receive anonymous versions of your request. After evaluating your condition and requirements, they construct a proposal featuring medical approaches, estimated costs, and physician credentials. You will be notified via email when a proposal is ready.
                                    </div>
                                </div>
                                
                                <!-- FAQ 4 -->
                                <div class="border border-gray-100 rounded-2xl overflow-hidden group">
                                    <button class="w-full text-left px-5 py-4 font-bold text-[15px] text-textMain bg-gray-50 group-hover:bg-softBlue transition-colors flex justify-between items-center" onclick="this.nextElementSibling.classList.toggle('hidden')">
                                        How to compare proposals
                                    </button>
                                    <div class="p-5 text-[14px] text-textMuted hidden bg-white">
                                        Go to the "Compare Proposals" tab. The system provides a side-by-side view of up to 3 proposals, comparing costs, hospital ratings, accommodation, and medical procedures to help you make an informed decision.
                                    </div>
                                </div>
                                
                                <!-- FAQ 5 -->
                                <div class="border border-gray-100 rounded-2xl overflow-hidden group">
                                    <button class="w-full text-left px-5 py-4 font-bold text-[15px] text-textMain bg-gray-50 group-hover:bg-softBlue transition-colors flex justify-between items-center" onclick="this.nextElementSibling.classList.toggle('hidden')">
                                        How secure messaging works
                                    </button>
                                    <div class="p-5 text-[14px] text-textMuted hidden bg-white">
                                        Once a hospital submits a proposal, you can securely chat with their administrative team via the "Messages" tab. Your contact information is never shared automatically.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- TAB: CONTACT SUPPORT -->
                    <div id="tab-contact" class="tab-content hidden animate-fade-in">
                        <form method="POST" action="{{ url_for('patient_support_submit') }}" enctype="multipart/form-data" class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8 flex flex-col gap-6">
                            <h2 class="text-[20px] font-extrabold text-primary mb-2">Contact Support</h2>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Category</label>
                                <select name="category" required class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all appearance-none">
                                    <option value="" disabled selected>Select an issue category</option>
                                    <option value="Technical Issue">Technical Issue</option>
                                    <option value="Account Settings">Account Settings</option>
                                    <option value="Medical Documents">Medical Documents</option>
                                    <option value="Proposals & Messaging">Proposals & Messaging</option>
                                    <option value="Billing & Payments">Billing & Payments</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Subject</label>
                                <input type="text" name="subject" required placeholder="Brief description of the issue" class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all">
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Message</label>
                                <textarea name="message" rows="5" required placeholder="Please describe your issue in detail..." class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all resize-none"></textarea>
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[13px] font-bold text-textMain">Attachment <span class="font-normal text-textMuted ml-1">(Optional)</span></label>
                                <input type="file" name="attachment" accept=".jpg,.jpeg,.png,.pdf" class="w-full text-[14px] text-gray-500 file:mr-4 file:py-3 file:px-4 file:rounded-xl file:border-0 file:text-[13px] file:font-bold file:bg-softBlue file:text-secondary hover:file:bg-blue-100 transition-colors">
                                <span class="text-[12px] text-textMuted mt-1">Accepted formats: JPG, PNG, PDF. Max size: 5MB.</span>
                            </div>
                            
                            <div class="mt-4 pt-6 border-t border-gray-100 flex justify-end">
                                <button type="submit" class="bg-secondary text-white font-bold px-8 py-3 rounded-xl hover:bg-blue-600 transition-colors shadow-sm flex items-center gap-2">
                                    <i data-lucide="send" class="w-4 h-4"></i> Submit Ticket
                                </button>
                            </div>
                        </form>
                    </div>

                    <!-- TAB: MY TICKETS -->
                    <div id="tab-tickets" class="tab-content hidden animate-fade-in">
                        <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 sm:p-8 flex flex-col gap-6">
                            <h2 class="text-[20px] font-extrabold text-primary mb-2">My Support Tickets</h2>
                            
                            {% if tickets %}
                            <div class="overflow-x-auto custom-scrollbar">
                                <table class="w-full text-left border-collapse">
                                    <thead>
                                        <tr class="border-b border-gray-200">
                                            <th class="py-3 px-4 text-[13px] font-bold text-textMuted uppercase tracking-wider">Ticket #</th>
                                            <th class="py-3 px-4 text-[13px] font-bold text-textMuted uppercase tracking-wider">Subject</th>
                                            <th class="py-3 px-4 text-[13px] font-bold text-textMuted uppercase tracking-wider">Status</th>
                                            <th class="py-3 px-4 text-[13px] font-bold text-textMuted uppercase tracking-wider">Created</th>
                                            <th class="py-3 px-4 text-[13px] font-bold text-textMuted uppercase tracking-wider text-right">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-gray-100">
                                        {% for t in tickets %}
                                        <tr class="hover:bg-gray-50 transition-colors group">
                                            <td class="py-4 px-4 text-[14px] font-bold text-primary">{{ t.ticket_number }}</td>
                                            <td class="py-4 px-4 text-[14px] text-textMain max-w-[200px] truncate">{{ t.subject }}</td>
                                            <td class="py-4 px-4">
                                                {% if t.status == 'Open' %}
                                                    <span class="bg-green-50 text-green-700 text-[12px] font-bold px-2.5 py-1 rounded-md">Open</span>
                                                {% elif t.status == 'In Progress' %}
                                                    <span class="bg-yellow-50 text-yellow-700 text-[12px] font-bold px-2.5 py-1 rounded-md">In Progress</span>
                                                {% else %}
                                                    <span class="bg-gray-100 text-gray-700 text-[12px] font-bold px-2.5 py-1 rounded-md">{{ t.status }}</span>
                                                {% endif %}
                                            </td>
                                            <td class="py-4 px-4 text-[13px] text-textMuted">{{ t.created_at.strftime('%b %d, %Y') }}</td>
                                            <td class="py-4 px-4 text-right">
                                                <a href="{{ url_for('patient_support_ticket_detail', ticket_number=t.ticket_number) }}" class="text-secondary font-bold text-[13px] hover:underline">View Details</a>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                            {% else %}
                            <div class="text-center py-10 bg-gray-50 rounded-2xl border border-gray-100">
                                <i data-lucide="ticket" class="w-10 h-10 text-gray-300 mx-auto mb-3"></i>
                                <h3 class="text-[16px] font-bold text-textMain">No tickets yet</h3>
                                <p class="text-[14px] text-textMuted mt-1">If you need help, submit a request from the Contact Support tab.</p>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    
                </div>
            </div>
        </main>
        
        <script>
            function switchTab(tabId) {
                document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
                document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('block'));
                
                document.getElementById(tabId).classList.remove('hidden');
                document.getElementById(tabId).classList.add('block');
                
                document.querySelectorAll('.tab-btn').forEach(btn => {
                    btn.className = 'tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-[14px] text-textMuted hover:bg-gray-50 hover:text-primary transition-colors whitespace-nowrap';
                });
                
                const activeBtn = document.getElementById('btn-' + tabId);
                activeBtn.className = 'tab-btn flex-1 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-[14px] transition-colors bg-softBlue text-secondary whitespace-nowrap';
                
                history.pushState(null, null, '#' + tabId.replace('tab-', ''));
            }
            
            document.addEventListener('DOMContentLoaded', () => {
                const hash = window.location.hash;
                if (hash && ['#faq', '#contact', '#tickets'].includes(hash)) {
                    switchTab('tab-' + hash.replace('#', ''));
                }
            });
        </script>
"""

with open(dest, 'w', encoding='utf-8') as f:
    f.write(header_part + new_main + footer_part)

print(f"Created {dest}")
