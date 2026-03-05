"""Addon CRUD endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.addon import AddonCreate, AddonResponse, AddonUpdate
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services import addon_service

router = APIRouter(prefix="/addons", tags=["Addons"])


@router.post("", response_model=AddonResponse, status_code=201, summary="Create a new addon")
def create_addon(data: AddonCreate, db: Session = Depends(get_db)):
    """Create a new addon/extra option.

    - **name**: Addon name (unique, required)
    - **price**: Addon price >= 0 (required)
    - **is_available**: Active status (default true)
    """
    return addon_service.create_addon(db, data)


@router.get("", response_model=PaginatedResponse[AddonResponse], summary="List all addons")
def list_addons(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_available: bool | None = Query(None, description="Filter by availability"),
    search: str | None = Query(None, description="Search in addon name"),
    db: Session = Depends(get_db),
):
    """Get paginated list of addons with optional filters."""
    return addon_service.get_all_addons(db, page, per_page, is_available, search)


@router.get("/{addon_id}", response_model=AddonResponse, summary="Get addon by ID")
def get_addon(addon_id: int, db: Session = Depends(get_db)):
    """Get a single addon by its ID."""
    return addon_service.get_addon(db, addon_id)


@router.patch("/{addon_id}", response_model=AddonResponse, summary="Update an addon")
def update_addon(addon_id: int, data: AddonUpdate, db: Session = Depends(get_db)):
    """Update an existing addon. Only provided fields are updated."""
    return addon_service.update_addon(db, addon_id, data)


@router.delete("/{addon_id}", response_model=MessageResponse, summary="Delete an addon")
def delete_addon(addon_id: int, db: Session = Depends(get_db)):
    """Delete an addon."""
    addon_service.delete_addon(db, addon_id)
    return MessageResponse(message=f"Addon {addon_id} deleted successfully")
