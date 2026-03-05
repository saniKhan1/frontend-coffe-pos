"""Discount schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class DiscountCreate(BaseModel):
    """Schema for creating a new discount.

    Attributes:
        name: Discount name / description.
        type: 'percentage' (0-100) or 'flat' (dollar amount).
        value: Discount value.
        is_active: Whether discount is currently usable.
        start_date: Optional start date (ISO 8601).
        end_date: Optional end date (ISO 8601).
    """

    name: str = Field(..., min_length=1, max_length=200, examples=["Happy Hour 20%"])
    type: str = Field("percentage", pattern="^(percentage|flat)$", examples=["percentage"])
    value: float = Field(..., gt=0, examples=[20.0])
    is_active: bool = True
    start_date: datetime | None = None
    end_date: datetime | None = None


class DiscountUpdate(BaseModel):
    """Schema for updating an existing discount. All fields optional.

    Attributes:
        name: Updated discount name.
        type: Updated discount type.
        value: Updated discount value.
        is_active: Updated active status.
        start_date: Updated start date.
        end_date: Updated end date.
    """

    name: str | None = Field(None, min_length=1, max_length=200)
    type: str | None = Field(None, pattern="^(percentage|flat)$")
    value: float | None = Field(None, gt=0)
    is_active: bool | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class DiscountResponse(BaseModel):
    """Schema for discount response.

    Attributes:
        id: Discount ID.
        name: Discount name.
        type: Discount type (percentage/flat).
        value: Discount value.
        is_active: Active status.
        start_date: Start date.
        end_date: End date.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int
    name: str
    type: str
    value: float
    is_active: bool
    start_date: datetime | None
    end_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
