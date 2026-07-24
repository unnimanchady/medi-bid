import re

with open('templates/hospital-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

inbox_main = '''
        <!-- MAIN CONTENT (INBOX) -->
        <main class="flex-1 flex flex-col min-w-0 overflow-hidden bg-bgLight">
            <header class="bg-white border-b border-gray-200 px-8 py-6 flex items-center justify-between flex-shrink-0">
                <div>
                    <h1 class="text-[24px] font-extrabold text-primary tracking-tight">Messages</h1>
                    <p class="text-[14px] text-textMuted mt-1">Manage patient inquiries and secure communications.</p>
                </div>
            </header>
            
            <div class="flex-1 overflow-y-auto p-8">
                <div class="max-w-4xl mx-auto bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
                    {% if threads %}
                        <div class="divide-y divide-gray-100">
                        {% for t in threads %}
                            <a href="{{ url_for('hospital_message_thread', thread_id=t.id) }}" class="flex items-center gap-4 p-5 hover:bg-gray-50 transition-colors">
                                <div class="w-12 h-12 rounded-full bg-softBlue flex items-center justify-center flex-shrink-0">
                                    <i data-lucide="user" class="w-6 h-6 text-secondary"></i>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <div class="flex justify-between items-start mb-1">
                                        <h3 class="text-[15px] font-bold text-textMain truncate pr-2">Patient ({{ t.treatment_request.reference_id }})</h3>
                                        {% if t.messages.count() > 0 %}
                                        <span class="text-[12px] text-textMuted whitespace-nowrap">{{ t.messages[-1].created_at.strftime('%b %d, %I:%M %p') }}</span>
                                        {% endif %}
                                    </div>
                                    <p class="text-[13px] {% if unread_counts[t.id] > 0 %}text-textMain font-bold{% else %}text-textMuted{% endif %} truncate">
                                        {% if t.messages.count() > 0 %}
                                            {% if t.messages[-1].sender_type == 'hospital' %}You: {% endif %}{{ t.messages[-1].message_body | truncate(60) }}
                                        {% else %}
                                            No messages yet.
                                        {% endif %}
                                    </p>
                                </div>
                                {% if unread_counts[t.id] > 0 %}
                                <div class="w-6 h-6 bg-secondary text-white rounded-full flex items-center justify-center text-[11px] font-bold flex-shrink-0">{{ unread_counts[t.id] }}</div>
                                {% else %}
                                <div class="flex-shrink-0">
                                    <i data-lucide="chevron-right" class="w-5 h-5 text-gray-300"></i>
                                </div>
                                {% endif %}
                            </a>
                        {% endfor %}
                        </div>
                    {% else %}
                        <div class="p-12 text-center flex flex-col items-center justify-center">
                            <div class="w-16 h-16 rounded-full bg-gray-50 flex items-center justify-center mb-4">
                                <i data-lucide="message-square" class="w-8 h-8 text-gray-300"></i>
                            </div>
                            <h3 class="text-[16px] font-bold text-textMain mb-2">No Conversations Yet</h3>
                            <p class="text-[14px] text-textMuted">When patients send you messages regarding proposals, they will appear here.</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </main>
'''

thread_main = '''
        <!-- MAIN CONTENT (THREAD) -->
        <main class="flex-1 flex flex-col min-w-0 overflow-hidden bg-white">
            <header class="bg-white border-b border-gray-200 px-6 sm:px-8 py-4 sm:py-5 flex items-center gap-4 flex-shrink-0">
                <a href="{{ url_for('hospital_messages') }}" class="p-2 -ml-2 text-textMuted hover:text-primary rounded-lg transition-colors focus:outline-none">
                    <i data-lucide="arrow-left" class="w-5 h-5"></i>
                </a>
                <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-softBlue flex items-center justify-center flex-shrink-0">
                    <i data-lucide="user" class="w-5 h-5 sm:w-6 sm:h-6 text-secondary"></i>
                </div>
                <div>
                    <h1 class="text-[16px] sm:text-[18px] font-extrabold text-primary tracking-tight leading-tight">Patient ({{ thread.treatment_request.reference_id }})</h1>
                    <div class="text-[12px] sm:text-[13px] text-textMuted font-medium mt-0.5">Secure End-to-End Communication</div>
                </div>
            </header>
            
            <div id="message-history-container" class="flex-1 overflow-y-auto custom-scrollbar p-6 bg-bgLight flex flex-col space-y-4">
                {% if not messages %}
                    <div class="text-center py-8 text-textMuted text-[14px]">No messages yet. Send a message to start the conversation.</div>
                {% endif %}
                
                {% for msg in messages %}
                    {% if msg.sender_type == 'patient' %}
                        <!-- Patient Message -->
                        <div class="flex gap-3 max-w-[95%] lg:max-w-[80%]">
                            <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0 mt-1 hidden sm:flex">
                                <i data-lucide="user" class="w-4 h-4 text-gray-500"></i>
                            </div>
                            <div class="flex flex-col gap-1 w-full">
                                <div class="flex items-baseline gap-2 ml-1">
                                    <span class="text-[12px] font-bold text-textMain">Patient</span>
                                    <span class="text-[11px] text-gray-400 font-medium">{{ msg.created_at.strftime('%I:%M %p') }}</span>
                                </div>
                                <div class="bg-white border border-gray-200 text-textMain text-[14px] sm:text-[14.5px] p-4 rounded-[16px] rounded-tl-sm shadow-sm leading-relaxed whitespace-pre-wrap w-full sm:w-auto sm:max-w-full">{{ msg.message_body }}</div>
                            </div>
                        </div>
                    {% else %}
                        <!-- Hospital Message -->
                        <div class="flex justify-end gap-3 max-w-[95%] lg:max-w-[80%] ml-auto mt-2">
                            <div class="flex flex-col gap-1 items-end w-full">
                                <div class="flex items-baseline gap-2 mr-1">
                                    <span class="text-[11px] text-gray-400 font-medium">{{ msg.created_at.strftime('%I:%M %p') }}</span>
                                    <span class="text-[12px] font-bold text-textMuted">You</span>
                                </div>
                                <div class="bg-softBlue border border-blue-200 text-textMain text-[14px] sm:text-[14.5px] p-4 rounded-[16px] rounded-tr-sm shadow-sm leading-relaxed whitespace-pre-wrap text-left w-full sm:w-auto sm:max-w-full">{{ msg.message_body }}</div>
                                {% if msg.is_read %}
                                <div class="flex items-center gap-1 text-[11.5px] text-secondary font-bold mr-1 mt-0.5">
                                    <i data-lucide="check-check" class="w-3.5 h-3.5"></i> Read
                                </div>
                                {% endif %}
                            </div>
                        </div>
                    {% endif %}
                {% endfor %}
            </div>
            
            <div class="bg-white border-t border-gray-200 p-4 sm:p-5 flex-shrink-0 z-20">
                <form action="{{ url_for('hospital_send_message', thread_id=thread.id) }}" method="POST" class="max-w-4xl mx-auto">
                    <div class="flex items-end gap-3 bg-gray-50 border border-gray-200 rounded-2xl p-2.5 focus-within:ring-2 focus-within:ring-secondary focus-within:border-secondary transition-all">
                        <textarea name="message_body" rows="1" required class="w-full bg-transparent border-none focus:ring-0 text-[14px] sm:text-[15px] text-textMain placeholder-gray-400 resize-none py-2.5 px-3 max-h-[120px] overflow-y-auto custom-scrollbar leading-relaxed" placeholder="Write your reply to the patient..."></textarea>
                        
                        <button type="submit" class="bg-primary text-white hover:bg-blue-800 p-3 sm:p-3.5 rounded-xl transition-colors focus:outline-none flex-shrink-0 shadow-sm disabled:opacity-50" aria-label="Send Message" onclick="this.innerHTML='<i data-lucide=\\'loader-2\\' class=\\'w-5 h-5 animate-spin\\'></i>'; setTimeout(()=>{this.innerHTML='<i data-lucide=\\'send\\' class=\\'w-5 h-5\\'></i>'; lucide.createIcons();}, 1000);">
                            <i data-lucide="send" class="w-5 h-5"></i>
                        </button>
                    </div>
                </form>
            </div>
        </main>
'''

def fix_nav(html):
    html = html.replace('<div class="px-4 py-3 text-textMuted flex items-center gap-3 rounded-xl cursor-not-allowed opacity-60 transition-opacity hover:opacity-100 group" title="Coming Soon">\n                <i data-lucide="message-square" class="w-5 h-5"></i>\n                <span class="font-medium">Messages</span>\n                <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-gray-100 text-gray-500 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>\n            </div>', '<a href="{{ url_for(\'hospital_messages\') }}" class="px-4 py-3 bg-softBlue text-secondary flex items-center gap-3 rounded-xl">\n                <i data-lucide="message-square" class="w-5 h-5"></i>\n                <span class="font-bold">Messages</span>\n            </a>')
    
    html = html.replace('<a href="{{ url_for(\'hospital_dashboard\') }}" class="px-4 py-3 bg-softBlue text-secondary flex items-center gap-3 rounded-xl">\n                <i data-lucide="layout-dashboard" class="w-5 h-5"></i>\n                <span class="font-bold">Dashboard</span>\n            </a>', '<a href="{{ url_for(\'hospital_dashboard\') }}" class="px-4 py-3 text-textMuted hover:bg-gray-50 hover:text-primary flex items-center gap-3 rounded-xl transition-colors">\n                <i data-lucide="layout-dashboard" class="w-5 h-5"></i>\n                <span class="font-medium">Dashboard</span>\n            </a>')
    return html

import re
main_pattern = re.compile(r'<main class=\"flex-1 flex flex-col h-screen overflow-y-auto\">.*?</main>', re.DOTALL)

inbox_html = main_pattern.sub(inbox_main, content)
inbox_html = fix_nav(inbox_html)

thread_html = main_pattern.sub(thread_main, content)
thread_html = fix_nav(thread_html)

scroll_script = '''
        const chatContainer = document.getElementById('message-history-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
'''
thread_html = thread_html.replace('lucide.createIcons();', 'lucide.createIcons();\n' + scroll_script)

with open('templates/hospital-messages.html', 'w', encoding='utf-8') as f:
    f.write(inbox_html)

with open('templates/hospital-message-thread.html', 'w', encoding='utf-8') as f:
    f.write(thread_html)

print("Created hospital messaging templates!")
