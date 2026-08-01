import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject the new get_visible_treatment_requests function
new_func = '''def get_visible_treatment_requests(hospital):
    """
    Returns a SQLAlchemy query for all treatment requests that the given hospital is allowed to view.
    MVP Logic: All verified hospitals can view all active/open requests.
    """
    if not hospital or hospital.verification_status != 'verified':
        return TreatmentRequest.query.filter(False)
        
    return TreatmentRequest.query.filter(
        TreatmentRequest.status.notin_(['Closed', 'Completed', 'Cancelled', 'Expired']),
        TreatmentRequest.status == 'Active'
    )

def _is_hospital_eligible(hospital, request_specialty):'''

content = content.replace("def _is_hospital_eligible(hospital, request_specialty):", new_func)

# 2. Update hospital_dashboard
old_dashboard_logic = '''    eligible_requests_count = 0
    if hospital and hospital.verification_status == 'verified':
        all_active = TreatmentRequest.query.filter_by(status='Active').all()
        for req in all_active:
            if _is_hospital_eligible(hospital, req.specialty):
                eligible_requests_count += 1'''

new_dashboard_logic = '''    eligible_requests_count = 0
    if hospital and hospital.verification_status == 'verified':
        eligible_requests_count = get_visible_treatment_requests(hospital).count()'''

content = content.replace(old_dashboard_logic, new_dashboard_logic)

# 3. Update hospital_treatment_requests
old_requests_logic = '''    query = TreatmentRequest.query.filter(
        TreatmentRequest.status.notin_(['Closed', 'Completed', 'Cancelled', 'Expired']),
        TreatmentRequest.status == 'Active'
    )'''

new_requests_logic = '''    query = get_visible_treatment_requests(hospital)'''

content = content.replace(old_requests_logic, new_requests_logic)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py to use shared request logic!")
