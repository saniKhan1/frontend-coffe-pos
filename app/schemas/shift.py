"""Shift schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class ShiftCreate(BaseModel):
    """Schema for opening a new shift.

    Attributes:
        opening_cash: Cash amount in register at shift start.
        notes: Optional shift notes.
    """

    opening_cash: float = Field(0.0, ge=0, examples=[200.00])
    notes: str | None = None


class ShiftClose(BaseModel):
    """Schema for closing a shift.

    Attributes:
        closing_cash: Cash in register at shift end.
        notes: Optional closing notes.
    """

    closing_cash: float = Field(..., ge=0, examples=[450.00])
    notes: str | None = None


class ShiftResponse(BaseModel):
    """Schema for shift response.

    Attributes:
        id: Shift ID.
        opened_at: Shift opening timestamp.
        closed_at: Shift closing timestamp (null if open).
        opening_cash: Opening cash amount.
        closing_cash: Closing cash amount (null if open).
        status: Shift status ('open' or 'closed').
        notes: Shift notes.
        total_orders: Number of orders in this shift.
        total_revenue: Revenue generated during shift.
        total_expenses: Expenses during shift.
    """

    id: int
    opened_at: datetime
    closed_at: datetime | None
    opening_cash: float
    closing_cash: float | None
    status: str
    notes: str | None
    total_orders: int = 0
    total_revenue: float = 0.0
    total_expenses: float = 0.0

    model_config = {"from_attributes": True}
