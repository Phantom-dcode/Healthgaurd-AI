"""
app/core/logging.py
─────────────────────────────────────────────────────────────────
Structured JSON logging so logs are parseable by AWS CloudWatch,
Datadog, ELK stack, or any log aggregation tool.

Every log line is a JSON object:
  {
    "timestamp": "2024-01-15T10:30:00Z",
    "level":     "INFO",
    "logger":    "app.routers.auth",
    "message":   "User login successful",
    "user_id":   "abc123",
    ...
  }
─────────────────────────────────────────────────────────────────
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from app.config import settings


def setup_logging() -> None:
    """
    Configure root logger with structured JSON output.
    Called once at application startup in main.py.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # JSON formatter — every log line is a parseable JSON object
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [handler]

    # Silence noisy third-party loggers in production
    if not settings.DEBUG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logging.getLogger(__name__).info(
        "Logging initialized",
        extra={"level": settings.LOG_LEVEL, "environment": settings.ENVIRONMENT},
    )
