"""
app/schemas/user.py
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from app.models.user import UserRole


class UserBase(BaseModel):
    name:  str
    email: EmailStr


class UserUpdate(BaseModel):
    name:  Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id:         uuid.UUID
    role:       UserRole
    is_active:  bool
    last_login: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserAdminResponse(UserResponse):
    updated_at: datetime
