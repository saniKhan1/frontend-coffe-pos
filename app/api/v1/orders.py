"""Order CRUD endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=201, summary="Create a new order")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order with line items and addons.

    Automatically calculates:
    - **subtotal**: Sum of (item_price + addon_prices) * quantity for each line
    - **tax_amount**: subtotal * tax_rate (configurable, default 8%)
    - **discount_amount**: Applied from discount_id if provided
    - **total**: subtotal - discount + tax

    Stock is deducted for items with limited stock.
    Order number is auto-generated as PHI-YYYYMMDD-XXXX.
    """
    order = order_service.create_order(db, data)
    return _build_order_response(order)


@router.get("", response_model=PaginatedResponse[OrderResponse], summary="List all orders")
def list_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: str | None = Query(None, description="Filter by status: pending|preparing|ready|completed|cancelled"),
    payment_method: str | None = Query(None, description="Filter by payment method: cash|card|mobile"),
    customer_id: int | None = Query(None, description="Filter by customer ID"),
    shift_id: int | None = Query(None, description="Filter by shift ID"),
    start_date: str | None = Query(None, description="Filter from date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter to date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """Get paginated list of orders with optional filters."""
    result = order_service.get_all_orders(
        db, page, per_page, status, payment_method, customer_id, start_date, end_date, shift_id
    )
    result["items"] = [_build_order_response(o) for o in result["items"]]
    return result


@router.get("/{order_id}", response_model=OrderResponse, summary="Get order by ID")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a single order by its ID with all line items and addons."""
    order = order_service.get_order(db, order_id)
    return _build_order_response(order)


@router.patch("/{order_id}/status", response_model=OrderResponse, summary="Update order status")
def update_order_status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db)):
    """Update order status with transition validation.

    Valid transitions:
    - **pending** → preparing, cancelled
    - **preparing** → ready, cancelled
    - **ready** → completed, cancelled
    - **completed** → (no further transitions)
    - **cancelled** → (no further transitions)

    Cancelling an order restores item stock.
    """
    order = order_service.update_order_status(db, order_id, data)
    return _build_order_response(order)


@router.delete("/{order_id}", response_model=MessageResponse, summary="Delete an order")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order. Cannot delete completed orders."""
    order_service.delete_order(db, order_id)
    return MessageResponse(message=f"Order {order_id} deleted successfully")


def _build_order_response(order) -> dict:
    """Build order response dict from ORM object."""
    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer_id": order.customer_id,
        "customer_name": order.customer.name if order.customer else None,
        "status": order.status,
        "payment_method": order.payment_method,
        "subtotal": order.subtotal,
        "tax_amount": order.tax_amount,
        "discount_amount": order.discount_amount,
        "discount_id": order.discount_id,
        "total": order.total,
        "shift_id": order.shift_id,
        "notes": order.notes,
        "items": [
            {
                "id": oi.id,
                "item_id": oi.item_id,
                "item_name": oi.item.name if oi.item else None,
                "quantity": oi.quantity,
                "unit_price": oi.unit_price,
                "subtotal": oi.subtotal,
                "addons": [
                    {
                        "id": a.id,
                        "addon_id": a.addon_id,
                        "addon_name": a.addon.name if a.addon else None,
                        "price": a.price,
                    }
                    for a in oi.addons
                ],
            }
            for oi in order.order_items
        ],
        "created_at": order.created_at,
        "updated_at": order.updated_at,
    }
