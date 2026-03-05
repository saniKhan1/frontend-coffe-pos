"""Addon schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class AddonCreate(BaseModel):
    """Schema for creating a new addon.

    Attributes:
        name: Addon name (1-100 chars).
        price: Additional price for this addon.
        is_available: Whether addon is currently available.
    """

    name: str = Field(..., min_length=1, max_length=100, examples=["Extra Espresso Shot"])
    price: float = Field(..., ge=0, examples=[0.75])
    is_available: bool = True


class AddonUpdate(BaseModel):
    """Schema for updating an existing addon. All fields optional.

    Attributes:
        name: Updated addon name.
        price: Updated price.
        is_available: Updated availability.
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    price: float | None = Field(None, ge=0)
    is_available: bool | None = None


class AddonResponse(BaseModel):
    """Schema for addon response.

    Attributes:
        id: Addon ID.
        name: Addon name.
        price: Addon price.
        is_available: Availability status.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int
    name: str
    price: float
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
