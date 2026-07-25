from app import app
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['registration_user_id'] = 2
    
    resp = client.get('/patient/hospital-responses?reference_id=TR-R5PDRXK8WW')
    import re
    matches = re.findall(r'<span class="text-\[12px\].*?>(.*?)</span>', resp.text, re.DOTALL)
    print(matches)
