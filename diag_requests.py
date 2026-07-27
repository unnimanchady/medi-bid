import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from models import db, TreatmentRequest

def diagnose_requests():
    with app.app_context():
        requests = TreatmentRequest.query.all()
        for r in requests:
            print(f"Ref: {r.reference_id} | Specialty: {r.specialty} | Condition: {r.condition} | Created: {r.created_at}")

if __name__ == '__main__':
    diagnose_requests()
