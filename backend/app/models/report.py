"""
app/models/report.py
─────────────────────────────────────────────────────────────────
Reports table — metadata for generated PDF/CSV reports, pointing
to S3 (or local) storage.

Relationships:
  Report ∞──1 Patient (Many-to-One)
─────────────────────────────────────────────────────────────────
"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ── FK to Patients ────────────────────────────────────────
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.patient_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Report Details ────────────────────────────────────────
    report_type = Column(String(50), nullable=False)  # e.g., "monthly_summary", "ml_analysis"
    file_url    = Column(String(500), nullable=False) # S3 bucket URL or local path
    generated_by= Column(UUID(as_uuid=True), nullable=True) # ID of user who clicked 'generate'

    # ── Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # ── Relationships ─────────────────────────────────────────
    patient = relationship("Patient", back_populates="reports")

    def __repr__(self) -> str:
        return f"<Report id={self.report_id} type={self.report_type}>"
