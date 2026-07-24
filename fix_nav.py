import glob

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Rename Request Details -> Treatment Request (display label)
    content = content.replace('>Request Details<', '>Treatment Request<')
    content = content.replace('title=\"Treatment Request Details', 'title=\"Treatment Request')
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'My Requests' in line and 'patient_hospital_responses' in line:
            line = line.replace('patient_hospital_responses', 'patient_dashboard')
        new_lines.append(line)
        
    content = '\n'.join(new_lines)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

for filename in glob.glob('templates/patient-*.html'):
    process_file(filename)

print('Done!')
