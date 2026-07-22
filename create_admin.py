import sys
from getpass import getpass
from werkzeug.security import generate_password_hash
from app import app, db
from models import User

def create_admin():
    print("=== MediBid Admin Account Creation ===")
    
    with app.app_context():
        email = input("Admin Email: ").strip().lower()
        if not email:
            print("Email is required.")
            sys.exit(1)
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Error: A user with email '{email}' already exists.")
            sys.exit(1)
            
        first_name = input("First Name [Admin]: ").strip() or "Admin"
        last_name = input("Last Name [User]: ").strip() or "User"
        
        password = getpass("Password: ")
        if len(password) < 8:
            print("Error: Password must be at least 8 characters.")
            sys.exit(1)
            
        confirm_password = getpass("Confirm Password: ")
        if password != confirm_password:
            print("Error: Passwords do not match.")
            sys.exit(1)
            
        try:
            admin_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password_hash=generate_password_hash(password),
                role="admin"
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print(f"\nSuccess! Admin account '{email}' created successfully.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Database error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    create_admin()
