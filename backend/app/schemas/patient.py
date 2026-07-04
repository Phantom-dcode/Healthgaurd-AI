"""
app/schemas/patient.py
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.patient import GenderType, BloodGroup


class PatientCreate(BaseModel):
    date_of_birth:     Optional[date]       = None
    gender:            Optional[GenderType] = None
    height_cm:         Optional[Decimal]    = None
    blood_group:       Optional[BloodGroup] = None
    emergency_contact: Optional[str]        = None
    emergency_phone:   Optional[str]        = None
    medical_history:   Optional[str]        = None


class PatientUpdate(PatientCreate):
    pass


class PatientResponse(PatientCreate):
    patient_id: uuid.UUID
    user_id:    uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Nested user info
    user_name:  Optional[str] = None
    user_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
