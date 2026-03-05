"""Order schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemAddonCreate(BaseModel):
    """Schema for adding an addon to an order line item.

    Attributes:
        addon_id: ID of the addon to add.
    """

    addon_id: int = Field(..., gt=0, examples=[1])


class OrderItemAddonResponse(BaseModel):
    """Schema for order item addon response.

    Attributes:
        id: OrderItemAddon ID.
        addon_id: Addon ID.
        addon_name: Addon name.
        price: Price charged for this addon.
    """

    id: int
    addon_id: int
    addon_name: str | None = None
    price: float

    model_config = {"from_attributes": True}


class OrderItemCreate(BaseModel):
    """Schema for a line item in an order creation request.

    Supports two addon formats:
    - ``addon_ids: [1, 3]`` — shorthand list of addon IDs
    - ``addons: [{"addon_id": 1}]`` — explicit objects

    Attributes:
        item_id: ID of the menu item.
        quantity: Number of this item (default 1).
        addon_ids: Shorthand list of addon IDs.
        addons: Explicit addon objects (auto-populated from addon_ids).
    """

    item_id: int = Field(..., gt=0, examples=[1])
    quantity: int = Field(1, gt=0, le=100, examples=[2])
    addon_ids: list[int] = Field(default_factory=list, examples=[[1, 3]])
    addons: list[OrderItemAddonCreate] = Field(default_factory=list)

    def model_post_init(self, __context: object) -> None:
        """Merge addon_ids into addons list for uniform processing."""
        if self.addon_ids and not self.addons:
            self.addons = [OrderItemAddonCreate(addon_id=aid) for aid in self.addon_ids]


class OrderItemResponse(BaseModel):
    """Schema for order line item response.

    Attributes:
        id: OrderItem ID.
        item_id: Menu item ID.
        item_name: Menu item name.
        quantity: Quantity ordered.
        unit_price: Price per unit.
        subtotal: Line item subtotal (qty * unit_price + addons).
        addons: List of addons applied.
    """

    id: int
    item_id: int
    item_name: str | None = None
    quantity: int
    unit_price: float
    subtotal: float
    addons: list[OrderItemAddonResponse] = []

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    """Schema for creating a new order.

    Attributes:
        customer_id: Optional customer ID (null for walk-in).
        payment_method: Payment type ('cash', 'card', 'mobile').
        discount_id: Optional discount to apply.
        shift_id: Optional shift this order belongs to.
        notes: Optional order notes.
        items: List of order line items (at least one required).
    """

    customer_id: int | None = Field(None, gt=0)
    payment_method: str = Field("cash", pattern="^(cash|card|mobile)$", examples=["cash"])
    discount_id: int | None = Field(None, gt=0)
    shift_id: int | None = Field(None, gt=0)
    notes: str | None = None
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status.

    Attributes:
        status: New status value. Must follow flow:
            pending → preparing → ready → completed/cancelled.
    """

    status: str = Field(
        ...,
        pattern="^(pending|preparing|ready|completed|cancelled)$",
        examples=["preparing"],
    )


class OrderResponse(BaseModel):
    """Schema for order response.

    Attributes:
        id: Order ID.
        order_number: Human-readable order number (PHI-YYYYMMDD-XXXX).
        customer_id: Customer ID (null for walk-in).
        customer_name: Customer name if linked.
        status: Current order status.
        payment_method: Payment type used.
        subtotal: Sum of line items before tax/discount.
        tax_amount: Tax applied.
        discount_amount: Discount applied.
        discount_id: Discount ID if applied.
        total: Final order total.
        shift_id: Shift ID if applicable.
        notes: Order notes.
        items: List of order line items.
        created_at: Order creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int
    order_number: str
    customer_id: int | None
    customer_name: str | None = None
    status: str
    payment_method: str
    subtotal: float
    tax_amount: float
    discount_amount: float
    discount_id: int | None
    total: float
    shift_id: int | None
    notes: str | None
    items: list[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
