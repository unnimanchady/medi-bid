import re

with open('templates/patient-hospital-profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace line 28 block
old_1 = """                <a href="{{ url_for('patient_treatment_proposal_details') }}" class="flex items-center gap-1.5 text-[13px] font-semibold text-secondary hover:underline focus:outline-none flex-shrink-0">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Proposal
                </a>"""
new_1 = """                {% if proposal %}
                <a href="{{ url_for('patient_treatment_proposal_details', proposal_id=proposal.id) }}" class="flex items-center gap-1.5 text-[13px] font-semibold text-secondary hover:underline focus:outline-none flex-shrink-0">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Proposal
                </a>
                {% endif %}"""

# Replace line 100 block
old_2 = """                    <a href="{{ url_for('patient_treatment_proposal_details') }}" class="w-full sm:w-auto bg-white border border-gray-200 hover:border-secondary hover:text-secondary text-textMain text-[13.5px] font-bold px-5 py-2.5 rounded-xl transition-colors focus:outline-none flex justify-center text-center shadow-sm">
                        View Proposal
                    </a>"""
new_2 = """                    {% if proposal %}
                    <a href="{{ url_for('patient_treatment_proposal_details', proposal_id=proposal.id) }}" class="w-full sm:w-auto bg-white border border-gray-200 hover:border-secondary hover:text-secondary text-textMain text-[13.5px] font-bold px-5 py-2.5 rounded-xl transition-colors focus:outline-none flex justify-center text-center shadow-sm">
                        View Proposal
                    </a>
                    {% endif %}"""

# Replace line 425 block
old_3 = """                <a href="{{ url_for('patient_treatment_proposal_details') }}" class="w-full md:w-auto bg-primary text-white hover:bg-blue-800 font-bold px-8 py-3 rounded-xl text-[14.5px] transition-all shadow-glow hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-primary flex items-center justify-center gap-2 text-center">
                    View Treatment Proposal <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </a>"""
new_3 = """                {% if proposal %}
                <a href="{{ url_for('patient_treatment_proposal_details', proposal_id=proposal.id) }}" class="w-full md:w-auto bg-primary text-white hover:bg-blue-800 font-bold px-8 py-3 rounded-xl text-[14.5px] transition-all shadow-glow hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-primary flex items-center justify-center gap-2 text-center">
                    View Treatment Proposal <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </a>
                {% endif %}"""

content = content.replace(old_1, new_1)
content = content.replace(old_2, new_2)
content = content.replace(old_3, new_3)

with open('templates/patient-hospital-profile.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated patient-hospital-profile.html successfully.')
