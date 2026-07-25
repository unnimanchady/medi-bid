with open('templates/patient-hospital-responses.html', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
for i, l in enumerate(lines):
    if 'id="compare-bar"' in l:
        for j in range(i-5, i+15):
            print(f'{j}: {lines[j]}')
        break
