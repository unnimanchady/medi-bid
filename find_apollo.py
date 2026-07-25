import re

def search_demo_data():
    with open('templates/patient-hospital-profile.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    terms = ['Apollo', 'Minimally Invasive CABG', 'Dr. Amit Singh', 'Dr. R. K. Sharma', 'Indraprastha', '718', 'NABH']
    for term in terms:
        matches = re.finditer(term, content, re.IGNORECASE)
        for match in matches:
            # find line number
            start = match.start()
            line_no = content.count('\n', 0, start) + 1
            print(f"Found '{term}' on line {line_no}")

if __name__ == '__main__':
    search_demo_data()
