"""
app/core/security.py
─────────────────────────────────────────────────────────────────
JWT token creation/verification + bcrypt password hashing.

Token payload structure:
  {
    "sub":  "<user_uuid>",     ← subject (user ID)
    "role": "patient|doctor|admin",
    "type": "access|refresh",
    "exp":  <unix timestamp>,
    "iat":  <issued at>
  }
─────────────────────────────────────────────────────────────────
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# ── Password Hashing ─────────────────────────────────────────
# bcrypt is the industry standard for password hashing.
# deprecated="auto" will auto-upgrade old hashes on next login.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Return bcrypt hash of plain-text password."""
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if plain matches the stored bcrypt hash."""
    return pwd_context.verify(plain, hashed)


# ── JWT Tokens ───────────────────────────────────────────────
def _build_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    payload = data.copy()
    now     = datetime.now(timezone.utc)
    payload.update({
        "type": token_type,
        "iat":  now,
        "exp":  now + expires_delta,
    })
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id: str, role: str) -> str:
    """Short-lived token (default 30 min) for API authorization."""
    return _build_token(
        {"sub": user_id, "role": role},
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: str, role: str) -> str:
    """Long-lived token (default 7 days) used to get a new access token."""
    return _build_token(
        {"sub": user_id, "role": role},
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT.
    Returns the payload dict on success, None on any failure.
    Caller decides whether to raise an HTTP 401.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


def token_pair(user_id: str, role: str) -> dict:
    """
    Convenience helper — returns both tokens and expiry info.
    Used by login and refresh endpoints.
    """
    return {
        "access_token":  create_access_token(user_id, role),
        "refresh_token": create_refresh_token(user_id, role),
        "token_type":    "bearer",
        "expires_in":    settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
