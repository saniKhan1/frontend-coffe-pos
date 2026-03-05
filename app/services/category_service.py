"""Category CRUD service."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)


def create_category(db: Session, data: CategoryCreate) -> Category:
    """Create a new category.

    Args:
        db: Database session.
        data: Category creation data.

    Returns:
        The created Category instance.

    Raises:
        HTTPException: If a category with the same name already exists.
    """
    existing = db.query(Category).filter(Category.name == data.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Category '{data.name}' already exists")

    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    logger.info(f"Created category: {category.name} (id={category.id})")
    return category


def get_category(db: Session, category_id: int) -> Category:
    """Get a category by ID.

    Args:
        db: Database session.
        category_id: Category primary key.

    Returns:
        The Category instance.

    Raises:
        HTTPException: If category not found.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} not found")
    return category


def get_all_categories(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    is_active: bool | None = None,
    search: str | None = None,
) -> dict:
    """Get all categories with optional filters and pagination.

    Args:
        db: Database session.
        page: Page number.
        per_page: Items per page.
        is_active: Filter by active status.
        search: Search in name.

    Returns:
        Paginated result dictionary.
    """
    query = db.query(Category).order_by(Category.display_order, Category.name)
    if is_active is not None:
        query = query.filter(Category.is_active == is_active)
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))
    return paginate(query, page, per_page)


def update_category(db: Session, category_id: int, data: CategoryUpdate) -> Category:
    """Update an existing category.

    Args:
        db: Database session.
        category_id: Category primary key.
        data: Fields to update.

    Returns:
        The updated Category instance.

    Raises:
        HTTPException: If category not found or name conflicts.
    """
    category = get_category(db, category_id)
    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing = db.query(Category).filter(Category.name == update_data["name"], Category.id != category_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Category '{update_data['name']}' already exists")

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    logger.info(f"Updated category: {category.name} (id={category.id})")
    return category


def delete_category(db: Session, category_id: int) -> None:
    """Delete a category.

    Args:
        db: Database session.
        category_id: Category primary key.

    Raises:
        HTTPException: If category not found or has items.
    """
    category = get_category(db, category_id)
    if category.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category '{category.name}' — it has {len(category.items)} item(s). Remove or reassign items first.",
        )
    db.delete(category)
    db.commit()
    logger.info(f"Deleted category: {category.name} (id={category_id})")
