from app import app
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['registration_user_id'] = 2
    
    resp = client.get('/patient/requests/TR-R5PDRXK8WW/responses')
    print("Status:", resp.status_code)
    import re
    matches = re.findall(r'<span class="text-\[12px\].*?>(.*?)</span>', resp.text, re.DOTALL)
    print("Reference IDs in page:", matches)
