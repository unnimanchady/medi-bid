import os

html_content = '''{% extends "hospital-layout.html" %}
{% set page_title = "Treatment Requests" %}
{% set active_page = "requests" %}

{% block content %}
<div class="mb-8">
    <h1 class="text-[26px] sm:text-[30px] font-extrabold text-primary tracking-tight mb-2">Patient Requests</h1>
    <p class="text-[14.5px] text-textMuted max-w-2xl leading-relaxed">Review active treatment requests from patients globally. You can filter and search to find specific cases.</p>
</div>

<!-- Search & Filters -->
<form action="{{ url_for('hospital_treatment_requests') }}" method="GET" class="bg-white rounded-[20px] border border-gray-200 p-5 shadow-sm mb-6 flex flex-col md:flex-row gap-4 items-center justify-between animate-fade-in opacity-0">
    <div class="relative w-full md:w-[350px]">
        <i data-lucide="search" class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"></i>
        <input type="text" name="search" value="{{ search }}" placeholder="Search by Reference ID or Treatment..." class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-[14px] focus:outline-none focus:ring-2 focus:ring-[#C2410C] focus:bg-white transition-all">
    </div>
    <div class="flex items-center gap-3 w-full md:w-auto overflow-x-auto pb-1 md:pb-0">
        <select name="category" class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-[14px] text-textMain font-medium focus:outline-none focus:ring-2 focus:ring-[#C2410C] min-w-[140px]">
            <option value="">All Specialties</option>
            <option value="Cardiology" {% if category == 'Cardiology' %}selected{% endif %}>Cardiology</option>
            <option value="Oncology" {% if category == 'Oncology' %}selected{% endif %}>Oncology</option>
            <option value="Neurology" {% if category == 'Neurology' %}selected{% endif %}>Neurology</option>
            <option value="Orthopedics" {% if category == 'Orthopedics' %}selected{% endif %}>Orthopedics</option>
        </select>
        <select name="country" class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-[14px] text-textMain font-medium focus:outline-none focus:ring-2 focus:ring-[#C2410C] min-w-[140px]">
            <option value="">All Countries</option>
            <option value="United States" {% if country == 'United States' %}selected{% endif %}>United States</option>
            <option value="United Kingdom" {% if country == 'United Kingdom' %}selected{% endif %}>United Kingdom</option>
            <option value="Canada" {% if country == 'Canada' %}selected{% endif %}>Canada</option>
            <option value="India" {% if country == 'India' %}selected{% endif %}>India</option>
        </select>
        <select name="sort" class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-[14px] text-textMain font-medium focus:outline-none focus:ring-2 focus:ring-[#C2410C] min-w-[120px]">
            <option value="newest" {% if sort == 'newest' %}selected{% endif %}>Newest</option>
            <option value="oldest" {% if sort == 'oldest' %}selected{% endif %}>Oldest</option>
        </select>
        <button type="submit" class="flex items-center gap-2 px-6 py-3 bg-[#C2410C] hover:bg-[#EA580C] text-white rounded-xl text-[14px] font-bold transition-colors whitespace-nowrap shadow-sm">
            <i data-lucide="filter" class="w-4 h-4"></i> Apply
        </button>
    </div>
</form>

{% if not requests.items %}
<!-- EMPTY STATE -->
<div class="bg-white rounded-[24px] border border-[#E8E8F0] border-dashed p-10 sm:p-14 flex flex-col items-center justify-center text-center shadow-premium animate-fade-in opacity-0 stagger-1">
    <div class="w-20 h-20 rounded-full bg-orange-50 flex items-center justify-center mb-5 border-[6px] border-white shadow-premium ring-1 ring-orange-100">
        <i data-lucide="file-x" class="w-8 h-8 text-[#C2410C]"></i>
    </div>
    <h3 class="text-[20px] font-extrabold text-primary mb-2">No matching treatment requests available.</h3>
    <p class="text-[14.5px] text-textMuted max-w-[450px] mb-8 leading-relaxed font-medium">
        Try adjusting your search filters or check back later.
    </p>
    <a href="{{ url_for('hospital_treatment_requests') }}" class="bg-white border border-gray-200 text-textMain font-bold px-8 py-3.5 rounded-full text-[14.5px] hover:bg-gray-50 shadow-sm flex items-center gap-2 transition-all">
        <i data-lucide="refresh-cw" class="w-4 h-4"></i> Reset Filters
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
                <th class="px-6 py-4 whitespace-nowrap">Patient Country</th>
                <th class="px-6 py-4 whitespace-nowrap">Submission Date</th>
                <th class="px-6 py-4 whitespace-nowrap">Proposal Status</th>
                <th class="px-6 py-4 whitespace-nowrap text-right">Action</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
            {% for req in requests.items %}
            <tr class="hover:bg-gray-50 transition-colors group">
                <td class="px-6 py-5">
                    <div class="font-bold text-textMain font-mono text-[14px]">{{ req.reference_id }}</div>
                    {% if req.priority == 'High' %}
                    <div class="inline-flex items-center gap-1 mt-1 text-[11px] font-bold text-red-600 uppercase">
                        <i data-lucide="alert-circle" class="w-3 h-3"></i> High Priority
                    </div>
                    {% endif %}
                </td>
                <td class="px-6 py-5">
                    <div class="text-[14.5px] font-bold text-textMain line-clamp-1 mb-1">{{ req.condition }}</div>
                    <div class="inline-flex items-center gap-1.5 text-[12.5px] text-textMuted font-medium">
                        <i data-lucide="stethoscope" class="w-3.5 h-3.5"></i> {{ req.specialty }}
                    </div>
                </td>
                <td class="px-6 py-5">
                    <div class="flex items-center gap-2 text-[14px] text-textMain font-medium">
                        <i data-lucide="map-pin" class="w-4 h-4 text-gray-400"></i>
                        {{ req.patient_profile.country_of_residence|default('Unknown', true) }}
                    </div>
                </td>
                <td class="px-6 py-5">
                    <div class="text-[14px] text-textMain font-medium">{{ req.created_at.strftime('%b %d, %Y') if req.created_at else 'N/A' }}</div>
                </td>
                <td class="px-6 py-5">
                    {% set proposal = hospital_proposals.get(req.id) %}
                    {% if proposal and proposal.status != 'draft' %}
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-green-50 text-green-700 border border-green-200 text-[12px] font-bold whitespace-nowrap">
                            <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i> Submitted
                        </span>
                    {% elif proposal and proposal.status == 'draft' %}
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-orange-50 text-orange-700 border border-orange-200 text-[12px] font-bold whitespace-nowrap">
                            <i data-lucide="edit-3" class="w-3.5 h-3.5"></i> Draft Saved
                        </span>
                    {% else %}
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200 text-[12px] font-bold whitespace-nowrap">
                            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> Needs Action
                        </span>
                    {% endif %}
                </td>
                <td class="px-6 py-5 text-right">
                    <a href="{{ url_for('hospital_treatment_request_detail', reference_id=req.reference_id) }}" class="inline-flex items-center justify-center bg-white border border-gray-200 text-textMain hover:text-[#C2410C] hover:border-orange-200 hover:bg-orange-50 px-4 py-2 rounded-xl text-[13px] font-bold transition-all shadow-sm">
                        View Details
                    </a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<!-- MOBILE CARDS -->
<div class="lg:hidden flex flex-col gap-4 animate-fade-in opacity-0 stagger-1 mb-6">
    {% for req in requests.items %}
    <div class="bg-white border border-gray-200 rounded-[20px] p-5 shadow-sm hover:shadow-md transition-shadow relative">
        <div class="flex justify-between items-start mb-3">
            <div>
                <div class="font-bold text-textMain font-mono text-[14px]">{{ req.reference_id }}</div>
                <div class="text-[12px] text-textMuted mt-0.5">{{ req.created_at.strftime('%b %d, %Y') if req.created_at else 'N/A' }}</div>
            </div>
            
            {% set proposal = hospital_proposals.get(req.id) %}
            {% if proposal and proposal.status != 'draft' %}
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-green-50 text-green-700 border border-green-200">Submitted</span>
            {% elif proposal and proposal.status == 'draft' %}
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-orange-50 text-orange-700 border border-orange-200">Draft Saved</span>
            {% else %}
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-blue-50 text-blue-700 border border-blue-200">Needs Action</span>
            {% endif %}
        </div>
        
        <h3 class="text-[16px] font-bold text-primary mb-1">{{ req.condition }}</h3>
        
        <div class="flex flex-col gap-1.5 mb-4">
            <span class="text-[13px] text-textMuted flex items-center gap-2"><i data-lucide="stethoscope" class="w-4 h-4 text-gray-400"></i> {{ req.specialty }}</span>
            <span class="text-[13px] text-textMuted flex items-center gap-2"><i data-lucide="map-pin" class="w-4 h-4 text-gray-400"></i> {{ req.patient_profile.country_of_residence|default('Unknown', true) }}</span>
            {% if req.priority == 'High' %}
            <span class="text-[12px] font-bold text-red-600 flex items-center gap-2 uppercase mt-1"><i data-lucide="alert-circle" class="w-3.5 h-3.5"></i> High Priority</span>
            {% endif %}
        </div>
        
        <a href="{{ url_for('hospital_treatment_request_detail', reference_id=req.reference_id) }}" class="w-full inline-flex items-center justify-center bg-white border border-gray-200 text-textMain px-4 py-2.5 rounded-xl text-[14px] font-bold transition-all shadow-sm">
            View Details
        </a>
    </div>
    {% endfor %}
</div>

<!-- PAGINATION -->
<div class="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white border border-gray-200 rounded-[20px] p-5 shadow-sm animate-fade-in opacity-0 stagger-2">
    <div class="text-[14px] text-textMuted font-medium">
        Showing <span class="font-bold text-textMain">{{ (requests.page - 1) * requests.per_page + 1 }}</span> to 
        <span class="font-bold text-textMain">{{ [(requests.page * requests.per_page), requests.total]|min }}</span> of 
        <span class="font-bold text-textMain">{{ requests.total }}</span> requests
    </div>
    
    <div class="flex items-center gap-2">
        {% if requests.has_prev %}
        <a href="{{ url_for('hospital_treatment_requests', page=requests.prev_num, search=search, category=category, country=country, sort=sort) }}" class="p-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-textMain focus:outline-none focus:ring-2 focus:ring-[#C2410C]">
            <i data-lucide="chevron-left" class="w-4 h-4"></i>
        </a>
        {% else %}
        <button disabled class="p-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-400 cursor-not-allowed">
            <i data-lucide="chevron-left" class="w-4 h-4"></i>
        </button>
        {% endif %}
        
        <div class="flex items-center gap-1">
            {% for page_num in requests.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}
                {% if page_num %}
                    {% if requests.page == page_num %}
                    <span class="w-9 h-9 flex items-center justify-center bg-[#C2410C] text-white font-bold rounded-lg text-[14px] shadow-sm">{{ page_num }}</span>
                    {% else %}
                    <a href="{{ url_for('hospital_treatment_requests', page=page_num, search=search, category=category, country=country, sort=sort) }}" class="w-9 h-9 flex items-center justify-center bg-white border border-gray-200 hover:bg-gray-50 text-textMain font-bold rounded-lg text-[14px] transition-colors focus:outline-none focus:ring-2 focus:ring-[#C2410C]">{{ page_num }}</a>
                    {% endif %}
                {% else %}
                    <span class="w-9 h-9 flex items-center justify-center text-gray-400 font-bold">...</span>
                {% endif %}
            {% endfor %}
        </div>
        
        {% if requests.has_next %}
        <a href="{{ url_for('hospital_treatment_requests', page=requests.next_num, search=search, category=category, country=country, sort=sort) }}" class="p-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-textMain focus:outline-none focus:ring-2 focus:ring-[#C2410C]">
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
        </a>
        {% else %}
        <button disabled class="p-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-400 cursor-not-allowed">
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
        </button>
        {% endif %}
    </div>
</div>

{% endif %}
{% endblock %}

{% block page_scripts %}
<script>
    lucide.createIcons();
</script>
{% endblock %}
'''

with open('templates/hospital-treatment-requests.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated hospital-treatment-requests.html successfully!")
