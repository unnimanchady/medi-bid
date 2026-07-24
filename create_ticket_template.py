import os

source = 'templates/patient-support.html'
dest = 'templates/patient-support-ticket.html'

with open(source, 'r', encoding='utf-8') as f:
    content = f.read()
    
header_part = content.split('<main')[0]
footer_part = content.split('</main>')[1]

new_main = """<main class="flex-grow w-full max-w-[900px] mx-auto py-6 sm:py-8 px-4 sm:px-6 flex flex-col gap-6">
            
            <nav class="flex items-center text-[13px] text-textMuted font-medium truncate gap-2" aria-label="Breadcrumb">
                <a href="{{ url_for('patient_dashboard') }}" class="hover:text-primary transition-colors hidden sm:inline">Dashboard</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300 hidden sm:inline"></i>
                <a href="{{ url_for('patient_support') }}#tickets" class="hover:text-primary transition-colors">Help & Support</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300"></i>
                <span class="text-textMain font-bold">{{ ticket.ticket_number }}</span>
            </nav>
            
            <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 overflow-hidden">
                <div class="p-6 sm:p-8 border-b border-gray-100 flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                    <div>
                        <div class="flex items-center gap-3 mb-2">
                            <h2 class="text-[20px] font-extrabold text-primary">{{ ticket.subject }}</h2>
                            {% if ticket.status == 'Open' %}
                                <span class="bg-green-50 text-green-700 text-[12px] font-bold px-2.5 py-1 rounded-md">Open</span>
                            {% elif ticket.status == 'In Progress' %}
                                <span class="bg-yellow-50 text-yellow-700 text-[12px] font-bold px-2.5 py-1 rounded-md">In Progress</span>
                            {% else %}
                                <span class="bg-gray-100 text-gray-700 text-[12px] font-bold px-2.5 py-1 rounded-md">{{ ticket.status }}</span>
                            {% endif %}
                        </div>
                        <p class="text-[13px] text-textMuted font-medium">Ticket {{ ticket.ticket_number }} &bull; {{ ticket.category }} &bull; Submitted {{ ticket.created_at.strftime('%b %d, %Y at %I:%M %p') }}</p>
                    </div>
                </div>
                
                <div class="p-6 sm:p-8 flex flex-col gap-6 bg-gray-50/50">
                    
                    <!-- Original Request -->
                    <div class="flex gap-4">
                        <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center border border-secondary/20 shadow-inner flex-shrink-0">
                            <span class="text-secondary font-bold text-[14px]">{{ user.first_name[0] }}{{ user.last_name[0] }}</span>
                        </div>
                        <div class="flex-grow bg-white border border-gray-100 rounded-2xl rounded-tl-none p-5 shadow-sm">
                            <div class="flex justify-between items-center mb-2">
                                <span class="font-bold text-[14px] text-textMain">You</span>
                                <span class="text-[12px] text-textMuted">{{ ticket.created_at.strftime('%b %d, %I:%M %p') }}</span>
                            </div>
                            <p class="text-[14px] text-textMain leading-relaxed whitespace-pre-wrap">{{ ticket.message }}</p>
                            
                            {% if ticket.attachment_filename %}
                            <div class="mt-4 pt-4 border-t border-gray-50">
                                <span class="text-[12px] font-bold text-textMuted uppercase tracking-wider mb-2 block">Attachment</span>
                                <div class="inline-flex items-center gap-2 bg-gray-50 border border-gray-100 px-3 py-2 rounded-lg">
                                    <i data-lucide="paperclip" class="w-4 h-4 text-gray-400"></i>
                                    <span class="text-[13px] text-textMain font-medium">{{ ticket.attachment_filename }}</span>
                                </div>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    
                    <!-- Replies Thread -->
                    {% for msg in ticket.messages %}
                        {% if msg.sender_type == 'patient' %}
                        <!-- Patient Reply -->
                        <div class="flex gap-4">
                            <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center border border-secondary/20 shadow-inner flex-shrink-0">
                                <span class="text-secondary font-bold text-[14px]">{{ user.first_name[0] }}{{ user.last_name[0] }}</span>
                            </div>
                            <div class="flex-grow bg-white border border-gray-100 rounded-2xl rounded-tl-none p-5 shadow-sm">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="font-bold text-[14px] text-textMain">You</span>
                                    <span class="text-[12px] text-textMuted">{{ msg.created_at.strftime('%b %d, %I:%M %p') }}</span>
                                </div>
                                <p class="text-[14px] text-textMain leading-relaxed whitespace-pre-wrap">{{ msg.message }}</p>
                            </div>
                        </div>
                        {% else %}
                        <!-- Admin Reply -->
                        <div class="flex gap-4 flex-row-reverse">
                            <div class="w-10 h-10 rounded-full bg-blue-900 flex items-center justify-center flex-shrink-0 shadow-sm">
                                <span class="text-white font-bold text-[14px]">A</span>
                            </div>
                            <div class="flex-grow bg-blue-50 border border-blue-100 rounded-2xl rounded-tr-none p-5 shadow-sm">
                                <div class="flex justify-between items-center mb-2 flex-row-reverse">
                                    <span class="font-bold text-[14px] text-blue-900">MediBid Support</span>
                                    <span class="text-[12px] text-blue-600/70">{{ msg.created_at.strftime('%b %d, %I:%M %p') }}</span>
                                </div>
                                <p class="text-[14px] text-blue-900 leading-relaxed whitespace-pre-wrap text-right">{{ msg.message }}</p>
                            </div>
                        </div>
                        {% endif %}
                    {% endfor %}
                    
                </div>
                
                {% if ticket.status != 'Closed' %}
                <div class="p-6 sm:p-8 border-t border-gray-100 bg-white">
                    <form method="POST" action="{{ url_for('patient_support_ticket_detail', ticket_number=ticket.ticket_number) }}" class="flex flex-col gap-4">
                        <textarea name="message" rows="3" required placeholder="Type your reply here..." class="w-full border border-gray-200 bg-gray-50 rounded-xl px-4 py-3 text-[14px] focus:outline-none focus:ring-2 focus:ring-secondary focus:bg-white transition-all resize-none"></textarea>
                        <div class="flex justify-end">
                            <button type="submit" class="bg-secondary text-white font-bold px-6 py-2.5 rounded-xl hover:bg-blue-600 transition-colors shadow-sm flex items-center gap-2">
                                <i data-lucide="send" class="w-4 h-4"></i> Send Reply
                            </button>
                        </div>
                    </form>
                </div>
                {% else %}
                <div class="p-6 sm:p-8 border-t border-gray-100 bg-gray-50 text-center">
                    <p class="text-[14px] font-bold text-gray-500">This ticket has been closed. If you need further assistance, please open a new ticket.</p>
                </div>
                {% endif %}
            </div>
            
        </main>
"""

with open(dest, 'w', encoding='utf-8') as f:
    f.write(header_part + new_main + footer_part)

print(f"Created {dest}")
