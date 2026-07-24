with open('templates/patient-message-thread.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will replace the entire right panel which is currently the empty state
pattern = re.compile(r'<!-- RIGHT PANEL \(Empty State for Inbox\) -->.*?(?=</main>)', re.DOTALL)

chat_panel = '''<!-- RIGHT PANEL: Active Chat -->
            <div id="active-chat" class="flex md:flex flex-col flex-grow bg-white h-full relative border-l border-gray-200">
                <!-- Background Pattern -->
                <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9IiNFMkU4RjAiLz48L3N2Zz4=')] opacity-50"></div>

                <!-- Chat Header -->
                <div class="h-[70px] sm:h-[80px] bg-white border-b border-gray-200 flex items-center justify-between px-4 sm:px-6 flex-shrink-0 z-10 shadow-sm relative">
                    <div class="flex items-center gap-3 min-w-0">
                        <a href="{{ url_for('patient_secure_messages') }}" id="back-to-list-btn" class="md:hidden p-2 -ml-2 text-textMuted hover:text-primary focus:outline-none rounded-lg flex-shrink-0">
                            <i data-lucide="arrow-left" class="w-5 h-5"></i>
                        </a>
                        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-softBlue border border-blue-100 flex items-center justify-center flex-shrink-0 hidden sm:flex">
                            <i data-lucide="building-2" class="w-5 h-5 sm:w-6 sm:h-6 text-secondary"></i>
                        </div>
                        <div class="flex flex-col min-w-0">
                            <h2 class="text-[15px] sm:text-[17px] font-extrabold text-primary truncate leading-tight">{{ thread.hospital.display_name or thread.hospital.legal_name }}</h2>
                            <div class="flex items-center gap-2 mt-0.5">
                                <span class="text-[11px] sm:text-[12px] text-textMuted font-mono tracking-wide truncate">REQ: {{ thread.treatment_request.reference_id }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Chat Messages Area -->
                <div class="flex-grow overflow-y-auto custom-scrollbar p-4 sm:p-6 flex flex-col relative z-10 space-y-4">
                    {% if not messages %}
                        <div class="text-center py-8 text-textMuted text-[14px]">No messages yet. Send a message to start the conversation.</div>
                    {% endif %}
                    
                    {% for msg in messages %}
                        {% if msg.sender_type == 'hospital' %}
                            <!-- Hospital Message -->
                            <div class="flex gap-3 max-w-[95%] lg:max-w-[80%]">
                                <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0 mt-1 hidden sm:flex">
                                    <i data-lucide="building" class="w-4 h-4 text-gray-500"></i>
                                </div>
                                <div class="flex flex-col gap-1 w-full">
                                    <div class="flex items-baseline gap-2 ml-1">
                                        <span class="text-[12px] font-bold text-textMain">{{ thread.hospital.display_name or thread.hospital.legal_name }}</span>
                                        <span class="text-[11px] text-gray-400 font-medium">{{ msg.created_at.strftime('%I:%M %p') }}</span>
                                    </div>
                                    <div class="bg-white border border-gray-200 text-textMain text-[14px] sm:text-[14.5px] p-4 rounded-[16px] rounded-tl-sm shadow-sm leading-relaxed whitespace-pre-wrap w-full sm:w-auto sm:max-w-full">{{ msg.message_body }}</div>
                                </div>
                            </div>
                        {% else %}
                            <!-- Patient Message -->
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
                    
                    <div class="h-4 flex-shrink-0"></div>
                </div>

                <!-- Composer Area -->
                <div class="bg-white border-t border-gray-200 p-3 sm:p-4 flex-shrink-0 z-20 shadow-[0_-4px_10px_rgba(0,0,0,0.02)]">
                    <form action="{{ url_for('patient_send_message', thread_id=thread.id) }}" method="POST">
                        <div class="flex items-end gap-2 sm:gap-3 bg-gray-50 border border-gray-200 rounded-[16px] p-2 focus-within:ring-2 focus-within:ring-secondary focus-within:border-secondary transition-all">
                            <textarea name="message_body" rows="1" required class="w-full bg-transparent border-none focus:ring-0 text-[14px] sm:text-[14.5px] text-textMain placeholder-gray-400 resize-none py-3 px-3 max-h-[120px] overflow-y-auto custom-scrollbar leading-relaxed" placeholder="Write a secure message..."></textarea>
                            
                            <button type="submit" class="bg-primary text-white hover:bg-blue-800 p-2.5 sm:p-3 rounded-xl transition-colors focus:outline-none flex-shrink-0 shadow-sm disabled:opacity-50" aria-label="Send Message" onclick="this.innerHTML='<i data-lucide=\\'loader-2\\' class=\\'w-5 h-5 animate-spin\\'></i>'; setTimeout(()=>{this.innerHTML='<i data-lucide=\\'send\\' class=\\'w-5 h-5\\'></i>'; lucide.createIcons();}, 1000);">
                                <i data-lucide="send" class="w-5 h-5"></i>
                            </button>
                        </div>
                    </form>
                    <div class="text-[11px] text-textMuted mt-2.5 px-1 flex justify-between items-center">
                        <span class="flex items-center gap-1 font-medium text-gray-500"><i data-lucide="lock" class="w-3 h-3"></i> Secure End-to-End Environment</span>
                    </div>
                </div>
            </div>
        </div>
'''

content = pattern.sub(chat_panel, content)

with open('templates/patient-message-thread.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated patient-message-thread.html')
