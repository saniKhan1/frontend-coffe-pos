"""Discount CRUD service."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.discount import Discount
from app.schemas.discount import DiscountCreate, DiscountUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)


def create_discount(db: Session, data: DiscountCreate) -> Discount:
    """Create a new discount/promotion."""
    discount = Discount(**data.model_dump())
    db.add(discount)
    db.commit()
    db.refresh(discount)
    logger.info(f"Created discount: {discount.name} (id={discount.id})")
    return discount


def get_discount(db: Session, discount_id: int) -> Discount:
    """Get a discount by ID."""
    discount = db.query(Discount).filter(Discount.id == discount_id).first()
    if not discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Discount with id {discount_id} not found")
    return discount


def get_all_discounts(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    is_active: bool | None = None,
    search: str | None = None,
) -> dict:
    """Get all discounts with optional filters and pagination."""
    query = db.query(Discount).order_by(Discount.created_at.desc())
    if is_active is not None:
        query = query.filter(Discount.is_active == is_active)
    if search:
        query = query.filter(Discount.name.ilike(f"%{search}%"))
    return paginate(query, page, per_page)


def update_discount(db: Session, discount_id: int, data: DiscountUpdate) -> Discount:
    """Update an existing discount."""
    discount = get_discount(db, discount_id)
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(discount, field, value)

    db.commit()
    db.refresh(discount)
    logger.info(f"Updated discount: {discount.name} (id={discount.id})")
    return discount


def delete_discount(db: Session, discount_id: int) -> None:
    """Delete a discount."""
    discount = get_discount(db, discount_id)
    db.delete(discount)
    db.commit()
    logger.info(f"Deleted discount: {discount.name} (id={discount_id})")
