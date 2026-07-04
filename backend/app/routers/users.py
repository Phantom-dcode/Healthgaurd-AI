"""
app/routers/users.py  — /api/v1/users/*
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database       import get_db
from app.dependencies   import get_current_user, require_admin
from app.models.user    import User
from app.schemas.user   import UserResponse, UserUpdate, UserAdminResponse
from app.schemas.common import APIResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=APIResponse[List[UserAdminResponse]])
def list_users(
    skip: int = 0,
    limit: int = 50,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """[Admin] List all users with pagination."""
    users = db.query(User).offset(skip).limit(limit).all()
    return APIResponse.ok(data=[UserAdminResponse.model_validate(u) for u in users])


@router.get("/me", response_model=APIResponse[UserResponse])
def get_me(current_user: User = Depends(get_current_user)):
    """Return the current authenticated user."""
    return APIResponse.ok(data=UserResponse.model_validate(current_user))


@router.put("/me", response_model=APIResponse[UserResponse])
def update_me(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update own name or email."""
    if body.name:
        current_user.name = body.name.strip()
    if body.email:
        # Check uniqueness
        existing = db.query(User).filter(
            User.email == body.email.lower(),
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already in use")
        current_user.email = body.email.lower().strip()

    db.commit()
    db.refresh(current_user)
    return APIResponse.ok(data=UserResponse.model_validate(current_user))


@router.get("/{user_id}", response_model=APIResponse[UserAdminResponse])
def get_user(
    user_id: uuid.UUID,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """[Admin] Get a specific user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse.ok(data=UserAdminResponse.model_validate(user))


@router.patch("/{user_id}/deactivate", response_model=APIResponse)
def deactivate_user(
    user_id: uuid.UUID,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """[Admin] Deactivate a user account (soft delete)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return APIResponse.ok(message=f"User {user.email} deactivated")


@router.delete("/{user_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def delete_user(
    user_id: uuid.UUID,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """[Admin] Permanently delete a user and all their data (cascade)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return APIResponse.ok(message="User permanently deleted")
