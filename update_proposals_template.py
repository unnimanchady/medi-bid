import os

# Open the file
with open('templates/hospital-proposals.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Title
content = content.replace('<title>Treatment Requests | MediBid Hospital Portal</title>', '<title>Proposals | MediBid Hospital Portal</title>')

# Update Navigation active state for Treatment Requests
content = content.replace('''            <a href="{{ url_for('hospital_treatment_requests') }}" class="flex items-center gap-3 px-4 py-3 bg-blue-50 text-blue-700 font-bold rounded-xl transition-colors relative">
                <div class="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-8 bg-blue-600 rounded-r-full"></div>
                <i data-lucide="file-text" class="w-5 h-5"></i>
                <span>Treatment Requests</span>
            </a>''', '''            <a href="{{ url_for('hospital_treatment_requests') }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">
                <i data-lucide="file-text" class="w-5 h-5"></i>
                <span>Treatment Requests</span>
            </a>''')

# Update Navigation active state for Proposals
content = content.replace('''            <a href="{{ url_for('hospital_proposals') }}" class="flex items-center gap-3 px-4 py-3 text-textMuted font-semibold rounded-xl hover:bg-slate-50 hover:text-textMain transition-all">
                <i data-lucide="file-text" class="w-5 h-5"></i>
                <span>Proposals</span>
            </a>''', '''            <a href="{{ url_for('hospital_proposals') }}" class="flex items-center gap-3 px-4 py-3 bg-blue-50 text-blue-700 font-bold rounded-xl transition-colors relative">
                <div class="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-8 bg-blue-600 rounded-r-full"></div>
                <i data-lucide="file-text" class="w-5 h-5"></i>
                <span>Proposals</span>
            </a>''')

# Header Title
content = content.replace('<h1 class="text-xl font-bold text-textMain hidden md:block">Treatment Requests</h1>', '<h1 class="text-xl font-bold text-textMain hidden md:block">Proposals</h1>')

# Main Title and Subtitle
content = content.replace('<h1 class="text-3xl font-extrabold tracking-tight mb-2">Patient Requests</h1>', '<h1 class="text-3xl font-extrabold tracking-tight mb-2">Proposals</h1>')
content = content.replace('<p class="text-textMuted">Review active treatment requests that match your hospital\'s specialties.</p>', '<p class="text-textMuted">Manage treatment proposals submitted for patient requests.</p>')

# Replace the entire table area
table_content = '''<div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-wider text-textMuted font-bold">
                                <th class="px-6 py-4 whitespace-nowrap">Reference ID</th>
                                <th class="px-6 py-4 whitespace-nowrap">Specialty & Condition</th>
                                <th class="px-6 py-4 whitespace-nowrap">Patient Summary</th>
                                <th class="px-6 py-4 whitespace-nowrap">Estimated Cost</th>
                                <th class="px-6 py-4 whitespace-nowrap">Valid Until</th>
                                <th class="px-6 py-4 whitespace-nowrap">Status</th>
                                <th class="px-6 py-4 whitespace-nowrap text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            {% for prop in proposals %}
                            {% set req = prop.treatment_request %}
                            <tr class="hover:bg-slate-50 transition-colors group">
                                <td class="px-6 py-5">
                                    <div class="font-bold text-textMain font-mono text-sm">{{ req.reference_id }}</div>
                                    <div class="text-xs text-textMuted mt-1">{{ prop.created_at.strftime('%b %d, %Y') }}</div>
                                </td>
                                <td class="px-6 py-5">
                                    <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-100 text-xs font-bold mb-2">
                                        <i data-lucide="stethoscope" class="w-3.5 h-3.5"></i>
                                        {{ req.specialty }}
                                    </div>
                                    <div class="text-sm font-semibold text-textMain line-clamp-1" title="{{ req.condition }}">{{ req.condition }}</div>
                                </td>
                                <td class="px-6 py-5">
                                    <div class="text-sm font-semibold text-textMain mb-1">
                                        {{ req.patient_profile.gender|default('Unspecified', true) }}, 
                                        {% if req.patient_profile.date_of_birth %}
                                            {% set age = 2026 - req.patient_profile.date_of_birth.year - ((7, 22) < (req.patient_profile.date_of_birth.month, req.patient_profile.date_of_birth.day)) %}
                                            {{ age }} years old
                                        {% else %}
                                            Age Unknown
                                        {% endif %}
                                    </div>
                                    <div class="text-xs text-textMuted flex items-center gap-1.5">
                                        <i data-lucide="map-pin" class="w-3.5 h-3.5"></i>
                                        {{ req.patient_profile.country_of_residence|default('Unknown', true) }}
                                    </div>
                                </td>
                                <td class="px-6 py-5">
                                    {% if prop.estimated_cost_min and prop.estimated_cost_max %}
                                    <div class="text-sm font-bold text-textMain">
                                        {{ prop.currency }} {{ "{:,.0f}".format(prop.estimated_cost_min) }} - {{ "{:,.0f}".format(prop.estimated_cost_max) }}
                                    </div>
                                    {% else %}
                                    <div class="text-sm text-textMuted">Not provided</div>
                                    {% endif %}
                                </td>
                                <td class="px-6 py-5">
                                    <div class="text-sm font-semibold text-textMain">
                                        {{ prop.valid_until.strftime('%b %d, %Y') if prop.valid_until else 'Not specified' }}
                                    </div>
                                </td>
                                <td class="px-6 py-5">
                                    {% if prop.display_status == 'Submitted' %}
                                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-100 text-xs font-bold whitespace-nowrap">
                                        <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
                                        Submitted
                                    </span>
                                    {% elif prop.display_status == 'Expired' %}
                                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-red-50 text-red-700 border border-red-100 text-xs font-bold whitespace-nowrap">
                                        <i data-lucide="alert-circle" class="w-3.5 h-3.5"></i>
                                        Expired
                                    </span>
                                    {% else %}
                                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-yellow-50 text-yellow-700 border border-yellow-100 text-xs font-bold whitespace-nowrap">
                                        <i data-lucide="edit-3" class="w-3.5 h-3.5"></i>
                                        Draft
                                    </span>
                                    {% endif %}
                                </td>
                                <td class="px-6 py-5 text-right">
                                    {% if prop.display_status == 'Draft' %}
                                    <a href="{{ url_for('hospital_proposal_edit', reference_id=req.reference_id) }}" class="inline-flex items-center justify-center bg-white border border-slate-200 text-slate-700 hover:text-accent hover:border-accent hover:bg-blue-50 px-4 py-2 rounded-xl text-sm font-bold transition-all shadow-sm">
                                        Continue Editing
                                    </a>
                                    {% else %}
                                    <a href="{{ url_for('hospital_proposal_view', reference_id=req.reference_id) }}" class="inline-flex items-center justify-center bg-white border border-slate-200 text-slate-700 hover:text-accent hover:border-accent hover:bg-blue-50 px-4 py-2 rounded-xl text-sm font-bold transition-all shadow-sm">
                                        View Proposal
                                    </a>
                                    {% endif %}
                                </td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="7" class="px-6 py-20 text-center">
                                    <div class="w-16 h-16 bg-slate-50 text-slate-400 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-100">
                                        <i data-lucide="file-x" class="w-8 h-8"></i>
                                    </div>
                                    <h3 class="text-lg font-bold text-textMain mb-2">No proposals yet.</h3>
                                    <p class="text-sm text-textMuted max-w-md mx-auto mb-6">Treatment proposals you create for patient requests will appear here.</p>
                                    <a href="{{ url_for('hospital_treatment_requests') }}" class="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-bold rounded-xl hover:bg-blue-600 transition-colors shadow-sm">
                                        View Treatment Requests
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>'''

# We need to find the start and end of the <div class="overflow-x-auto"> to replace it
start_idx = content.find('<div class="overflow-x-auto">')
end_idx = content.find('</div>\n            </div>\n            \n        </div>', start_idx) + 6

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + table_content + content[end_idx:]

with open('templates/hospital-proposals.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated templates/hospital-proposals.html")
