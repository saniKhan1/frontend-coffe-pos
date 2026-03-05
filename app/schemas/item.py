"""Item schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Schema for creating a new menu item.

    Attributes:
        category_id: ID of the parent category.
        name: Item name (1-200 chars).
        description: Optional item description.
        price: Item price (must be > 0).
        image_url: Optional URL to item image.
        is_available: Whether item is orderable (default True).
        stock_qty: Stock quantity (-1 for unlimited).
    """

    category_id: int = Field(..., gt=0, examples=[1])
    name: str = Field(..., min_length=1, max_length=200, examples=["Caramel Latte"])
    description: str | None = Field(None, examples=["Rich espresso with caramel syrup and steamed milk"])
    price: float = Field(..., gt=0, examples=[5.50])
    image_url: str | None = Field(None, max_length=500)
    is_available: bool = True
    stock_qty: int = Field(-1, ge=-1, examples=[-1])


class ItemUpdate(BaseModel):
    """Schema for updating an existing item. All fields optional.

    Attributes:
        category_id: Updated parent category.
        name: Updated item name.
        description: Updated description.
        price: Updated price.
        image_url: Updated image URL.
        is_available: Updated availability.
        stock_qty: Updated stock quantity.
    """

    category_id: int | None = Field(None, gt=0)
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    price: float | None = Field(None, gt=0)
    image_url: str | None = None
    is_available: bool | None = None
    stock_qty: int | None = Field(None, ge=-1)


class ItemResponse(BaseModel):
    """Schema for item response.

    Attributes:
        id: Item ID.
        category_id: Parent category ID.
        category_name: Parent category name.
        name: Item name.
        description: Item description.
        price: Item price.
        image_url: Image URL.
        is_available: Availability status.
        stock_qty: Current stock (-1 = unlimited).
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int
    category_id: int
    category_name: str | None = None
    name: str
    description: str | None
    price: float
    image_url: str | None
    is_available: bool
    stock_qty: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
