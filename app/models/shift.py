"""Shift model for cashier shift management."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Shift(Base):
    """Represents a cashier shift with open/close tracking.

    Attributes:
        id: Primary key.
        opened_at: Shift opening timestamp.
        closed_at: Shift closing timestamp (null if still open).
        opening_cash: Cash in register at shift start.
        closing_cash: Cash in register at shift end.
        status: Shift status ('open' or 'closed').
        notes: Optional shift notes.
    """

    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    opened_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    opening_cash: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    closing_cash: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="open")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    orders = relationship("Order", back_populates="shift", lazy="selectin")
    expenses = relationship("Expense", back_populates="shift", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Shift(id={self.id}, status='{self.status}', opened_at={self.opened_at})>"
