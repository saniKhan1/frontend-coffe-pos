API Schemas
===========

This page documents all Pydantic schemas used for request validation and response serialization.

Common Schemas
--------------

**MessageResponse:**

.. code-block:: json

   {"message": "Resource deleted successfully"}

**ErrorResponse:**

.. code-block:: json

   {"detail": "Resource not found"}

**PaginatedResponse:**

.. code-block:: json

   {
     "items": [],
     "total": 42,
     "page": 1,
     "per_page": 20,
     "total_pages": 3
   }


Category Schemas
----------------

**CategoryCreate / CategoryUpdate:**

.. code-block:: python

   class CategoryCreate(BaseModel):
       name: str                         # Required, unique
       description: str | None = None
       display_order: int = 0

**CategoryResponse:**

.. code-block:: python

   class CategoryResponse(BaseModel):
       id: int
       name: str
       description: str | None
       display_order: int
       is_active: bool
       item_count: int                   # Number of items in this category
       created_at: datetime
       updated_at: datetime


Item Schemas
------------

**ItemCreate / ItemUpdate:**

.. code-block:: python

   class ItemCreate(BaseModel):
       name: str                         # Required
       description: str | None = None
       price: float                      # Required, > 0
       category_id: int                  # Required, FK to categories
       stock_qty: int = -1               # -1 = unlimited
       is_available: bool = True

**ItemResponse:**

.. code-block:: python

   class ItemResponse(BaseModel):
       id: int
       name: str
       description: str | None
       price: float
       stock_qty: int
       is_available: bool
       category: CategoryResponse | None
       created_at: datetime
       updated_at: datetime


Addon Schemas
-------------

**AddonCreate / AddonUpdate:**

.. code-block:: python

   class AddonCreate(BaseModel):
       name: str
       price: float                      # >= 0
       is_available: bool = True

**AddonResponse:**

.. code-block:: python

   class AddonResponse(BaseModel):
       id: int
       name: str
       price: float
       is_available: bool
       created_at: datetime
       updated_at: datetime


Customer Schemas
----------------

**CustomerCreate / CustomerUpdate:**

.. code-block:: python

   class CustomerCreate(BaseModel):
       name: str
       phone: str | None = None
       email: str | None = None          # Valid email format

**CustomerResponse:**

.. code-block:: python

   class CustomerResponse(BaseModel):
       id: int
       name: str
       phone: str | None
       email: str | None
       total_orders: int
       total_spent: float
       created_at: datetime
       updated_at: datetime


Order Schemas
-------------

**OrderItemCreate** (nested within OrderCreate):

.. code-block:: python

   class OrderItemCreate(BaseModel):
       item_id: int
       quantity: int = 1                 # >= 1
       addon_ids: list[int] = []

**OrderCreate:**

.. code-block:: python

   class OrderCreate(BaseModel):
       customer_id: int | None = None
       payment_method: str = "cash"      # cash | card | mobile
       discount_id: int | None = None
       notes: str | None = None
       items: list[OrderItemCreate]      # At least 1 item required

**OrderStatusUpdate:**

.. code-block:: python

   class OrderStatusUpdate(BaseModel):
       status: str                       # pending → preparing → ready → completed | cancelled

**OrderResponse:**

.. code-block:: python

   class OrderResponse(BaseModel):
       id: int
       order_number: str                 # Format: PHI-YYYYMMDD-XXXX
       status: str
       payment_method: str
       subtotal: float
       tax_amount: float
       discount_amount: float
       total: float
       notes: str | None
       customer: CustomerResponse | None
       discount: DiscountResponse | None
       items: list[OrderItemResponse]
       created_at: datetime
       updated_at: datetime


Discount Schemas
----------------

**DiscountCreate / DiscountUpdate:**

.. code-block:: python

   class DiscountCreate(BaseModel):
       name: str
       type: str                         # "percentage" or "flat"
       value: float                      # > 0
       is_active: bool = True

**DiscountResponse:**

.. code-block:: python

   class DiscountResponse(BaseModel):
       id: int
       name: str
       type: str
       value: float
       is_active: bool
       created_at: datetime
       updated_at: datetime


Shift Schemas
-------------

**ShiftOpen:**

.. code-block:: python

   class ShiftOpen(BaseModel):
       opening_cash: float = 0.0
       notes: str | None = None

**ShiftClose:**

.. code-block:: python

   class ShiftClose(BaseModel):
       closing_cash: float
       notes: str | None = None

**ShiftResponse:**

.. code-block:: python

   class ShiftResponse(BaseModel):
       id: int
       opened_at: datetime
       closed_at: datetime | None
       opening_cash: float
       closing_cash: float | None
       status: str                       # "open" or "closed"
       notes: str | None
       created_at: datetime
       updated_at: datetime


Expense Schemas
---------------

**ExpenseCreate / ExpenseUpdate:**

.. code-block:: python

   class ExpenseCreate(BaseModel):
       category: str                     # supplies, wages, utilities, etc.
       description: str
       amount: float                     # > 0
       shift_id: int | None = None

**ExpenseResponse:**

.. code-block:: python

   class ExpenseResponse(BaseModel):
       id: int
       category: str
       description: str
       amount: float
       date: datetime
       shift_id: int | None
       created_at: datetime
       updated_at: datetime


Dashboard Schemas
-----------------

**DashboardSummary:**

.. code-block:: python

   class DashboardSummary(BaseModel):
       total_revenue: float
       total_orders: int
       completed_orders: int
       cancelled_orders: int
       average_order_value: float
       total_customers: int
       new_customers: int
       total_items_sold: int
       revenue_change_pct: float         # % change vs previous period
       total_tax_collected: float
       total_discounts_given: float
       busiest_hour: int | None          # 0-23

**TopItem:**

.. code-block:: python

   class TopItem(BaseModel):
       item_id: int
       item_name: str
       category_name: str
       total_quantity: int
       total_revenue: float

**OrderTrend:**

.. code-block:: python

   class OrderTrend(BaseModel):
       date: str
       order_count: int
       revenue: float

**ProfitLoss:**

.. code-block:: python

   class ProfitLoss(BaseModel):
       total_revenue: float
       total_expenses: float
       net_profit: float
       profit_margin_pct: float
       expense_breakdown: list[ExpenseBreakdownItem]
