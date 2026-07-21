import re

with open("templates/patient-hospital-responses.html", "r", encoding="utf-8") as f:
    content = f.read()

pattern_responses = r'(<!-- HOSPITAL RESPONSE LIST -->\s*<div class="flex flex-col gap-6 opacity-0 animate-fade-in stagger-3">).*?(</div>\s*</main>)'

replacement_responses = r'''\1
            {% if responses %}
                {% for response in responses %}
                    <!-- Render response -->
                {% endfor %}
            {% else %}
            <!-- No Responses State -->
            <div class="bg-white border-2 border-gray-100 border-dashed rounded-[24px] p-10 sm:p-14 flex flex-col items-center justify-center text-center">
                <div class="w-16 h-16 rounded-full bg-gray-50 flex items-center justify-center mb-4">
                    <i data-lucide="clock" class="w-8 h-8 text-gray-400"></i>
                </div>
                <h3 class="text-[18px] font-bold text-textMain mb-2">No hospital responses yet.</h3>
                <p class="text-[14px] text-textMuted max-w-[450px] mb-6 leading-relaxed">
                    Your treatment request is being matched with relevant healthcare providers. You will be notified when a hospital submits a Treatment Estimate &amp; Proposal.
                </p>
                {% if request and request.reference_id %}
                <a href="{{ url_for('patient_request_details', reference_id=request.reference_id) }}" class="bg-white border border-gray-200 text-textMain hover:bg-gray-50 font-bold px-6 py-2.5 rounded-full text-[13.5px] transition-shadow shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-300">
                    View Treatment Request
                </a>
                {% endif %}
            </div>
            {% endif %}
        \2'''

content = re.sub(pattern_responses, replacement_responses, content, flags=re.DOTALL)

pattern_compare = r'(<!-- STICKY COMPARE ACTION BAR -->\s*<div id="compare-bar".*?</div>\s*</div>\s*</div>)'
replacement_compare = r'''{% if responses %}
    \1
    {% endif %}'''
content = re.sub(pattern_compare, replacement_compare, content, flags=re.DOTALL)

with open("templates/patient-hospital-responses.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
