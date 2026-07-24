import re

html_path = 'templates/patient-request-details.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """                    <h3 class="text-[16px] font-extrabold text-primary mt-4">Hospital Responses</h3>
                    
                    {% if request.response_count > 0 %}
                    <div class="bg-softBlue border border-blue-100 rounded-[20px] p-8 sm:p-12 shadow-sm flex flex-col items-center text-center">
                        <div class="w-16 h-16 rounded-full bg-secondary text-white flex items-center justify-center mb-4 shadow-sm">
                            <i data-lucide="file-check" class="w-8 h-8"></i>
                        </div>
                        <h4 class="text-[18px] font-extrabold text-primary mb-2">You have {{ request.response_count }} hospital response{% if request.response_count != 1 %}s{% endif %}</h4>
                        <p class="text-[14px] text-textMuted max-w-[400px] mb-6">
                            Healthcare providers have reviewed your request and submitted proposals. Compare them to choose the best option.
                        </p>
                        <a href="{{ url_for('patient_hospital_responses', reference_id=request.reference_id) }}" class="bg-secondary text-white font-bold px-8 py-3 rounded-full text-[14.5px] hover:bg-blue-600 shadow-sm flex items-center gap-2 transition-all">
                            View Responses <i data-lucide="arrow-right" class="w-4 h-4"></i>
                        </a>
                    </div>
                    {% else %}
                    <!-- Empty State for Responses -->
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

pattern = r'<h3 class="text-\[16px\] font-extrabold text-primary mt-4">Hospital Responses</h3>\s*<!-- Empty State for Responses -->\s*<div class="bg-bgLight border border-gray-200 rounded-\[20px\].*?</div>'

content_replaced = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content_replaced)

print("Updated responses state.")
