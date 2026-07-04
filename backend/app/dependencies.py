"""
app/dependencies.py
─────────────────────────────────────────────────────────────────
FastAPI Dependency Injection (DI) functions.

DI in FastAPI works like this:
  def my_route(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
      ...

FastAPI automatically calls these functions before the route handler,
injects the return values, and handles errors like 401/403 automatically.

Three role guards:
  require_patient → 403 if user is not a patient
  require_doctor  → 403 if user is not a doctor
  require_admin   → 403 if user is not an admin
─────────────────────────────────────────────────────────────────
"""
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)

# OAuth2PasswordBearer extracts the Bearer token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ── Current User ─────────────────────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Validates the JWT access token and returns the authenticated User.
    Raises HTTP 401 if the token is invalid, expired, or the user is inactive.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if not payload:
        raise credentials_error

    if payload.get("type") != "access":
        raise credentials_error

    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise credentials_error

    import uuid
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise credentials_error

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise credentials_error
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact administrator.",
        )

    return user


# ── Optional User (for public-but-aware routes) ───────────────
def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Returns the current user if authenticated, or None if not."""
    if not token:
        return None
    try:
        return get_current_user(token=token, db=db)
    except HTTPException:
        return None


# ── Role Guards ───────────────────────────────────────────────
def require_patient(current_user: User = Depends(get_current_user)) -> User:
    """Ensures the authenticated user is a Patient. Returns the user."""
    if current_user.role != UserRole.patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient access required.",
        )
    return current_user


def require_doctor(current_user: User = Depends(get_current_user)) -> User:
    """Ensures the authenticated user is a Doctor. Returns the user."""
    if current_user.role != UserRole.doctor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor access required.",
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Ensures the authenticated user is an Admin. Returns the user."""
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user


def require_doctor_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Allows both Doctors and Admins."""
    if current_user.role not in (UserRole.doctor, UserRole.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor or Admin access required.",
        )
    return current_user
