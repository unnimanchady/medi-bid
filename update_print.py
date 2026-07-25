import re

with open('templates/patient-compare-hospitals.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Make Print button trigger print
c = c.replace('<button class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-textMain text-[13px] font-bold rounded-xl hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-secondary shadow-sm transition-all">\n                        <i data-lucide="printer" class="w-4 h-4 text-textMuted"></i> Print\n                    </button>', 
'<button onclick="window.print()" class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-textMain text-[13px] font-bold rounded-xl hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-secondary shadow-sm transition-all">\n                        <i data-lucide="printer" class="w-4 h-4 text-textMuted"></i> Print\n                    </button>')

# Make Export PDF trigger print too
c = c.replace('<button class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-textMain text-[13px] font-bold rounded-xl hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-secondary shadow-sm transition-all">\n                        <i data-lucide="download" class="w-4 h-4 text-textMuted"></i> Export PDF\n                    </button>',
'<button onclick="window.print()" class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-textMain text-[13px] font-bold rounded-xl hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-secondary shadow-sm transition-all">\n                        <i data-lucide="download" class="w-4 h-4 text-textMuted"></i> Export PDF\n                    </button>')

# Fix no-print issues
c = c.replace('<header class="bg-white border-b border-gray-100 sticky top-0 z-30 shadow-sm no-print">', '<header class="bg-white border-b border-gray-100 sticky top-0 z-30 shadow-sm print:static print:border-none print:shadow-none">')
c = c.replace('<div class="flex items-center gap-3 self-end sm:self-auto">', '<div class="flex items-center gap-3 self-end sm:self-auto no-print">')
c = c.replace('<button id="mobile-menu-btn" class="md:hidden p-2', '<button id="mobile-menu-btn" class="md:hidden p-2 no-print')

# Remove no-print from treatment name row
c = c.replace('<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 opacity-0 animate-fade-in no-print">', '<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 opacity-0 animate-fade-in">')

# Add no-print to toggle switch
c = c.replace('<div class="flex items-center gap-3 self-end sm:self-auto bg-white border border-gray-200 px-4 py-2 rounded-xl shadow-sm">', '<div class="flex items-center gap-3 self-end sm:self-auto bg-white border border-gray-200 px-4 py-2 rounded-xl shadow-sm no-print">')

# Fix hospital header row
c = c.replace('z-20 bg-bgLight pt-2 pb-4 no-print">', 'z-20 bg-bgLight pt-2 pb-4 print:static">')

# Remove no-print from accordion buttons
c = c.replace('accordion-btn no-print"', 'accordion-btn"')

# Define .no-print in a <style> block at the top of content block
style_block = """
<style>
@media print {
    .no-print { display: none !important; }
    body { background-color: white !important; }
    .bg-bgLight { background-color: white !important; }
    .shadow-sm, .shadow-dropdown, .shadow-card { box-shadow: none !important; }
    * { color: black !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    /* Expand all accordions for print */
    .comparison-section-content { height: auto !important; overflow: visible !important; }
    .lucide-chevron-down, .lucide-chevron-up { display: none !important; }
}
</style>
"""
c = c.replace('{% block content %}', '{% block content %}\n' + style_block)

with open('templates/patient-compare-hospitals.html', 'w', encoding='utf-8') as f:
    f.write(c)

with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    l = f.read()
l = l.replace('<header class="bg-white border-b border-gray-200 h-[70px] lg:h-[80px] flex items-center justify-between px-4 sm:px-6 lg:px-8 sticky top-0 z-50 shadow-sm">', '<header class="bg-white border-b border-gray-200 h-[70px] lg:h-[80px] flex items-center justify-between px-4 sm:px-6 lg:px-8 sticky top-0 z-50 shadow-sm no-print">')
with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(l)
