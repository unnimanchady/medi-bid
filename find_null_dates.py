from app import app
from models import db, TreatmentProposal

with app.app_context():
    props = TreatmentProposal.query.filter(TreatmentProposal.submitted_at == None).all()
    for p in props:
        print(f"Proposal ID: {p.id}, Status: {p.status}, Created: {p.created_at}")
