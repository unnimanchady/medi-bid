import re

html_path = 'templates/patient-request-details.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """{% set progress_percent = 20 %}
{% set step1 = true %}
{% set step2 = false %}
{% set step3 = false %}
{% set step4 = false %}
{% set step5 = false %}

{% if request.status != 'Pending' %}
    {% set progress_percent = 40 %}
    {% set step2 = true %}
{% endif %}
{% if request.matched_count > 0 %}
    {% set progress_percent = 60 %}
    {% set step3 = true %}
{% endif %}
{% if request.response_count > 0 %}
    {% set progress_percent = 80 %}
    {% set step4 = true %}
{% endif %}
{% if request.status in ['Completed', 'Provider Selected', 'Accepted'] %}
    {% set progress_percent = 100 %}
    {% set step5 = true %}
{% endif %}

<div class="min-w-[500px] relative">
                            <div class="progress-line"></div>
                            <div class="progress-line-active" style="width: {{ progress_percent }}%;"></div>
                            
                            <div class="flex justify-between relative z-10">
                                <!-- Stage 1 -->
                                <div class="flex flex-col items-center w-1/5 relative group">
                                    <div class="w-7 h-7 rounded-full bg-white {% if step1 %}border-[3px] border-secondary ring-4 ring-blue-50{% else %}border-2 border-gray-200{% endif %} flex items-center justify-center shadow-sm">
                                        {% if step1 %}<div class="w-2 h-2 rounded-full bg-secondary"></div>{% endif %}
                                    </div>
                                    <span class="text-[11px] {% if step1 %}font-extrabold text-secondary{% else %}font-bold text-gray-400{% endif %} mt-3 text-center leading-tight">Request Submitted</span>
                                </div>
                                <!-- Stage 2 -->
                                <div class="flex flex-col items-center w-1/5 relative">
                                    <div class="w-7 h-7 rounded-full bg-white {% if step2 %}border-[3px] border-secondary ring-4 ring-blue-50{% else %}border-2 border-gray-200{% endif %} flex items-center justify-center">
                                        {% if step2 %}<div class="w-2 h-2 rounded-full bg-secondary"></div>{% endif %}
                                    </div>
                                    <span class="text-[11px] {% if step2 %}font-extrabold text-secondary{% else %}font-bold text-gray-400{% endif %} mt-3 text-center leading-tight">Request Reviewed</span>
                                </div>
                                <!-- Stage 3 -->
                                <div class="flex flex-col items-center w-1/5 relative">
                                    <div class="w-7 h-7 rounded-full bg-white {% if step3 %}border-[3px] border-secondary ring-4 ring-blue-50{% else %}border-2 border-gray-200{% endif %} flex items-center justify-center">
                                        {% if step3 %}<div class="w-2 h-2 rounded-full bg-secondary"></div>{% endif %}
                                    </div>
                                    <span class="text-[11px] {% if step3 %}font-extrabold text-secondary{% else %}font-bold text-gray-400{% endif %} mt-3 text-center leading-tight">Matched with Hospitals</span>
                                </div>
                                <!-- Stage 4 -->
                                <div class="flex flex-col items-center w-1/5 relative">
                                    <div class="w-7 h-7 rounded-full bg-white {% if step4 %}border-[3px] border-secondary ring-4 ring-blue-50{% else %}border-2 border-gray-200{% endif %} flex items-center justify-center">
                                        {% if step4 %}<div class="w-2 h-2 rounded-full bg-secondary"></div>{% endif %}
                                    </div>
                                    <span class="text-[11px] {% if step4 %}font-extrabold text-secondary{% else %}font-bold text-gray-400{% endif %} mt-3 text-center leading-tight">Responses Received</span>
                                </div>
                                <!-- Stage 5 -->
                                <div class="flex flex-col items-center w-1/5 relative">
                                    <div class="w-7 h-7 rounded-full bg-white {% if step5 %}border-[3px] border-secondary ring-4 ring-blue-50{% else %}border-2 border-gray-200{% endif %} flex items-center justify-center">
                                        {% if step5 %}<div class="w-2 h-2 rounded-full bg-secondary"></div>{% endif %}
                                    </div>
                                    <span class="text-[11px] {% if step5 %}font-extrabold text-secondary{% else %}font-bold text-gray-400{% endif %} mt-3 text-center leading-tight">Provider Selected</span>
                                </div>
                            </div>
                        </div>"""

pattern = r'<div class="min-w-\[500px\] relative">.*?</div>\s*</div>\s*</div>\s*</section>'
content_replaced = re.sub(pattern, replacement + '\n                    </div>\n                </section>', content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content_replaced)

print("Updated progress bar in patient-request-details.html")
