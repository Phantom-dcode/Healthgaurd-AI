"""
app/middleware/audit.py
─────────────────────────────────────────────────────────────────
Starlette middleware that writes an AuditLog row for every
mutating request (POST, PUT, PATCH, DELETE).

GET requests are not logged to avoid log noise.
Health checks (/health, /docs, /openapi.json) are skipped.
─────────────────────────────────────────────────────────────────
"""
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests        import Request
from starlette.responses       import Response
from sqlalchemy.orm            import Session

from app.database    import SessionLocal
from app.models.audit_log import AuditLog
from app.core.security    import decode_token

logger = logging.getLogger(__name__)

SKIP_PATHS   = {"/", "/health", "/docs", "/openapi.json", "/redoc"}
LOG_METHODS  = {"POST", "PUT", "PATCH", "DELETE"}


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Only log mutating methods on API routes
        if request.method not in LOG_METHODS:
            return response
        if request.url.path in SKIP_PATHS:
            return response
        if not request.url.path.startswith("/api/"):
            return response

        # Attempt to extract user_id from Bearer token (best-effort)
        user_id = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token   = auth_header.split(" ", 1)[1]
            payload = decode_token(token)
            if payload:
                user_id = payload.get("sub")

        # Derive action name from method + path
        # e.g. POST /api/v1/health-records → POST_HEALTH_RECORDS
        path_parts = request.url.path.strip("/").replace("-", "_").split("/")
        action     = f"{request.method}_{path_parts[-1].upper()}"

        ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or request.client.host
            if request.client else "unknown"
        )

        try:
            db: Session = SessionLocal()
            log = AuditLog(
                user_id       = user_id,
                action        = action[:100],
                resource_type = path_parts[-2] if len(path_parts) >= 2 else None,
                resource_id   = path_parts[-1] if len(path_parts) >= 1 else None,
                ip_address    = ip[:45],
                user_agent    = request.headers.get("User-Agent", "")[:500],
            )
            db.add(log)
            db.commit()
        except Exception as exc:
            logger.warning("Audit log write failed: %s", exc)
        finally:
            db.close()

        return response
