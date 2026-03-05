"""Expense CRUD service."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)


def create_expense(db: Session, data: ExpenseCreate) -> Expense:
    """Create a new expense record."""
    expense_data = data.model_dump()
    if expense_data.get("date") is None:
        expense_data.pop("date", None)

    expense = Expense(**expense_data)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    logger.info(f"Created expense: {expense.category} ${expense.amount:.2f} (id={expense.id})")
    return expense


def get_expense(db: Session, expense_id: int) -> Expense:
    """Get an expense by ID."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {expense_id} not found")
    return expense


def get_all_expenses(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    category: str | None = None,
    shift_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    """Get all expenses with optional filters and pagination."""
    query = db.query(Expense).order_by(Expense.date.desc())
    if category:
        query = query.filter(Expense.category == category)
    if shift_id:
        query = query.filter(Expense.shift_id == shift_id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    return paginate(query, page, per_page)


def update_expense(db: Session, expense_id: int, data: ExpenseUpdate) -> Expense:
    """Update an existing expense."""
    expense = get_expense(db, expense_id)
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    logger.info(f"Updated expense: {expense.category} ${expense.amount:.2f} (id={expense.id})")
    return expense


def delete_expense(db: Session, expense_id: int) -> None:
    """Delete an expense."""
    expense = get_expense(db, expense_id)
    db.delete(expense)
    db.commit()
    logger.info(f"Deleted expense id={expense_id}")
