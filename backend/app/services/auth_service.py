"""
app/services/auth_service.py
─────────────────────────────────────────────────────────────────
Authentication business logic: registration, login, token refresh.
Routes are thin — they validate input and call this service.
All DB logic and password operations live here.
─────────────────────────────────────────────────────────────────
"""
import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user    import User, UserRole
from app.models.patient import Patient
from app.models.doctor  import Doctor
from app.core.security  import hash_password, verify_password, token_pair, decode_token
from app.schemas.auth   import RegisterRequest, LoginRequest

logger = logging.getLogger(__name__)


def register_user(req: RegisterRequest, db: Session) -> dict:
    """
    Create a new user account and the associated profile row.

    Steps:
      1. Check email is not already registered
      2. Hash the password
      3. Insert User row
      4. Insert Patient or Doctor profile row
      5. Return token pair
    """
    # 1. Duplicate email check
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{req.email}' is already registered.",
        )

    # 2. Create User
    user = User(
        name          = req.name.strip(),
        email         = req.email.lower().strip(),
        password_hash = hash_password(req.password),
        role          = req.role,
    )
    db.add(user)
    db.flush()   # flush to get user.id before creating profile

    # 3. Create profile based on role
    if req.role == UserRole.patient:
        db.add(Patient(user_id=user.id))
    elif req.role == UserRole.doctor:
        db.add(Doctor(user_id=user.id))
    # Admins have no separate profile table

    db.commit()
    db.refresh(user)

    logger.info("User registered", extra={"user_id": str(user.id), "role": user.role})
    return token_pair(str(user.id), user.role.value)


def login_user(req: LoginRequest, db: Session) -> dict:
    """
    Authenticate credentials and return a token pair.
    Always gives a generic error to prevent email enumeration attacks.
    """
    generic_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password.",
    )

    user = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise generic_error

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact administrator.",
        )

    # Update last_login timestamp
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    logger.info("User login", extra={"user_id": str(user.id), "role": user.role})
    return token_pair(str(user.id), user.role.value)


def refresh_access_token(refresh_token: str, db: Session) -> dict:
    """
    Exchange a valid refresh token for a new token pair.
    Invalidates the old pair (stateless — relies on expiry).
    """
    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")
        
    import uuid
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID in token.")

    user    = db.query(User).filter(User.id == user_uuid, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

    return token_pair(str(user.id), user.role.value)
