"""app/schemas/__init__.py"""
from app.schemas.common        import APIResponse, PaginatedResponse
from app.schemas.auth          import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user          import UserResponse, UserUpdate, UserAdminResponse
from app.schemas.patient       import PatientCreate, PatientUpdate, PatientResponse
from app.schemas.doctor        import DoctorCreate, DoctorUpdate, DoctorResponse, AssignPatientRequest, AssignmentResponse
from app.schemas.health_record import HealthRecordCreate, HealthRecordResponse
from app.schemas.alert         import AlertResponse, AlertUpdateRequest, PredictionResponse, PredictRequest, ReportCreate, ReportResponse

__all__ = [
    "APIResponse", "PaginatedResponse",
    "RegisterRequest", "LoginRequest", "TokenResponse", "RefreshRequest",
    "UserResponse", "UserUpdate", "UserAdminResponse",
    "PatientCreate", "PatientUpdate", "PatientResponse",
    "DoctorCreate", "DoctorUpdate", "DoctorResponse",
    "AssignPatientRequest", "AssignmentResponse",
    "HealthRecordCreate", "HealthRecordResponse",
    "AlertResponse", "AlertUpdateRequest",
    "PredictionResponse", "PredictRequest",
    "ReportCreate", "ReportResponse",
]
