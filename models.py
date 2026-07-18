from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )
    
    phone = db.Column(
    db.String(30),
    unique=True,
    nullable=True,
    index=True
)

    password_hash = db.Column(
        db.String(255),
        nullable=True
    )

    role = db.Column(
        db.String(50),
        nullable=False,
        default="patient",
        index=True
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )


class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    patient_id = db.Column(
        db.String(20),
        unique=True,
        nullable=True,
        index=True
    )
    
    relationship_type = db.Column(
        db.String(50),
        nullable=False,
        default="Self"
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    gender = db.Column(
        db.String(20),
        nullable=False
    )

    nationality = db.Column(
        db.String(100),
        nullable=False
    )

    country_of_residence = db.Column(
        db.String(100),
        nullable=False
    )
    
    city = db.Column(
        db.String(100),
        nullable=False
    )
    
    passport_number = db.Column(
        db.String(100),
        nullable=True
    )
    
    pregnancy_status = db.Column(
        db.String(20),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "patient_profiles",
            cascade="all, delete-orphan"
        )
    )

    treatment_requests = db.relationship(
        "TreatmentRequest",
        backref="patient_profile",
        cascade="all, delete-orphan"
    )



class TreatmentRequest(db.Model):
    __tablename__ = "treatment_requests"

    id = db.Column(db.Integer, primary_key=True)

    reference_id = db.Column(db.String(20), unique=True, nullable=False, index=True)

    patient_profile_id = db.Column(
        db.Integer,
        db.ForeignKey("patient_profiles.id"),
        nullable=False,
        index=True
    )

    status = db.Column(db.String(20), nullable=False, default="Active", index=True)

    specialty = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(255), nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    symptoms = db.Column(db.Text, nullable=True)
    previous_treatments = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    
    allergies = db.Column(db.JSON, nullable=True)
    allergy_other_text = db.Column(db.String(255), nullable=True)
    blood_group = db.Column(db.String(10), nullable=True)
    
    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    height_ft = db.Column(db.Float, nullable=True)
    height_in = db.Column(db.Float, nullable=True)
    weight_lbs = db.Column(db.Float, nullable=True)

    emergency_name = db.Column(db.String(100), nullable=True)
    emergency_relationship = db.Column(db.String(50), nullable=True)
    emergency_country_code = db.Column(db.String(10), nullable=True)
    emergency_phone = db.Column(db.String(30), nullable=True)

    timeframe = db.Column(db.String(100), nullable=True)
    location_preference = db.Column(db.String(100), nullable=True)
    specific_countries = db.Column(db.JSON, nullable=True)
    assistance_required = db.Column(db.JSON, nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )