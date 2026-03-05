"""Order, OrderItem, and OrderItemAddon models."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Order(Base):
    """Represents a customer order.

    Attributes:
        id: Primary key.
        order_number: Human-readable order number (PHI-YYYYMMDD-XXXX).
        customer_id: FK to customers table (nullable for walk-ins).
        status: Order status (pending/preparing/ready/completed/cancelled).
        payment_method: Payment type (cash/card/mobile).
        subtotal: Sum of all line items before tax/discount.
        tax_amount: Calculated tax.
        discount_amount: Applied discount amount.
        discount_id: FK to discounts table (nullable).
        total: Final total after tax and discount.
        shift_id: FK to shifts table (nullable).
        notes: Optional order notes.
        created_at: Order creation timestamp.
        updated_at: Last modification timestamp.
    """

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    customer_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("customers.id"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False, default="cash")
    subtotal: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    tax_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    discount_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    discount_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("discounts.id"), nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    shift_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("shifts.id"), nullable=True, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    customer = relationship("Customer", back_populates="orders", lazy="selectin")
    order_items = relationship("OrderItem", back_populates="order", lazy="selectin", cascade="all, delete-orphan")
    discount = relationship("Discount", lazy="selectin")
    shift = relationship("Shift", back_populates="orders", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status}', total={self.total})>"


class OrderItem(Base):
    """Represents a line item within an order.

    Attributes:
        id: Primary key.
        order_id: FK to orders table.
        item_id: FK to items table.
        quantity: Number of this item ordered.
        unit_price: Price per unit at time of order.
        subtotal: quantity * unit_price + addon prices.
    """

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items", lazy="selectin")
    addons = relationship("OrderItemAddon", back_populates="order_item", lazy="selectin", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, item_id={self.item_id}, qty={self.quantity})>"


class OrderItemAddon(Base):
    """Represents an addon applied to a specific order line item.

    Attributes:
        id: Primary key.
        order_item_id: FK to order_items table.
        addon_id: FK to addons table.
        price: Addon price at time of order.
    """

    __tablename__ = "order_item_addons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("order_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    addon_id: Mapped[int] = mapped_column(Integer, ForeignKey("addons.id"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    order_item = relationship("OrderItem", back_populates="addons")
    addon = relationship("Addon", lazy="selectin")

    def __repr__(self) -> str:
        return f"<OrderItemAddon(id={self.id}, addon_id={self.addon_id})>"
