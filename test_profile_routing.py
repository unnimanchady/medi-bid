import unittest
from app import app, db
from models import User, Hospital, TreatmentRequest, TreatmentProposal, PatientProfile

class TestHospitalProfile(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_mayo_and_cleveland_profiles(self):
        with app.app_context():
            req = TreatmentRequest.query.filter_by(reference_id='TR-R5PDRXK8WW').first()
            self.assertIsNotNone(req, "Request not found")
            profile = PatientProfile.query.get(req.patient_profile_id)
            user = User.query.get(profile.user_id)
            self.assertIsNotNone(user, "Patient user not found")
            
            # Find Mayo and Cleveland proposals
            proposals = TreatmentProposal.query.filter_by(treatment_request_id=req.id).all()
            mayo_proposal = next((p for p in proposals if p.hospital_id == 2), None)
            cleveland_proposal = next((p for p in proposals if p.hospital_id == 3), None)
            
            self.assertIsNotNone(mayo_proposal, "Mayo proposal not found")
            self.assertIsNotNone(cleveland_proposal, "Cleveland proposal not found")
            
        # Log in
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['role'] = 'patient'
            sess['registration_user_id'] = user.id
            
        # Fetch Mayo
        resp_mayo = self.client.get(f'/patient/treatment-proposal/{mayo_proposal.id}/hospital')
        self.assertEqual(resp_mayo.status_code, 200)
        html_mayo = resp_mayo.get_data(as_text=True)
        
        self.assertIn('Mayo Clinic', html_mayo)
        self.assertNotIn('Apollo Hospitals', html_mayo)
        self.assertNotIn('Dr. Amit Singh', html_mayo)
        self.assertNotIn('Minimally Invasive CABG', html_mayo)
        self.assertIn(req.condition, html_mayo) # Dynamic based on req
        
        # Fetch Cleveland
        resp_clev = self.client.get(f'/patient/treatment-proposal/{cleveland_proposal.id}/hospital')
        self.assertEqual(resp_clev.status_code, 200)
        html_clev = resp_clev.get_data(as_text=True)
        
        self.assertIn('Cleveland Clinic', html_clev)
        self.assertNotIn('Apollo Hospitals', html_clev)
        self.assertNotIn('Dr. Amit Singh', html_clev)
        self.assertNotIn('Minimally Invasive CABG', html_clev)
        self.assertIn(req.condition, html_clev)

        print("TEST PASSED")

if __name__ == '__main__':
    unittest.main()
