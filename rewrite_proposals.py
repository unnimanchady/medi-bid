content = '''{% extends "hospital-layout.html" %}
{% set page_title = "Proposals" %}
{% set active_page = "proposals" %}

{% block content %}
<div class="mb-8">
    <h1 class="text-[26px] sm:text-[30px] font-extrabold text-primary tracking-tight mb-2">Proposals</h1>
    <p class="text-[14.5px] text-textMuted max-w-2xl leading-relaxed">Manage treatment proposals submitted for patient requests.</p>
</div>

{% if not proposals %}
<!-- EMPTY STATE -->
<div class="bg-white rounded-[24px] border border-[#E8E8F0] border-dashed p-10 sm:p-14 flex flex-col items-center justify-center text-center shadow-premium animate-fade-in opacity-0 stagger-1">
    <div class="w-20 h-20 rounded-full bg-orange-50 flex items-center justify-center mb-5 border-[6px] border-white shadow-premium ring-1 ring-orange-100">
        <i data-lucide="file-text" class="w-8 h-8 text-[#C2410C]"></i>
    </div>
    <h3 class="text-[20px] font-extrabold text-primary mb-2">No proposals yet.</h3>
    <p class="text-[14.5px] text-textMuted max-w-[450px] mb-8 leading-relaxed font-medium">
        Treatment proposals you create for patient requests will appear here.
    </p>
    <a href="{{ url_for('hospital_treatment_requests') }}" class="bg-[#C2410C] hover:bg-[#EA580C] text-white font-bold px-8 py-3.5 rounded-full text-[14.5px] shadow-sm flex items-center gap-2 transition-all">
        View Treatment Requests <i data-lucide="arrow-right" class="w-4 h-4"></i>
    </a>
</div>
{% else %}
<!-- DESKTOP TABLE -->
<div class="hidden lg:block bg-white border border-gray-200 rounded-[20px] shadow-sm overflow-hidden animate-fade-in opacity-0 stagger-1 mb-6">
    <table class="w-full text-left border-collapse">
        <thead>
            <tr class="bg-gray-50 border-b border-gray-200 text-[12px] uppercase tracking-wider text-textMuted font-bold">
                <th class="px-6 py-4 whitespace-nowrap">Reference ID</th>
                <th class="px-6 py-4 whitespace-nowrap">Requested Treatment</th>
                <th class="px-6 py-4 whitespace-nowrap">Estimated Cost</th>
                <th class="px-6 py-4 whitespace-nowrap">Valid Until</th>
                <th class="px-6 py-4 whitespace-nowrap">Status</th>
                <th class="px-6 py-4 whitespace-nowrap text-right">Action</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
            {% for prop in proposals %}
            {% set req = prop.treatment_request %}
            <tr class="hover:bg-gray-50 transition-colors group">
                <td class="px-6 py-5">
                    <div class="font-bold text-textMain font-mono text-[14px]">{{ req.reference_id }}</div>
                    <div class="text-[12px] text-textMuted mt-1">{{ prop.created_at.strftime('%b %d, %Y') }}</div>
                </td>
                <td class="px-6 py-5">
                    <div class="text-[14.5px] font-bold text-textMain line-clamp-1 mb-1">{{ req.condition }}</div>
                    <div class="inline-flex items-center gap-1.5 text-[12.5px] text-textMuted font-medium">
                        <i data-lucide="stethoscope" class="w-3.5 h-3.5"></i> {{ req.specialty }}
                    </div>
                </td>
                <td class="px-6 py-5">
                    {% if prop.estimated_cost_min and prop.estimated_cost_max %}
                    <div class="text-[14px] font-bold text-textMain">
                        {{ prop.currency }} {{ "{:,.0f}".format(prop.estimated_cost_min) }} - {{ "{:,.0f}".format(prop.estimated_cost_max) }}
                    </div>
                    {% else %}
                    <div class="text-[14px] text-textMuted font-medium">Not provided</div>
                    {% endif %}
                </td>
                <td class="px-6 py-5">
                    <div class="text-[14px] font-medium text-textMain">
                        {{ prop.valid_until.strftime('%b %d, %Y') if prop.valid_until else 'Not specified' }}
                    </div>
                </td>
                <td class="px-6 py-5">
                    {% if prop.display_status == 'Submitted' %}
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-green-50 text-green-700 border border-green-200 text-[12px] font-bold whitespace-nowrap">
                        <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> Submitted
                    </span>
                    {% elif prop.display_status == 'Expired' %}
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-red-50 text-red-700 border border-red-200 text-[12px] font-bold whitespace-nowrap">
                        <i data-lucide="alert-circle" class="w-3.5 h-3.5"></i> Expired
                    </span>
                    {% else %}
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-orange-50 text-orange-700 border border-orange-200 text-[12px] font-bold whitespace-nowrap">
                        <i data-lucide="edit-3" class="w-3.5 h-3.5"></i> Draft
                    </span>
                    {% endif %}
                </td>
                <td class="px-6 py-5 text-right">
                    {% if prop.display_status == 'Draft' %}
                    <a href="{{ url_for('hospital_proposal_edit', reference_id=req.reference_id) }}" class="inline-flex items-center justify-center bg-white border border-gray-200 text-textMain hover:text-[#C2410C] hover:border-orange-200 hover:bg-orange-50 px-4 py-2 rounded-xl text-[13px] font-bold transition-all shadow-sm">
                        Continue Editing
                    </a>
                    {% else %}
                    <a href="{{ url_for('hospital_proposal_view', reference_id=req.reference_id) }}" class="inline-flex items-center justify-center bg-white border border-gray-200 text-textMain hover:text-[#C2410C] hover:border-orange-200 hover:bg-orange-50 px-4 py-2 rounded-xl text-[13px] font-bold transition-all shadow-sm">
                        View Proposal
                    </a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<!-- MOBILE CARDS -->
<div class="lg:hidden flex flex-col gap-4 animate-fade-in opacity-0 stagger-1 mb-6">
    {% for prop in proposals %}
    {% set req = prop.treatment_request %}
    <div class="bg-white border border-gray-200 rounded-[20px] p-5 shadow-sm hover:shadow-md transition-shadow relative">
        <div class="flex justify-between items-start mb-3">
            <div>
                <div class="font-bold text-textMain font-mono text-[14px]">{{ req.reference_id }}</div>
                <div class="text-[12px] text-textMuted mt-0.5">{{ prop.created_at.strftime('%b %d, %Y') }}</div>
            </div>
            
            {% if prop.display_status == 'Submitted' %}
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-green-50 text-green-700 border border-green-200">Submitted</span>
            {% elif prop.display_status == 'Expired' %}
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-red-50 text-red-700 border border-red-200">Expired</span>
            {% else %}
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-orange-50 text-orange-700 border border-orange-200">Draft</span>
            {% endif %}
        </div>
        
        <h3 class="text-[16px] font-bold text-primary mb-1">{{ req.condition }}</h3>
        
        <div class="flex flex-col gap-1.5 mb-4">
            <span class="text-[13px] text-textMuted flex items-center gap-2"><i data-lucide="stethoscope" class="w-4 h-4 text-gray-400"></i> {{ req.specialty }}</span>
            <span class="text-[13px] text-textMuted flex items-center gap-2">
                <i data-lucide="banknote" class="w-4 h-4 text-gray-400"></i> 
                {% if prop.estimated_cost_min and prop.estimated_cost_max %}
                {{ prop.currency }} {{ "{:,.0f}".format(prop.estimated_cost_min) }} - {{ "{:,.0f}".format(prop.estimated_cost_max) }}
                {% else %}
                Not provided
                {% endif %}
            </span>
            <span class="text-[13px] text-textMuted flex items-center gap-2"><i data-lucide="calendar" class="w-4 h-4 text-gray-400"></i> Valid until {{ prop.valid_until.strftime('%b %d, %Y') if prop.valid_until else 'N/A' }}</span>
        </div>
        
        {% if prop.display_status == 'Draft' %}
        <a href="{{ url_for('hospital_proposal_edit', reference_id=req.reference_id) }}" class="w-full inline-flex items-center justify-center bg-white border border-gray-200 text-textMain px-4 py-2.5 rounded-xl text-[14px] font-bold transition-all shadow-sm">
            Continue Editing
        </a>
        {% else %}
        <a href="{{ url_for('hospital_proposal_view', reference_id=req.reference_id) }}" class="w-full inline-flex items-center justify-center bg-white border border-gray-200 text-textMain px-4 py-2.5 rounded-xl text-[14px] font-bold transition-all shadow-sm">
            View Proposal
        </a>
        {% endif %}
    </div>
    {% endfor %}
</div>
{% endif %}
{% endblock %}
'''
with open('templates/hospital-proposals.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
