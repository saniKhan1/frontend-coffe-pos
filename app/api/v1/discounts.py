"""Discount CRUD endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.discount import DiscountCreate, DiscountResponse, DiscountUpdate
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services import discount_service

router = APIRouter(prefix="/discounts", tags=["Discounts"])


@router.post("", response_model=DiscountResponse, status_code=201, summary="Create a new discount")
def create_discount(data: DiscountCreate, db: Session = Depends(get_db)):
    """Create a new discount/promotion.

    - **name**: Discount name (required)
    - **type**: 'percentage' (0-100) or 'flat' (dollar amount)
    - **value**: Discount value > 0
    - **is_active**: Active status (default true)
    - **start_date/end_date**: Optional validity period
    """
    return discount_service.create_discount(db, data)


@router.get("", response_model=PaginatedResponse[DiscountResponse], summary="List all discounts")
def list_discounts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_active: bool | None = Query(None, description="Filter by active status"),
    search: str | None = Query(None, description="Search in discount name"),
    db: Session = Depends(get_db),
):
    """Get paginated list of discounts with optional filters."""
    return discount_service.get_all_discounts(db, page, per_page, is_active, search)


@router.get("/{discount_id}", response_model=DiscountResponse, summary="Get discount by ID")
def get_discount(discount_id: int, db: Session = Depends(get_db)):
    """Get a single discount by its ID."""
    return discount_service.get_discount(db, discount_id)


@router.patch("/{discount_id}", response_model=DiscountResponse, summary="Update a discount")
def update_discount(discount_id: int, data: DiscountUpdate, db: Session = Depends(get_db)):
    """Update an existing discount. Only provided fields are updated."""
    return discount_service.update_discount(db, discount_id, data)


@router.delete("/{discount_id}", response_model=MessageResponse, summary="Delete a discount")
def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    """Delete a discount."""
    discount_service.delete_discount(db, discount_id)
    return MessageResponse(message=f"Discount {discount_id} deleted successfully")
