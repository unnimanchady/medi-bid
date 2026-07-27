import os

filepath = 'templates/hospital-proposal-review.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the header for Submitted Proposals to add Print / Download PDF buttons
target_header = '''                {% if is_view_only %}
                <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold mb-3">
                    <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> SUBMITTED PROPOSAL
                </div>
                <h1 class="text-3xl font-extrabold tracking-tight mb-2">Submitted Treatment Proposal</h1>'''

replacement_header = '''                {% if is_view_only %}
                <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold mb-3 print:hidden">
                    <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> SUBMITTED PROPOSAL
                </div>
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-2">
                    <h1 class="text-3xl font-extrabold tracking-tight">Submitted Treatment Proposal</h1>
                    <div class="flex items-center gap-3 print:hidden">
                        <button onclick="window.print()" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-bold rounded-xl hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2 text-sm">
                            <i data-lucide="printer" class="w-4 h-4"></i> Print
                        </button>
                        <button onclick="downloadPDF()" class="px-4 py-2 bg-accent text-white font-bold rounded-xl hover:bg-blue-600 transition-colors shadow-sm flex items-center gap-2 text-sm">
                            <i data-lucide="download" class="w-4 h-4"></i> Download PDF
                        </button>
                    </div>
                </div>'''
content = content.replace(target_header, replacement_header)

# 2. Fix the location formatting
target_location = '''                        <p class="text-textMuted text-sm mt-1 flex items-center gap-1.5">
                            <i data-lucide="map-pin" class="w-4 h-4"></i> {{ hospital.city }}, {{ hospital.country }}
                        </p>'''

replacement_location = '''                        <p class="text-textMuted text-sm mt-1 flex items-center gap-1.5">
                            <i data-lucide="map-pin" class="w-4 h-4"></i>
                            {% set loc = [] %}
                            {% if hospital.city and hospital.city != 'None' %}{% set _ = loc.append(hospital.city) %}{% endif %}
                            {% if hospital.state and hospital.state != 'None' %}{% set _ = loc.append(hospital.state) %}{% endif %}
                            {% if hospital.country and hospital.country != 'None' %}{% set _ = loc.append(hospital.country) %}{% endif %}
                            {{ loc | join(', ') }}
                        </p>'''
content = content.replace(target_location, replacement_location)

# 3. Add html2pdf.js and downloadPDF function
target_script = '''    <script>
        lucide.createIcons();
        
        function confirmSubmit() {'''

replacement_script = '''    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script>
        lucide.createIcons();
        
        function downloadPDF() {
            const element = document.getElementById('proposal-card');
            
            // Temporarily hide elements we don't want in PDF
            const hiddenElements = document.querySelectorAll('.print\\\\:hidden');
            hiddenElements.forEach(el => el.style.display = 'none');
            
            const opt = {
                margin:       [10, 10, 10, 10],
                filename:     'proposal-{{ req.reference_id }}.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true },
                jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };

            html2pdf().set(opt).from(element).save().then(() => {
                // Restore hidden elements
                hiddenElements.forEach(el => el.style.display = '');
            });
        }
        
        function confirmSubmit() {'''

content = content.replace(target_script, replacement_script)

# Add id to the review card to target it for PDF
target_card = '''            <!-- Review Card -->
            <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">'''

replacement_card = '''            <!-- Review Card -->
            <div id="proposal-card" class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden print:border-none print:shadow-none">'''
            
content = content.replace(target_card, replacement_card)

# Hide Sidebar and Header on print
target_sidebar = '<aside class="w-64 bg-white border-r border-gray-100 flex-col hidden md:flex sticky top-0 h-screen shrink-0">'
replacement_sidebar = '<aside class="w-64 bg-white border-r border-gray-100 flex-col hidden md:flex sticky top-0 h-screen shrink-0 print:hidden">'
content = content.replace(target_sidebar, replacement_sidebar)

target_header_ui = '<header class="bg-white border-b border-slate-200 sticky top-0 z-20 px-6 py-4 flex items-center justify-between">'
replacement_header_ui = '<header class="bg-white border-b border-slate-200 sticky top-0 z-20 px-6 py-4 flex items-center justify-between print:hidden">'
content = content.replace(target_header_ui, replacement_header_ui)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated templates/hospital-proposal-review.html")
