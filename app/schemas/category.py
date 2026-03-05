"""Category schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """Schema for creating a new category.

    Attributes:
        name: Category name (required, 1-100 chars).
        description: Optional category description.
        display_order: Sort order for display (default 0).
        is_active: Whether the category is active (default True).
    """

    name: str = Field(..., min_length=1, max_length=100, examples=["Hot Coffee"])
    description: str | None = Field(None, examples=["Freshly brewed hot coffee drinks"])
    display_order: int = Field(0, ge=0)
    is_active: bool = True


class CategoryUpdate(BaseModel):
    """Schema for updating an existing category. All fields optional.

    Attributes:
        name: Updated category name.
        description: Updated description.
        display_order: Updated sort order.
        is_active: Updated active status.
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    display_order: int | None = Field(None, ge=0)
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    """Schema for category response.

    Attributes:
        id: Category ID.
        name: Category name.
        description: Category description.
        display_order: Sort order.
        is_active: Active status.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int
    name: str
    description: str | None
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
