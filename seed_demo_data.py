import json
import random
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash
from app import app, db
from models import (
    User, PatientProfile, Hospital, HospitalUser, TreatmentRequest, 
    TreatmentProposal, MessageThread, Message, MedicalDocument, 
    Notification, SupportTicket, SupportTicketMessage, CostLineItem
)

def generate_random_reference():
    import string
    chars = string.ascii_uppercase + string.digits
    return "TR-" + "".join(random.choices(chars, k=10))

def seed_database():
    with app.app_context():
        # 1. Idempotency Check
        if User.query.filter_by(email="admin@medibid.com").first():
            print("Demo data already seeded. Exiting.")
            return

        print("Seeding demo data...")

        # 2. Admin User
        admin_pass = "Admin123!"
        admin_user = User(
            email="admin@medibid.com",
            first_name="Admin",
            last_name="User",
            country_of_residence="USA",
            password_hash=generate_password_hash(admin_pass),
            role="admin"
        )
        db.session.add(admin_user)

        # 3. Patients
        patients_data = [
            {"email": "sijo@example.com", "first": "Sijo", "last": "Kurian", "country": "India"},
            {"email": "jane.smith@example.com", "first": "Jane", "last": "Smith", "country": "USA"},
            {"email": "ali.khan@example.com", "first": "Ali", "last": "Khan", "country": "UAE"}
        ]
        
        patient_pass = "Patient123!"
        patient_users = []
        for p in patients_data:
            user = User(
                email=p["email"],
                first_name=p["first"],
                last_name=p["last"],
                country_of_residence=p["country"],
                password_hash=generate_password_hash(patient_pass),
                role="patient"
            )
            db.session.add(user)
            patient_users.append(user)
        db.session.commit()

        # 4. Patient Profiles
        profiles = []
        for idx, user in enumerate(patient_users):
            profile = PatientProfile(
                user_id=user.id,
                patient_id=f"PT-{1000 + idx}",
                relationship_type="Self",
                first_name=user.first_name,
                last_name=user.last_name,
                date_of_birth=datetime(1980 + idx, 5, 15).date(),
                gender="Male" if idx % 2 == 0 else "Female",
                nationality=user.country_of_residence,
                country_of_residence=user.country_of_residence,
                city="Metropolis"
            )
            db.session.add(profile)
            profiles.append(profile)
        db.session.commit()

        # 5. Hospitals
        hospitals_data = [
            {"legal": "Lisie Hospital", "display": "Lisie Medical Center", "country": "India"},
            {"legal": "Mayo Clinic", "display": "Mayo Clinic", "country": "USA"},
            {"legal": "Cleveland Clinic", "display": "Cleveland Clinic", "country": "USA"},
            {"legal": "Apollo Hospitals", "display": "Apollo Group", "country": "India"}
        ]
        
        hospitals = []
        for h in hospitals_data:
            hospital = Hospital(
                legal_name=h["legal"],
                display_name=h["display"],
                hospital_type="General",
                country=h["country"],
                verification_status="verified"
            )
            db.session.add(hospital)
            hospitals.append(hospital)
        db.session.commit()

        # 6. Hospital Users
        h_user_pass = "Hospital123!"
        hospital_users = []
        for idx, h in enumerate(hospitals):
            h_user = HospitalUser(
                hospital_id=h.id,
                first_name=f"{h.display_name.split()[0]}",
                last_name="Admin",
                work_email=f"admin@{h.display_name.replace(' ', '').lower()}.com",
                password_hash=generate_password_hash(h_user_pass),
                role="hospital_admin"
            )
            db.session.add(h_user)
            hospital_users.append(h_user)
        db.session.commit()

        # 7. Treatment Requests
        conditions = ["Cardiac Bypass", "Knee Replacement", "Spinal Fusion", "Cataract Surgery", "Dental Implants"]
        requests = []
        for i in range(10):
            profile = random.choice(profiles)
            req = TreatmentRequest(
                reference_id=generate_random_reference(),
                patient_profile_id=profile.id,
                status="Active",
                specialty="General Surgery",
                condition=random.choice(conditions),
                symptoms="Patient reports moderate to severe symptoms.",
                current_weight=75.0,
                current_weight_unit="kg"
            )
            db.session.add(req)
            requests.append(req)
        db.session.commit()

        # 8. Medical Documents
        for req in requests:
            doc = MedicalDocument(
                treatment_request_id=req.id,
                uploaded_by_id=req.patient_profile.user_id,
                patient_profile_id=req.patient_profile_id,
                original_filename="medical_report.pdf",
                storage_filename=f"medical_report_{req.id}.pdf",
                document_type="Medical Report",
                mime_type="application/pdf",
                file_size=102400
            )
            db.session.add(doc)
        db.session.commit()

        # 9. Treatment Proposals
        proposals = []
        for req in requests[:6]:
            hospitals_sample = random.sample(hospitals, 2)
            for h in hospitals_sample:
                prop = TreatmentProposal(
                    treatment_request_id=req.id,
                    hospital_id=h.id,
                    status="submitted",
                    proposed_treatment=req.condition,
                    treatment_plan=f"We will perform {req.condition} using advanced techniques.",
                    currency="USD",
                    estimated_cost_min=5000.0,
                    estimated_cost_max=7000.0,
                    valid_until=(datetime.now(timezone.utc) + timedelta(days=30)).date()
                )
                db.session.add(prop)
                proposals.append(prop)
        db.session.commit()
        
        for prop in proposals:
            item = CostLineItem(
                proposal_id=prop.id,
                description="Surgical Procedure",
                amount=6000.0
            )
            db.session.add(item)
        db.session.commit()

        # 10. Secure Messages
        for prop in proposals[:3]:
            thread = MessageThread(
                treatment_request_id=prop.treatment_request_id,
                hospital_id=prop.hospital_id
            )
            db.session.add(thread)
            db.session.commit()

            msg1 = Message(
                thread_id=thread.id,
                sender_type="patient",
                sender_user_id=prop.treatment_request.patient_profile.user_id,
                message_body="Hello, I have a question about the proposal."
            )
            msg2 = Message(
                thread_id=thread.id,
                sender_type="hospital",
                sender_hospital_id=prop.hospital_id,
                message_body="Please feel free to ask."
            )
            db.session.add_all([msg1, msg2])
        db.session.commit()

        # 11. Notifications
        for user in patient_users:
            notif = Notification(
                recipient_type="patient",
                recipient_user_id=user.id,
                title="Welcome to TreatAnywhere",
                message="Thank you for registering on TreatAnywhere.",
                notification_type="welcome"
            )
            db.session.add(notif)
        db.session.commit()

        # 12. Support Tickets
        for user in patient_users[:1]:
            ticket = SupportTicket(
                ticket_number=f"TKT-{random.randint(1000, 9999)}",
                user_id=user.id,
                subject="Upload Issue",
                category="Technical",
                message="I cannot upload my documents."
            )
            db.session.add(ticket)
            db.session.commit()
            
            ticket_msg = SupportTicketMessage(
                ticket_id=ticket.id,
                sender_type="patient",
                message="I cannot upload my documents."
            )
            db.session.add(ticket_msg)
        db.session.commit()

        # 13. Print Credentials
        print("\n--- DEMO ACCOUNTS CREATED SUCCESSFULLY ---")
        print("\nAdmin Account:")
        print(f"Email: {admin_user.email} | Password: {admin_pass}")

        print("\nPatient Accounts:")
        for p in patient_users:
            print(f"Email: {p.email} | Password: {patient_pass}")

        print("\nHospital Admin Accounts:")
        for h in hospital_users:
            print(f"Email: {h.work_email} | Password: {h_user_pass} | Hospital: {Hospital.query.get(h.hospital_id).display_name}")

if __name__ == "__main__":
    seed_database()
