"""
app/database.py
─────────────────────────────────────────────────────────────────
SQLAlchemy engine, session factory, and declarative base.

Key Concepts:
  - Engine     : The connection pool to PostgreSQL. Created ONCE.
  - Session    : A unit-of-work. Opened per request, closed after.
  - Base       : All ORM models inherit from this. create_all()
                 uses it to create tables.
  - get_db()   : FastAPI dependency that yields a session and
                 guarantees it closes even if the request fails.
─────────────────────────────────────────────────────────────────
"""
import logging
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

logger = logging.getLogger(__name__)


# ── Engine ────────────────────────────────────────────────────
# pool_pre_ping=True: checks connection health before using it
#   (prevents "connection reset" errors after DB restart)
# pool_size=10: max persistent connections in the pool
# max_overflow=20: additional temporary connections under load
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,          # logs SQL queries in debug mode
)


# ── Session Factory ───────────────────────────────────────────
# autocommit=False : we control transactions explicitly
# autoflush=False  : we flush manually when needed
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ── Declarative Base ──────────────────────────────────────────
# All SQLAlchemy models inherit from Base.
# Base.metadata tracks all table definitions.
class Base(DeclarativeBase):
    pass


# ── Database Dependency ───────────────────────────────────────
def get_db():
    """
    FastAPI dependency that provides a database session per request.

    Usage in router:
        @router.get("/")
        def list_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ── Database Initialization ───────────────────────────────────
def init_db() -> None:
    """
    Create all tables that don't exist yet.
    Called once at application startup.

    Note: For production, use Alembic migrations instead.
    This is here so the app runs immediately out of the box.
    """
    try:
        # Import all models so Base.metadata knows about them
        from app.models import (  # noqa: F401
            user, patient, doctor, health_record,
            alert, prediction, report, audit_log
        )
        Base.metadata.create_all(bind=engine, checkfirst=True)
        logger.info("✅ Database tables verified / created")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
