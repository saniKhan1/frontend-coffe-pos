"""Common schemas shared across the application."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class MessageResponse(BaseModel):
    """Generic message response.

    Attributes:
        message: Human-readable status message.
        success: Whether the operation succeeded.
    """

    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response schema.

    Attributes:
        detail: Error description.
        error_code: Machine-readable error code.
    """

    detail: str
    error_code: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response wrapper.

    Attributes:
        items: List of items for the current page.
        total: Total number of items across all pages.
        page: Current page number.
        per_page: Items per page.
        total_pages: Total number of pages.
    """

    items: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int


class TimestampMixin(BaseModel):
    """Mixin providing created_at and updated_at fields."""

    created_at: datetime
    updated_at: datetime


class AuditLogResponse(BaseModel):
    """Schema for audit log entries.

    Attributes:
        id: Audit log entry ID.
        entity_type: Name of the affected entity.
        entity_id: ID of the affected record.
        action: Operation type (create/update/delete).
        old_values: Previous values as JSON string.
        new_values: New values as JSON string.
        ip_address: Client IP address.
        timestamp: When the change occurred.
    """

    id: int
    entity_type: str
    entity_id: int | None
    action: str
    old_values: str | None
    new_values: str | None
    ip_address: str | None
    timestamp: datetime

    model_config = {"from_attributes": True}
