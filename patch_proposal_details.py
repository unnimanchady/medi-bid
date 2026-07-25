import re

with open('templates/patient-treatment-proposal-details.html', 'r', encoding='utf-8') as f:
    c = f.read()

replacement = """<div class="flex flex-col sm:items-end gap-3 w-full sm:w-auto">
                <div class="flex items-center gap-2 no-print self-start sm:self-auto">
                    <form action="{{ url_for('patient_secure_messages_start') }}" method="POST" class="inline">
                        <input type="hidden" name="treatment_request_id" value="{{ request.id }}">
                        <input type="hidden" name="hospital_id" value="{{ hospital.id }}">
                        <button type="submit" class="flex items-center gap-2 bg-secondary text-white px-4 py-2 rounded-lg font-bold text-[13.5px] hover:bg-blue-600 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-secondary">
                            <i data-lucide="message-square" class="w-4 h-4"></i> Message Hospital
                        </button>
                    </form>
                    <button onclick="window.print()" class="text-textMuted hover:text-primary bg-white border border-gray-200 p-2 rounded-lg transition-colors focus:outline-none shadow-sm" aria-label="Print Proposal" title="Print">
                        <i data-lucide="printer" class="w-4 h-4"></i>
                    </button>
                </div>"""

c = re.sub(
    r'<div class="flex flex-col sm:items-end gap-3 w-full sm:w-auto">.*?<div class="flex items-center gap-2 no-print self-start sm:self-auto">.*?<button onclick="window\.print\(\)" class="text-textMuted hover:text-primary bg-white border border-gray-200 p-2 rounded-lg transition-colors focus:outline-none shadow-sm" aria-label="Print Proposal" title="Print">.*?<i data-lucide="printer" class="w-4 h-4"></i>.*?</button>.*?</div>',
    replacement,
    c,
    flags=re.DOTALL
)

with open('templates/patient-treatment-proposal-details.html', 'w', encoding='utf-8') as f:
    f.write(c)
