import os

def create_templates():
    with open('templates/admin-dashboard.html', 'r', encoding='utf-8') as f:
        dash_content = f.read()

    # Find where the main content starts
    content_start_marker = '<div class="p-6 md:p-10 lg:p-12 max-w-6xl mx-auto w-full">'
    content_start = dash_content.find(content_start_marker)
    
    header = dash_content[:content_start + len(content_start_marker)]
    footer = '\n    </main>\n\n    <script>\n        lucide.createIcons();\n    </script>\n</body>\n</html>\n'
    
    # --- 1. admin-patients.html ---
    patients_content = """
            <div class="mb-8">
                <h1 class="text-3xl font-extrabold text-textMain tracking-tight">Patient Management</h1>
                <p class="text-textMuted mt-1">View all registered patient accounts securely.</p>
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
        </div>
    """
    with open('templates/admin-patients.html', 'w', encoding='utf-8') as f:
        f.write(header.replace('<title>Admin Dashboard | MediBid</title>', '<title>Manage Patients | MediBid Admin</title>') + patients_content + footer)


    # --- 2. admin-patient-detail.html ---
    patient_detail_content = """
            <div class="mb-8">
                <a href="{{ url_for('admin_patients') }}" class="text-accent hover:text-blue-700 font-bold flex items-center gap-2 mb-4 transition-colors text-sm">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Patients
                </a>
                <h1 class="text-3xl font-extrabold text-textMain tracking-tight">{{ patient.first_name }} {{ patient.last_name }}</h1>
                <p class="text-textMuted mt-1">Patient Account Details</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Account Info -->
                <div class="lg:col-span-1 space-y-8">
                    <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
                        <h3 class="text-lg font-bold text-textMain mb-4 flex items-center gap-2"><i data-lucide="user" class="w-5 h-5 text-accent"></i> Account</h3>
                        <div class="space-y-4">
                            <div>
                                <p class="text-xs font-bold text-textMuted uppercase tracking-wider">Email Address</p>
                                <p class="text-textMain font-medium">{{ patient.email }}</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-textMuted uppercase tracking-wider">Phone</p>
                                <p class="text-textMain font-medium">{{ patient.phone or 'Not provided' }}</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-textMuted uppercase tracking-wider">Country of Residence</p>
                                <p class="text-textMain font-medium">{{ patient.country_of_residence or 'Not provided' }}</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-textMuted uppercase tracking-wider">Registered</p>
                                <p class="text-textMain font-medium">{{ patient.created_at.strftime('%Y-%m-%d %H:%M UTC') }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Associated Data -->
                <div class="lg:col-span-2 space-y-8">
                    <!-- Patient Profiles -->
                    <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
                        <h3 class="text-lg font-bold text-textMain mb-4 flex items-center gap-2"><i data-lucide="users" class="w-5 h-5 text-emerald-500"></i> Profiles</h3>
                        {% if profiles %}
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {% for profile in profiles %}
                            <div class="border border-slate-100 bg-slate-50 rounded-2xl p-4">
                                <div class="flex justify-between items-start mb-2">
                                    <h4 class="font-bold text-textMain">{{ profile.first_name }} {{ profile.last_name }}</h4>
                                    <span class="text-xs font-bold bg-white text-emerald-600 px-2 py-1 rounded-full border border-emerald-100 shadow-sm">{{ profile.relationship_type }}</span>
                                </div>
                                <p class="text-sm text-textMuted"><span class="font-medium text-slate-500">ID:</span> {{ profile.patient_id }}</p>
                                <p class="text-sm text-textMuted"><span class="font-medium text-slate-500">Gender:</span> {{ profile.gender }}</p>
                                <p class="text-sm text-textMuted"><span class="font-medium text-slate-500">Nationality:</span> {{ profile.nationality }}</p>
                            </div>
                            {% endfor %}
                        </div>
                        {% else %}
                        <p class="text-textMuted">No profiles created yet.</p>
                        {% endif %}
                    </div>

                    <!-- Treatment Requests -->
                    <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
                        <h3 class="text-lg font-bold text-textMain mb-4 flex items-center gap-2"><i data-lucide="file-text" class="w-5 h-5 text-purple-500"></i> Treatment Requests</h3>
                        {% if requests %}
                        <div class="overflow-x-auto">
                            <table class="w-full text-left">
                                <thead>
                                    <tr class="text-xs font-bold text-textMuted uppercase tracking-wider border-b border-slate-100">
                                        <th class="py-3">Reference</th>
                                        <th class="py-3">Specialty</th>
                                        <th class="py-3">Status</th>
                                        <th class="py-3 text-right">Proposals</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    {% for req in requests %}
                                    <tr class="hover:bg-slate-50 transition-colors">
                                        <td class="py-3 font-bold text-textMain">
                                            <a href="{{ url_for('admin_treatment_request_detail', reference_id=req.reference_id) }}" class="text-accent hover:underline">{{ req.reference_id }}</a>
                                        </td>
                                        <td class="py-3 text-textMuted">{{ req.specialty }}</td>
                                        <td class="py-3">
                                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold {% if req.status == 'Active' %}bg-emerald-100 text-emerald-700{% elif req.status == 'Pending' %}bg-amber-100 text-amber-700{% else %}bg-slate-100 text-slate-700{% endif %}">
                                                {{ req.status }}
                                            </span>
                                        </td>
                                        <td class="py-3 text-right text-textMuted font-medium">
                                            {{ req.response_count }}
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                        {% else %}
                        <p class="text-textMuted">No treatment requests submitted yet.</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    """
    with open('templates/admin-patient-detail.html', 'w', encoding='utf-8') as f:
        f.write(header.replace('<title>Admin Dashboard | MediBid</title>', '<title>Patient Details | MediBid Admin</title>') + patient_detail_content + footer)

    # --- 3. admin-proposals.html ---
    proposals_content = """
            <div class="mb-8">
                <h1 class="text-3xl font-extrabold text-textMain tracking-tight">Treatment Proposals</h1>
                <p class="text-textMuted mt-1">Review proposals submitted by hospitals to patients.</p>
            </div>

            <!-- Filters -->
            <div class="bg-white p-4 rounded-3xl border border-slate-200 shadow-sm mb-8">
                <form method="GET" class="flex flex-col md:flex-row gap-4 items-end">
                    <div class="flex-1 w-full">
                        <label class="block text-xs font-bold text-textMuted uppercase tracking-wider mb-2">Hospital</label>
                        <select name="hospital_id" class="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent font-medium">
                            <option value="">All Hospitals</option>
                            {% for h in hospitals %}
                            <option value="{{ h.id }}" {% if current_hospital == h.id|string %}selected{% endif %}>{{ h.hospital_name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="flex-1 w-full">
                        <label class="block text-xs font-bold text-textMuted uppercase tracking-wider mb-2">Status</label>
                        <select name="status" class="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent font-medium text-textMain">
                            <option value="">All Statuses</option>
                            <option value="submitted" {% if current_status == 'submitted' %}selected{% endif %}>Submitted</option>
                            <option value="draft" {% if current_status == 'draft' %}selected{% endif %}>Draft</option>
                            <option value="withdrawn" {% if current_status == 'withdrawn' %}selected{% endif %}>Withdrawn</option>
                        </select>
                    </div>
                    <div class="w-full md:w-auto">
                        <button type="submit" class="w-full md:w-auto bg-slate-800 text-white px-6 py-2.5 rounded-xl font-bold hover:bg-slate-700 transition-colors shadow-sm">Filter</button>
                    </div>
                    {% if current_hospital or current_status %}
                    <div class="w-full md:w-auto text-center">
                        <a href="{{ url_for('admin_proposals') }}" class="text-textMuted hover:text-primary font-bold px-4 py-2.5 inline-block">Clear</a>
                    </div>
                    {% endif %}
                </form>
            </div>

            <!-- Table -->
            <div class="bg-white border border-slate-200 rounded-3xl overflow-hidden shadow-sm">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-sm font-bold text-textMuted uppercase tracking-wider">
                                <th class="px-6 py-4">Request Ref</th>
                                <th class="px-6 py-4">Hospital</th>
                                <th class="px-6 py-4">Status</th>
                                <th class="px-6 py-4">Submitted</th>
                                <th class="px-6 py-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            {% for proposal in proposals %}
                            <tr class="hover:bg-slate-50/50 transition-colors group">
                                <td class="px-6 py-4 font-bold text-textMain">
                                    <a href="{{ url_for('admin_treatment_request_detail', reference_id=proposal.treatment_request.reference_id) }}" class="text-accent hover:underline">{{ proposal.treatment_request.reference_id }}</a>
                                </td>
                                <td class="px-6 py-4 font-medium text-textMain">
                                    <a href="{{ url_for('admin_application_review', hospital_id=proposal.hospital.id) }}" class="hover:text-accent transition-colors">{{ proposal.hospital.hospital_name }}</a>
                                </td>
                                <td class="px-6 py-4">
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-bold {% if proposal.status == 'submitted' %}bg-emerald-100 text-emerald-700{% elif proposal.status == 'draft' %}bg-amber-100 text-amber-700{% else %}bg-slate-100 text-slate-700{% endif %}">
                                        {{ proposal.status|title }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 text-textMuted">
                                    {{ proposal.created_at.strftime('%Y-%m-%d %H:%M') }}
                                </td>
                                <td class="px-6 py-4 text-right">
                                    {% if proposal.status == 'submitted' %}
                                    <a href="{{ url_for('admin_proposal_view', reference_id=proposal.treatment_request.reference_id, proposal_id=proposal.id) }}" class="inline-flex items-center gap-1.5 text-accent font-bold text-sm bg-blue-50 px-3 py-1.5 rounded-lg hover:bg-blue-100 transition-colors">
                                        View <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                                    </a>
                                    {% else %}
                                    <span class="text-slate-400 text-sm font-medium">N/A</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="5" class="px-6 py-12 text-center text-textMuted">
                                    <i data-lucide="file-check" class="w-8 h-8 mx-auto mb-3 text-slate-300"></i>
                                    <p class="font-medium">No proposals found matching your criteria.</p>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    """
    with open('templates/admin-proposals.html', 'w', encoding='utf-8') as f:
        f.write(header.replace('<title>Admin Dashboard | MediBid</title>', '<title>Proposals | MediBid Admin</title>') + proposals_content + footer)


if __name__ == '__main__':
    create_templates()
