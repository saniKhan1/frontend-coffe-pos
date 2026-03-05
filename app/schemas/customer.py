"""Customer schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    """Schema for creating a new customer.

    Attributes:
        name: Customer full name.
        phone: Phone number (optional, unique).
        email: Email address (optional, unique).
    """

    name: str = Field(..., min_length=1, max_length=200, examples=["John Doe"])
    phone: str | None = Field(None, max_length=20, examples=["+1234567890"])
    email: str | None = Field(None, max_length=200, examples=["john@example.com"])


class CustomerUpdate(BaseModel):
    """Schema for updating an existing customer. All fields optional.

    Attributes:
        name: Updated name.
        phone: Updated phone.
        email: Updated email.
    """

    name: str | None = Field(None, min_length=1, max_length=200)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=200)


class CustomerResponse(BaseModel):
    """Schema for customer response.

    Attributes:
        id: Customer ID.
        name: Customer name.
        phone: Phone number.
        email: Email address.
        total_orders: Number of completed orders.
        total_spent: Total amount spent.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int
    name: str
    phone: str | None
    email: str | None
    total_orders: int
    total_spent: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
