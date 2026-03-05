"""Category CRUD endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=201, summary="Create a new category")
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new menu category.

    - **name**: Category name (unique, required)
    - **description**: Optional description
    - **display_order**: Sort order (default 0)
    - **is_active**: Active status (default true)
    """
    return category_service.create_category(db, data)


@router.get("", response_model=PaginatedResponse[CategoryResponse], summary="List all categories")
def list_categories(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    search: str | None = Query(None, description="Search in category name"),
    db: Session = Depends(get_db),
):
    """Get paginated list of categories with optional filters."""
    return category_service.get_all_categories(db, page, per_page, is_active, search)


@router.get("/{category_id}", response_model=CategoryResponse, summary="Get category by ID")
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a single category by its ID."""
    return category_service.get_category(db, category_id)


@router.patch("/{category_id}", response_model=CategoryResponse, summary="Update a category")
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    """Update an existing category. Only provided fields are updated."""
    return category_service.update_category(db, category_id, data)


@router.delete("/{category_id}", response_model=MessageResponse, summary="Delete a category")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category. Fails if the category has items."""
    category_service.delete_category(db, category_id)
    return MessageResponse(message=f"Category {category_id} deleted successfully")
