"""Order service with business logic for order creation, status management, and calculations."""

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.models.addon import Addon
from app.models.customer import Customer
from app.models.discount import Discount
from app.models.item import Item
from app.models.order import Order, OrderItem, OrderItemAddon
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)

# Valid status transitions
VALID_TRANSITIONS = {
    "pending": ["preparing", "cancelled"],
    "preparing": ["ready", "cancelled"],
    "ready": ["completed", "cancelled"],
    "completed": [],
    "cancelled": [],
}


def _generate_order_number(db: Session) -> str:
    """Generate a unique order number in format PHI-YYYYMMDD-XXXX."""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"PHI-{today}-"

    last_order = (
        db.query(Order)
        .filter(Order.order_number.like(f"{prefix}%"))
        .order_by(Order.id.desc())
        .first()
    )

    if last_order:
        last_num = int(last_order.order_number.split("-")[-1])
        next_num = last_num + 1
    else:
        next_num = 1

    return f"{prefix}{next_num:04d}"


def create_order(db: Session, data: OrderCreate) -> Order:
    """Create a new order with line items and addons.

    Calculates subtotal, tax, discount, and total automatically.
    Deducts stock for items with limited stock.

    Args:
        db: Database session.
        data: Order creation data with items and addons.

    Returns:
        The created Order instance with all relationships loaded.

    Raises:
        HTTPException: If items not found, out of stock, or discount invalid.
    """
    # Validate customer if provided
    if data.customer_id:
        customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id {data.customer_id} not found")

    # Validate and calculate discount
    discount_amount = 0.0
    if data.discount_id:
        discount = db.query(Discount).filter(Discount.id == data.discount_id, Discount.is_active == True).first()  # noqa: E712
        if not discount:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Active discount with id {data.discount_id} not found")

    # Build order items and calculate subtotal
    order_items = []
    subtotal = 0.0
    total_items_qty = 0

    for item_data in data.items:
        item = db.query(Item).filter(Item.id == item_data.item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {item_data.item_id} not found")
        if not item.is_available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Item '{item.name}' is not available")
        if item.stock_qty != -1 and item.stock_qty < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for '{item.name}'. Available: {item.stock_qty}, Requested: {item_data.quantity}",
            )

        # Calculate addon prices for this line item
        addon_total = 0.0
        order_item_addons = []
        for addon_data in item_data.addons:
            addon = db.query(Addon).filter(Addon.id == addon_data.addon_id).first()
            if not addon:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Addon with id {addon_data.addon_id} not found")
            if not addon.is_available:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Addon '{addon.name}' is not available")
            addon_total += addon.price
            order_item_addons.append(OrderItemAddon(addon_id=addon.id, price=addon.price))

        line_subtotal = (item.price + addon_total) * item_data.quantity

        order_item = OrderItem(
            item_id=item.id,
            quantity=item_data.quantity,
            unit_price=item.price,
            subtotal=round(line_subtotal, 2),
        )
        order_item.addons = order_item_addons
        order_items.append(order_item)

        subtotal += line_subtotal
        total_items_qty += item_data.quantity

        # Deduct stock
        if item.stock_qty != -1:
            item.stock_qty -= item_data.quantity

    subtotal = round(subtotal, 2)

    # Apply discount
    if data.discount_id:
        discount = db.query(Discount).filter(Discount.id == data.discount_id).first()
        if discount.type == "percentage":
            discount_amount = round(subtotal * (discount.value / 100), 2)
        else:  # flat
            discount_amount = min(discount.value, subtotal)

    # Calculate tax on discounted subtotal
    taxable_amount = subtotal - discount_amount
    tax_amount = round(taxable_amount * settings.TAX_RATE, 2)
    total = round(taxable_amount + tax_amount, 2)

    # Create order
    order = Order(
        order_number=_generate_order_number(db),
        customer_id=data.customer_id,
        status="pending",
        payment_method=data.payment_method,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        discount_id=data.discount_id,
        total=total,
        shift_id=data.shift_id,
        notes=data.notes,
    )
    order.order_items = order_items

    db.add(order)

    # Update customer stats
    if data.customer_id:
        customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
        customer.total_orders += 1
        customer.total_spent += total

    db.commit()
    db.refresh(order)
    logger.info(f"Created order: {order.order_number} (total={order.total}, items={total_items_qty})")
    return order


def get_order(db: Session, order_id: int) -> Order:
    """Get an order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    return order


def get_all_orders(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    status_filter: str | None = None,
    payment_method: str | None = None,
    customer_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    shift_id: int | None = None,
) -> dict:
    """Get all orders with filters and pagination."""
    query = db.query(Order).order_by(Order.created_at.desc())

    if status_filter:
        query = query.filter(Order.status == status_filter)
    if payment_method:
        query = query.filter(Order.payment_method == payment_method)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    if shift_id:
        query = query.filter(Order.shift_id == shift_id)
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)

    return paginate(query, page, per_page)


def update_order_status(db: Session, order_id: int, data: OrderStatusUpdate) -> Order:
    """Update order status with transition validation.

    Args:
        db: Database session.
        order_id: Order primary key.
        data: New status.

    Returns:
        The updated Order instance.

    Raises:
        HTTPException: If order not found or invalid status transition.
    """
    order = get_order(db, order_id)

    valid_next = VALID_TRANSITIONS.get(order.status, [])
    if data.status not in valid_next:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition from '{order.status}' to '{data.status}'. Valid transitions: {valid_next}",
        )

    # If cancelling, restore stock
    if data.status == "cancelled":
        for order_item in order.order_items:
            item = db.query(Item).filter(Item.id == order_item.item_id).first()
            if item and item.stock_qty != -1:
                item.stock_qty += order_item.quantity

        # Reverse customer stats
        if order.customer_id:
            customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
            if customer:
                customer.total_orders = max(0, customer.total_orders - 1)
                customer.total_spent = max(0.0, customer.total_spent - order.total)

    order.status = data.status
    db.commit()
    db.refresh(order)
    logger.info(f"Updated order {order.order_number} status to '{data.status}'")
    return order


def delete_order(db: Session, order_id: int) -> None:
    """Delete an order (soft-cancel if completed, hard-delete if pending)."""
    order = get_order(db, order_id)
    if order.status in ("completed",):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a completed order. Cancel it instead.",
        )

    # Restore stock for non-cancelled orders
    if order.status != "cancelled":
        for order_item in order.order_items:
            item = db.query(Item).filter(Item.id == order_item.item_id).first()
            if item and item.stock_qty != -1:
                item.stock_qty += order_item.quantity

    db.delete(order)
    db.commit()
    logger.info(f"Deleted order: {order.order_number} (id={order_id})")
