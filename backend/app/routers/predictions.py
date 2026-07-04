"""
app/routers/predictions.py  — /api/v1/predictions/*
"""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database              import get_db
from app.dependencies          import get_current_user, require_patient
from app.models.user           import User, UserRole
from app.models.patient        import Patient
from app.models.health_record  import HealthRecord
from app.models.prediction     import Prediction
from app.schemas.alert         import PredictionResponse, PredictRequest
from app.schemas.common        import APIResponse
from app.services.prediction_service import predict_risk

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/predict", response_model=APIResponse[PredictionResponse])
def run_prediction(
    body: PredictRequest,
    current_user: User = Depends(require_patient),
    db: Session = Depends(get_db),
):
    """[Patient] Manually trigger an AI risk prediction from the latest (or specified) record."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(404, "Patient profile not found")

    if body.record_id:
        record = db.query(HealthRecord).filter(
            HealthRecord.record_id == body.record_id,
            HealthRecord.patient_id == patient.patient_id,
        ).first()
        if not record:
            raise HTTPException(404, "Health record not found")
    else:
        record = (
            db.query(HealthRecord)
            .filter(HealthRecord.patient_id == patient.patient_id)
            .order_by(HealthRecord.recorded_at.desc())
            .first()
        )
        if not record:
            raise HTTPException(404, "No health records found. Submit a record first.")

    prediction = predict_risk(patient, record, db)
    return APIResponse.ok(
        data=PredictionResponse.model_validate(prediction),
        message=f"Risk level: {prediction.risk_level.value.upper()}",
    )


@router.get("/", response_model=APIResponse[List[PredictionResponse]])
def list_predictions(
    patient_id: Optional[uuid.UUID] = Query(None),
    skip: int = 0, limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Prediction)
    if current_user.role == UserRole.patient:
        p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if not p:
            return APIResponse.ok(data=[])
        q = q.filter(Prediction.patient_id == p.patient_id)
    elif patient_id:
        q = q.filter(Prediction.patient_id == patient_id)

    preds = q.order_by(Prediction.created_at.desc()).offset(skip).limit(limit).all()
    return APIResponse.ok(data=[PredictionResponse.model_validate(p) for p in preds])


@router.get("/latest", response_model=APIResponse[PredictionResponse])
def latest_prediction(
    current_user: User = Depends(require_patient),
    db: Session = Depends(get_db),
):
    """[Patient] Get own most recent prediction — used on dashboard."""
    p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not p:
        raise HTTPException(404, "Patient profile not found")
    pred = (
        db.query(Prediction)
        .filter(Prediction.patient_id == p.patient_id)
        .order_by(Prediction.created_at.desc())
        .first()
    )
    if not pred:
        raise HTTPException(404, "No predictions yet. Submit a health record first.")
    return APIResponse.ok(data=PredictionResponse.model_validate(pred))
