from app import app
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['registration_user_id'] = 2
    
    resp = client.get('/patient/requests')
    import re
    matches = re.findall(r'<h3.*?>(.*?)</h3>.*?<a href=\"(.*?patient/hospital-responses.*?)\"', resp.text, re.DOTALL)
    for title, href in matches:
        print(f'Card: {title.strip()}')
        print(f'HREF: {href.strip()}')
