import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from models import db, Hospital, Specialty, TreatmentRequest, TreatmentProposal

def verify():
    with app.app_context():
        # 1. Mayo Clinic has Cardiology in its registered specialties
        mayo = Hospital.query.get(2)
        specialties = [s.name for s in mayo.specialties]
        has_cardio = "Cardiology" in specialties
        print(f"1. Mayo Clinic has Cardiology: {has_cardio} (Current specialties: {specialties})")
        
        # 2. Mayo Clinic remains verified
        is_verified = mayo.verification_status == 'verified'
        print(f"2. Mayo Clinic remains verified: {is_verified} (Status: {mayo.verification_status})")
        
        # 3. TR-60B44F95ED still exists
        tr = TreatmentRequest.query.filter_by(reference_id='TR-60B44F95ED').first()
        if tr:
            print(f"3. TR-60B44F95ED still exists: True")
        else:
            print(f"3. TR-60B44F95ED still exists: False (Not found in DB)")
            
        # 4. Existing Mayo proposal data remains unchanged
        proposals = TreatmentProposal.query.filter_by(hospital_id=2).all()
        print(f"4. Existing Mayo proposals count: {len(proposals)}")
        for p in proposals:
            print(f"   - Proposal {p.id} for Request {p.treatment_request.reference_id if p.treatment_request else 'Unknown'}")
            
        # 6. Matching logic recognizes Mayo as specialty-eligible for Cardiology requests
        # We can test the app logic by calling the internal function
        from app import _is_hospital_eligible
        is_eligible = _is_hospital_eligible(mayo, "Cardiology")
        print(f"6. Matching logic recognizes Mayo for Cardiology: {is_eligible}")
        
        # 7. No duplicate Specialty records
        total_cardio = Specialty.query.filter_by(name="Cardiology").count()
        print(f"7. No duplicate Specialty records (Count of 'Cardiology' = {total_cardio})")

if __name__ == '__main__':
    verify()
