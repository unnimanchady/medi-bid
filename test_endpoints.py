from app import app
from urllib.parse import urlparse

with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['registration_user_id'] = 2
    
    print("TESTING TR-R5PDRXK8WW:")
    resp1 = client.get('/patient/requests/TR-R5PDRXK8WW/responses')
    print("Status code:", resp1.status_code)
    print("Reference ID in text:", "TR-R5PDRXK8WW" in resp1.text)
    
    print("\nTESTING TR-GIDLD012XM:")
    resp2 = client.get('/patient/requests/TR-GIDLD012XM/responses')
    print("Status code:", resp2.status_code)
    print("Reference ID in text:", "TR-GIDLD012XM" in resp2.text)
