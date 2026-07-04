"""
app/routers/patients.py  — /api/v1/patients/*
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database         import get_db
from app.dependencies     import get_current_user, require_patient, require_doctor_or_admin
from app.models.user      import User
from app.models.patient   import Patient
from app.schemas.patient  import PatientCreate, PatientUpdate, PatientResponse
from app.schemas.common   import APIResponse

router = APIRouter(prefix="/patients", tags=["Patients"])


def _enrich(p: Patient) -> dict:
    d = PatientResponse.model_validate(p).model_dump()
    if p.user:
        d["user_name"]  = p.user.name
        d["user_email"] = p.user.email
    return d


@router.get("/", response_model=APIResponse[List[PatientResponse]])
def list_patients(
    skip: int = 0, limit: int = 50,
    _user: User = Depends(require_doctor_or_admin),
    db: Session = Depends(get_db),
):
    """[Doctor/Admin] List all patients."""
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return APIResponse.ok(data=[_enrich(p) for p in patients])


@router.get("/me", response_model=APIResponse[PatientResponse])
def get_my_profile(
    current_user: User = Depends(require_patient),
    db: Session = Depends(get_db),
):
    """[Patient] Get own patient profile."""
    p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return APIResponse.ok(data=_enrich(p))


@router.put("/me", response_model=APIResponse[PatientResponse])
def update_my_profile(
    body: PatientUpdate,
    current_user: User = Depends(require_patient),
    db: Session = Depends(get_db),
):
    """[Patient] Update own clinical profile."""
    p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    db.commit(); db.refresh(p)
    return APIResponse.ok(data=_enrich(p))


@router.get("/{patient_id}", response_model=APIResponse[PatientResponse])
def get_patient(
    patient_id: uuid.UUID,
    _user: User = Depends(require_doctor_or_admin),
    db: Session = Depends(get_db),
):
    """[Doctor/Admin] Get a specific patient."""
    p = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return APIResponse.ok(data=_enrich(p))
