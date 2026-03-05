"""Audit log model for tracking all data changes."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditLog(Base):
    """Records all create/update/delete operations for accountability.

    Attributes:
        id: Primary key.
        entity_type: Name of the affected table/model (e.g., 'Order', 'Item').
        entity_id: ID of the affected record.
        action: Operation type ('create', 'update', 'delete').
        old_values: JSON string of previous values (for update/delete).
        new_values: JSON string of new values (for create/update).
        ip_address: Client IP that triggered the change.
        user_agent: Client user agent string.
        timestamp: When the change occurred.
    """

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # create, update, delete
    old_values: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_values: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, entity='{self.entity_type}', action='{self.action}')>"
