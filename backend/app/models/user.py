"""
app/models/user.py
─────────────────────────────────────────────────────────────────
Users table — the root identity record for every person in the
system (patient, doctor, admin). Every other profile table
points back to a user_id here.

Relationships:
  User 1──1 Patient   (one-to-one: user can have one patient profile)
  User 1──1 Doctor    (one-to-one: user can have one doctor profile)
  User 1──∞ AuditLog  (one-to-many: user has many activity logs)
─────────────────────────────────────────────────────────────────
"""
import uuid
import enum
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserRole(str, enum.Enum):
    """Defines which portal and permissions the user gets."""
    patient = "patient"
    doctor  = "doctor"
    admin   = "admin"


class User(Base):
    __tablename__ = "users"

    # ── Primary Key ───────────────────────────────────────────
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # ── Core Fields ───────────────────────────────────────────
    name          = Column(String(100), nullable=False)
    email         = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role          = Column(
        SAEnum(UserRole, name="user_role", create_type=True),
        nullable=False,
        default=UserRole.patient,
        index=True,
    )
    is_active  = Column(Boolean, nullable=False, default=True, index=True)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # ── Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    # ── Relationships ─────────────────────────────────────────
    # uselist=False → one-to-one
    patient    = relationship("Patient",   back_populates="user",
                              uselist=False, cascade="all, delete-orphan")
    doctor     = relationship("Doctor",    back_populates="user",
                              uselist=False, cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog",  back_populates="user",
                              cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"
