from app import app
from models import db, Language
import re

LANGUAGES = [
    "English",
    "Arabic",
    "French",
    "Spanish",
    "German",
    "Russian",
    "Hindi",
    "Malayalam",
    "Tamil",
    "Bengali",
    "Mandarin Chinese",
    "Japanese",
    "Korean",
    "Portuguese",
    "Turkish"
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
    for name in LANGUAGES:
        slug = generate_slug(name)
        existing = Language.query.filter_by(slug=slug).first()
        if not existing:
            language = Language(name=name, slug=slug)
            db.session.add(language)
            added += 1
    
    if added > 0:
        db.session.commit()
        print(f"Successfully added {added} languages.")
    else:
        print("All languages already exist.")
