"""Addon CRUD service."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.addon import Addon
from app.schemas.addon import AddonCreate, AddonUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)


def create_addon(db: Session, data: AddonCreate) -> Addon:
    """Create a new addon."""
    existing = db.query(Addon).filter(Addon.name == data.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Addon '{data.name}' already exists")

    addon = Addon(**data.model_dump())
    db.add(addon)
    db.commit()
    db.refresh(addon)
    logger.info(f"Created addon: {addon.name} (id={addon.id})")
    return addon


def get_addon(db: Session, addon_id: int) -> Addon:
    """Get an addon by ID."""
    addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not addon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Addon with id {addon_id} not found")
    return addon


def get_all_addons(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    is_available: bool | None = None,
    search: str | None = None,
) -> dict:
    """Get all addons with optional filters and pagination."""
    query = db.query(Addon).order_by(Addon.name)
    if is_available is not None:
        query = query.filter(Addon.is_available == is_available)
    if search:
        query = query.filter(Addon.name.ilike(f"%{search}%"))
    return paginate(query, page, per_page)


def update_addon(db: Session, addon_id: int, data: AddonUpdate) -> Addon:
    """Update an existing addon."""
    addon = get_addon(db, addon_id)
    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing = db.query(Addon).filter(Addon.name == update_data["name"], Addon.id != addon_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Addon '{update_data['name']}' already exists")

    for field, value in update_data.items():
        setattr(addon, field, value)

    db.commit()
    db.refresh(addon)
    logger.info(f"Updated addon: {addon.name} (id={addon.id})")
    return addon


def delete_addon(db: Session, addon_id: int) -> None:
    """Delete an addon."""
    addon = get_addon(db, addon_id)
    db.delete(addon)
    db.commit()
    logger.info(f"Deleted addon: {addon.name} (id={addon_id})")
