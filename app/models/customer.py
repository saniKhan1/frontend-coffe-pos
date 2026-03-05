"""Customer model for loyalty tracking."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Customer(Base):
    """Represents a customer for loyalty and order tracking.

    Attributes:
        id: Primary key.
        name: Customer full name.
        phone: Phone number (unique, optional).
        email: Email address (unique, optional).
        total_orders: Cached count of completed orders.
        total_spent: Cached total amount spent.
        created_at: Record creation timestamp.
        updated_at: Last modification timestamp.
    """

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True, index=True)
    email: Mapped[str | None] = mapped_column(String(200), unique=True, nullable=True, index=True)
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    total_spent: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    orders = relationship("Order", back_populates="customer", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, name='{self.name}')>"
