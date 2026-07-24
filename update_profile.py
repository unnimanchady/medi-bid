import re

filepath = 'templates/patient-hospital-profile.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Header (User Info)
# Look for "Sarah Jenkins" and "sarah.j@example.com"
content = re.sub(
    r'<div class="font-bold text-\[14px\] text-textMain">.*?</div>\s*<div class="text-\[12px\] text-textMuted">.*?</div>',
    r'<div class="font-bold text-[14px] text-textMain">{{ user.first_name }} {{ user.last_name }}</div>\n                            <div class="text-[12px] text-textMuted">{{ user.email }}</div>',
    content,
    flags=re.DOTALL
)

# Back navigation
# Replace the static breadcrumb and back button.
breadcrumb_regex = r'<!-- BREADCRUMBS -->.*?</div>\s*</div>'
breadcrumb_replacement = r'''<!-- BREADCRUMBS -->
        <div class="flex items-center justify-between no-print">
            <nav class="flex items-center text-[13px] text-textMuted font-medium truncate gap-2">
                <a href="{{ url_for('patient_dashboard') }}" class="hover:text-primary transition-colors hidden sm:inline">Dashboard</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300 hidden sm:inline"></i>
                <span class="text-textMain font-bold truncate">Hospital Profile</span>
            </nav>
            <div class="flex items-center gap-4">
                {% if proposal %}
                <a href="{{ url_for('patient_treatment_proposal_details', proposal_id=proposal.id) }}" class="flex items-center gap-1.5 text-[13px] font-semibold text-secondary hover:underline focus:outline-none flex-shrink-0">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Back to Proposal</span>
                    <span class="sm:hidden">Back</span>
                </a>
                {% else %}
                <a href="{{ url_for('patient_dashboard') }}" class="flex items-center gap-1.5 text-[13px] font-semibold text-secondary hover:underline focus:outline-none flex-shrink-0">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Back to Dashboard</span>
                    <span class="sm:hidden">Back</span>
                </a>
                {% endif %}
            </div>
        </div>'''
content = re.sub(breadcrumb_regex, breadcrumb_replacement, content, flags=re.DOTALL)

# Header Section (Hospital Name, Verification, Location, Establishment)
header_regex = r'<!-- HOSPITAL HEADER -->.*?<!-- End Header -->'
header_replacement = r'''<!-- HOSPITAL HEADER -->
        <div class="bg-white border border-gray-200 rounded-[20px] p-5 sm:p-6 shadow-sm flex flex-col md:flex-row gap-6 relative overflow-hidden">
            <!-- Decorative Accent -->
            <div class="absolute top-0 left-0 w-1.5 h-full bg-secondary"></div>
            
            <div class="w-[80px] h-[80px] sm:w-[100px] sm:h-[100px] rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center flex-shrink-0 shadow-sm overflow-hidden">
                <i data-lucide="building" class="w-10 h-10 text-gray-300"></i>
            </div>
            
            <div class="flex flex-col justify-center flex-grow">
                <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h1 class="text-[24px] sm:text-[28px] font-extrabold text-primary tracking-tight leading-tight">
                                {{ hospital.display_name or hospital.legal_name }}
                            </h1>
                            {% if hospital.verification_status == 'approved' %}
                            <span class="inline-flex items-center gap-1 bg-green-50 text-green-700 px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wide border border-green-200">
                                <i data-lucide="shield-check" class="w-3 h-3"></i> Verified
                            </span>
                            {% endif %}
                        </div>
                        <p class="text-[14px] sm:text-[15px] font-medium text-textMuted flex items-center gap-2 mt-2">
                            <i data-lucide="map-pin" class="w-4 h-4 text-gray-400"></i>
                            {{ hospital.city }}, {{ hospital.country }}
                        </p>
                    </div>
                    
                    <div class="flex flex-col sm:items-end gap-2 shrink-0">
                        <div class="text-[13px] text-textMuted bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-100 whitespace-nowrap">
                            Est. <strong>{{ hospital.year_established or 'Not provided by hospital' }}</strong>
                        </div>
                        <div class="text-[13px] text-textMuted bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-100 whitespace-nowrap">
                            Type: <strong>{{ hospital.hospital_type or 'Not provided by hospital' }}</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- End Header -->'''
content = re.sub(header_regex, header_replacement, content, flags=re.DOTALL)

# Main Grid (Overview, Quick Facts, Specializations, Facilities, Services)
grid_regex = r'<!-- MAIN CONTENT GRID -->.*?(?=<!-- FLOATING ACTION BAR)'
grid_replacement = r'''<!-- MAIN CONTENT GRID -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- LEFT COLUMN (Main Details) -->
            <div class="lg:col-span-2 flex flex-col gap-6">
                
                <!-- Overview -->
                <div class="bg-white border border-gray-200 rounded-[16px] overflow-hidden shadow-sm">
                    <div class="px-5 py-4 border-b border-gray-100 bg-gray-50/50 flex items-center gap-2">
                        <i data-lucide="info" class="w-4 h-4 text-secondary"></i>
                        <h2 class="text-[16px] font-extrabold text-primary">Overview</h2>
                    </div>
                    <div class="p-5 text-[14px] text-textMain leading-relaxed space-y-4">
                        {% if hospital.description %}
                        <p>{{ hospital.description }}</p>
                        {% else %}
                        <p class="text-textMuted italic">Not provided by hospital</p>
                        {% endif %}
                    </div>
                </div>
                
                <!-- Specializations -->
                <div class="bg-white border border-gray-200 rounded-[16px] overflow-hidden shadow-sm">
                    <div class="px-5 py-4 border-b border-gray-100 bg-gray-50/50 flex items-center gap-2">
                        <i data-lucide="activity" class="w-4 h-4 text-secondary"></i>
                        <h2 class="text-[16px] font-extrabold text-primary">Centers of Excellence & Specialties</h2>
                    </div>
                    <div class="p-5">
                        {% if hospital.specialties %}
                        <div class="flex flex-wrap gap-2">
                            {% for specialty in hospital.specialties %}
                            <span class="bg-blue-50 text-secondary border border-blue-100 px-3 py-1.5 rounded-lg text-[13px] font-bold shadow-sm">
                                {{ specialty }}
                            </span>
                            {% endfor %}
                            {% if hospital.other_specialty %}
                            <span class="bg-blue-50 text-secondary border border-blue-100 px-3 py-1.5 rounded-lg text-[13px] font-bold shadow-sm">
                                {{ hospital.other_specialty }}
                            </span>
                            {% endif %}
                        </div>
                        {% else %}
                        <p class="text-[14px] text-textMuted italic">Not provided by hospital</p>
                        {% endif %}
                    </div>
                </div>

                <!-- Facilities -->
                <div class="bg-white border border-gray-200 rounded-[16px] overflow-hidden shadow-sm">
                    <div class="px-5 py-4 border-b border-gray-100 bg-gray-50/50 flex items-center gap-2">
                        <i data-lucide="stethoscope" class="w-4 h-4 text-secondary"></i>
                        <h2 class="text-[16px] font-extrabold text-primary">Medical Facilities & Equipment</h2>
                    </div>
                    <div class="p-5">
                        {% if hospital.core_facilities %}
                        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            {% for facility in hospital.core_facilities %}
                            <li class="flex items-start gap-2 text-[14px] text-textMain">
                                <i data-lucide="check-circle-2" class="w-4 h-4 text-green-500 mt-0.5 shrink-0"></i>
                                <span>{{ facility }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                        {% else %}
                        <p class="text-[14px] text-textMuted italic">Not provided by hospital</p>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- RIGHT COLUMN (Sidebar Info) -->
            <div class="flex flex-col gap-6">
                
                <!-- Quick Facts -->
                <div class="bg-white border border-gray-200 rounded-[16px] overflow-hidden shadow-sm">
                    <div class="px-5 py-4 border-b border-gray-100 bg-gray-50/50 flex items-center gap-2">
                        <i data-lucide="zap" class="w-4 h-4 text-secondary"></i>
                        <h2 class="text-[16px] font-extrabold text-primary">Quick Facts</h2>
                    </div>
                    <div class="p-5 flex flex-col gap-4">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center text-secondary shrink-0">
                                <i data-lucide="bed" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="text-[11px] font-bold text-textMuted uppercase tracking-wider">Bed Capacity</div>
                                <div class="text-[14px] font-bold text-textMain">Not provided by hospital</div>
                            </div>
                        </div>
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center text-red-500 shrink-0">
                                <i data-lucide="heart-pulse" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="text-[11px] font-bold text-textMuted uppercase tracking-wider">ICU & Emergency</div>
                                <div class="text-[14px] font-bold text-textMain">Not provided by hospital</div>
                            </div>
                        </div>
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-lg bg-green-50 flex items-center justify-center text-green-600 shrink-0">
                                <i data-lucide="award" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="text-[11px] font-bold text-textMuted uppercase tracking-wider">Accreditations</div>
                                <div class="text-[14px] font-bold text-textMain">
                                    {% if hospital.has_accreditations and hospital.accreditations %}
                                    {{ hospital.accreditations|join(', ') }}
                                    {% else %}
                                    Not provided by hospital
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- International Patient Services -->
                <div class="bg-white border border-gray-200 rounded-[16px] overflow-hidden shadow-sm">
                    <div class="px-5 py-4 border-b border-gray-100 bg-gray-50/50 flex items-center gap-2">
                        <i data-lucide="globe" class="w-4 h-4 text-secondary"></i>
                        <h2 class="text-[16px] font-extrabold text-primary">International Services</h2>
                    </div>
                    <div class="p-5">
                        {% if hospital.international_services_offered %}
                        <ul class="space-y-3">
                            {% for service in hospital.international_services_offered %}
                            <li class="flex items-start gap-2 text-[14px] text-textMain">
                                <i data-lucide="check" class="w-4 h-4 text-secondary mt-0.5 shrink-0"></i>
                                <span>{{ service }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                        {% else %}
                        <p class="text-[14px] text-textMuted italic">Not provided by hospital</p>
                        {% endif %}
                        
                        <div class="mt-5 pt-4 border-t border-gray-100">
                            <div class="text-[12px] font-bold text-textMuted mb-2 uppercase tracking-wider">Languages Spoken</div>
                            <div class="flex flex-wrap gap-1.5">
                                {% if hospital.languages %}
                                {% for lang in hospital.languages %}
                                <span class="bg-gray-100 text-textMain px-2.5 py-1 rounded text-[12px] font-medium">{{ lang }}</span>
                                {% endfor %}
                                {% if hospital.other_languages %}
                                <span class="bg-gray-100 text-textMain px-2.5 py-1 rounded text-[12px] font-medium">{{ hospital.other_languages }}</span>
                                {% endif %}
                                {% else %}
                                <span class="text-[13px] text-textMuted italic">Not provided by hospital</span>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        '''
content = re.sub(grid_regex, grid_replacement, content, flags=re.DOTALL)

# Floating Action Bar (View Proposal)
fab_regex = r'<!-- FLOATING ACTION BAR.*?</div>\s*</div>'
fab_replacement = r'''<!-- FLOATING ACTION BAR (Only if accessed via proposal) -->
        {% if proposal %}
        <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-40 md:relative md:border md:rounded-[16px] md:shadow-sm md:mt-6 md:p-5">
            <div class="max-w-[1000px] mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
                <div class="text-center md:text-left">
                    <h3 class="text-[15px] font-bold text-primary">Ready to proceed?</h3>
                    <p class="text-[13px] text-textMuted">Review their proposed treatment plan and costs.</p>
                </div>
                <a href="{{ url_for('patient_treatment_proposal_details', proposal_id=proposal.id) }}" class="w-full md:w-auto bg-primary text-white hover:bg-blue-800 font-bold px-8 py-3 rounded-xl text-[14.5px] transition-all shadow-glow hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-primary flex items-center justify-center gap-2 text-center">
                    View Treatment Proposal <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </a>
            </div>
        </div>
        {% endif %}'''
content = re.sub(fab_regex, fab_replacement, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done modifying patient-hospital-profile.html.')
