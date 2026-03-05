"""Customer CRUD endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schemas.order import OrderResponse
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services import customer_service

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, status_code=201, summary="Create a new customer")
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    """Register a new customer.

    - **name**: Customer name (required)
    - **phone**: Phone number (optional, unique)
    - **email**: Email address (optional, unique)
    """
    return customer_service.create_customer(db, data)


@router.get("", response_model=PaginatedResponse[CustomerResponse], summary="List all customers")
def list_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, description="Search by name, phone, or email"),
    db: Session = Depends(get_db),
):
    """Get paginated list of customers with optional search."""
    return customer_service.get_all_customers(db, page, per_page, search)


@router.get("/{customer_id}", response_model=CustomerResponse, summary="Get customer by ID")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a single customer by their ID."""
    return customer_service.get_customer(db, customer_id)


@router.get("/{customer_id}/orders", response_model=list[OrderResponse], summary="Get customer orders")
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    """Get all orders for a specific customer."""
    orders = customer_service.get_customer_orders(db, customer_id)
    return [_build_order_response(o) for o in orders]


@router.patch("/{customer_id}", response_model=CustomerResponse, summary="Update a customer")
def update_customer(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    """Update an existing customer. Only provided fields are updated."""
    return customer_service.update_customer(db, customer_id, data)


@router.delete("/{customer_id}", response_model=MessageResponse, summary="Delete a customer")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer record."""
    customer_service.delete_customer(db, customer_id)
    return MessageResponse(message=f"Customer {customer_id} deleted successfully")


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
