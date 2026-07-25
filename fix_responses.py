with open('templates/patient-hospital-responses.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Location
c = c.replace(
    '<i data-lucide="map-pin" class="w-4 h-4"></i> {{ response.hospital.city }}, {{ response.hospital.country }}',
    '''<i data-lucide="map-pin" class="w-4 h-4"></i> {% if response.hospital.city and response.hospital.country %}{{ response.hospital.city }}, {{ response.hospital.country }}{% elif response.hospital.country %}{{ response.hospital.country }}{% elif response.hospital.city %}{{ response.hospital.city }}{% else %}Not provided{% endif %}'''
)

# 2. Duration
c = c.replace(
    '<span class="font-bold text-primary">{{ response.estimated_duration_value }} {{ response.estimated_duration_unit }}s</span>',
    '''<span class="font-bold text-primary">{% if response.estimated_duration_value and response.estimated_duration_unit %}{{ response.estimated_duration_value }} {{ response.estimated_duration_unit }}{% if response.estimated_duration_value != 1 and response.estimated_duration_value != '1' %}s{% endif %}{% else %}Not provided{% endif %}</span>'''
)

# 3. Submitted Date
c = c.replace(
    '<span class="font-bold text-primary">{{ (response.submitted_at.strftime(\'%b %d, %Y\') if response.submitted_at else \'Unknown\') }}</span>',
    '''<span class="font-bold text-primary">{% if response.submitted_at %}{{ response.submitted_at.strftime('%b %d, %Y') }}{% else %}Not provided{% endif %}</span>'''
)

# 4. Shortlisted Count
c = c.replace(
    '''<div class="bg-softLavender border border-purple-50 rounded-[16px] p-4 flex flex-col justify-center min-w-[120px] flex-1">
                    <span class="text-[12px] font-bold text-lavenderAccent uppercase tracking-wide mb-1">Shortlisted</span>
                    <span class="text-[24px] font-extrabold text-primary leading-none">0</span>
                </div>''',
    '''<div class="bg-softLavender border border-purple-50 rounded-[16px] p-4 flex flex-col justify-center min-w-[120px] flex-1">
                    <span class="text-[12px] font-bold text-lavenderAccent uppercase tracking-wide mb-1">Shortlisted</span>
                    <span class="text-[24px] font-extrabold text-primary leading-none">{{ responses|selectattr('patient_shortlisted')|list|length }}</span>
                </div>'''
)

with open('templates/patient-hospital-responses.html', 'w', encoding='utf-8') as f:
    f.write(c)
