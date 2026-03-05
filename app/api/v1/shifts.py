"""Shift management endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.shift import ShiftCreate, ShiftClose, ShiftResponse
from app.schemas.common import PaginatedResponse
from app.services import shift_service

router = APIRouter(prefix="/shifts", tags=["Shifts"])


@router.post("/open", response_model=ShiftResponse, status_code=201, summary="Open a new shift")
def open_shift(data: ShiftCreate, db: Session = Depends(get_db)):
    """Open a new cashier shift.

    Only one shift can be open at a time. Close the current shift before opening a new one.

    - **opening_cash**: Cash in register at shift start (default 0)
    - **notes**: Optional shift notes
    """
    shift = shift_service.open_shift(db, data)
    return _build_shift_response(shift, db)


@router.get("", response_model=PaginatedResponse[ShiftResponse], summary="List all shifts")
def list_shifts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: str | None = Query(None, description="Filter by status: open|closed"),
    db: Session = Depends(get_db),
):
    """Get paginated list of shifts with optional status filter."""
    result = shift_service.get_all_shifts(db, page, per_page, status)
    result["items"] = [_build_shift_response(s, db) for s in result["items"]]
    return result


@router.get("/{shift_id}", response_model=ShiftResponse, summary="Get shift by ID")
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    """Get a single shift by its ID with order and expense summaries."""
    shift = shift_service.get_shift(db, shift_id)
    return _build_shift_response(shift, db)


@router.patch("/{shift_id}/close", response_model=ShiftResponse, summary="Close a shift")
def close_shift(shift_id: int, data: ShiftClose, db: Session = Depends(get_db)):
    """Close an open shift.

    - **closing_cash**: Cash in register at shift end (required)
    - **notes**: Optional closing notes
    """
    shift = shift_service.close_shift(db, shift_id, data)
    return _build_shift_response(shift, db)


def _build_shift_response(shift, db) -> dict:
    """Build shift response with computed totals."""
    total_orders = len([o for o in shift.orders if o.status != "cancelled"]) if shift.orders else 0
    total_revenue = sum(o.total for o in shift.orders if o.status != "cancelled") if shift.orders else 0.0
    total_expenses = sum(e.amount for e in shift.expenses) if shift.expenses else 0.0

    return {
        "id": shift.id,
        "opened_at": shift.opened_at,
        "closed_at": shift.closed_at,
        "opening_cash": shift.opening_cash,
        "closing_cash": shift.closing_cash,
        "status": shift.status,
        "notes": shift.notes,
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
    }
