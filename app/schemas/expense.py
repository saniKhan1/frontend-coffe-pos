"""Expense schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense.

    Attributes:
        category: Expense category (e.g., 'supplies', 'maintenance', 'wages', 'utilities').
        description: Expense description.
        amount: Expense amount (must be > 0).
        date: Date of expense (defaults to now).
        shift_id: Optional shift this expense belongs to.
    """

    category: str = Field(..., min_length=1, max_length=100, examples=["supplies"])
    description: str | None = Field(None, examples=["Coffee beans restocking"])
    amount: float = Field(..., gt=0, examples=[150.00])
    date: datetime | None = None
    shift_id: int | None = Field(None, gt=0)


class ExpenseUpdate(BaseModel):
    """Schema for updating an existing expense. All fields optional.

    Attributes:
        category: Updated category.
        description: Updated description.
        amount: Updated amount.
        date: Updated date.
        shift_id: Updated shift ID.
    """

    category: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    amount: float | None = Field(None, gt=0)
    date: datetime | None = None
    shift_id: int | None = None


class ExpenseResponse(BaseModel):
    """Schema for expense response.

    Attributes:
        id: Expense ID.
        category: Expense category.
        description: Expense description.
        amount: Expense amount.
        date: Expense date.
        shift_id: Shift ID (if applicable).
        created_at: Creation timestamp.
    """

    id: int
    category: str
    description: str | None
    amount: float
    date: datetime
    shift_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
