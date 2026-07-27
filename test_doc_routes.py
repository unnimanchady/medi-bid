import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from models import db, Hospital, HospitalUser, TreatmentRequest, MedicalDocument

def test_routes():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            # Find Mayo Clinic admin user
            mayo = Hospital.query.filter_by(legal_name='Mayo Clinic').first()
            hospital_user = HospitalUser.query.filter_by(hospital_id=mayo.id).first()
            user_id = hospital_user.user_id
            
            # Find the document for TR-UEL6NYULN8
            req = TreatmentRequest.query.filter_by(reference_id='TR-UEL6NYULN8').first()
            doc = req.medical_documents[0]
            doc_id = doc.id
            print(f"Testing with Mayo Clinic (Hospital ID: {mayo.id}), Doc ID: {doc_id}")
            
        # Simulate login by setting session variables manually
        with client.session_transaction() as sess:
            sess['user_id'] = user_id
            sess['user_type'] = 'hospital'
            sess['hospital_id'] = mayo.id
            
        # Test View
        print("\n--- Testing View Route ---")
        response = client.get(f"/hospital/treatment-requests/document/{doc_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        if response.status_code != 200:
            print(f"Data: {response.data}")
            
        # Test Download
        print("\n--- Testing Download Route ---")
        response = client.get(f"/hospital/treatment-requests/document/{doc_id}/download")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        if response.status_code != 200:
            print(f"Data: {response.data}")

if __name__ == '__main__':
    test_routes()
