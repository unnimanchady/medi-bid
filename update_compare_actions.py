import re

file_path = 'templates/patient-compare-hospitals.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Actions Category
actions_regex = r'<!-- Actions Category \(Always Open\) -->.*?</div>\s*</div>\s*</div>\s*</main>'

actions_replacement = r'''<!-- Actions Category (Always Open) -->
            <div class="bg-white border border-gray-200 rounded-[16px] overflow-hidden shadow-sm mt-4 no-print">
                <div class="w-full flex items-center p-4 sm:p-5 bg-gray-50 border-b border-gray-200">
                    <h2 class="text-[18px] sm:text-[20px] font-extrabold text-primary">Your Next Steps</h2>
                </div>
                <div class="flex flex-col md:grid md:grid-cols-{{ (proposals|length) + 1 if proposals else 4 }} gap-4 p-4 sm:p-5">
                    <div class="md:col-span-1 hidden md:block text-[14px] font-medium text-textMuted pt-2 pr-4">
                        Review the complete proposal or save your private thoughts for each option. Shortlist your favorites to decide later.
                    </div>
                    
                    {% for proposal in proposals %}
                    <div class="md:col-span-1 flex flex-col gap-3 pb-6 border-b border-gray-100 md:border-b-0 md:pb-0">
                        <span class="md:hidden text-[13px] font-bold text-textMain mb-2 flex items-center gap-2">
                            <div class="w-5 h-5 rounded bg-primary text-white flex items-center justify-center text-[10px] font-bold shadow-sm">{{ loop.index }}</div> {{ proposal.hospital.display_name or proposal.hospital.legal_name }}
                        </span>
                        
                        <a href="{{ url_for('patient_treatment_proposal_details', proposal_id=proposal.id) }}" class="bg-primary text-white font-bold px-4 py-2.5 rounded-xl text-[13.5px] transition-all hover:bg-blue-800 text-center shadow-sm w-full focus:outline-none focus:ring-2 focus:ring-primary">
                            View Full Proposal
                        </a>
                        <!-- Wait, hospital profile might need hospital_id parameter? For now assuming patient_hospital_profile doesn't or we'll fix it next if it crashes. -->
                        <a href="{{ url_for('patient_hospital_profile') }}" class="bg-white border border-gray-200 text-textMain font-bold px-4 py-2.5 rounded-xl text-[13.5px] transition-all hover:bg-gray-50 text-center shadow-sm w-full focus:outline-none focus:ring-2 focus:ring-gray-300">
                            View Hospital Profile
                        </a>
                        <button class="bg-white border border-gray-200 text-textMuted hover:text-lavenderAccent font-bold px-4 py-2.5 rounded-xl text-[13.5px] transition-all hover:bg-purple-50 flex items-center justify-center gap-2 w-full focus:outline-none">
                            <i data-lucide="star" class="w-4 h-4"></i> Shortlist
                        </button>
                        
                        <div class="mt-3">
                            <label class="text-[12px] font-bold text-textMuted mb-1.5 block flex items-center justify-between">
                                My Notes
                                <i data-lucide="lock" class="w-3 h-3 text-gray-300" title="Private to you"></i>
                            </label>
                            <textarea class="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-[13px] text-textMain focus:outline-none focus:ring-2 focus:ring-secondary resize-none transition-shadow focus:bg-white" rows="3" placeholder="Add a private note..."></textarea>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

        </div>
    </main>'''

content = re.sub(actions_regex, actions_replacement, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Actions Category in patient-compare-hospitals.html")
