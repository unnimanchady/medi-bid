import os

source_path = 'templates/patient-medical-documents.html'
with open(source_path, 'r', encoding='utf-8') as f:
    source_content = f.read()

# Extract header part (up to <main...>)
header_part = source_content.split('<!-- DASHBOARD MAIN CONTENT -->')[0]
footer_part = source_content.split('</main>')[1]

# Modify header part to reflect correct active sidebar link and title
header_part = header_part.replace('<title>Patient Dashboard | MediBid</title>', '<title>Patient Notifications | MediBid</title>')

# Deselect all sidebar links
header_part = header_part.replace('class="flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-white bg-white/10 backdrop-blur-sm transition-all shadow-sm"', 'class="flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-all group"')
header_part = header_part.replace('class="flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-white bg-white/10 backdrop-blur-sm transition-all shadow-sm border border-white/5"', 'class="flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-all group"')

# Wait, there's no sidebar link for Notifications in the prompt, but it mentions "Patient Portal -> Notifications". I can add one or leave it out, but the bell dropdown is the main entry point. 

main_content = """
        <!-- DASHBOARD MAIN CONTENT -->
        
        <main class="flex-grow p-4 sm:p-6 lg:p-8 flex flex-col gap-8 max-w-[1400px] w-full mx-auto relative">
            
            <!-- TOP / HEADER SECTION -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-5 opacity-0 animate-fade-in">
                <div class="flex flex-col">
                    <h1 class="text-[26px] sm:text-[30px] font-extrabold text-primary tracking-tight">Notifications</h1>
                    <p class="text-[14px] sm:text-[15px] text-textMuted font-medium mt-1">Stay updated on your treatment requests and messages.</p>
                </div>
                
                {% if unread_count > 0 %}
                <button onclick="markAllRead()" class="bg-white border border-gray-200 text-textMain font-bold px-5 py-2.5 rounded-full shadow-sm hover:bg-gray-50 flex items-center gap-2 self-start sm:self-auto whitespace-nowrap transition-all text-[14px]">
                    <i data-lucide="check-check" class="w-4 h-4 text-textMuted"></i> Mark All as Read
                </button>
                {% endif %}
            </div>

            <!-- FILTERS -->
            <div class="bg-white p-2 rounded-2xl border border-gray-200 shadow-sm flex gap-2 opacity-0 animate-fade-in stagger-1 w-full max-w-md">
                <button onclick="setFilter('all')" id="filter-all" class="flex-1 py-2 text-[14px] font-bold rounded-xl transition-colors bg-softBlue text-secondary">All</button>
                <button onclick="setFilter('unread')" id="filter-unread" class="flex-1 py-2 text-[14px] font-medium rounded-xl transition-colors text-textMuted hover:text-textMain hover:bg-gray-50">Unread</button>
                <button onclick="setFilter('read')" id="filter-read" class="flex-1 py-2 text-[14px] font-medium rounded-xl transition-colors text-textMuted hover:text-textMain hover:bg-gray-50">Read</button>
            </div>

            <!-- NOTIFICATIONS LIST -->
            <div class="flex flex-col gap-3 opacity-0 animate-fade-in stagger-2" id="notificationsContainer">
                {% if notifications %}
                    {% for notif in notifications %}
                        <div class="notification-item group relative bg-white border {{ 'border-secondary/30 bg-softBlue/30 shadow-sm' if not notif.is_read else 'border-gray-100 hover:border-gray-200 shadow-sm hover:shadow' }} rounded-2xl p-5 flex flex-col sm:flex-row gap-5 items-start sm:items-center transition-all cursor-pointer" 
                             data-read="{{ 'true' if notif.is_read else 'false' }}" 
                             onclick="handleNotifClick({{ notif.id }}, '{{ notif.target_url or '#' }}', {{ 'true' if notif.is_read else 'false' }})">
                            
                            <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 {{ 'bg-secondary text-white' if not notif.is_read else 'bg-gray-100 text-textMuted group-hover:bg-gray-200' }} transition-colors">
                                {% if notif.notification_type == 'proposal_submitted' or notif.notification_type == 'proposal_updated' %}
                                    <i data-lucide="file-text" class="w-5 h-5"></i>
                                {% elif notif.notification_type == 'new_message' %}
                                    <i data-lucide="message-square" class="w-5 h-5"></i>
                                {% elif notif.notification_type == 'status_change' %}
                                    <i data-lucide="activity" class="w-5 h-5"></i>
                                {% else %}
                                    <i data-lucide="bell" class="w-5 h-5"></i>
                                {% endif %}
                            </div>
                            
                            <div class="flex-grow flex flex-col">
                                <h3 class="text-[16px] font-bold {{ 'text-primary' if not notif.is_read else 'text-textMain' }}">{{ notif.title }}</h3>
                                <p class="text-[14px] text-textMuted mt-1">{{ notif.message }}</p>
                                <span class="text-[12px] text-textMuted mt-2 font-medium flex items-center gap-1.5"><i data-lucide="clock" class="w-3.5 h-3.5"></i> {{ notif.created_at.strftime('%b %d, %Y %I:%M %p') }}</span>
                            </div>
                            
                            {% if not notif.is_read %}
                            <div class="absolute top-5 right-5 w-2.5 h-2.5 rounded-full bg-secondary"></div>
                            {% endif %}
                        </div>
                    {% endfor %}
                {% else %}
                    <div class="flex flex-col items-center justify-center py-20 bg-white rounded-3xl border border-gray-100 shadow-sm text-center px-4">
                        <div class="w-20 h-20 bg-softBlue rounded-full flex items-center justify-center mb-5">
                            <i data-lucide="bell-off" class="w-10 h-10 text-secondary"></i>
                        </div>
                        <h3 class="text-[20px] font-bold text-primary mb-2">All caught up!</h3>
                        <p class="text-[15px] text-textMuted max-w-md">You don't have any notifications right now. Check back later for updates.</p>
                    </div>
                {% endif %}
                
                <div id="noResults" class="hidden flex-col items-center justify-center py-20 bg-white rounded-3xl border border-gray-100 shadow-sm text-center px-4">
                    <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-5">
                        <i data-lucide="inbox" class="w-10 h-10 text-gray-400"></i>
                    </div>
                    <h3 class="text-[20px] font-bold text-primary mb-2">No matching notifications</h3>
                    <p class="text-[15px] text-textMuted max-w-md">Try changing your filters to see more results.</p>
                </div>
            </div>
        </main>
"""

# Insert JS functions in footer_part before </body>
js_code = """
    <script>
        function setFilter(filter) {
            // Update buttons styling
            ['all', 'unread', 'read'].forEach(f => {
                const btn = document.getElementById(`filter-${f}`);
                if (f === filter) {
                    btn.className = 'flex-1 py-2 text-[14px] font-bold rounded-xl transition-colors bg-softBlue text-secondary';
                } else {
                    btn.className = 'flex-1 py-2 text-[14px] font-medium rounded-xl transition-colors text-textMuted hover:text-textMain hover:bg-gray-50';
                }
            });
            
            // Filter list
            const items = document.querySelectorAll('.notification-item');
            let visible = 0;
            items.forEach(item => {
                const isRead = item.getAttribute('data-read') === 'true';
                if (filter === 'all' || (filter === 'read' && isRead) || (filter === 'unread' && !isRead)) {
                    item.style.display = 'flex';
                    visible++;
                } else {
                    item.style.display = 'none';
                }
            });
            
            const noResults = document.getElementById('noResults');
            if (visible === 0 && items.length > 0) {
                noResults.style.display = 'flex';
            } else {
                noResults.style.display = 'none';
            }
        }
        
        async function markAllRead() {
            try {
                await fetch('/api/notifications/read-all', { method: 'POST' });
                window.location.reload();
            } catch (e) {
                console.error(e);
            }
        }
        
        async function handleNotifClick(notifId, targetUrl, isRead) {
            if (!isRead) {
                try {
                    await fetch(`/api/notifications/${notifId}/read`, { method: 'POST' });
                } catch (e) {
                    console.error(e);
                }
            }
            if (targetUrl && targetUrl !== '#') {
                window.location.href = targetUrl;
            } else {
                window.location.reload();
            }
        }
    </script>
"""

footer_part = footer_part.replace('</body>', js_code + '\n</body>')

with open('templates/patient-notifications.html', 'w', encoding='utf-8') as f:
    f.write(header_part + main_content + footer_part)
print("Created templates/patient-notifications.html")
