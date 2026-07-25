import re
from app import app
with app.app_context():
    app.config['TESTING'] = True
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['registration_user_id'] = 2
    
    resp = client.get('/patient/compare-hospitals')
    html = resp.get_data(as_text=True)
    links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>\s*View Hospital Profile\s*</a>', html, re.IGNORECASE)
    print('Generated hrefs:', links)
