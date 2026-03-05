"""Item model for menu products."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Item(Base):
    """Represents a menu item (e.g., Caramel Latte, Croissant).

    Attributes:
        id: Primary key.
        category_id: FK to categories table.
        name: Item name.
        description: Optional item description.
        price: Base price of the item.
        image_url: Optional URL to item image.
        is_available: Whether item is currently orderable.
        stock_qty: Current stock quantity (-1 for unlimited).
        created_at: Record creation timestamp.
        updated_at: Last modification timestamp.
    """

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    stock_qty: Mapped[int] = mapped_column(Integer, default=-1)  # -1 = unlimited
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    category = relationship("Category", back_populates="items", lazy="selectin")
    order_items = relationship("OrderItem", back_populates="item", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, name='{self.name}', price={self.price})>"
