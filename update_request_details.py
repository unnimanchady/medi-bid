import re

with open('templates/patient-request-details.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix navigation links
c = c.replace('<a href="{{ url_for(\'patient_hospital_responses\') }}" class="px-4 py-3 rounded-xl bg-softBlue text-secondary font-bold text-[15px] flex items-center gap-3"><i data-lucide="file-text" class="w-5 h-5"></i> My Requests</a>',
'<a href="{{ url_for(\'patient_requests\') }}" class="px-4 py-3 rounded-xl bg-softBlue text-secondary font-bold text-[15px] flex items-center gap-3"><i data-lucide="file-text" class="w-5 h-5"></i> My Requests</a>')

c = c.replace('<a href="{{ url_for(\'patient_hospital_responses\') }}" class="hover:text-primary transition-colors hidden sm:block">My Requests</a>',
'<a href="{{ url_for(\'patient_requests\') }}" class="hover:text-primary transition-colors hidden sm:block">My Requests</a>')

c = c.replace('<a href="{{ url_for(\'patient_dashboard\') }}" class="flex items-center gap-1.5 text-[13px] font-semibold text-secondary hover:underline focus:outline-none">\n                            <i data-lucide="arrow-left" class="w-4 h-4"></i>\n                            <span class="hidden sm:inline">Back to My Requests</span>\n                        </a>',
'<a href="{{ url_for(\'patient_requests\') }}" class="flex items-center gap-1.5 text-[13px] font-semibold text-secondary hover:underline focus:outline-none">\n                            <i data-lucide="arrow-left" class="w-4 h-4"></i>\n                            <span class="hidden sm:inline">Back to My Requests</span>\n                        </a>')

empty_responses = """<div class="bg-bgLight border border-gray-200 rounded-[20px] p-8 sm:p-12 shadow-sm flex flex-col items-center text-center">
                        <div class="w-16 h-16 rounded-full bg-white border border-gray-200 flex items-center justify-center mb-4 shadow-sm">
                            <i data-lucide="clock" class="w-8 h-8 text-gray-400"></i>
                        </div>
                        <h4 class="text-[16px] font-bold text-textMain mb-2">No hospital responses received yet</h4>
                        <p class="text-[14px] text-textMuted max-w-[400px]">
                            We are currently matching your request with our network of healthcare providers. You will be notified as soon as proposals arrive.
                        </p>
                    </div>"""

new_responses = """{% if request.proposals and request.proposals|length > 0 %}
                    <div class="bg-blue-50 border border-blue-100 rounded-[20px] p-8 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
                        <div class="flex items-center gap-4 flex-col sm:flex-row">
                            <div class="w-16 h-16 rounded-full bg-white border border-blue-200 flex items-center justify-center shadow-sm">
                                <i data-lucide="building-2" class="w-8 h-8 text-secondary"></i>
                            </div>
                            <div>
                                <h4 class="text-[18px] font-extrabold text-primary mb-1">Good News! You have {{ request.proposals|length }} hospital {% if request.proposals|length == 1 %}response{% else %}responses{% endif %}</h4>
                                <p class="text-[14px] text-textMuted max-w-[400px]">
                                    Hospitals have reviewed your request and submitted treatment proposals for you to compare.
                                </p>
                            </div>
                        </div>
                        <a href="{{ url_for('patient_hospital_responses', reference_id=request.reference_id) }}" class="bg-secondary text-white px-6 py-3 rounded-xl font-bold hover:bg-blue-600 transition-colors shadow-sm whitespace-nowrap">
                            View Responses
                        </a>
                    </div>
                    {% else %}
                    <div class="bg-bgLight border border-gray-200 rounded-[20px] p-8 sm:p-12 shadow-sm flex flex-col items-center text-center">
                        <div class="w-16 h-16 rounded-full bg-white border border-gray-200 flex items-center justify-center mb-4 shadow-sm">
                            <i data-lucide="clock" class="w-8 h-8 text-gray-400"></i>
                        </div>
                        <h4 class="text-[16px] font-bold text-textMain mb-2">No hospital responses received yet</h4>
                        <p class="text-[14px] text-textMuted max-w-[400px]">
                            We are currently matching your request with our network of healthcare providers. You will be notified as soon as proposals arrive.
                        </p>
                    </div>
                    {% endif %}"""

c = c.replace(empty_responses, new_responses)

with open('templates/patient-request-details.html', 'w', encoding='utf-8') as f:
    f.write(c)
