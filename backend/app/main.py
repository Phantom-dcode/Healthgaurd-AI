"""
app/main.py
─────────────────────────────────────────────────────────────────
FastAPI application factory.
Creates the app, registers middleware, mounts all routers,
runs DB initialization on startup.
─────────────────────────────────────────────────────────────────
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.config   import settings
from app.database import init_db
from app.core.logging import setup_logging
from app.middleware.audit import AuditMiddleware

# ── Routers ───────────────────────────────────────────────────
from app.routers import (
    auth, users, patients, doctors,
    health_records, alerts, predictions, reports, audit_logs,
)

# ── Startup / Shutdown ───────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("🚀 HealthGuard AI starting up…")
    init_db()
    logger.info("✅ Ready — %s v%s", settings.APP_NAME, settings.APP_VERSION)
    yield
    logger.info("🛑 HealthGuard AI shutting down…")


# ── App Factory ───────────────────────────────────────────────
app = FastAPI(
    title       = settings.APP_NAME,
    version     = settings.APP_VERSION,
    description = "AI-powered remote patient monitoring platform",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
    lifespan    = lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = settings.origins_list,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Audit Middleware ──────────────────────────────────────────
app.add_middleware(AuditMiddleware)


# ── Global Exception Handlers ────────────────────────────────
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"success": False, "message": "A record with this data already exists."},
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": "Resource not found."},
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    logging.getLogger(__name__).exception("Unhandled server error")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error. Please try again."},
    )


# ── Routes ────────────────────────────────────────────────────
PREFIX = "/api/v1"

app.include_router(auth.router,          prefix=PREFIX)
app.include_router(users.router,         prefix=PREFIX)
app.include_router(patients.router,      prefix=PREFIX)
app.include_router(doctors.router,       prefix=PREFIX)
app.include_router(health_records.router,prefix=PREFIX)
app.include_router(alerts.router,        prefix=PREFIX)
app.include_router(predictions.router,   prefix=PREFIX)
app.include_router(reports.router,       prefix=PREFIX)
app.include_router(audit_logs.router,    prefix=PREFIX)


# ── Health Check ─────────────────────────────────────────────
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}

@app.get("/", tags=["System"])
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API", "docs": "/docs"}
