import os

def update_treatment_requests():
    with open('templates/admin-treatment-requests.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # The original template only had a status filter and a search bar. We'll update the filter form completely.
    
    old_filter_form = """<form method="GET" class="flex flex-col sm:flex-row gap-4 items-center">
                    <div class="flex-1 w-full relative">
                        <i data-lucide="search" class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                        <input type="text" name="q" value="{{ search_query or '' }}" placeholder="Search by Reference ID or Patient Name..." class="w-full pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all shadow-sm">
                    </div>
                    
                    <div class="w-full sm:w-auto relative">
                        <select name="status" onchange="this.form.submit()" class="w-full sm:w-48 appearance-none pl-4 pr-10 py-3 bg-white border border-slate-200 rounded-xl font-bold text-slate-700 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent cursor-pointer shadow-sm">
                            <option value="">All Statuses</option>
                            <option value="Active" {% if current_status == 'Active' %}selected{% endif %}>Active</option>
                            <option value="Pending" {% if current_status == 'Pending' %}selected{% endif %}>Pending</option>
                            <option value="Completed" {% if current_status == 'Completed' %}selected{% endif %}>Completed</option>
                        </select>
                        <i data-lucide="chevron-down" class="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                    </div>
                    
                    <button type="submit" class="w-full sm:w-auto bg-slate-800 hover:bg-slate-700 text-white font-bold py-3 px-6 rounded-xl transition-all shadow-sm">
                        Search
                    </button>
                    
                    {% if search_query or current_status %}
                    <a href="{{ url_for('admin_treatment_requests') }}" class="w-full sm:w-auto text-center px-4 py-3 text-slate-500 hover:text-slate-800 font-bold transition-colors">
                        Clear
                    </a>
                    {% endif %}
                </form>"""
                
    new_filter_form = """<form method="GET" class="flex flex-col gap-4">
                    <div class="flex flex-col sm:flex-row gap-4 items-center">
                        <div class="flex-1 w-full relative">
                            <i data-lucide="search" class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                            <input type="text" name="q" value="{{ search_query or '' }}" placeholder="Search by Reference ID or Patient Name..." class="w-full pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all shadow-sm">
                        </div>
                        
                        <div class="w-full sm:w-auto relative min-w-[160px]">
                            <select name="status" class="w-full appearance-none pl-4 pr-10 py-3 bg-white border border-slate-200 rounded-xl font-bold text-slate-700 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent cursor-pointer shadow-sm">
                                <option value="">All Statuses</option>
                                <option value="Active" {% if current_status == 'Active' %}selected{% endif %}>Active</option>
                                <option value="Pending" {% if current_status == 'Pending' %}selected{% endif %}>Pending</option>
                                <option value="Completed" {% if current_status == 'Completed' %}selected{% endif %}>Completed</option>
                            </select>
                            <i data-lucide="chevron-down" class="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                        </div>
                        
                        <div class="w-full sm:w-auto relative min-w-[160px]">
                            <select name="specialty" class="w-full appearance-none pl-4 pr-10 py-3 bg-white border border-slate-200 rounded-xl font-bold text-slate-700 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent cursor-pointer shadow-sm">
                                <option value="">All Specialties</option>
                                <option value="Cardiology" {% if current_specialty == 'Cardiology' %}selected{% endif %}>Cardiology</option>
                                <option value="Oncology" {% if current_specialty == 'Oncology' %}selected{% endif %}>Oncology</option>
                                <option value="Neurology" {% if current_specialty == 'Neurology' %}selected{% endif %}>Neurology</option>
                                <option value="Orthopedics" {% if current_specialty == 'Orthopedics' %}selected{% endif %}>Orthopedics</option>
                                <option value="Pediatrics" {% if current_specialty == 'Pediatrics' %}selected{% endif %}>Pediatrics</option>
                                <option value="General Surgery" {% if current_specialty == 'General Surgery' %}selected{% endif %}>General Surgery</option>
                            </select>
                            <i data-lucide="chevron-down" class="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                        </div>
                        
                        <div class="w-full sm:w-auto relative min-w-[160px]">
                            <select name="country" class="w-full appearance-none pl-4 pr-10 py-3 bg-white border border-slate-200 rounded-xl font-bold text-slate-700 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent cursor-pointer shadow-sm">
                                <option value="">All Countries</option>
                                <option value="United States" {% if current_country == 'United States' %}selected{% endif %}>United States</option>
                                <option value="United Kingdom" {% if current_country == 'United Kingdom' %}selected{% endif %}>United Kingdom</option>
                                <option value="Canada" {% if current_country == 'Canada' %}selected{% endif %}>Canada</option>
                                <option value="India" {% if current_country == 'India' %}selected{% endif %}>India</option>
                                <option value="Australia" {% if current_country == 'Australia' %}selected{% endif %}>Australia</option>
                                <option value="Germany" {% if current_country == 'Germany' %}selected{% endif %}>Germany</option>
                            </select>
                            <i data-lucide="chevron-down" class="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                        </div>
                    </div>
                    
                    <div class="flex gap-4 items-center justify-end">
                        {% if search_query or current_status or current_specialty or current_country %}
                        <a href="{{ url_for('admin_treatment_requests') }}" class="text-slate-500 hover:text-slate-800 font-bold transition-colors">
                            Clear Filters
                        </a>
                        {% endif %}
                        <button type="submit" class="bg-slate-800 hover:bg-slate-700 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-sm">
                            Filter Requests
                        </button>
                    </div>
                </form>"""
                
    if old_filter_form in content:
        content = content.replace(old_filter_form, new_filter_form)
        with open('templates/admin-treatment-requests.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated admin-treatment-requests.html with new filters.")
    else:
        print("Could not find the old filter form in admin-treatment-requests.html")

if __name__ == '__main__':
    update_treatment_requests()
