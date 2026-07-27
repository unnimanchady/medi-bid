import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from models import db, Specialty, Hospital, hospital_specialty
from sqlalchemy import text

def restore_specialties():
    with app.app_context():
        # Let's count specialties using SQLAlchemy
        count = Specialty.query.count()
        print(f"SQLAlchemy counts {count} specialties.")
        
        all_specs = Specialty.query.all()
        for s in all_specs:
            print(f"ID: {s.id}, Name: {s.name}")

if __name__ == "__main__":
    restore_specialties()
