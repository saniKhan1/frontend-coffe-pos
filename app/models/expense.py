"""Expense model for tracking shop expenditures."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Expense(Base):
    """Represents a business expense for profit/loss tracking.

    Attributes:
        id: Primary key.
        category: Expense category (e.g., 'supplies', 'maintenance', 'wages').
        description: Expense description.
        amount: Expense amount in dollars.
        date: Date of the expense.
        shift_id: FK to shifts table (nullable - not all expenses are shift-bound).
        created_at: Record creation timestamp.
    """

    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    shift_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("shifts.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    shift = relationship("Shift", back_populates="expenses")

    def __repr__(self) -> str:
        return f"<Expense(id={self.id}, category='{self.category}', amount={self.amount})>"
