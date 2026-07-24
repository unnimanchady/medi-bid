import os

with open('templates/patient-hospital-profile.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

main_idx = -1
footer_idx = -1
for i, line in enumerate(lines):
    if '<!-- MAIN CONTENT -->' in line: main_idx = i
    if '<!-- FOOTER -->' in line: footer_idx = i

if main_idx != -1 and footer_idx != -1:
    new_main = """    <!-- MAIN CONTENT -->
    <main class="flex-grow w-full max-w-[850px] mx-auto py-6 sm:py-8 px-4 sm:px-6 flex flex-col gap-6">
        
        <!-- BREADCRUMBS & TOP NAVIGATION -->
        <div class="flex items-center justify-between opacity-0 animate-fade-in">
            <nav class="flex items-center text-[13px] text-textMuted font-medium truncate gap-2" aria-label="Breadcrumb">
                <a href="{{ url_for('patient_dashboard') }}" class="hover:text-primary transition-colors hidden sm:inline">Dashboard</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300 hidden sm:inline"></i>
                <a href="{{ url_for('patient_hospital_responses') }}" class="hover:text-primary transition-colors hidden md:inline">Hospital Responses</a>
                <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-gray-300 hidden md:inline"></i>
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
                <a href="{{ url_for('patient_hospital_responses') }}" class="flex items-center gap-1.5 text-[13px] font-semibold text-secondary hover:underline focus:outline-none flex-shrink-0">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Back</span>
                </a>
                {% endif %}
            </div>
        </div>

        <!-- 1. HOSPITAL IDENTITY & VERIFICATION HERO -->
        <div class="bg-white rounded-[20px] shadow-sm border border-gray-200 overflow-hidden relative opacity-0 animate-fade-in stagger-1">
            <div class="h-24 sm:h-32 bg-gray-50 relative overflow-hidden flex items-center justify-center">
                <div class="absolute inset-0 bg-primary opacity-[0.02]">
                    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" stroke-width="1"/></pattern></defs>
                        <rect width="100%" height="100%" fill="url(#grid)" />
                    </svg>
                </div>
            </div>
            
            <div class="px-5 sm:px-8 pb-6 sm:pb-8 relative pt-12 sm:pt-14">
                <div class="absolute -top-12 sm:-top-16 left-5 sm:left-8 w-24 h-24 sm:w-28 sm:h-28 bg-white rounded-2xl border-4 border-white shadow-card flex items-center justify-center overflow-hidden z-10">
                    <i data-lucide="building-2" class="w-10 h-10 sm:w-12 sm:h-12 text-primary opacity-50"></i>
                </div>
                
                <div class="flex flex-col md:flex-row md:items-start justify-between gap-4 mt-2">
                    <div class="flex flex-col">
                        <h1 class="text-[24px] sm:text-[30px] font-extrabold text-primary leading-tight">{{ hospital.display_name or hospital.legal_name }}</h1>
                        <div class="text-[14px] text-textMuted flex items-center gap-1.5 mt-1.5 font-medium">
                            <i data-lucide="map-pin" class="w-4 h-4"></i> {{ hospital.city }}, {{ hospital.country }}
                        </div>
                    </div>
                    
                    <div class="flex flex-col gap-2 md:items-end">
                        {% if hospital.verification_status == 'approved' %}
                        <div class="flex items-center gap-1.5 bg-softGreen border border-green-200 text-green-800 px-3 py-1.5 rounded-lg uppercase text-[11px] font-bold tracking-wider relative group cursor-help shadow-sm">
                            <i data-lucide="shield-check" class="w-4 h-4"></i> Verified by MediBid
                            <div class="absolute top-full right-0 mt-2 w-[280px] bg-gray-800 text-white text-[12.5px] p-4 rounded-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 text-left font-normal normal-case leading-relaxed shadow-floating">
                                Verification indicates that MediBid has reviewed selected healthcare provider information according to its verification process. It is not a medical endorsement.
                            </div>
                        </div>
                        {% endif %}
                        <div class="flex flex-wrap gap-2 md:justify-end mt-1">
                            <span class="text-[12px] bg-gray-50 border border-gray-200 px-2.5 py-1 rounded-md text-textMuted font-semibold">{{ hospital.hospital_type or 'Not provided' }}</span>
                            {% if hospital.has_accreditations and hospital.accreditations %}
                            <span class="text-[12px] bg-gray-50 border border-gray-200 px-2.5 py-1 rounded-md text-textMuted font-semibold">{{ hospital.accreditations[0] }} Accredited</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        {% if proposal %}
        <!-- 2. RELEVANT TO YOUR TREATMENT REQUEST -->
        <div class="bg-softBlue/30 border border-blue-100 rounded-[16px] p-5 shadow-sm opacity-0 animate-fade-in stagger-2">
            <h2 class="text-[13px] font-bold text-primary mb-3 flex items-center gap-2 uppercase tracking-wider">
                <i data-lucide="file-text" class="w-4 h-4 text-secondary"></i> Relevant to Your Request
            </h2>
            <div class="flex flex-col sm:flex-row items-center justify-between bg-white rounded-xl p-4 border border-blue-50 shadow-sm gap-4">
                <div class="flex flex-col gap-1 w-full sm:w-auto">
                    <span class="text-[12px] text-textMuted font-medium">Proposed Treatment</span>
                    <span class="text-[14.5px] font-bold text-textMain">{{ proposal.treatment_request.condition or 'Not specified' }}</span>
                    <div class="text-[12.5px] font-bold text-secondary bg-softBlue px-2.5 py-0.5 rounded-md inline-flex items-center gap-1.5 w-max mt-1">
                        <i data-lucide="clock" class="w-3.5 h-3.5"></i> Under Consideration
                    </div>
                </div>
                <div class="w-full sm:w-auto">
                    <a href="{{ url_for('patient_treatment_proposal_details', proposal_id=proposal.id) }}" class="w-full sm:w-auto bg-white border border-gray-200 hover:border-secondary hover:text-secondary text-textMain text-[13.5px] font-bold px-5 py-2.5 rounded-xl transition-colors focus:outline-none flex justify-center text-center shadow-sm">
                        View Proposal
                    </a>
                </div>
            </div>
        </div>
        {% endif %}

        <!-- 3. HOSPITAL OVERVIEW -->
        <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7 opacity-0 animate-fade-in stagger-3">
            <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                <i data-lucide="building" class="w-5 h-5 text-secondary"></i> Hospital Overview
            </h2>
            
            <div class="flex flex-col md:flex-row gap-8">
                <!-- About Text -->
                <div class="md:w-3/5">
                    {% if hospital.description %}
                    <p class="text-[14.5px] text-textMain leading-relaxed mb-4">{{ hospital.description }}</p>
                    {% else %}
                    <p class="text-[14.5px] text-textMuted italic leading-relaxed mb-4">Not provided by hospital</p>
                    {% endif %}
                    <div class="mt-4 flex items-center gap-1.5 text-[11.5px] text-textMuted italic">
                        <i data-lucide="info" class="w-3.5 h-3.5"></i> Information provided by hospital.
                    </div>
                </div>
                
                <!-- Quick Summary -->
                <div class="md:w-2/5 bg-gray-50 rounded-xl border border-gray-100 p-5">
                    <h3 class="text-[12px] font-bold text-textMuted uppercase mb-4 tracking-widest">Quick Facts</h3>
                    <div class="flex flex-col gap-3">
                        <div class="flex justify-between items-center text-[14px]">
                            <span class="text-textMuted font-medium">Established</span>
                            <span class="font-bold text-textMain">{{ hospital.year_established or 'Not provided' }}</span>
                        </div>
                        <div class="w-full h-px bg-gray-200"></div>
                        <div class="flex justify-between items-center text-[14px]">
                            <span class="text-textMuted font-medium">Bed Capacity</span>
                            <span class="font-bold text-textMain">Not provided by hospital</span>
                        </div>
                        <div class="w-full h-px bg-gray-200"></div>
                        <div class="flex justify-between items-center text-[14px]">
                            <span class="text-textMuted font-medium">ICU Beds</span>
                            <span class="font-bold text-textMain">Not provided by hospital</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 opacity-0 animate-fade-in stagger-4">
            <!-- LEFT COLUMN (Details) -->
            <div class="lg:col-span-2 flex flex-col gap-6">
                <!-- Specializations -->
                <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7">
                    <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                        <i data-lucide="activity" class="w-5 h-5 text-secondary"></i> Centers of Excellence & Specialties
                    </h2>
                    {% if hospital.specialties %}
                    <div class="flex flex-wrap gap-2.5">
                        {% for specialty in hospital.specialties %}
                        <span class="bg-blue-50 text-secondary border border-blue-100 px-3 py-1.5 rounded-lg text-[13.5px] font-bold shadow-sm">{{ specialty }}</span>
                        {% endfor %}
                        {% if hospital.other_specialty %}
                        <span class="bg-blue-50 text-secondary border border-blue-100 px-3 py-1.5 rounded-lg text-[13.5px] font-bold shadow-sm">{{ hospital.other_specialty }}</span>
                        {% endif %}
                    </div>
                    {% else %}
                    <p class="text-[14px] text-textMuted italic">Not provided by hospital</p>
                    {% endif %}
                </div>
                
                <!-- Facilities -->
                <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7">
                    <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                        <i data-lucide="stethoscope" class="w-5 h-5 text-secondary"></i> Medical Facilities & Equipment
                    </h2>
                    {% if hospital.core_facilities %}
                    <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {% for facility in hospital.core_facilities %}
                        <li class="flex items-start gap-2 text-[14.5px] text-textMain">
                            <i data-lucide="check-circle-2" class="w-4.5 h-4.5 text-green-500 mt-0.5 flex-shrink-0"></i>
                            <span>{{ facility }}</span>
                        </li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <p class="text-[14px] text-textMuted italic">Not provided by hospital</p>
                    {% endif %}
                </div>
                
                <!-- Photos/Gallery (Not in DB currently) -->
                <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7">
                    <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                        <i data-lucide="image" class="w-5 h-5 text-secondary"></i> Hospital Gallery
                    </h2>
                    <p class="text-[14px] text-textMuted italic">Not provided by hospital</p>
                </div>
            </div>

            <!-- RIGHT COLUMN (Sidebar) -->
            <div class="flex flex-col gap-6">
                <!-- International Services -->
                <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7">
                    <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                        <i data-lucide="globe" class="w-5 h-5 text-secondary"></i> International Patient Services
                    </h2>
                    {% if hospital.international_services_offered %}
                    <ul class="space-y-3">
                        {% for service in hospital.international_services_offered %}
                        <li class="flex items-start gap-2.5 text-[14.5px] text-textMain">
                            <i data-lucide="check" class="w-4 h-4 text-secondary mt-0.5 flex-shrink-0"></i>
                            <span>{{ service }}</span>
                        </li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <p class="text-[14px] text-textMuted italic">Not provided by hospital</p>
                    {% endif %}
                    
                    <div class="mt-6 pt-5 border-t border-gray-100">
                        <h3 class="text-[12px] font-bold text-textMuted uppercase mb-3 tracking-widest">Languages Spoken</h3>
                        <div class="flex flex-wrap gap-2">
                            {% if hospital.languages %}
                            {% for lang in hospital.languages %}
                            <span class="bg-gray-100 text-textMain px-2.5 py-1 rounded-[6px] text-[13px] font-medium border border-gray-200">{{ lang }}</span>
                            {% endfor %}
                            {% if hospital.other_languages %}
                            <span class="bg-gray-100 text-textMain px-2.5 py-1 rounded-[6px] text-[13px] font-medium border border-gray-200">{{ hospital.other_languages }}</span>
                            {% endif %}
                            {% else %}
                            <span class="text-[13px] text-textMuted italic">Not provided by hospital</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>
"""
    new_lines = lines[:main_idx] + [new_main] + lines[footer_idx:]
    with open('templates/patient-hospital-profile.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Rewritten MAIN CONTENT.")
