"""
app/routers/health_records.py  — /api/v1/health-records/*
"""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database                 import get_db
from app.dependencies             import get_current_user, require_patient, require_doctor_or_admin
from app.models.user              import User, UserRole
from app.models.patient           import Patient
from app.models.health_record     import HealthRecord
from app.schemas.health_record    import HealthRecordCreate, HealthRecordResponse
from app.schemas.common           import APIResponse
from app.services.alert_service   import check_and_create_alerts
from app.services.prediction_service import predict_risk

router = APIRouter(prefix="/health-records", tags=["Health Records"])


@router.post("/", response_model=APIResponse[HealthRecordResponse], status_code=201)
def submit_health_record(
    body: HealthRecordCreate,
    current_user: User = Depends(require_patient),
    db: Session = Depends(get_db),
):
    """
    [Patient] Submit a new vitals reading.
    Automatically:
      1. Saves the record
      2. Runs alert threshold checks
      3. Generates an AI risk prediction
    """
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(404, "Patient profile not found")

    record = HealthRecord(
        patient_id   = patient.patient_id,
        systolic_bp  = body.systolic_bp,
        diastolic_bp = body.diastolic_bp,
        heart_rate   = body.heart_rate,
        blood_sugar  = body.blood_sugar,
        oxygen_level = body.oxygen_level,
        temperature  = body.temperature,
        weight_kg    = body.weight_kg,
        notes        = body.notes,
        recorded_at  = body.recorded_at,
    )
    db.add(record)
    db.flush()   # get record_id before alert creation

    # Auto-generate alerts for any violated thresholds
    check_and_create_alerts(record, db)

    # Auto-generate AI risk prediction
    try:
        predict_risk(patient, record, db)
    except Exception as e:
        # Prediction failure must not block record submission
        import logging; logging.getLogger(__name__).warning(f"Prediction failed: {e}")

    db.commit()
    db.refresh(record)
    return APIResponse.ok(
        data=HealthRecordResponse.model_validate(record),
        message="Health record submitted successfully",
    )


@router.get("/", response_model=APIResponse[List[HealthRecordResponse]])
def list_records(
    patient_id: Optional[uuid.UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Patient   → returns own records only.
    Doctor/Admin → can filter by patient_id.
    """
    q = db.query(HealthRecord)

    if current_user.role == UserRole.patient:
        p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if not p:
            return APIResponse.ok(data=[])
        q = q.filter(HealthRecord.patient_id == p.patient_id)
    elif patient_id:
        q = q.filter(HealthRecord.patient_id == patient_id)

    records = q.order_by(HealthRecord.recorded_at.desc()).offset(skip).limit(limit).all()
    return APIResponse.ok(data=[HealthRecordResponse.model_validate(r) for r in records])


@router.get("/{record_id}", response_model=APIResponse[HealthRecordResponse])
def get_record(
    record_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = db.query(HealthRecord).filter(HealthRecord.record_id == record_id).first()
    if not record:
        raise HTTPException(404, "Record not found")

    # Patients can only see their own records
    if current_user.role == UserRole.patient:
        p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if not p or record.patient_id != p.patient_id:
            raise HTTPException(403, "Access denied")

    return APIResponse.ok(data=HealthRecordResponse.model_validate(record))
