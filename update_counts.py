import re

html_path = 'templates/patient-request-details.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """<div class="flex items-center gap-4 bg-white border border-gray-200 rounded-xl px-4 py-2 shadow-sm flex-shrink-0 self-start sm:self-auto">
                            <div class="flex flex-col items-center">
                                <span class="text-[11px] text-textMuted font-bold uppercase">Matched</span>
                                <span class="text-[16px] font-extrabold text-primary">{{ request.matched_count }}</span>
                            </div>
                            <div class="w-[1px] h-8 bg-gray-200"></div>
                            <div class="flex flex-col items-center">
                                <span class="text-[11px] text-textMuted font-bold uppercase">Responses</span>
                                <span class="text-[16px] font-extrabold text-secondary">{{ request.response_count }}</span>
                            </div>
                        </div>"""

pattern = r'<div class="flex items-center gap-4 bg-white border border-gray-200 rounded-xl px-4 py-2 shadow-sm flex-shrink-0 self-start sm:self-auto">.*?<span class="text-\[16px\] font-extrabold text-primary">0</span>.*?<span class="text-\[16px\] font-extrabold text-secondary">0</span>.*?</div>'

content_replaced = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content_replaced)

print("Updated matched/response count display.")
