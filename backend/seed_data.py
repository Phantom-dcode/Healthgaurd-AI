import sys
import os
import uuid
from datetime import datetime, date

# Add the backend directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.patient import Patient
from app.models.doctor import Doctor, DoctorPatient
from app.models.health_record import HealthRecord
from app.models.alert import Alert, AlertType, SeverityLevel
from app.models.prediction import Prediction
from app.core.security import hash_password

db = SessionLocal()

def seed():
    print("Starting data seeding...")
    # Check if admin already exists to prevent duplicate
    admin_email = "doctor@healthguard.com"
    existing = db.query(User).filter(User.email == admin_email).first()
    if existing:
        print("Data already seeded!")
        return

    # Create a Doctor
    doc_user = User(
        name="Dr. Sarah Connor",
        email=admin_email,
        password_hash=hash_password("password123"),
        role=UserRole.doctor
    )
    db.add(doc_user)
    db.flush()
    
    doc_profile = Doctor(
        user_id=doc_user.id,
        specialization="Cardiology",
        license_number="CARDIO-9921",
        hospital_name="Central Hospital"
    )
    db.add(doc_profile)
    db.flush()
    
    # Create Patients
    patients_data = [
        {"name": "John Doe", "email": "john@example.com", "dob": date(1980, 5, 14), "blood": "O+", "conditions": "Hypertension"},
        {"name": "Alice Smith", "email": "alice@example.com", "dob": date(1992, 11, 23), "blood": "A-", "conditions": "Asthma"},
        {"name": "Bob Johnson", "email": "bob@example.com", "dob": date(1975, 2, 10), "blood": "B+", "conditions": "Diabetes Type 2"}
    ]
    
    for pd in patients_data:
        p_user = User(
            name=pd["name"],
            email=pd["email"],
            password_hash=hash_password("password123"),
            role=UserRole.patient
        )
        db.add(p_user)
        db.flush()
        
        p_profile = Patient(
            user_id=p_user.id,
            date_of_birth=pd["dob"],
            gender="male" if pd["name"] in ["John Doe", "Bob Johnson"] else "female",
            blood_group=pd["blood"],
            medical_history=pd["conditions"],
            emergency_phone="555-0192"
        )
        db.add(p_profile)
        db.flush()
        
        # Assign patient to doctor
        assignment = DoctorPatient(
            doctor_id=doc_profile.doctor_id,
            patient_id=p_profile.patient_id
        )
        db.add(assignment)
        
        # Add a Health Record
        hr = HealthRecord(
            patient_id=p_profile.patient_id,
            heart_rate=85 if pd["name"] != "John Doe" else 115,
            blood_pressure_sys=120 if pd["name"] != "John Doe" else 150,
            blood_pressure_dia=80 if pd["name"] != "John Doe" else 95,
            temperature=98.6,
            oxygen_saturation=98,
            extra_metrics={"respiratory_rate": 16, "notes": f"Routine checkup for {pd['name']}."}
        )
        db.add(hr)
        
    db.commit()
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed()
