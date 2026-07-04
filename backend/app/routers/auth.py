"""
app/routers/auth.py  — /api/v1/auth/*
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database            import get_db
from app.dependencies        import get_current_user
from app.schemas.auth        import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from app.schemas.common      import APIResponse
from app.schemas.user        import UserResponse
from app.services.auth_service import register_user, login_user, refresh_access_token
from app.models.user         import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user (patient, doctor, or admin) and return tokens."""
    tokens = register_user(req, db)
    return APIResponse.ok(data=tokens, message="Registration successful")


@router.post("/login", response_model=APIResponse[TokenResponse])
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate credentials and return a JWT token pair."""
    tokens = login_user(req, db)
    return APIResponse.ok(data=tokens, message="Login successful")


@router.post("/refresh", response_model=APIResponse[TokenResponse])
def refresh(req: RefreshRequest, db: Session = Depends(get_db)):
    """Exchange a refresh token for a new token pair."""
    tokens = refresh_access_token(req.refresh_token, db)
    return APIResponse.ok(data=tokens, message="Token refreshed")


@router.post("/logout", response_model=APIResponse)
def logout(current_user: User = Depends(get_current_user)):
    """
    Stateless logout — client must discard tokens.
    For production, implement a token blacklist in Redis.
    """
    return APIResponse.ok(message="Logged out successfully")


@router.get("/me", response_model=APIResponse[UserResponse])
def me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return APIResponse.ok(data=UserResponse.model_validate(current_user))
