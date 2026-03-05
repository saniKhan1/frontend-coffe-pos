"""Shift management service."""

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.schemas.shift import ShiftClose, ShiftCreate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)


def open_shift(db: Session, data: ShiftCreate) -> Shift:
    """Open a new shift. Only one shift can be open at a time.

    Args:
        db: Database session.
        data: Shift opening data.

    Returns:
        The created Shift instance.

    Raises:
        HTTPException: If there's already an open shift.
    """
    existing_open = db.query(Shift).filter(Shift.status == "open").first()
    if existing_open:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Shift #{existing_open.id} is still open. Close it before opening a new one.",
        )

    shift = Shift(opening_cash=data.opening_cash, notes=data.notes)
    db.add(shift)
    db.commit()
    db.refresh(shift)
    logger.info(f"Opened shift #{shift.id} with opening cash ${shift.opening_cash:.2f}")
    return shift


def close_shift(db: Session, shift_id: int, data: ShiftClose) -> Shift:
    """Close an open shift.

    Args:
        db: Database session.
        shift_id: Shift primary key.
        data: Closing data.

    Returns:
        The closed Shift instance.

    Raises:
        HTTPException: If shift not found or already closed.
    """
    shift = get_shift(db, shift_id)
    if shift.status == "closed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Shift #{shift_id} is already closed")

    shift.closing_cash = data.closing_cash
    shift.closed_at = datetime.now(timezone.utc)
    shift.status = "closed"
    if data.notes:
        shift.notes = (shift.notes or "") + f"\n[Close] {data.notes}"

    db.commit()
    db.refresh(shift)
    logger.info(f"Closed shift #{shift.id} with closing cash ${shift.closing_cash:.2f}")
    return shift


def get_shift(db: Session, shift_id: int) -> Shift:
    """Get a shift by ID."""
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shift with id {shift_id} not found")
    return shift


def get_all_shifts(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    status_filter: str | None = None,
) -> dict:
    """Get all shifts with optional status filter and pagination."""
    query = db.query(Shift).order_by(Shift.opened_at.desc())
    if status_filter:
        query = query.filter(Shift.status == status_filter)
    return paginate(query, page, per_page)
