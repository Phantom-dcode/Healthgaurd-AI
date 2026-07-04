"""app/routers/audit_logs.py  — /api/v1/audit-logs/*"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database        import get_db
from app.dependencies    import require_admin
from app.models.user     import User
from app.models.audit_log import AuditLog
from app.schemas.common  import APIResponse

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.get("/", response_model=APIResponse[List[dict]])
def list_logs(
    skip: int = 0, limit: int = 100,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    return APIResponse.ok(data=[{
        "log_id": str(l.log_id), "user_id": str(l.user_id) if l.user_id else None,
        "action": l.action, "entity_type": l.entity_type,
        "ip_address": l.ip_address, "created_at": l.created_at.isoformat(),
        "metadata": l.metadata,
    } for l in logs])
