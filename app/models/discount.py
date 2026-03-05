"""Discount model for promotions and coupons."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Discount(Base):
    """Represents a discount/promotion that can be applied to orders.

    Attributes:
        id: Primary key.
        name: Discount name (e.g., 'Happy Hour 20%').
        type: Either 'percentage' or 'flat'.
        value: Discount value (percentage 0-100 or flat dollar amount).
        is_active: Whether discount is currently usable.
        start_date: Optional start date for time-limited discounts.
        end_date: Optional end date for time-limited discounts.
        created_at: Record creation timestamp.
        updated_at: Last modification timestamp.
    """

    __tablename__ = "discounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="percentage")  # percentage or flat
    value: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<Discount(id={self.id}, name='{self.name}', type='{self.type}', value={self.value})>"
