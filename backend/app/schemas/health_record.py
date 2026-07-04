"""
app/schemas/health_record.py
Pydantic schemas for health record input/output.
Validators mirror the DB CHECK constraints — invalid values are
rejected at the API layer BEFORE reaching the database.
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class HealthRecordCreate(BaseModel):
    systolic_bp:  Optional[int]     = None
    diastolic_bp: Optional[int]     = None
    heart_rate:   Optional[int]     = None
    blood_sugar:  Optional[Decimal] = None
    oxygen_level: Optional[Decimal] = None
    temperature:  Optional[Decimal] = None
    weight_kg:    Optional[Decimal] = None
    notes:        Optional[str]     = None
    recorded_at:  Optional[datetime] = None

    @field_validator("systolic_bp")
    @classmethod
    def validate_systolic(cls, v):
        if v is not None and not (50 <= v <= 300):
            raise ValueError("Systolic BP must be between 50 and 300 mmHg")
        return v

    @field_validator("diastolic_bp")
    @classmethod
    def validate_diastolic(cls, v):
        if v is not None and not (30 <= v <= 200):
            raise ValueError("Diastolic BP must be between 30 and 200 mmHg")
        return v

    @field_validator("heart_rate")
    @classmethod
    def validate_hr(cls, v):
        if v is not None and not (20 <= v <= 300):
            raise ValueError("Heart rate must be between 20 and 300 bpm")
        return v

    @field_validator("blood_sugar")
    @classmethod
    def validate_sugar(cls, v):
        if v is not None and not (20 <= float(v) <= 600):
            raise ValueError("Blood sugar must be between 20 and 600 mg/dL")
        return v

    @field_validator("oxygen_level")
    @classmethod
    def validate_o2(cls, v):
        if v is not None and not (50 <= float(v) <= 100):
            raise ValueError("Oxygen level must be between 50% and 100%")
        return v

    @field_validator("temperature")
    @classmethod
    def validate_temp(cls, v):
        if v is not None and not (30 <= float(v) <= 45):
            raise ValueError("Temperature must be between 30°C and 45°C")
        return v

    @field_validator("weight_kg")
    @classmethod
    def validate_weight(cls, v):
        if v is not None and not (1 <= float(v) <= 500):
            raise ValueError("Weight must be between 1 and 500 kg")
        return v

    @model_validator(mode="after")
    def bp_logic(self):
        s = self.systolic_bp
        d = self.diastolic_bp
        if s is not None and d is not None and s <= d:
            raise ValueError("Systolic BP must be greater than diastolic BP")
        return self


class HealthRecordResponse(BaseModel):
    record_id:    uuid.UUID
    patient_id:   uuid.UUID
    systolic_bp:  Optional[int]     = None
    diastolic_bp: Optional[int]     = None
    heart_rate:   Optional[int]     = None
    blood_sugar:  Optional[Decimal] = None
    oxygen_level: Optional[Decimal] = None
    temperature:  Optional[Decimal] = None
    weight_kg:    Optional[Decimal] = None
    notes:        Optional[str]     = None
    recorded_at:  datetime
    created_at:   datetime

    model_config = ConfigDict(from_attributes=True)
