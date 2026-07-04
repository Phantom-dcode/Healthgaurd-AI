"""
app/schemas/alert.py
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.alert import AlertType, SeverityLevel


class AlertResponse(BaseModel):
    alert_id:    uuid.UUID
    patient_id:  uuid.UUID
    record_id:   Optional[uuid.UUID] = None
    alert_type:  AlertType
    severity:    SeverityLevel
    message:     str
    is_read:     bool
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    created_at:  datetime

    model_config = ConfigDict(from_attributes=True)


class AlertUpdateRequest(BaseModel):
    is_read:     Optional[bool] = None
    is_resolved: Optional[bool] = None


"""
app/schemas/prediction.py
"""
import uuid as _uuid
from datetime import datetime as _dt
from decimal import Decimal as _Dec
from typing import Optional as _Opt, Any as _Any
from pydantic import BaseModel as _BM, ConfigDict as _CD
from app.models.prediction import RiskLevel


class PredictionResponse(_BM):
    prediction_id:    _uuid.UUID
    patient_id:       _uuid.UUID
    record_id:        _Opt[_uuid.UUID] = None
    risk_score:       _Dec
    risk_level:       RiskLevel
    model_version:    str
    feature_snapshot: _Opt[dict[str, _Any]] = None
    created_at:       _dt

    model_config = _CD(from_attributes=True)


class PredictRequest(_BM):
    """Optionally pass a specific record_id; defaults to latest record."""
    record_id: _Opt[_uuid.UUID] = None


"""
app/schemas/report.py
"""
import uuid as _uuid
from datetime import date as _date, datetime as _dt
from typing import Optional as _Opt
from pydantic import BaseModel as _BM, ConfigDict as _CD


class ReportCreate(_BM):
    patient_id: _uuid.UUID
    title:      _Opt[str]      = None
    date_from:  _date
    date_to:    _date


class ReportResponse(_BM):
    report_id:  _uuid.UUID
    patient_id: _uuid.UUID
    doctor_id:  _uuid.UUID
    title:      _Opt[str] = None
    date_from:  _date
    date_to:    _date
    file_path:  _Opt[str] = None
    created_at: _dt

    patient_name: _Opt[str] = None
    doctor_name:  _Opt[str] = None

    model_config = _CD(from_attributes=True)
