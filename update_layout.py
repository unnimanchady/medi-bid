with open('templates/patient-layout.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    '''<a href="{{ url_for('patient_hospital_responses') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all group">''',
    '''<a href="{{ url_for('patient_hospital_responses', reference_id=request.reference_id) if request and request.reference_id else url_for('patient_hospital_responses') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all group">'''
)
c = c.replace(
    '''<a href="{{ url_for('patient_compare_hospitals') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all group">''',
    '''<a href="{{ url_for('patient_compare_hospitals', request_id=request.id) if request and request.reference_id else url_for('patient_compare_hospitals') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all group">'''
)
c = c.replace(
    '''<a href="{{ url_for('patient_hospital_responses') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all">''',
    '''<a href="{{ url_for('patient_hospital_responses', reference_id=request.reference_id) if request and request.reference_id else url_for('patient_hospital_responses') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all">'''
)
c = c.replace(
    '''<a href="{{ url_for('patient_compare_hospitals') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all">''',
    '''<a href="{{ url_for('patient_compare_hospitals', request_id=request.id) if request and request.reference_id else url_for('patient_compare_hospitals') }}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-white/60 hover:text-white hover:bg-white/5 font-medium transition-all">'''
)

with open('templates/patient-layout.html', 'w', encoding='utf-8') as f:
    f.write(c)
