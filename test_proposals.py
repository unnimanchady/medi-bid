from app import app, db
from models import Hospital, TreatmentProposal, TreatmentRequest

with app.app_context():
    # Let's find the hospital that owns the proposal for TR-UEL6NYULN8
    req = TreatmentRequest.query.filter_by(reference_id='TR-UEL6NYULN8').first()
    if not req:
        print("Request TR-UEL6NYULN8 not found!")
    else:
        proposal = TreatmentProposal.query.filter_by(treatment_request_id=req.id).first()
        if not proposal:
            print("No proposal found for this request.")
        else:
            hospital = proposal.hospital
            print(f"Hospital ID: {hospital.id}, Name: {hospital.legal_name}")
            print(f"Proposal Status: {proposal.status}")
            
            # Now let's simulate a test client request
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['hospital_id'] = hospital.id
                
                # Test Proposals List
                res = client.get('/hospital/proposals')
                print(f"Proposals Endpoint Status: {res.status_code}")
                
                # Test Proposal Review
                res2 = client.get(f'/hospital/treatment-requests/{req.reference_id}/proposal/review')
                print(f"Review Endpoint Status: {res2.status_code}")
                content = res2.data.decode('utf-8')
                
                # Check for Print Proposal Button
                if "Print" in content and "Download PDF" in content:
                    print("Print/PDF buttons found!")
                else:
                    print("Print/PDF buttons missing!")
                    
                # Check for Location (None, USA shouldn't be there)
                if "None," in content:
                    print("Location still has 'None,'!")
                else:
                    print("Location looks clean.")
