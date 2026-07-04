"""
app/services/alert_service.py
─────────────────────────────────────────────────────────────────
Checks a newly submitted health record against clinical thresholds
and inserts Alert rows for any violations.

Clinical thresholds are based on:
  - JNC 8 (Blood Pressure Guidelines)
  - ADA (American Diabetes Association — Blood Sugar)
  - AHA (Heart Rate / Oxygen guidelines)

The DB trigger (schema.sql) also does this, but having it in Python
means alerts work even on a plain SQLite test database, and we can
unit-test the logic without a PostgreSQL instance.
─────────────────────────────────────────────────────────────────
"""
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from app.models.health_record import HealthRecord
from app.models.alert         import Alert, AlertType, SeverityLevel

logger = logging.getLogger(__name__)

# ── Threshold Definitions ────────────────────────────────────
# Each entry: (condition_fn, alert_type, severity, message_template)
# message_template is a callable that takes the value and returns the string

THRESHOLDS = [
    # Blood Pressure — Systolic
    (lambda r: r.systolic_bp is not None and r.systolic_bp >= 180,
     AlertType.blood_pressure, SeverityLevel.critical,
     lambda r: f"CRITICAL: Systolic BP is {r.systolic_bp} mmHg — Hypertensive Crisis. Seek emergency care immediately."),

    (lambda r: r.systolic_bp is not None and 140 <= r.systolic_bp < 180,
     AlertType.blood_pressure, SeverityLevel.high,
     lambda r: f"High BP: Systolic is {r.systolic_bp} mmHg (Stage 2 Hypertension). Please consult your doctor."),

    (lambda r: r.systolic_bp is not None and r.systolic_bp < 90,
     AlertType.blood_pressure, SeverityLevel.medium,
     lambda r: f"Low BP: Systolic is {r.systolic_bp} mmHg (Hypotension). Monitor for dizziness."),

    # Oxygen Level
    (lambda r: r.oxygen_level is not None and float(r.oxygen_level) < 90,
     AlertType.oxygen_level, SeverityLevel.critical,
     lambda r: f"CRITICAL: SpO2 is {r.oxygen_level}% — Severe Hypoxia. Seek emergency care immediately."),

    (lambda r: r.oxygen_level is not None and 90 <= float(r.oxygen_level) < 95,
     AlertType.oxygen_level, SeverityLevel.high,
     lambda r: f"Low oxygen: SpO2 is {r.oxygen_level}%. Monitor closely and rest."),

    # Heart Rate
    (lambda r: r.heart_rate is not None and r.heart_rate > 150,
     AlertType.heart_rate, SeverityLevel.critical,
     lambda r: f"CRITICAL: Heart rate is {r.heart_rate} bpm — Severe Tachycardia. Seek emergency care."),

    (lambda r: r.heart_rate is not None and 100 < r.heart_rate <= 150,
     AlertType.heart_rate, SeverityLevel.high,
     lambda r: f"Elevated heart rate: {r.heart_rate} bpm (Tachycardia). Rest and monitor."),

    (lambda r: r.heart_rate is not None and r.heart_rate < 50,
     AlertType.heart_rate, SeverityLevel.medium,
     lambda r: f"Low heart rate: {r.heart_rate} bpm (Bradycardia). Consult your doctor if symptomatic."),

    # Blood Sugar
    (lambda r: r.blood_sugar is not None and float(r.blood_sugar) > 400,
     AlertType.blood_sugar, SeverityLevel.critical,
     lambda r: f"CRITICAL: Blood sugar is {r.blood_sugar} mg/dL — DKA risk. Seek emergency care."),

    (lambda r: r.blood_sugar is not None and 200 < float(r.blood_sugar) <= 400,
     AlertType.blood_sugar, SeverityLevel.high,
     lambda r: f"High blood sugar: {r.blood_sugar} mg/dL (Hyperglycemia). Consult your doctor."),

    (lambda r: r.blood_sugar is not None and float(r.blood_sugar) < 70,
     AlertType.blood_sugar, SeverityLevel.high,
     lambda r: f"Low blood sugar: {r.blood_sugar} mg/dL (Hypoglycemia). Consume glucose immediately."),

    # Temperature
    (lambda r: r.temperature is not None and float(r.temperature) > 39.5,
     AlertType.temperature, SeverityLevel.critical,
     lambda r: f"CRITICAL: Temperature is {r.temperature}°C — High Fever. Seek medical attention."),

    (lambda r: r.temperature is not None and 38.0 < float(r.temperature) <= 39.5,
     AlertType.temperature, SeverityLevel.medium,
     lambda r: f"Fever detected: Temperature is {r.temperature}°C. Rest, hydrate, and monitor."),

    (lambda r: r.temperature is not None and float(r.temperature) < 35.0,
     AlertType.temperature, SeverityLevel.high,
     lambda r: f"Low temperature: {r.temperature}°C (Hypothermia risk). Seek warmth and medical attention."),
]


def check_and_create_alerts(record: HealthRecord, db: Session) -> list[Alert]:
    """
    Evaluate all thresholds against a health record.
    Inserts an Alert row for every violated threshold.
    Returns the list of created alerts.
    """
    created: list[Alert] = []

    for condition, alert_type, severity, message_fn in THRESHOLDS:
        try:
            if condition(record):
                alert = Alert(
                    patient_id  = record.patient_id,
                    record_id   = record.record_id,
                    alert_type  = alert_type,
                    severity    = severity,
                    message     = message_fn(record),
                )
                db.add(alert)
                created.append(alert)
        except Exception as e:
            logger.warning(f"Alert threshold check error: {e}")
            continue

    if created:
        db.flush()
        logger.info(
            f"Created {len(created)} alert(s) for record {record.record_id}",
            extra={"patient_id": str(record.patient_id), "alert_count": len(created)},
        )

    return created
