import re

with open('templates/patient-compare-hospitals.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix overview statement
content = content.replace(
    'for <strong class="text-textMain">{{ target_req.treatment_type }}</strong>.',
    'for <strong class="text-textMain">{{ target_req.primary_diagnosis or target_req.treatment_category or "Treatment" }}</strong>.'
)

# 2. Fix hospital name
# It's already item.hospital.name, but maybe display_name is better if available, but name is fine.
# 3. Accreditation
content = content.replace(
    "item.hospital.accreditations or 'N/A'",
    "item.hospital.has_accreditations and 'Yes' or 'No'"
)

# 4. Founded Year
content = content.replace(
    "item.hospital.established_year or 'N/A'",
    "item.hospital.year_established or 'Not provided'"
)

# 5. Treatment Approach
content = content.replace(
    "item.proposal.treatment_approach or 'See Full Proposal'",
    "item.proposal.proposed_treatment or 'Not provided'"
)

# 6. Estimated Cost
# Replace text-[16px] font-extrabold text-primary">${{ item.proposal.estimated_cost }}</span>
# with min/max and currency.
content = re.sub(
    r'\$\{\{\s*item\.proposal\.estimated_cost\s*\}\}',
    r"{{ item.proposal.currency or '$' }}{{ item.proposal.estimated_cost_min or '0' }}{% if item.proposal.estimated_cost_max %} - {{ item.proposal.estimated_cost_max }}{% endif %}",
    content
)

# 7. Total Duration
content = content.replace(
    "{{ item.proposal.duration_weeks }} Weeks",
    "{% if item.proposal.estimated_duration_value %}{{ item.proposal.estimated_duration_value }} {{ item.proposal.estimated_duration_unit or 'Days' }}{% else %}Not provided{% endif %}"
)

# 8. Inclusions / Exclusions
content = content.replace(
    "{{ item.proposal.inclusions_exclusions }}",
    "{% if item.proposal.inclusions %}<strong>Inclusions:</strong>\n{{ item.proposal.inclusions }}\n\n{% endif %}{% if item.proposal.exclusions %}<strong>Exclusions:</strong>\n{{ item.proposal.exclusions }}{% endif %}{% if not item.proposal.inclusions and not item.proposal.exclusions %}Not provided{% endif %}"
)

# 9. Validity
content = content.replace(
    "{{ item.proposal.validity_date.strftime('%b %d, %Y') if item.proposal.validity_date else 'N/A' }}",
    "{{ item.proposal.valid_until.strftime('%b %d, %Y') if item.proposal.valid_until else 'Not specified' }}"
)

# 10. Private Notes text area value binding
# <textarea class="..." rows="3" placeholder="Add a private note..."></textarea>
content = re.sub(
    r'<textarea class="([^"]+)" rows="3" placeholder="Add a private note..."></textarea>',
    r'<textarea class="\1" rows="3" placeholder="Add a private note...">{{ item.proposal.patient_notes or "" }}</textarea>',
    content
)

# 11. Shortlist button active state
# <button class="bg-white border border-gray-200 text-textMuted hover:text-lavenderAccent font-bold px-4 py-2.5 rounded-xl text-[13.5px] transition-all hover:bg-purple-50 flex items-center justify-center gap-2 w-full focus:outline-none">
content = re.sub(
    r'<button class="bg-white border border-gray-200 text-textMuted hover:text-lavenderAccent font-bold px-4 py-2.5 rounded-xl text-\[13.5px\] transition-all hover:bg-purple-50 flex items-center justify-center gap-2 w-full focus:outline-none">\s*<i data-lucide="star" class="w-4 h-4"></i> Shortlist\s*</button>',
    r'''<button class="bg-white border border-gray-200 font-bold px-4 py-2.5 rounded-xl text-[13.5px] transition-all flex items-center justify-center gap-2 w-full focus:outline-none {% if item.proposal.patient_shortlisted %}bg-softLavender text-lavenderAccent border-purple-100 hover:bg-purple-100{% else %}text-textMuted hover:text-lavenderAccent hover:bg-purple-50{% endif %}">
                                <i data-lucide="star" class="w-4 h-4 {% if item.proposal.patient_shortlisted %}fill-lavenderAccent{% endif %}"></i> {% if item.proposal.patient_shortlisted %}Shortlisted{% else %}Shortlist{% endif %}
                            </button>''',
    content
)

with open('templates/patient-compare-hospitals.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
