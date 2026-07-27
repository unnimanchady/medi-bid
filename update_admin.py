import os
import re

sidebar_content = """<!-- admin-sidebar.html -->
<aside class="w-64 bg-primary text-slate-300 flex-col hidden md:flex sticky top-0 h-screen shrink-0">
    <div class="p-6 border-b border-slate-700/50">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
                <i data-lucide="shield-check" class="text-primary w-5 h-5"></i>
            </div>
            <span class="font-extrabold text-lg tracking-tight text-white">MediBid Admin</span>
        </div>
    </div>
    
    <nav class="flex-1 overflow-y-auto py-6 px-4 space-y-1">
        <a href="{{ url_for('admin_dashboard') }}" class="flex items-center gap-3 px-4 py-3 {% if request.endpoint == 'admin_dashboard' %}bg-slate-800 text-white font-bold{% else %}text-slate-300 hover:text-white hover:bg-slate-800/50 font-medium{% endif %} rounded-xl transition-colors">
            <i data-lucide="layout-dashboard" class="w-5 h-5 {% if request.endpoint == 'admin_dashboard' %}text-accent{% endif %}"></i>
            Dashboard
        </a>
        
        <a href="{{ url_for('admin_applications') }}" class="flex items-center justify-between px-4 py-3 {% if request.endpoint in ['admin_applications', 'admin_application_review'] %}bg-slate-800 text-white font-bold{% else %}text-slate-300 hover:text-white hover:bg-slate-800/50 font-medium{% endif %} rounded-xl transition-colors">
            <div class="flex items-center gap-3">
                <i data-lucide="clipboard-check" class="w-5 h-5 {% if request.endpoint in ['admin_applications', 'admin_application_review'] %}text-accent{% endif %}"></i>
                Hospital Applications
            </div>
            {% if pending_count and pending_count > 0 %}
            <span class="bg-accent text-white text-xs font-bold px-2 py-0.5 rounded-full">{{ pending_count }}</span>
            {% endif %}
        </a>
        
        <a href="{{ url_for('admin_treatment_requests') }}" class="flex items-center gap-3 px-4 py-3 {% if request.endpoint in ['admin_treatment_requests', 'admin_treatment_request_detail'] %}bg-slate-800 text-white font-bold{% else %}text-slate-300 hover:text-white hover:bg-slate-800/50 font-medium{% endif %} rounded-xl transition-colors">
            <i data-lucide="file-text" class="w-5 h-5 {% if request.endpoint in ['admin_treatment_requests', 'admin_treatment_request_detail'] %}text-accent{% endif %}"></i>
            Treatment Requests
        </a>
        
        <a href="{{ url_for('admin_proposals') }}" class="flex items-center gap-3 px-4 py-3 {% if request.endpoint in ['admin_proposals', 'admin_proposal_view'] %}bg-slate-800 text-white font-bold{% else %}text-slate-300 hover:text-white hover:bg-slate-800/50 font-medium{% endif %} rounded-xl transition-colors">
            <i data-lucide="file-check" class="w-5 h-5 {% if request.endpoint in ['admin_proposals', 'admin_proposal_view'] %}text-accent{% endif %}"></i>
            Submitted Proposals
        </a>
        
        <div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">
            <i data-lucide="users" class="w-5 h-5"></i>
            <span class="font-medium">Patients</span>
            <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
        </div>
        
        <div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">
            <i data-lucide="building-2" class="w-5 h-5"></i>
            <span class="font-medium">Hospitals</span>
            <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
        </div>
        
        <div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">
            <i data-lucide="message-square" class="w-5 h-5"></i>
            <span class="font-medium">Messages</span>
            <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
        </div>
        
        <div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">
            <i data-lucide="bell" class="w-5 h-5"></i>
            <span class="font-medium">Notifications</span>
            <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
        </div>
        
        <div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">
            <i data-lucide="settings" class="w-5 h-5"></i>
            <span class="font-medium">Platform Settings</span>
            <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
        </div>

        <div class="px-4 py-3 text-slate-500 flex items-center gap-3 rounded-xl cursor-not-allowed group" title="Coming Soon">
            <i data-lucide="activity" class="w-5 h-5"></i>
            <span class="font-medium">Audit Logs</span>
            <span class="ml-auto text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity">Soon</span>
        </div>
    </nav>
    
    <div class="p-4 border-t border-slate-700/50">
        <a href="{{ url_for('admin_logout') }}" class="flex items-center gap-3 px-4 py-3 text-red-400 hover:text-white hover:bg-red-500/20 font-bold rounded-xl transition-colors">
            <i data-lucide="log-out" class="w-5 h-5"></i>
            Log Out
        </a>
    </div>
</aside>
"""

with open(r'f:\projects\medi-bid\templates\admin-sidebar.html', 'w', encoding='utf-8') as f:
    f.write(sidebar_content)

template_dir = r'f:\projects\medi-bid\templates'
for fname in os.listdir(template_dir):
    if fname.startswith('admin-') and fname.endswith('.html') and fname != 'admin-sidebar.html' and fname != 'admin-login.html':
        filepath = os.path.join(template_dir, fname)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the entire <aside>...</aside> block with the include
        # Using regex dotall
        new_content = re.sub(r'<aside.*?</aside>', '{% include "admin-sidebar.html" %}', content, flags=re.DOTALL)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated sidebar in {fname}")

# Now update app.py for the admin_proposals route
app_path = r'f:\projects\medi-bid\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

old_route = """@app.route("/admin/proposals")
@admin_required
def admin_proposals():
    hospital_id = request.args.get('hospital_id')
    status_filter = request.args.get('status')
    
    query = TreatmentProposal.query.join(TreatmentRequest)
    
    if hospital_id:
        query = query.filter(TreatmentProposal.hospital_id == hospital_id)
        
    if status_filter:
        query = query.filter(TreatmentProposal.status == status_filter)
        
    proposals = query.order_by(TreatmentProposal.created_at.desc()).all()
    
    hospitals = Hospital.query.order_by(Hospital.legal_name.asc()).all()
    
    return render_template("admin-proposals.html", proposals=proposals, hospitals=hospitals, current_status=status_filter, current_hospital=hospital_id)"""

new_route = """@app.route("/admin/proposals")
@admin_required
def admin_proposals():
    q = request.args.get('q', '').strip()
    
    query = TreatmentProposal.query.join(TreatmentRequest).join(Hospital).filter(TreatmentProposal.status == 'submitted')
    
    if q:
        query = query.filter(
            db.or_(
                TreatmentRequest.reference_id.ilike(f'%{q}%'),
                Hospital.legal_name.ilike(f'%{q}%')
            )
        )
        
    proposals = query.order_by(TreatmentProposal.created_at.desc()).all()
    
    return render_template("admin-proposals.html", proposals=proposals, q=q)"""

app_content = app_content.replace(old_route, new_route)
with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_content)
print("Updated app.py")

# Now update admin-proposals.html structure
proposals_html = r'f:\projects\medi-bid\templates\admin-proposals.html'
with open(proposals_html, 'r', encoding='utf-8') as f:
    prop_content = f.read()

# Replace the Filters block and Table block
import re

# Replace Filters
prop_content = re.sub(
    r'<!-- Filters -->.*?<!-- Table -->',
    '''<!-- Filters -->
            <div class="bg-white p-4 rounded-3xl border border-slate-200 shadow-sm mb-8">
                <form method="GET" class="flex flex-col md:flex-row gap-4 items-end">
                    <div class="flex-1 w-full">
                        <label class="block text-xs font-bold text-textMuted uppercase tracking-wider mb-2">Search</label>
                        <input type="text" name="q" value="{{ q }}" placeholder="Search by Request ID or Hospital..." class="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent font-medium text-textMain">
                    </div>
                    <div class="w-full md:w-auto">
                        <button type="submit" class="w-full md:w-auto bg-slate-800 text-white px-6 py-2.5 rounded-xl font-bold hover:bg-slate-700 transition-colors shadow-sm">Search</button>
                    </div>
                    {% if q %}
                    <div class="w-full md:w-auto text-center">
                        <a href="{{ url_for('admin_proposals') }}" class="text-textMuted hover:text-primary font-bold px-4 py-2.5 inline-block">Clear</a>
                    </div>
                    {% endif %}
                </form>
            </div>

            <!-- Table -->''',
    prop_content, flags=re.DOTALL
)

# Replace Table Headers and rows
prop_content = re.sub(
    r'<table class="w-full text-left border-collapse">.*?</table>',
    '''<table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-sm font-bold text-textMuted uppercase tracking-wider">
                                <th class="px-6 py-4">Request ID</th>
                                <th class="px-6 py-4">Hospital</th>
                                <th class="px-6 py-4">Patient</th>
                                <th class="px-6 py-4">Treatment / Condition</th>
                                <th class="px-6 py-4">Estimated Cost</th>
                                <th class="px-6 py-4">Submitted Date</th>
                                <th class="px-6 py-4">Status</th>
                                <th class="px-6 py-4 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            {% for proposal in proposals %}
                            <tr class="hover:bg-slate-50/50 transition-colors group">
                                <td class="px-6 py-4 font-bold text-textMain">
                                    <a href="{{ url_for('admin_treatment_request_detail', reference_id=proposal.treatment_request.reference_id) }}" class="text-accent hover:underline">{{ proposal.treatment_request.reference_id }}</a>
                                </td>
                                <td class="px-6 py-4 font-medium text-textMain">
                                    <a href="{{ url_for('admin_application_review', hospital_id=proposal.hospital.id) }}" class="hover:text-accent transition-colors">{{ proposal.hospital.legal_name }}</a>
                                </td>
                                <td class="px-6 py-4 font-medium text-textMain">
                                    {{ proposal.treatment_request.patient_profile.first_name }} {{ proposal.treatment_request.patient_profile.last_name }}
                                </td>
                                <td class="px-6 py-4 font-medium text-textMain">
                                    {{ proposal.proposed_treatment|default(proposal.treatment_request.condition, true) }}
                                </td>
                                <td class="px-6 py-4 font-bold text-textMain">
                                    {{ proposal.currency }} {{ "{:,.0f}".format(proposal.estimated_cost_min) }} &ndash; {{ "{:,.0f}".format(proposal.estimated_cost_max) }}
                                </td>
                                <td class="px-6 py-4 text-textMuted font-medium">
                                    {{ proposal.created_at.strftime('%b %d, %Y') }}
                                </td>
                                <td class="px-6 py-4">
                                    <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-700">
                                        <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i> Submitted
                                    </span>
                                </td>
                                <td class="px-6 py-4 text-right">
                                    <a href="{{ url_for('admin_proposal_view', reference_id=proposal.treatment_request.reference_id, proposal_id=proposal.id) }}" class="inline-flex items-center gap-1.5 text-accent font-bold text-sm bg-blue-50 px-3 py-1.5 rounded-lg hover:bg-blue-100 transition-colors">
                                        View Proposal
                                    </a>
                                </td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="8" class="px-6 py-12 text-center text-textMuted">
                                    <i data-lucide="file-check" class="w-8 h-8 mx-auto mb-3 text-slate-300"></i>
                                    <p class="font-medium">No finalized proposals found.</p>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>''',
    prop_content, flags=re.DOTALL
)

with open(proposals_html, 'w', encoding='utf-8') as f:
    f.write(prop_content)

print("Updated admin-proposals.html")
