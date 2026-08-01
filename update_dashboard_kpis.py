import re

with open('templates/hospital-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new cards block
new_cards = '''<!-- Eligible Requests -->
                <div class="bg-white p-5 sm:p-6 rounded-[16px] border border-gray-100 border-t-4 border-t-[#F97316] shadow-md hover:-translate-y-[3px] hover:shadow-lg transition-all duration-200">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-12 h-12 rounded-full bg-[#F97316]/15 flex items-center justify-center">
                            <i data-lucide="file-text" class="w-6 h-6 text-[#F97316]"></i>
                        </div>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[32px] font-extrabold text-[#1E293B] leading-none">{{ eligible_requests_count }}</span>
                        <span class="text-[13px] font-semibold text-[#64748B] mt-1.5">Eligible Patient Requests</span>
                    </div>
                </div>

                <!-- Submitted Proposals -->
                <div class="bg-white p-5 sm:p-6 rounded-[16px] border border-gray-100 border-t-4 border-t-[#2563EB] shadow-md hover:-translate-y-[3px] hover:shadow-lg transition-all duration-200">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-12 h-12 rounded-full bg-[#2563EB]/15 flex items-center justify-center">
                            <i data-lucide="send" class="w-6 h-6 text-[#2563EB]"></i>
                        </div>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[32px] font-extrabold text-[#1E293B] leading-none">0</span>
                        <span class="text-[13px] font-semibold text-[#64748B] mt-1.5">Submitted Proposals</span>
                    </div>
                </div>

                <!-- Unread Messages -->
                <div class="bg-white p-5 sm:p-6 rounded-[16px] border border-gray-100 border-t-4 border-t-[#7C3AED] shadow-md hover:-translate-y-[3px] hover:shadow-lg transition-all duration-200">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-12 h-12 rounded-full bg-[#7C3AED]/15 flex items-center justify-center">
                            <i data-lucide="message-circle" class="w-6 h-6 text-[#7C3AED]"></i>
                        </div>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[32px] font-extrabold text-[#1E293B] leading-none">0</span>
                        <span class="text-[13px] font-semibold text-[#64748B] mt-1.5">Unread Messages</span>
                    </div>
                </div>
                
                <!-- Profile Completion -->
                <div class="bg-white p-5 sm:p-6 rounded-[16px] border border-gray-100 border-t-4 border-t-[#22C55E] shadow-md hover:-translate-y-[3px] hover:shadow-lg transition-all duration-200">
                    <div class="flex items-center gap-4 mb-4">
                        <div class="w-12 h-12 rounded-full bg-[#22C55E]/15 flex items-center justify-center">
                            <i data-lucide="check-circle" class="w-6 h-6 text-[#22C55E]"></i>
                        </div>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[32px] font-extrabold text-[#1E293B] leading-none">100%</span>
                        <span class="text-[13px] font-semibold text-[#64748B] mt-1.5">Profile Completion</span>
                    </div>
                </div>'''

# Extract the existing grid container to replace its content
# The grid starts at <div class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6 opacity-0 animate-fade-in stagger-1 mb-6">
pattern = r'(<div class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6 opacity-0 animate-fade-in stagger-1 mb-6">)(.*?)(</div>\s*<!-- MAIN GRID CONTENT -->)'
match = re.search(pattern, content, re.DOTALL)

if match:
    new_full_content = content[:match.start(2)] + "\n" + new_cards + "\n            " + content[match.end(2):]
    with open('templates/hospital-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(new_full_content)
    print("Dashboard KPI cards successfully updated.")
else:
    print("Could not find the target block in hospital-dashboard.html")
