from app import app
from models import db, Specialty

def count_spec():
    with app.app_context():
        count = Specialty.query.count()
        print("Total Specialties in DB using SQLAlchemy:", count)
        
        all_specs = Specialty.query.all()
        for s in all_specs:
            print(f"ID: {s.id}, Name: {s.name}")

if __name__ == '__main__':
    count_spec()
