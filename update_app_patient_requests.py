with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_func = False
skip_next = False

for line in lines:
    if line.startswith('def patient_requests():'):
        in_func = True
        new_lines.append(line)
        continue
    
    if in_func:
        if 'if profile_ids:' in line:
            new_lines.append(line)
            new_lines.append('''        requests_query = TreatmentRequest.query.filter(TreatmentRequest.patient_profile_id.in_(profile_ids)).order_by(TreatmentRequest.created_at.desc()).all()
        for req in requests_query:
            proposals = [p for p in req.proposals if p.status == 'submitted']
            if proposals:
                latest_proposal_time = max((p.submitted_at for p in proposals if p.submitted_at), default=req.created_at)
                req._latest_response_time = latest_proposal_time
            else:
                req._latest_response_time = None

        requests = sorted(
            requests_query,
            key=lambda r: (r._latest_response_time is not None, r._latest_response_time or r.created_at),
            reverse=True
        )
''')
            skip_next = True
            continue
        elif skip_next and 'requests = ' in line:
            # skip the original requests assignment
            skip_next = False
            continue
        elif "return render_template('patient-requests.html'" in line:
            new_lines.append('''    context = request.args.get('context')
    if context == 'responses':
        page_title = "Hospital Responses"
        page_desc = "Select a treatment request to review responses from healthcare providers."
    else:
        page_title = "My Requests"
        page_desc = "Manage and track your submitted treatment requests."
        
    return render_template('patient-requests.html', user=user, requests=requests, page_title=page_title, page_desc=page_desc)
''')
            in_func = False
            continue

    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
