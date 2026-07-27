from app import app, db
from models import Hospital, TreatmentProposal, TreatmentRequest

with app.app_context():
    req = TreatmentRequest.query.filter_by(reference_id='TR-UEL6NYULN8').first()
    proposal = TreatmentProposal.query.filter_by(treatment_request_id=req.id).first()
    hospital = proposal.hospital
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['hospital_id'] = hospital.id
        
        res = client.get(f'/hospital/treatment-requests/{req.reference_id}/proposal/view')
        content = res.data.decode('utf-8')
        
        if 'window.print()' in content and 'downloadPDF()' in content:
            print('Print/PDF buttons found in view endpoint!')
        else:
            print('Print/PDF buttons missing in view endpoint!')
