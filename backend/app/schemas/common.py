"""
app/schemas/common.py
Shared response envelopes and pagination models.
Every API response is wrapped in APIResponse for consistency.
"""
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    """
    Standard API response envelope.
    Success:  { "success": true,  "data": {...} }
    Error:    { "success": false, "message": "..." }
    """
    success: bool = True
    message: Optional[str] = None
    data: Optional[DataT] = None

    @classmethod
    def ok(cls, data: Any = None, message: str = "Success") -> "APIResponse":
        return cls(success=True, message=message, data=data)

    @classmethod
    def error(cls, message: str) -> "APIResponse":
        return cls(success=False, message=message, data=None)


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Paginated list response."""
    items: list[DataT]
    total: int
    page: int
    per_page: int
    pages: int
