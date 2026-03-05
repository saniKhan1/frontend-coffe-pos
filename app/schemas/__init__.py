"""Pydantic schemas for request/response validation."""

from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.schemas.addon import AddonCreate, AddonResponse, AddonUpdate
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schemas.order import (
    OrderCreate,
    OrderItemCreate,
    OrderResponse,
    OrderItemResponse,
    OrderStatusUpdate,
)
from app.schemas.discount import DiscountCreate, DiscountResponse, DiscountUpdate
from app.schemas.shift import ShiftCreate, ShiftClose, ShiftResponse
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.schemas.common import MessageResponse, PaginatedResponse

__all__ = [
    "CategoryCreate", "CategoryUpdate", "CategoryResponse",
    "ItemCreate", "ItemUpdate", "ItemResponse",
    "AddonCreate", "AddonUpdate", "AddonResponse",
    "CustomerCreate", "CustomerUpdate", "CustomerResponse",
    "OrderCreate", "OrderItemCreate", "OrderResponse", "OrderItemResponse", "OrderStatusUpdate",
    "DiscountCreate", "DiscountUpdate", "DiscountResponse",
    "ShiftCreate", "ShiftClose", "ShiftResponse",
    "ExpenseCreate", "ExpenseUpdate", "ExpenseResponse",
    "MessageResponse", "PaginatedResponse",
]
