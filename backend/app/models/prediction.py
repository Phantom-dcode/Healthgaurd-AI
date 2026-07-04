"""
app/models/prediction.py
─────────────────────────────────────────────────────────────────
Predictions table — stores outputs from ML models (e.g. Sepsis,
Heart Failure, Readmission).

Relationships:
  Prediction ∞──1 Patient (Many-to-One)
─────────────────────────────────────────────────────────────────
"""
import uuid
import enum
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy import Uuid as UUID, JSON as JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class RiskLevel(str, enum.Enum):
    low    = "low"
    medium = "medium"
    high   = "high"


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ── FK to Patients ────────────────────────────────────────
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.patient_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Prediction Details ────────────────────────────────────
    model_name   = Column(String(100), nullable=False)     # e.g., "Sepsis_XGBoost_v1"
    risk_score   = Column(Numeric(5, 4), nullable=False)   # 0.0000 to 1.0000
    risk_level   = Column(SAEnum(RiskLevel, name="risk_level", create_type=True), nullable=False)
    
    # Store feature importances / SHAP values explaining *why* this prediction was made
    explanations = Column(JSONB, nullable=True) 

    # ── Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # ── Relationships ─────────────────────────────────────────
    patient = relationship("Patient", back_populates="predictions")

    def __repr__(self) -> str:
        return f"<Prediction id={self.prediction_id} model={self.model_name} risk={self.risk_level}>"
