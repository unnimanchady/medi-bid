import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from models import db, Hospital, Specialty

def restore_mayo():
    with app.app_context():
        hospital = Hospital.query.get(2)
        if not hospital:
            print("Mayo Clinic (ID 2) not found!")
            return
            
        print(f"Hospital: {hospital.display_name}")
        
        # Get specialties
        cardio = Specialty.query.filter_by(name="Cardiology").first()
        gen_surg = Specialty.query.filter_by(name="General Surgery").first()
        
        if not cardio or not gen_surg:
            print("Error: Could not find Cardiology or General Surgery in Specialties table.")
            return
            
        print(f"Found specialties: {cardio.name} (ID: {cardio.id}), {gen_surg.name} (ID: {gen_surg.id})")
        
        # Restore specialties
        hospital.specialties = [cardio, gen_surg]
        db.session.commit()
        print("Restored specialties for Mayo Clinic successfully.")

if __name__ == '__main__':
    restore_mayo()
