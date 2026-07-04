"""app/routers/reports.py  — /api/v1/reports/*"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database       import get_db
from app.dependencies   import get_current_user, require_doctor
from app.models.user    import User, UserRole
from app.models.patient import Patient
from app.models.doctor  import Doctor
from app.models.report  import Report
from app.schemas.alert  import ReportCreate, ReportResponse
from app.schemas.common import APIResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/", response_model=APIResponse[ReportResponse], status_code=201)
def create_report(
    body: ReportCreate,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db),
):
    doc = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    report = Report(
        patient_id=body.patient_id, doctor_id=doc.doctor_id,
        title=body.title, date_from=body.date_from, date_to=body.date_to,
    )
    db.add(report); db.commit(); db.refresh(report)
    data = ReportResponse.model_validate(report).model_dump()
    if report.patient and report.patient.user:
        data["patient_name"] = report.patient.user.name
    data["doctor_name"] = current_user.name
    return APIResponse.ok(data=data, message="Report created")

@router.get("/", response_model=APIResponse[List[ReportResponse]])
def list_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Report)
    if current_user.role == UserRole.doctor:
        doc = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
        if doc: q = q.filter(Report.doctor_id == doc.doctor_id)
    elif current_user.role == UserRole.patient:
        p = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if p: q = q.filter(Report.patient_id == p.patient_id)
    reports = q.order_by(Report.created_at.desc()).all()
    return APIResponse.ok(data=[ReportResponse.model_validate(r) for r in reports])
