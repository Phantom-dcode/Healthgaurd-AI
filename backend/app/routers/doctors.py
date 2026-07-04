"""
app/routers/doctors.py  — /api/v1/doctors/*
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database        import get_db
from app.dependencies    import require_doctor, require_admin, get_current_user
from app.models.user     import User
from app.models.doctor   import Doctor, DoctorPatient
from app.schemas.doctor  import DoctorUpdate, DoctorResponse, AssignPatientRequest, AssignmentResponse
from app.schemas.common  import APIResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])


def _enrich(d: Doctor) -> dict:
    data = DoctorResponse.model_validate(d).model_dump()
    if d.user:
        data["user_name"]  = d.user.name
        data["user_email"] = d.user.email
    return data


@router.get("/me", response_model=APIResponse[DoctorResponse])
def get_my_profile(
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db),
):
    doc = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(404, "Doctor profile not found")
    return APIResponse.ok(data=_enrich(doc))


@router.put("/me", response_model=APIResponse[DoctorResponse])
def update_profile(
    body: DoctorUpdate,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db),
):
    doc = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(404, "Doctor profile not found")
    for f, v in body.model_dump(exclude_unset=True).items():
        setattr(doc, f, v)
    db.commit(); db.refresh(doc)
    return APIResponse.ok(data=_enrich(doc))


@router.get("/my-patients", response_model=APIResponse[list])
def my_patients(
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db),
):
    """Return all patients assigned to this doctor."""
    doc = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    assignments = db.query(DoctorPatient).filter(
        DoctorPatient.doctor_id == doc.doctor_id,
    ).all()
    patients_data = []
    for a in assignments:
        p = a.patient
        patients_data.append({
            "patient_id":   str(p.patient_id),
            "name":         p.user.name  if p.user else None,
            "email":        p.user.email if p.user else None,
            "assigned_at":  a.assigned_at.isoformat(),
        })
    return APIResponse.ok(data=patients_data)


@router.post("/assign-patient", response_model=APIResponse[AssignmentResponse])
def assign_patient(
    body: AssignPatientRequest,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db),
):
    """Assign a patient to this doctor."""
    doc = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    existing = db.query(DoctorPatient).filter(
        DoctorPatient.doctor_id  == doc.doctor_id,
        DoctorPatient.patient_id == body.patient_id,
    ).first()
    if existing:
        return APIResponse.ok(data=AssignmentResponse.model_validate(existing))

    assignment = DoctorPatient(doctor_id=doc.doctor_id, patient_id=body.patient_id)
    db.add(assignment); db.commit(); db.refresh(assignment)
    return APIResponse.ok(data=AssignmentResponse.model_validate(assignment))


@router.get("/", response_model=APIResponse[List[DoctorResponse]])
def list_doctors(
    skip: int = 0, limit: int = 50,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    docs = db.query(Doctor).offset(skip).limit(limit).all()
    return APIResponse.ok(data=[_enrich(d) for d in docs])
