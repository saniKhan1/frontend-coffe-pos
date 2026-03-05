"""Dashboard schemas for rich analytics responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


# ─── Summary ──────────────────────────────────────────────

class DashboardSummary(BaseModel):
    """Overall dashboard KPI summary.

    Attributes:
        total_revenue: Total revenue in the selected period.
        total_orders: Number of orders placed.
        completed_orders: Number of completed orders.
        cancelled_orders: Number of cancelled orders.
        avg_order_value: Average order total.
        total_customers: Total unique customers.
        new_customers: Customers created in the period.
        total_items_sold: Total quantity of items sold.
        revenue_change_pct: Revenue change vs previous period (%).
        order_change_pct: Order count change vs previous period (%).
        top_payment_method: Most used payment method.
        busiest_hour: Hour with most orders (0-23).
    """

    total_revenue: float = 0.0
    total_orders: int = 0
    completed_orders: int = 0
    cancelled_orders: int = 0
    avg_order_value: float = 0.0
    total_customers: int = 0
    new_customers: int = 0
    total_items_sold: int = 0
    revenue_change_pct: float = 0.0
    order_change_pct: float = 0.0
    top_payment_method: str | None = None
    busiest_hour: int | None = None


# ─── Revenue ──────────────────────────────────────────────

class RevenueBreakdown(BaseModel):
    """Revenue data point for a time period.

    Attributes:
        period: Time period label (date/week/month).
        revenue: Total revenue in this period.
        order_count: Number of orders.
        avg_order_value: Average order value.
    """

    period: str
    revenue: float
    order_count: int
    avg_order_value: float = 0.0


# ─── Top Items ────────────────────────────────────────────

class TopItem(BaseModel):
    """Top-selling menu item.

    Attributes:
        item_id: Item ID.
        name: Item name.
        category: Category name.
        qty_sold: Total quantity sold.
        revenue: Total revenue from this item.
        order_count: Number of orders containing this item.
    """

    item_id: int
    name: str
    category: str | None = None
    qty_sold: int
    revenue: float
    order_count: int = 0


# ─── Top Categories ──────────────────────────────────────

class TopCategory(BaseModel):
    """Top-performing category.

    Attributes:
        category_id: Category ID.
        name: Category name.
        item_count: Number of distinct items sold.
        total_revenue: Total revenue from this category.
        order_count: Number of orders with items from this category.
        qty_sold: Total quantity of items sold.
    """

    category_id: int
    name: str
    item_count: int
    total_revenue: float
    order_count: int
    qty_sold: int = 0


# ─── Order Trends ────────────────────────────────────────

class OrderTrend(BaseModel):
    """Order volume trend data point.

    Attributes:
        date: Date or period label.
        order_count: Number of orders.
        revenue: Revenue for the period.
        avg_order_value: Average order value.
        completed: Completed orders count.
        cancelled: Cancelled orders count.
    """

    date: str
    order_count: int
    revenue: float
    avg_order_value: float = 0.0
    completed: int = 0
    cancelled: int = 0


# ─── Hourly Heatmap ──────────────────────────────────────

class HourlySales(BaseModel):
    """Hourly sales data point for heatmap.

    Attributes:
        hour: Hour of the day (0-23).
        order_count: Number of orders in this hour.
        revenue: Revenue in this hour.
        avg_order_value: Average order value.
        items_sold: Number of items sold.
    """

    hour: int = Field(ge=0, le=23)
    order_count: int
    revenue: float
    avg_order_value: float = 0.0
    items_sold: int = 0


# ─── Customer Insights ───────────────────────────────────

class TopCustomer(BaseModel):
    """Top customer by spending or order count.

    Attributes:
        customer_id: Customer ID.
        name: Customer name.
        email: Customer email.
        order_count: Number of orders.
        total_spent: Total amount spent.
        avg_order_value: Average order value.
    """

    customer_id: int
    name: str
    email: str | None = None
    order_count: int
    total_spent: float
    avg_order_value: float = 0.0


class CustomerInsight(BaseModel):
    """Customer analytics overview.

    Attributes:
        total_customers: Total registered customers.
        active_customers: Customers who ordered in the period.
        new_customers: Customers created in the period.
        repeat_customers: Customers with >1 order.
        repeat_rate: Percentage of repeat customers.
        avg_customer_spend: Average total spend per customer.
        top_customers: Highest-spending customers.
    """

    total_customers: int
    active_customers: int = 0
    new_customers: int = 0
    repeat_customers: int = 0
    repeat_rate: float = 0.0
    avg_customer_spend: float = 0.0
    top_customers: list[TopCustomer] = []


# ─── Payment Breakdown ───────────────────────────────────

class PaymentBreakdown(BaseModel):
    """Payment method usage breakdown.

    Attributes:
        method: Payment method name (cash/card/mobile).
        count: Number of transactions.
        total_amount: Total amount processed.
        percentage: Percentage of total transactions.
    """

    method: str
    count: int
    total_amount: float
    percentage: float


# ─── Inventory Alerts ─────────────────────────────────────

class InventoryAlert(BaseModel):
    """Low or out-of-stock item alert.

    Attributes:
        item_id: Item ID.
        name: Item name.
        category: Category name.
        stock_qty: Current stock quantity.
        status: 'low_stock' or 'out_of_stock'.
    """

    item_id: int
    name: str
    category: str | None = None
    stock_qty: int
    status: str  # low_stock, out_of_stock


# ─── Profit/Loss ─────────────────────────────────────────

class ExpenseBreakdownItem(BaseModel):
    """Expense category breakdown item.

    Attributes:
        category: Expense category name.
        amount: Total amount for this category.
        percentage: Percentage of total expenses.
    """

    category: str
    amount: float
    percentage: float = 0.0


class ProfitLoss(BaseModel):
    """Profit and loss overview.

    Attributes:
        total_revenue: Total revenue (from completed orders).
        total_expenses: Total expenses.
        gross_profit: Revenue minus expenses.
        profit_margin: Profit as percentage of revenue.
        total_tax_collected: Total tax collected.
        total_discounts_given: Total discounts applied.
        net_revenue: Revenue minus discounts.
        expense_breakdown: Breakdown by expense category.
    """

    total_revenue: float = 0.0
    total_expenses: float = 0.0
    gross_profit: float = 0.0
    profit_margin: float = 0.0
    total_tax_collected: float = 0.0
    total_discounts_given: float = 0.0
    net_revenue: float = 0.0
    expense_breakdown: list[ExpenseBreakdownItem] = []


# ─── Shift Summary ────────────────────────────────────────

class ShiftSummaryItem(BaseModel):
    """Individual shift performance summary.

    Attributes:
        shift_id: Shift ID.
        opened_at: Shift opening time.
        closed_at: Shift closing time.
        status: Shift status (open/closed).
        total_orders: Orders processed during shift.
        total_revenue: Revenue during shift.
        total_expenses: Expenses during shift.
        net: Revenue minus expenses.
        opening_cash: Opening cash amount.
        closing_cash: Closing cash amount.
        cash_difference: Difference between expected and actual closing cash.
    """

    shift_id: int
    opened_at: datetime
    closed_at: datetime | None
    status: str
    total_orders: int = 0
    total_revenue: float = 0.0
    total_expenses: float = 0.0
    net: float = 0.0
    opening_cash: float = 0.0
    closing_cash: float | None = None
    cash_difference: float = 0.0
