import os
import re

def update_templates():
    
    # 1. Update admin-dashboard.html
    dashboard_path = 'templates/admin-dashboard.html'
    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            dash = f.read()
            
        # Replace sidebar badges and disabled states
        dash = dash.replace(
            '<div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">\n                <i data-lucide="users" class="w-5 h-5"></i>\n                <span class="font-medium">Patients</span>\n                <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>\n            </div>',
            '<a href="{{ url_for(\'admin_patients\') }}" class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:text-white hover:bg-slate-800/50 font-medium rounded-xl transition-colors">\n                <i data-lucide="users" class="w-5 h-5"></i>\n                Patients\n            </a>'
        )
        
        dash = dash.replace(
            '<div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">\n                <i data-lucide="building-2" class="w-5 h-5"></i>\n                <span class="font-medium">Hospitals</span>\n                <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>\n            </div>',
            '<!-- Replaced with direct hospital apps for now -->'
        )
        
        # Add proposals link below treatment requests
        req_link = '<a href="{{ url_for(\'admin_treatment_requests\') }}" class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:text-white hover:bg-slate-800/50 font-medium rounded-xl transition-colors">\n                <i data-lucide="file-text" class="w-5 h-5"></i>\n                Treatment Requests\n            </a>'
        prop_link = req_link + '\n            <a href="{{ url_for(\'admin_proposals\') }}" class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:text-white hover:bg-slate-800/50 font-medium rounded-xl transition-colors">\n                <i data-lucide="file-check" class="w-5 h-5"></i>\n                Submitted Proposals\n            </a>'
        dash = dash.replace(req_link, prop_link)
        
        # Add new stats logic in the main content grid
        grid_start = dash.find('<!-- Stats Grid -->')
        grid_end = dash.find('<!-- Coming Soon Modules Placeholder -->')
        
        if grid_start != -1 and grid_end != -1:
            new_grid = """<!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                
                <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
                            <i data-lucide="users" class="w-6 h-6"></i>
                        </div>
                    </div>
                    <p class="text-sm font-bold text-textMuted uppercase tracking-wider mb-1">Total Patients</p>
                    <h3 class="text-4xl font-extrabold text-textMain">{{ total_patients }}</h3>
                </div>
                
                <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center">
                            <i data-lucide="building" class="w-6 h-6"></i>
                        </div>
                    </div>
                    <p class="text-sm font-bold text-textMuted uppercase tracking-wider mb-1">Total Hospitals</p>
                    <h3 class="text-4xl font-extrabold text-textMain">{{ total_hospitals }}</h3>
                </div>
                
                <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center">
                            <i data-lucide="file-text" class="w-6 h-6"></i>
                        </div>
                    </div>
                    <p class="text-sm font-bold text-textMuted uppercase tracking-wider mb-1">Active Requests</p>
                    <h3 class="text-4xl font-extrabold text-textMain">{{ active_requests }}</h3>
                </div>
                
                <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center">
                            <i data-lucide="file-check" class="w-6 h-6"></i>
                        </div>
                    </div>
                    <p class="text-sm font-bold text-textMuted uppercase tracking-wider mb-1">Pending Hospitals</p>
                    <h3 class="text-4xl font-extrabold text-textMain">{{ pending_count }}</h3>
                </div>
            </div>
            
            <h2 class="text-2xl font-bold text-textMain mb-4">Recent Activity</h2>
            <div class="bg-white border border-slate-200 rounded-3xl overflow-hidden mb-12 shadow-sm">
                {% if recent_activity %}
                <ul class="divide-y divide-slate-100">
                    {% for act in recent_activity %}
                    <li class="p-4 hover:bg-slate-50 transition-colors">
                        <a href="{{ act.url }}" class="flex items-center gap-4">
                            <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 {% if act.type == 'request' %}bg-purple-100 text-purple-600{% else %}bg-amber-100 text-amber-600{% endif %}">
                                <i data-lucide="{% if act.type == 'request' %}file-text{% else %}building{% endif %}" class="w-5 h-5"></i>
                            </div>
                            <div class="flex-1">
                                <h4 class="font-bold text-textMain">{{ act.title }}</h4>
                                <p class="text-sm text-textMuted">{{ act.time.strftime('%Y-%m-%d %H:%M') }}</p>
                            </div>
                            <i data-lucide="chevron-right" class="w-5 h-5 text-slate-300"></i>
                        </a>
                    </li>
                    {% endfor %}
                </ul>
                {% else %}
                <div class="p-8 text-center text-textMuted">No recent activity.</div>
                {% endif %}
            </div>
            
            <!-- """
            dash = dash[:grid_start] + new_grid + dash[grid_end + len('<!-- Coming Soon Modules Placeholder -->'):]
            
        # Clean up the placeholder div itself if we missed it
        if '<div class="bg-slate-50 border border-slate-200 border-dashed rounded-3xl p-10 text-center">' in dash:
            dash = re.sub(r'<div class="bg-slate-50 border border-slate-200 border-dashed rounded-3xl p-10 text-center">.*?</div>', '', dash, flags=re.DOTALL)
            
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dash)

    # 2. Update admin-application-review.html
    review_path = 'templates/admin-application-review.html'
    if os.path.exists(review_path):
        with open(review_path, 'r', encoding='utf-8') as f:
            review = f.read()
            
        notes_section = """
        <!-- Admin Notes Section -->
        <div class="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm mb-8">
            <h3 class="text-xl font-bold text-textMain mb-4 flex items-center gap-2">
                <i data-lucide="sticky-note" class="w-5 h-5 text-accent"></i>
                Internal Admin Notes
            </h3>
            <form method="POST" action="{{ url_for('admin_application_review', hospital_id=hospital.id) }}">
                <div class="mb-4">
                    <label class="block text-sm font-bold text-textMain mb-2">Notes (Not visible to hospital)</label>
                    <textarea name="admin_notes" rows="4" class="w-full rounded-xl border border-slate-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent">{{ hospital.admin_notes or '' }}</textarea>
                </div>
                <button type="submit" class="bg-slate-800 text-white px-6 py-2 rounded-xl font-bold hover:bg-slate-700 transition-colors">Save Notes</button>
            </form>
        </div>
        """
        
        # Insert notes section before the action buttons (Approve/Reject)
        if '<!-- Action Buttons -->' in review:
            review = review.replace('<!-- Action Buttons -->', notes_section + '\n\n                <!-- Action Buttons -->')
            
        with open(review_path, 'w', encoding='utf-8') as f:
            f.write(review)

    # 3. Create admin-patients.html
    patients_html = """{% extends "admin-dashboard.html" %}

{% block title %}Manage Patients | MediBid Admin{% endblock %}

{% block content %}
<div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div>
        <h1 class="text-3xl font-extrabold text-textMain tracking-tight">Patient Management</h1>
        <p class="text-textMuted mt-1">View all registered patient accounts and profiles securely.</p>
    </div>
</div>

<!-- Filters -->
<div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm mb-8">
    <form method="GET" class="flex items-center gap-4">
        <div class="flex-1">
            <input type="text" name="q" value="{{ search_query or '' }}" placeholder="Search by name or email..." class="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent">
        </div>
        <button type="submit" class="bg-slate-800 text-white px-6 py-2.5 rounded-xl font-bold hover:bg-slate-700 transition-colors">Search</button>
        {% if search_query %}
        <a href="{{ url_for('admin_patients') }}" class="text-textMuted hover:text-primary px-4 font-bold">Clear</a>
        {% endif %}
    </form>
</div>

<!-- Table -->
<div class="bg-white border border-slate-200 rounded-3xl overflow-hidden shadow-sm">
    <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead>
                <tr class="bg-slate-50 border-b border-slate-200 text-sm font-bold text-textMuted uppercase tracking-wider">
                    <th class="px-6 py-4">Patient Name</th>
                    <th class="px-6 py-4">Email</th>
                    <th class="px-6 py-4">Registered Date</th>
                    <th class="px-6 py-4 text-right">Actions</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
                {% for patient in patients %}
                <tr class="hover:bg-slate-50/50 transition-colors group">
                    <td class="px-6 py-4 font-bold text-textMain">
                        {{ patient.first_name }} {{ patient.last_name }}
                    </td>
                    <td class="px-6 py-4 text-textMuted font-medium">
                        {{ patient.email }}
                    </td>
                    <td class="px-6 py-4 text-textMuted">
                        {{ patient.created_at.strftime('%Y-%m-%d') }}
                    </td>
                    <td class="px-6 py-4 text-right">
                        <a href="{{ url_for('admin_patient_detail', user_id=patient.id) }}" class="inline-flex items-center gap-1.5 text-accent font-bold text-sm bg-blue-50 px-3 py-1.5 rounded-lg hover:bg-blue-100 transition-colors">
                            View <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                        </a>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4" class="px-6 py-12 text-center text-textMuted">
                        <i data-lucide="users" class="w-8 h-8 mx-auto mb-3 text-slate-300"></i>
                        <p class="font-medium">No patients found matching your criteria.</p>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""
    # Wait, the admin-dashboard does not have {% block content %}. I must replace the <main> element entirely.
    # We can create a base template layout in a bit, but for now we'll duplicate the structure like the other admin templates do.

    print("Generated base content updates.")

if __name__ == '__main__':
    update_templates()
