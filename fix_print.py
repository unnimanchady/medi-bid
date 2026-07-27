import sys

filepath = r'f:\projects\medi-bid\templates\hospital-proposal-review.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add @page CSS rule in head
head_old = '''    <script>
        tailwind.config = {'''
head_new = '''    <style>
        @media print {
            @page {
                size: A4;
                margin: 15mm;
            }
        }
    </style>
    
    <script>
        tailwind.config = {'''
content = content.replace(head_old, head_new)

# 2. Update body classes
body_old = '''<body class="bg-bgLight min-h-screen text-textMain selection:bg-accent selection:text-white flex">'''
body_new = '''<body class="bg-bgLight min-h-screen text-textMain selection:bg-accent selection:text-white flex print:block print:h-auto print:min-h-0 print:overflow-visible print:bg-white">'''
content = content.replace(body_old, body_new)

# 3. Update main classes
main_old = '''    <main class="flex-1 flex flex-col h-screen overflow-y-auto">'''
main_new = '''    <main class="flex-1 flex flex-col h-screen overflow-y-auto print:block print:h-auto print:overflow-visible">'''
content = content.replace(main_old, main_new)

# 4. Update container classes
container_old = '''        <div class="p-4 md:p-8 lg:p-10 max-w-[1000px] mx-auto w-full pb-32">'''
container_new = '''        <div class="p-4 md:p-8 lg:p-10 max-w-[1000px] mx-auto w-full pb-32 print:p-0 print:max-w-none print:pb-0">'''
content = content.replace(container_old, container_new)

# 5. Add print:break-inside-avoid to Timeline block
timeline_old = '''                    <!-- Section 2: Timeline -->
                    <div>'''
timeline_new = '''                    <!-- Section 2: Timeline -->
                    <div class="print:break-inside-avoid">'''
content = content.replace(timeline_old, timeline_new)

# 6. Add print:break-inside-avoid to Total Box
total_old = '''                        <!-- Total Box -->
                        <div class="bg-gradient-to-r from-slate-800 to-slate-900 print:bg-none print:bg-white print:border-2 print:border-slate-800 print:text-black rounded-3xl p-8 md:p-10 text-white mb-8 flex flex-col md:flex-row gap-6 justify-between items-start md:items-center shadow-xl print:shadow-none">'''
total_new = '''                        <!-- Total Box -->
                        <div class="bg-gradient-to-r from-slate-800 to-slate-900 print:bg-none print:bg-white print:border-2 print:border-slate-800 print:text-black rounded-3xl p-8 md:p-10 text-white mb-8 flex flex-col md:flex-row gap-6 justify-between items-start md:items-center shadow-xl print:shadow-none print:break-inside-avoid">'''
content = content.replace(total_old, total_new)

# 7. Add print:break-inside-avoid to Table rows
tr_old = '''                                        <tr class="hover:bg-slate-50 transition-colors">'''
tr_new = '''                                        <tr class="hover:bg-slate-50 transition-colors print:break-inside-avoid">'''
content = content.replace(tr_old, tr_new)

# 8. Add print:break-inside-avoid to Inclusions, Exclusions, Notes, Disclaimer
inclusions_old = '''                            <div>
                                <p class="text-sm font-bold text-emerald-600 uppercase tracking-wider mb-3 flex items-center gap-2"><i data-lucide="check" class="w-5 h-5"></i> Included in Estimate</p>'''
inclusions_new = '''                            <div class="print:break-inside-avoid">
                                <p class="text-sm font-bold text-emerald-600 uppercase tracking-wider mb-3 flex items-center gap-2 print:text-black"><i data-lucide="check" class="w-5 h-5 print:text-black"></i> Included in Estimate</p>'''
content = content.replace(inclusions_old, inclusions_new)

exclusions_old = '''                            <div>
                                <p class="text-sm font-bold text-red-600 uppercase tracking-wider mb-3 flex items-center gap-2"><i data-lucide="x" class="w-5 h-5"></i> Excluded from Estimate</p>'''
exclusions_new = '''                            <div class="print:break-inside-avoid">
                                <p class="text-sm font-bold text-red-600 uppercase tracking-wider mb-3 flex items-center gap-2 print:text-black"><i data-lucide="x" class="w-5 h-5 print:text-black"></i> Excluded from Estimate</p>'''
content = content.replace(exclusions_old, exclusions_new)

requirements_old = '''                            <div class="md:col-span-2 mt-4">
                                <p class="text-sm font-bold text-amber-600 uppercase tracking-wider mb-3 flex items-center gap-2"><i data-lucide="alert-circle" class="w-5 h-5"></i> Pre-treatment Requirements</p>'''
requirements_new = '''                            <div class="md:col-span-2 mt-4 print:break-inside-avoid">
                                <p class="text-sm font-bold text-amber-600 uppercase tracking-wider mb-3 flex items-center gap-2 print:text-black"><i data-lucide="alert-circle" class="w-5 h-5 print:text-black"></i> Pre-treatment Requirements</p>'''
content = content.replace(requirements_old, requirements_new)

notes_old = '''                            <div class="md:col-span-2 mt-4">
                                <p class="text-sm font-bold text-textMuted uppercase tracking-wider mb-3 flex items-center gap-2"><i data-lucide="file-text" class="w-5 h-5"></i> Additional Notes</p>'''
notes_new = '''                            <div class="md:col-span-2 mt-4 print:break-inside-avoid">
                                <p class="text-sm font-bold text-textMuted uppercase tracking-wider mb-3 flex items-center gap-2 print:text-black"><i data-lucide="file-text" class="w-5 h-5 print:text-black"></i> Additional Notes</p>'''
content = content.replace(notes_old, notes_new)

disclaimer_old = '''                    <!-- Standard Disclaimer -->
                    <div class="mt-12 p-6 bg-slate-100 rounded-2xl border border-slate-200 text-sm text-textMuted leading-relaxed print:bg-transparent print:border-slate-300 print:text-black">'''
disclaimer_new = '''                    <!-- Standard Disclaimer -->
                    <div class="mt-12 p-6 bg-slate-100 rounded-2xl border border-slate-200 text-sm text-textMuted leading-relaxed print:bg-transparent print:border-slate-300 print:text-black print:break-inside-avoid">'''
content = content.replace(disclaimer_old, disclaimer_new)

# Let's write the modified content back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Update completed.")
