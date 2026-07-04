"""
app/models/__init__.py
Imports every model so Base.metadata.create_all() discovers all tables.
Import ORDER matters — models with FKs must come after their parents.
"""
from app.models.user          import User, UserRole                    # noqa
from app.models.patient       import Patient, GenderType, BloodGroup   # noqa
from app.models.doctor        import Doctor, DoctorPatient             # noqa
from app.models.health_record import HealthRecord                      # noqa
from app.models.alert         import Alert, AlertType, SeverityLevel   # noqa
from app.models.prediction    import Prediction, RiskLevel             # noqa
from app.models.report        import Report                            # noqa
from app.models.audit_log     import AuditLog                          # noqa
