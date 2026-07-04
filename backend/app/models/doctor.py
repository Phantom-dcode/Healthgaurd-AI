"""
app/models/doctor.py
─────────────────────────────────────────────────────────────────
Doctors table — extends a User with professional profile data.
One-to-One with User.
Many-to-Many with Patient (via DoctorPatient).

Relationships:
  Doctor 1──1 User
  Doctor ∞──∞ Patient (via DoctorPatient junction)
─────────────────────────────────────────────────────────────────
"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DoctorPatient(Base):
    """
    Junction table for Many-to-Many relationship between Doctors and Patients.
    Allows a doctor to have many patients, and a patient to have many doctors.
    """
    __tablename__ = "doctor_patients"

    doctor_id  = Column(UUID(as_uuid=True), ForeignKey("doctors.doctor_id",   ondelete="CASCADE"), primary_key=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id", ondelete="CASCADE"), primary_key=True)

    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    doctor  = relationship("Doctor",  back_populates="patient_assignments")
    patient = relationship("Patient", back_populates="doctor_assignments")


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ── FK to Users ───────────────────────────────────────────
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ── Professional Profile ──────────────────────────────────
    specialization = Column(String(100), nullable=True)  # e.g. "Cardiologist"
    license_number = Column(String(100), nullable=True, unique=True)
    hospital_name  = Column(String(200), nullable=True)

    # ── Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    # ── Relationships ─────────────────────────────────────────
    user = relationship("User", back_populates="doctor")
    
    # Back-populates to the junction table
    patient_assignments = relationship("DoctorPatient", back_populates="doctor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Doctor id={self.doctor_id} user_id={self.user_id} spec={self.specialization}>"
