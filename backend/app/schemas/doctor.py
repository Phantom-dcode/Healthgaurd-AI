"""
app/schemas/doctor.py
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DoctorCreate(BaseModel):
    specialization:   Optional[str] = None
    license_number:   Optional[str] = None
    hospital_name:    Optional[str] = None
    years_experience: Optional[int] = None
    bio:              Optional[str] = None


class DoctorUpdate(DoctorCreate):
    pass


class DoctorResponse(DoctorCreate):
    doctor_id:  uuid.UUID
    user_id:    uuid.UUID
    created_at: datetime

    user_name:  Optional[str] = None
    user_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AssignPatientRequest(BaseModel):
    patient_id: uuid.UUID


class AssignmentResponse(BaseModel):
    doctor_id:  uuid.UUID
    patient_id: uuid.UUID
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)
