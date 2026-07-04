"""
app/models/patient.py
─────────────────────────────────────────────────────────────────
Patients table — extends a User with clinical profile data.
One-to-One with User (each patient has exactly one user account).

Relationships:
  Patient 1──1 User
  Patient 1──∞ HealthRecord
  Patient 1──∞ Alert
  Patient 1──∞ Prediction
  Patient 1──∞ Report
  Patient ∞──∞ Doctor  (via DoctorPatient junction)
─────────────────────────────────────────────────────────────────
"""
import uuid
import enum
from sqlalchemy import (
    Column, String, Date, Numeric, Text,
    DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class GenderType(str, enum.Enum):
    male   = "male"
    female = "female"
    other  = "other"


class BloodGroup(str, enum.Enum):
    A_pos  = "A+"
    A_neg  = "A-"
    B_pos  = "B+"
    B_neg  = "B-"
    AB_pos = "AB+"
    AB_neg = "AB-"
    O_pos  = "O+"
    O_neg  = "O-"


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ── FK to Users ───────────────────────────────────────────
    # unique=True enforces the 1:1 relationship at the DB level
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ── Clinical Profile ──────────────────────────────────────
    date_of_birth     = Column(Date, nullable=True)
    gender            = Column(SAEnum(GenderType,  name="gender_type",  create_type=True), nullable=True)
    height_cm         = Column(Numeric(5, 2), nullable=True)     # e.g. 172.50 cm
    blood_group       = Column(SAEnum(BloodGroup,  name="blood_group",  create_type=True), nullable=True)
    emergency_contact = Column(String(100), nullable=True)
    emergency_phone   = Column(String(20),  nullable=True)
    medical_history   = Column(Text, nullable=True)

    # ── Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    # ── Relationships ─────────────────────────────────────────
    user           = relationship("User",          back_populates="patient")
    health_records = relationship("HealthRecord",  back_populates="patient",
                                  cascade="all, delete-orphan", order_by="HealthRecord.recorded_at.desc()")
    alerts         = relationship("Alert",         back_populates="patient",
                                  cascade="all, delete-orphan")
    predictions    = relationship("Prediction",    back_populates="patient",
                                  cascade="all, delete-orphan")
    reports        = relationship("Report",        back_populates="patient",
                                  cascade="all, delete-orphan")
    doctor_assignments = relationship("DoctorPatient", back_populates="patient",
                                      cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Patient id={self.patient_id} user_id={self.user_id}>"
