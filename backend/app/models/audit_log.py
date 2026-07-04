"""
app/models/audit_log.py
─────────────────────────────────────────────────────────────────
Audit Logs table — system-wide audit trail for compliance (HIPAA).
Tracks WHO did WHAT and WHEN.

Relationships:
  AuditLog ∞──1 User (Many-to-One)
─────────────────────────────────────────────────────────────────
"""
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ── FK to Users ───────────────────────────────────────────
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ── Audit Details ─────────────────────────────────────────
    action        = Column(String(100), nullable=False) # e.g., "VIEW_PATIENT", "LOGIN"
    resource_type = Column(String(50), nullable=True)   # e.g., "HealthRecord"
    resource_id   = Column(String(100), nullable=True)  # UUID string of the resource accessed
    ip_address    = Column(String(45), nullable=True)
    user_agent    = Column(Text, nullable=True)
    
    # ── Timestamps ────────────────────────────────────────────
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # ── Relationships ─────────────────────────────────────────
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self) -> str:
        return f"<AuditLog id={self.log_id} action={self.action} user={self.user_id}>"
