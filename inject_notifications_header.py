import os
import glob
import re

html_files = glob.glob('templates/patient-*.html')

new_bell_html = """
            <!-- Notifications Dropdown -->
            <div class="relative">
                <button id="notif-btn" onclick="toggleNotifDropdown()" class="relative p-2 text-textMuted hover:text-primary transition-colors focus:outline-none focus:ring-2 focus:ring-secondary rounded-full" aria-label="Notifications">
                    <i data-lucide="bell" class="w-5 h-5"></i>
                    <span id="notif-badge" class="hidden absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white"></span>
                </button>
                
                <div id="notif-dropdown" class="absolute right-0 top-[110%] w-80 bg-white border border-gray-100 rounded-2xl shadow-dropdown z-50 py-2 hidden">
                    <div class="px-4 py-3 border-b border-gray-50 flex justify-between items-center">
                        <span class="font-bold text-textMain text-[15px]">Notifications</span>
                    </div>
                    <div id="notif-list" class="max-h-[300px] overflow-y-auto custom-scrollbar flex flex-col">
                        <!-- Items inserted by JS -->
                    </div>
                    <a href="/patient/notifications" class="block border-t border-gray-50 px-4 py-3 text-center text-[13px] font-bold text-secondary hover:bg-gray-50 transition-colors rounded-b-2xl">
                        View All Notifications
                    </a>
                </div>
            </div>
"""

js_injection = """
    <!-- Notification Logic -->
    <script>
        function toggleNotifDropdown() {
            const notifDropdown = document.getElementById('notif-dropdown');
            if (!notifDropdown) return;
            if (notifDropdown.classList.contains('hidden')) {
                notifDropdown.classList.remove('hidden');
                fetchNotifications();
            } else {
                notifDropdown.classList.add('hidden');
            }
        }
        
        document.addEventListener('click', (e) => {
            const notifBtn = document.getElementById('notif-btn');
            const notifDropdown = document.getElementById('notif-dropdown');
            if (notifBtn && notifDropdown && !notifBtn.contains(e.target) && !notifDropdown.contains(e.target)) {
                notifDropdown.classList.add('hidden');
            }
        });

        async function fetchNotifications() {
            try {
                const res = await fetch('/api/notifications');
                const data = await res.json();
                
                const badge = document.getElementById('notif-badge');
                if (data.unread_count > 0) {
                    badge.classList.remove('hidden');
                } else {
                    badge.classList.add('hidden');
                }
                
                const list = document.getElementById('notif-list');
                if (!list) return;
                
                if (data.notifications.length === 0) {
                    list.innerHTML = '<div class="p-4 text-center text-[13px] text-textMuted">No notifications</div>';
                    return;
                }
                
                let html = '';
                data.notifications.forEach(n => {
                    const bg = n.is_read ? 'hover:bg-gray-50' : 'bg-softBlue/30 hover:bg-softBlue/50';
                    const dot = n.is_read ? '' : '<div class="w-2 h-2 rounded-full bg-secondary flex-shrink-0 mt-1.5"></div>';
                    
                    html += `
                        <div class="px-4 py-3 border-b border-gray-50 cursor-pointer transition-colors flex gap-3 ${bg}" onclick="handleNotifHeaderClick(${n.id}, '${n.target_url || '#'}', ${n.is_read})">
                            <div class="w-8 h-8 rounded-full bg-softBlue text-secondary flex items-center justify-center flex-shrink-0 mt-0.5">
                                <i data-lucide="bell" class="w-4 h-4"></i>
                            </div>
                            <div class="flex-grow min-w-0">
                                <p class="text-[13px] font-bold text-textMain truncate">${n.title}</p>
                                <p class="text-[12px] text-textMuted line-clamp-2 mt-0.5">${n.message}</p>
                            </div>
                            ${dot}
                        </div>
                    `;
                });
                list.innerHTML = html;
                if (typeof lucide !== 'undefined') lucide.createIcons();
                
            } catch (e) {
                console.error(e);
            }
        }
        
        async function handleNotifHeaderClick(notifId, targetUrl, isRead) {
            if (!isRead) {
                try {
                    await fetch(`/api/notifications/${notifId}/read`, { method: 'POST' });
                } catch(e) {}
            }
            if (targetUrl && targetUrl !== '#') {
                window.location.href = targetUrl;
            } else {
                window.location.reload();
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            const notifBtn = document.getElementById('notif-btn');
            if (notifBtn) fetchNotifications();
        });
    </script>
"""

count = 0
for filepath in html_files:
    if 'registration' in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'id="notif-btn"' in content:
        continue
        
    # Replace anything between <button ... aria-label="Notifications"> and </button>
    pattern = re.compile(r'<button[^>]*aria-label="Notifications"[^>]*>.*?</button>', re.DOTALL)
    new_content = pattern.sub(new_bell_html.strip(), content)
    
    # Also update the sidebar link from <a href="#"> Notifications</a> to <a href="/patient/notifications"> Notifications</a>
    # The exact pattern:
    # <a href="#" class="px-4 py-3 rounded-xl text-textMain font-semibold text-[15px] flex items-center gap-3"><i data-lucide="bell" class="w-5 h-5 text-textMuted"></i> Notifications</a>
    # Let's just blindly replace `<a href="#" ` with `<a href="{{ url_for('patient_notifications') }}" ` if it contains Notifications
    sidebar_pattern = re.compile(r'<a href="[^"]*"([^>]*)>(.*?)Notifications</a>')
    new_content = sidebar_pattern.sub(r'<a href="{{ url_for(\'patient_notifications\') }}"\1>\2Notifications</a>', new_content)
    
    if new_content != content:
        if '<!-- Notification Logic -->' not in new_content:
            new_content = new_content.replace('</body>', js_injection + '\n</body>')
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Injected into {filepath}")

print(f"Finished injecting into {count} files.")
