"""Expense CRUD endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("", response_model=ExpenseResponse, status_code=201, summary="Create a new expense")
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    """Record a new business expense.

    - **category**: Expense category (e.g., 'supplies', 'maintenance', 'wages', 'utilities')
    - **description**: Expense description (optional)
    - **amount**: Expense amount > 0 (required)
    - **date**: Expense date (defaults to now)
    - **shift_id**: Optional: link expense to a shift
    """
    return expense_service.create_expense(db, data)


@router.get("", response_model=PaginatedResponse[ExpenseResponse], summary="List all expenses")
def list_expenses(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: str | None = Query(None, description="Filter by expense category"),
    shift_id: int | None = Query(None, description="Filter by shift ID"),
    start_date: str | None = Query(None, description="Filter from date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="Filter to date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """Get paginated list of expenses with optional filters."""
    return expense_service.get_all_expenses(db, page, per_page, category, shift_id, start_date, end_date)


@router.get("/{expense_id}", response_model=ExpenseResponse, summary="Get expense by ID")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Get a single expense by its ID."""
    return expense_service.get_expense(db, expense_id)


@router.patch("/{expense_id}", response_model=ExpenseResponse, summary="Update an expense")
def update_expense(expense_id: int, data: ExpenseUpdate, db: Session = Depends(get_db)):
    """Update an existing expense. Only provided fields are updated."""
    return expense_service.update_expense(db, expense_id, data)


@router.delete("/{expense_id}", response_model=MessageResponse, summary="Delete an expense")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense record."""
    expense_service.delete_expense(db, expense_id)
    return MessageResponse(message=f"Expense {expense_id} deleted successfully")
