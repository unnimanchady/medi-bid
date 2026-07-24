with open('original_dashboard.html', 'r', encoding='utf-16') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'id="profile-dropdown"' in line:
            print(''.join(lines[i-5:i+25]))
            break
