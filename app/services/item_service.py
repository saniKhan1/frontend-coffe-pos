"""Item CRUD service."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.category import Category
from app.schemas.item import ItemCreate, ItemUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)


def create_item(db: Session, data: ItemCreate) -> Item:
    """Create a new menu item.

    Args:
        db: Database session.
        data: Item creation data.

    Returns:
        The created Item instance.

    Raises:
        HTTPException: If category not found.
    """
    category = db.query(Category).filter(Category.id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {data.category_id} not found")

    item = Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"Created item: {item.name} (id={item.id}, price={item.price})")
    return item


def get_item(db: Session, item_id: int) -> Item:
    """Get an item by ID.

    Args:
        db: Database session.
        item_id: Item primary key.

    Returns:
        The Item instance.

    Raises:
        HTTPException: If item not found.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {item_id} not found")
    return item


def get_all_items(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    category_id: int | None = None,
    is_available: bool | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> dict:
    """Get all items with filters and pagination.

    Args:
        db: Database session.
        page: Page number.
        per_page: Items per page.
        category_id: Filter by category.
        is_available: Filter by availability.
        search: Search in name/description.
        min_price: Minimum price filter.
        max_price: Maximum price filter.

    Returns:
        Paginated result dictionary.
    """
    query = db.query(Item).order_by(Item.name)
    if category_id is not None:
        query = query.filter(Item.category_id == category_id)
    if is_available is not None:
        query = query.filter(Item.is_available == is_available)
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%") | Item.description.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    return paginate(query, page, per_page)


def update_item(db: Session, item_id: int, data: ItemUpdate) -> Item:
    """Update an existing item.

    Args:
        db: Database session.
        item_id: Item primary key.
        data: Fields to update.

    Returns:
        The updated Item instance.

    Raises:
        HTTPException: If item or category not found.
    """
    item = get_item(db, item_id)
    update_data = data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = db.query(Category).filter(Category.id == update_data["category_id"]).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {update_data['category_id']} not found")

    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    logger.info(f"Updated item: {item.name} (id={item.id})")
    return item


def delete_item(db: Session, item_id: int) -> None:
    """Delete an item.

    Args:
        db: Database session.
        item_id: Item primary key.

    Raises:
        HTTPException: If item not found.
    """
    item = get_item(db, item_id)
    db.delete(item)
    db.commit()
    logger.info(f"Deleted item: {item.name} (id={item_id})")
