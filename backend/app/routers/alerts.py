"""
app/routers/alerts.py  — /api/v1/alerts/*
"""
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database       import get_db
from app.dependencies   import get_current_user, require_doctor_or_admin
from app.models.user    import User, UserRole
from app.models.patient import Patient
from app.models.alert   import Alert, SeverityLevel
from app.schemas.alert  import AlertResponse, AlertUpdateRequest
from app.schemas.common import APIResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=APIResponse[List[AlertResponse]])
def list_alerts(
    severity: Optional[SeverityLevel] = Query(None),
    unread_only: bool = Query(False),
    patient_id: Optional[uuid.UUID] = Query(None),
    skip: int = 0, limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Alert)

    if current_user.role == UserRole.patient:
        p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if not p:
            return APIResponse.ok(data=[])
        q = q.filter(Alert.patient_id == p.patient_id)
    elif patient_id:
        q = q.filter(Alert.patient_id == patient_id)

    if severity:
        q = q.filter(Alert.severity == severity)
    if unread_only:
        q = q.filter(Alert.is_read == False)

    alerts = q.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    return APIResponse.ok(data=[AlertResponse.model_validate(a) for a in alerts])


@router.patch("/{alert_id}", response_model=APIResponse[AlertResponse])
def update_alert(
    alert_id: uuid.UUID,
    body: AlertUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(404, "Alert not found")

    if body.is_read is not None:
        alert.is_read = body.is_read
    if body.is_resolved is not None:
        alert.is_resolved = body.is_resolved
        if body.is_resolved:
            alert.resolved_at = datetime.now(timezone.utc)

    db.commit(); db.refresh(alert)
    return APIResponse.ok(data=AlertResponse.model_validate(alert))


@router.get("/summary", response_model=APIResponse[dict])
def alerts_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns counts per severity for the dashboard KPI cards."""
    q = db.query(Alert)
    if current_user.role == UserRole.patient:
        p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if p:
            q = q.filter(Alert.patient_id == p.patient_id)

    total    = q.count()
    unread   = q.filter(Alert.is_read == False).count()
    critical = q.filter(Alert.severity == SeverityLevel.critical).count()
    high     = q.filter(Alert.severity == SeverityLevel.high).count()

    return APIResponse.ok(data={
        "total": total, "unread": unread,
        "critical": critical, "high": high,
    })
