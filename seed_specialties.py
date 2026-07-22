from app import app
from models import db, Specialty
import re

SPECIALTIES = [
    "Cardiology",
    "Cardiothoracic Surgery",
    "Oncology",
    "Neurology",
    "Neurosurgery",
    "Orthopedics",
    "Gastroenterology",
    "General Surgery",
    "Urology",
    "Nephrology",
    "Pulmonology",
    "Endocrinology",
    "Rheumatology",
    "Dermatology",
    "Ophthalmology",
    "ENT / Otolaryngology",
    "Obstetrics & Gynecology",
    "Pediatrics",
    "Pediatric Surgery",
    "Fertility & Reproductive Medicine",
    "Transplant Medicine & Surgery",
    "Hematology",
    "Plastic & Reconstructive Surgery",
    "Vascular Surgery",
    "Bariatric Surgery",
    "Dental & Maxillofacial Surgery",
    "Rehabilitation Medicine",
    "Psychiatry & Mental Health"
]

def generate_slug(name):
    # Convert to lowercase
    slug = name.lower()
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading and trailing hyphens
    return slug.strip('-')

with app.app_context():
    added = 0
    for name in SPECIALTIES:
        slug = generate_slug(name)
        existing = Specialty.query.filter_by(slug=slug).first()
        if not existing:
            specialty = Specialty(name=name, slug=slug)
            db.session.add(specialty)
            added += 1
    
    if added > 0:
        db.session.commit()
        print(f"Successfully added {added} specialties.")
    else:
        print("All specialties already exist.")
