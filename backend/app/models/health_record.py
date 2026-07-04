"""
app/models/health_record.py
─────────────────────────────────────────────────────────────────
Health Records table — stores time-series vital signs and 
biomarkers for a Patient.

Relationships:
  HealthRecord ∞──1 Patient (Many-to-One)
─────────────────────────────────────────────────────────────────
"""
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy import Uuid as UUID, JSON as JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class HealthRecord(Base):
    __tablename__ = "health_records"

    record_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ── FK to Patients ────────────────────────────────────────
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.patient_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Vitals & Biomarkers ───────────────────────────────────
    heart_rate        = Column(Numeric(5, 2), nullable=True)  # bpm
    blood_pressure_sys= Column(Numeric(5, 2), nullable=True)  # mmHg (Systolic)
    blood_pressure_dia= Column(Numeric(5, 2), nullable=True)  # mmHg (Diastolic)
    oxygen_saturation = Column(Numeric(5, 2), nullable=True)  # % (SpO2)
    temperature       = Column(Numeric(5, 2), nullable=True)  # Celsius
    blood_sugar       = Column(Numeric(5, 2), nullable=True)  # mg/dL
    
    # Allow arbitrary extra data (e.g. ECG arrays, bespoke metrics)
    extra_metrics     = Column(JSONB, nullable=True)

    # ── Timestamps ────────────────────────────────────────────
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(),
                         onupdate=func.now(), nullable=False)

    # ── Relationships ─────────────────────────────────────────
    patient = relationship("Patient", back_populates="health_records")

    def __repr__(self) -> str:
        return f"<HealthRecord id={self.record_id} patient_id={self.patient_id}>"
