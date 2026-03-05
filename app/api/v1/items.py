"""Item CRUD endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services import item_service

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("", response_model=ItemResponse, status_code=201, summary="Create a new item")
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    """Create a new menu item.

    - **category_id**: Parent category ID (required)
    - **name**: Item name (required)
    - **price**: Item price > 0 (required)
    - **stock_qty**: Stock count, -1 = unlimited (default -1)
    """
    item = item_service.create_item(db, data)
    return _build_item_response(item)


@router.get("", response_model=PaginatedResponse[ItemResponse], summary="List all items")
def list_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category_id: int | None = Query(None, description="Filter by category"),
    is_available: bool | None = Query(None, description="Filter by availability"),
    search: str | None = Query(None, description="Search in name/description"),
    min_price: float | None = Query(None, ge=0, description="Minimum price"),
    max_price: float | None = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db),
):
    """Get paginated list of items with optional filters."""
    result = item_service.get_all_items(db, page, per_page, category_id, is_available, search, min_price, max_price)
    result["items"] = [_build_item_response(i) for i in result["items"]]
    return result


@router.get("/{item_id}", response_model=ItemResponse, summary="Get item by ID")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by its ID."""
    item = item_service.get_item(db, item_id)
    return _build_item_response(item)


@router.patch("/{item_id}", response_model=ItemResponse, summary="Update an item")
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item. Only provided fields are updated."""
    item = item_service.update_item(db, item_id, data)
    return _build_item_response(item)


@router.delete("/{item_id}", response_model=MessageResponse, summary="Delete an item")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a menu item."""
    item_service.delete_item(db, item_id)
    return MessageResponse(message=f"Item {item_id} deleted successfully")


def _build_item_response(item) -> dict:
    """Build item response with category name."""
    return {
        "id": item.id,
        "category_id": item.category_id,
        "category_name": item.category.name if item.category else None,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "image_url": item.image_url,
        "is_available": item.is_available,
        "stock_qty": item.stock_qty,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }
