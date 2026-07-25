import re

def rewrite():
    with open('templates/patient-hospital-profile.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Title & Location
    content = re.sub(
        r'<h1 class="text-\[24px\] sm:text-\[30px\] font-extrabold text-primary leading-tight">Apollo Hospitals</h1>',
        r'<h1 class="text-[24px] sm:text-[30px] font-extrabold text-primary leading-tight">{{ hospital.display_name or hospital.legal_name or "Not provided" }}</h1>',
        content
    )
    content = re.sub(
        r'<i data-lucide="map-pin" class="w-4 h-4"></i> New Delhi, India',
        r'<i data-lucide="map-pin" class="w-4 h-4"></i> {% set loc_parts=[] %}{% if hospital.city and hospital.city != "None" %}{% set _ = loc_parts.append(hospital.city) %}{% endif %}{% if hospital.state_region and hospital.state_region != "None" %}{% set _ = loc_parts.append(hospital.state_region) %}{% endif %}{% if hospital.country and hospital.country != "None" %}{% set _ = loc_parts.append(hospital.country) %}{% endif %}{{ loc_parts|join(", ") if loc_parts else "Not provided" }}',
        content
    )
    
    # 2. Proposed Treatment
    content = re.sub(
        r'<span class="text-\[14\.5px\] font-bold text-textMain">Minimally Invasive CABG</span>',
        r'<span class="text-[14.5px] font-bold text-textMain">{{ target_req.treatment_type if target_req else "Treatment Type Not specified" }}</span>',
        content
    )
    
    # 3. Overview Text
    content = re.sub(
        r'<p class="text-\[14\.5px\] text-textMain leading-relaxed mb-4">\s*Apollo Hospitals, New Delhi is a leading comprehensive multispecialty hospital in India\. Established with the goal of bringing world-class healthcare within the reach of every individual, it is known for pioneering advanced medical procedures\.\s*</p>\s*<p class="text-\[14\.5px\] text-textMain leading-relaxed">\s*The facility integrates clinical excellence with state-of-the-art medical technology\. The international patient department is dedicated to providing seamless, personalized care for global patients traveling for specialized treatment\.\s*</p>',
        r'<p class="text-[14.5px] text-textMain leading-relaxed mb-4">{{ hospital.description or "Hospital description not provided." }}</p>',
        content
    )
    
    # 4. Quick Facts
    content = re.sub(r'<span class="font-bold text-textMain">1996</span>', r'<span class="font-bold text-textMain">{{ hospital.year_established or "Not provided" }}</span>', content)
    content = re.sub(r'<span class="font-bold text-textMain">718</span>', r'<span class="font-bold text-textMain">{{ hospital.inpatient_rooms or "Not provided" }}</span>', content)
    content = re.sub(r'<span class="font-bold text-textMain">120\+</span>', r'<span class="font-bold text-textMain">Not provided</span>', content)
    content = re.sub(r'<span class="font-bold text-textMain">24/7</span>', r'<span class="font-bold text-textMain">Not provided</span>', content)

    # ACCREDITATIONS
    acc_regex = r'(<!-- 4\. ACCREDITATION & CERTIFICATIONS -->.*?<!-- 5\. MEDICAL SPECIALTIES -->)'
    acc_replacement = """<!-- 4. ACCREDITATION & CERTIFICATIONS -->
        {% if hospital.has_accreditations %}
        <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7 opacity-0 animate-fade-in stagger-3">
            <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                <i data-lucide="award" class="w-5 h-5 text-secondary"></i> Accreditation & Certifications
            </h2>
            <div class="text-[14px] text-textMain">Accreditation information available.</div>
        </div>
        {% endif %}

        <!-- 5. MEDICAL SPECIALTIES -->"""
    content = re.sub(acc_regex, acc_replacement, content, flags=re.DOTALL)

    # MEDICAL SPECIALTIES
    spec_regex = r'(<!-- 5\. MEDICAL SPECIALTIES -->.*?<!-- 6\. DOCTORS & MEDICAL TEAM -->)'
    spec_replacement = """<!-- 5. MEDICAL SPECIALTIES -->
        {% if hospital.treatments or hospital.centers_of_excellence %}
        <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7 opacity-0 animate-fade-in stagger-3">
            <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                <i data-lucide="stethoscope" class="w-5 h-5 text-secondary"></i> Medical Specialties
            </h2>
            <div class="text-[14px] text-textMain">{{ hospital.treatments or hospital.centers_of_excellence }}</div>
        </div>
        {% endif %}

        <!-- 6. DOCTORS & MEDICAL TEAM -->"""
    content = re.sub(spec_regex, spec_replacement, content, flags=re.DOTALL)

    # DOCTORS & MEDICAL TEAM (Hide it since doctors aren't in the DB model)
    doc_regex = r'(<!-- 6\. DOCTORS & MEDICAL TEAM -->.*?<!-- 7\. INTERNATIONAL PATIENT SERVICES -->)'
    doc_replacement = """<!-- 6. DOCTORS & MEDICAL TEAM (Omitted - Not Provided) -->

        <!-- 7. INTERNATIONAL PATIENT SERVICES -->"""
    content = re.sub(doc_regex, doc_replacement, content, flags=re.DOTALL)

    # INTERNATIONAL PATIENT SERVICES
    int_regex = r'(<!-- 7\. INTERNATIONAL PATIENT SERVICES -->.*?<!-- 8\. PATIENT AMENITIES -->)'
    int_replacement = """<!-- 7. INTERNATIONAL PATIENT SERVICES -->
        {% if hospital.international_services_offered or hospital.other_languages %}
        <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7 opacity-0 animate-fade-in stagger-3">
            <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                <i data-lucide="globe" class="w-5 h-5 text-secondary"></i> International Patient Services
            </h2>
            <div class="text-[14px] text-textMain">
                <p><strong>Services:</strong> {{ hospital.international_services_offered or "Not provided" }}</p>
                <p class="mt-2"><strong>Languages:</strong> {{ hospital.other_languages or "Not provided" }}</p>
            </div>
        </div>
        {% endif %}

        <!-- 8. PATIENT AMENITIES -->"""
    content = re.sub(int_regex, int_replacement, content, flags=re.DOTALL)

    # AMENITIES
    amen_regex = r'(<!-- 8\. PATIENT AMENITIES -->.*?<!-- 9\. LOCATION & CONTACT -->)'
    amen_replacement = """<!-- 8. PATIENT AMENITIES -->
        {% if hospital.core_facilities %}
        <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7 opacity-0 animate-fade-in stagger-3">
            <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                <i data-lucide="coffee" class="w-5 h-5 text-secondary"></i> Patient Amenities
            </h2>
            <div class="text-[14px] text-textMain">{{ hospital.core_facilities }}</div>
        </div>
        {% endif %}

        <!-- 9. LOCATION & CONTACT -->"""
    content = re.sub(amen_regex, amen_replacement, content, flags=re.DOTALL)
    
    # LOCATION & CONTACT
    loc_regex = r'(<!-- 9\. LOCATION & CONTACT -->.*?<!-- HOSPITAL FLOATING ACTION BAR -->)'
    loc_replacement = """<!-- 9. LOCATION & CONTACT -->
        <div class="bg-white border border-gray-200 rounded-[16px] shadow-sm overflow-hidden p-5 sm:p-7 opacity-0 animate-fade-in stagger-3">
            <h2 class="text-[18px] font-extrabold text-primary mb-5 flex items-center gap-2">
                <i data-lucide="map" class="w-5 h-5 text-secondary"></i> Location & Contact
            </h2>
            <div class="text-[14px] text-textMain">
                <h3 class="font-bold">{{ hospital.display_name or hospital.legal_name or "Not provided" }}</h3>
                <p class="mt-2">{% set loc_parts=[] %}{% if hospital.city and hospital.city != "None" %}{% set _ = loc_parts.append(hospital.city) %}{% endif %}{% if hospital.state_region and hospital.state_region != "None" %}{% set _ = loc_parts.append(hospital.state_region) %}{% endif %}{% if hospital.country and hospital.country != "None" %}{% set _ = loc_parts.append(hospital.country) %}{% endif %}{{ loc_parts|join(", ") if loc_parts else "Not provided" }}</p>
                <p class="mt-2"><strong>Address:</strong> {{ hospital.address or "Not provided" }}</p>
            </div>
        </div>

        <!-- HOSPITAL FLOATING ACTION BAR -->"""
    content = re.sub(loc_regex, loc_replacement, content, flags=re.DOTALL)
    
    with open('templates/patient-hospital-profile.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Full Replacements done.")

if __name__ == '__main__':
    rewrite()
