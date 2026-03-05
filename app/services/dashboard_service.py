"""Dashboard analytics service providing rich data for frontend consumption."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

from sqlalchemy import func, case, distinct, extract
from sqlalchemy.orm import Session

from app.config import settings
from app.models.category import Category
from app.models.customer import Customer
from app.models.expense import Expense
from app.models.item import Item
from app.models.order import Order, OrderItem
from app.models.shift import Shift
from app.schemas.dashboard import (
    CustomerInsight,
    DashboardSummary,
    ExpenseBreakdownItem,
    HourlySales,
    InventoryAlert,
    OrderTrend,
    PaymentBreakdown,
    ProfitLoss,
    RevenueBreakdown,
    ShiftSummaryItem,
    TopCategory,
    TopCustomer,
    TopItem,
)
from app.utils.filters import get_date_range, get_grouping_format
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _get_date_range_with_defaults(
    start_date: date | None, end_date: date | None
) -> tuple[datetime, datetime]:
    """Get datetime range, defaulting to last 30 days."""
    return get_date_range(start_date, end_date)


def _get_previous_period(
    start_dt: datetime, end_dt: datetime
) -> tuple[datetime, datetime]:
    """Calculate the equivalent previous period for comparison."""
    delta = end_dt - start_dt
    prev_end = start_dt
    prev_start = prev_end - delta
    return prev_start, prev_end


def get_dashboard_summary(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
) -> DashboardSummary:
    """Get overall dashboard KPI summary with period-over-period comparison.

    Args:
        db: Database session.
        start_date: Start of analysis period.
        end_date: End of analysis period.

    Returns:
        DashboardSummary with all KPIs.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)
    prev_start, prev_end = _get_previous_period(start_dt, end_dt)

    # Current period metrics
    current_orders = (
        db.query(Order)
        .filter(Order.created_at.between(start_dt, end_dt))
        .all()
    )

    total_revenue = sum(o.total for o in current_orders if o.status != "cancelled")
    total_orders = len(current_orders)
    completed = sum(1 for o in current_orders if o.status == "completed")
    cancelled = sum(1 for o in current_orders if o.status == "cancelled")
    non_cancelled = [o for o in current_orders if o.status != "cancelled"]
    avg_order = total_revenue / len(non_cancelled) if non_cancelled else 0.0

    # Items sold
    total_items_sold = (
        db.query(func.coalesce(func.sum(OrderItem.quantity), 0))
        .join(Order)
        .filter(Order.created_at.between(start_dt, end_dt), Order.status != "cancelled")
        .scalar()
    ) or 0

    # Customer metrics
    total_customers = db.query(Customer).count()
    new_customers = (
        db.query(Customer)
        .filter(Customer.created_at.between(start_dt, end_dt))
        .count()
    )

    # Previous period for comparison
    prev_orders = (
        db.query(Order)
        .filter(Order.created_at.between(prev_start, prev_end))
        .all()
    )
    prev_revenue = sum(o.total for o in prev_orders if o.status != "cancelled")
    prev_count = len(prev_orders)

    rev_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0.0
    ord_change = ((total_orders - prev_count) / prev_count * 100) if prev_count > 0 else 0.0

    # Top payment method
    payment_query = (
        db.query(Order.payment_method, func.count(Order.id).label("cnt"))
        .filter(Order.created_at.between(start_dt, end_dt), Order.status != "cancelled")
        .group_by(Order.payment_method)
        .order_by(func.count(Order.id).desc())
        .first()
    )
    top_payment = payment_query[0] if payment_query else None

    # Busiest hour
    busiest_hour_result = (
        db.query(
            func.strftime("%H", Order.created_at).label("hr"),
            func.count(Order.id).label("cnt"),
        )
        .filter(Order.created_at.between(start_dt, end_dt), Order.status != "cancelled")
        .group_by(func.strftime("%H", Order.created_at))
        .order_by(func.count(Order.id).desc())
        .first()
    )
    busiest_hour = int(busiest_hour_result[0]) if busiest_hour_result else None

    return DashboardSummary(
        total_revenue=round(total_revenue, 2),
        total_orders=total_orders,
        completed_orders=completed,
        cancelled_orders=cancelled,
        avg_order_value=round(avg_order, 2),
        total_customers=total_customers,
        new_customers=new_customers,
        total_items_sold=total_items_sold,
        revenue_change_pct=round(rev_change, 2),
        order_change_pct=round(ord_change, 2),
        top_payment_method=top_payment,
        busiest_hour=busiest_hour,
    )


def get_revenue_breakdown(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    group_by: str = "daily",
) -> list[RevenueBreakdown]:
    """Get revenue breakdown grouped by period.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.
        group_by: Grouping ('daily', 'weekly', 'monthly').

    Returns:
        List of RevenueBreakdown data points.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)
    fmt = get_grouping_format(group_by)

    results = (
        db.query(
            func.strftime(fmt, Order.created_at).label("period"),
            func.coalesce(func.sum(Order.total), 0).label("revenue"),
            func.count(Order.id).label("order_count"),
        )
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
        .group_by(func.strftime(fmt, Order.created_at))
        .order_by(func.strftime(fmt, Order.created_at))
        .all()
    )

    return [
        RevenueBreakdown(
            period=r.period,
            revenue=round(r.revenue, 2),
            order_count=r.order_count,
            avg_order_value=round(r.revenue / r.order_count, 2) if r.order_count > 0 else 0.0,
        )
        for r in results
    ]


def get_top_items(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 10,
) -> list[TopItem]:
    """Get top-selling menu items.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.
        limit: Number of items to return.

    Returns:
        List of TopItem sorted by quantity sold.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)

    results = (
        db.query(
            Item.id,
            Item.name,
            Category.name.label("category_name"),
            func.coalesce(func.sum(OrderItem.quantity), 0).label("qty_sold"),
            func.coalesce(func.sum(OrderItem.subtotal), 0).label("revenue"),
            func.count(distinct(OrderItem.order_id)).label("order_count"),
        )
        .join(OrderItem, OrderItem.item_id == Item.id)
        .join(Order, Order.id == OrderItem.order_id)
        .outerjoin(Category, Category.id == Item.category_id)
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
        .group_by(Item.id, Item.name, Category.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )

    return [
        TopItem(
            item_id=r.id,
            name=r.name,
            category=r.category_name,
            qty_sold=r.qty_sold,
            revenue=round(r.revenue, 2),
            order_count=r.order_count,
        )
        for r in results
    ]


def get_top_categories(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 10,
) -> list[TopCategory]:
    """Get top-performing categories.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.
        limit: Max categories to return.

    Returns:
        List of TopCategory sorted by revenue.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)

    results = (
        db.query(
            Category.id,
            Category.name,
            func.count(distinct(Item.id)).label("item_count"),
            func.coalesce(func.sum(OrderItem.subtotal), 0).label("total_revenue"),
            func.count(distinct(OrderItem.order_id)).label("order_count"),
            func.coalesce(func.sum(OrderItem.quantity), 0).label("qty_sold"),
        )
        .join(Item, Item.category_id == Category.id)
        .join(OrderItem, OrderItem.item_id == Item.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
        .group_by(Category.id, Category.name)
        .order_by(func.sum(OrderItem.subtotal).desc())
        .limit(limit)
        .all()
    )

    return [
        TopCategory(
            category_id=r.id,
            name=r.name,
            item_count=r.item_count,
            total_revenue=round(r.total_revenue, 2),
            order_count=r.order_count,
            qty_sold=r.qty_sold,
        )
        for r in results
    ]


def get_order_trends(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    group_by: str = "daily",
) -> list[OrderTrend]:
    """Get order volume and revenue trends over time.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.
        group_by: Grouping ('daily', 'weekly', 'monthly').

    Returns:
        List of OrderTrend data points.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)
    fmt = get_grouping_format(group_by)

    results = (
        db.query(
            func.strftime(fmt, Order.created_at).label("date"),
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(case((Order.status != "cancelled", Order.total), else_=0)), 0).label("revenue"),
            func.sum(case((Order.status == "completed", 1), else_=0)).label("completed"),
            func.sum(case((Order.status == "cancelled", 1), else_=0)).label("cancelled"),
        )
        .filter(Order.created_at.between(start_dt, end_dt))
        .group_by(func.strftime(fmt, Order.created_at))
        .order_by(func.strftime(fmt, Order.created_at))
        .all()
    )

    return [
        OrderTrend(
            date=r.date,
            order_count=r.order_count,
            revenue=round(float(r.revenue), 2),
            avg_order_value=round(float(r.revenue) / r.order_count, 2) if r.order_count > 0 else 0.0,
            completed=r.completed or 0,
            cancelled=r.cancelled or 0,
        )
        for r in results
    ]


def get_hourly_heatmap(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    day_of_week: int | None = None,
) -> list[HourlySales]:
    """Get hourly sales data for heatmap visualization.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.
        day_of_week: Optional filter for specific day (0=Sunday, 6=Saturday).

    Returns:
        List of 24 HourlySales entries (one per hour).
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)

    query = (
        db.query(
            func.strftime("%H", Order.created_at).label("hour"),
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(Order.total), 0).label("revenue"),
        )
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
    )

    if day_of_week is not None:
        query = query.filter(func.strftime("%w", Order.created_at) == str(day_of_week))

    results = (
        query.group_by(func.strftime("%H", Order.created_at))
        .order_by(func.strftime("%H", Order.created_at))
        .all()
    )

    # Build a dict from results for easy lookup
    hourly_data = {int(r.hour): {"order_count": r.order_count, "revenue": float(r.revenue)} for r in results}

    # Items sold per hour
    items_query = (
        db.query(
            func.strftime("%H", Order.created_at).label("hour"),
            func.coalesce(func.sum(OrderItem.quantity), 0).label("items_sold"),
        )
        .join(Order, Order.id == OrderItem.order_id)
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
        .group_by(func.strftime("%H", Order.created_at))
        .all()
    )
    items_data = {int(r.hour): r.items_sold for r in items_query}

    # Return all 24 hours (fill zeros for missing hours)
    return [
        HourlySales(
            hour=h,
            order_count=hourly_data.get(h, {}).get("order_count", 0),
            revenue=round(hourly_data.get(h, {}).get("revenue", 0.0), 2),
            avg_order_value=(
                round(hourly_data[h]["revenue"] / hourly_data[h]["order_count"], 2)
                if h in hourly_data and hourly_data[h]["order_count"] > 0
                else 0.0
            ),
            items_sold=items_data.get(h, 0),
        )
        for h in range(24)
    ]


def get_customer_insights(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    top_limit: int = 10,
) -> CustomerInsight:
    """Get customer analytics and insights.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.
        top_limit: Number of top customers to include.

    Returns:
        CustomerInsight with breakdown and top customers.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)

    total_customers = db.query(Customer).count()
    new_customers = db.query(Customer).filter(Customer.created_at.between(start_dt, end_dt)).count()

    # Active customers (who placed orders in the period)
    active_customer_ids = (
        db.query(distinct(Order.customer_id))
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.customer_id.isnot(None),
            Order.status != "cancelled",
        )
        .all()
    )
    active_count = len(active_customer_ids)

    # Repeat customers (>1 order in period)
    repeat_query = (
        db.query(Order.customer_id, func.count(Order.id).label("cnt"))
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.customer_id.isnot(None),
            Order.status != "cancelled",
        )
        .group_by(Order.customer_id)
        .having(func.count(Order.id) > 1)
        .all()
    )
    repeat_count = len(repeat_query)
    repeat_rate = (repeat_count / active_count * 100) if active_count > 0 else 0.0

    # Average spend per customer
    avg_spend = (
        db.query(func.avg(Customer.total_spent))
        .filter(Customer.total_spent > 0)
        .scalar()
    ) or 0.0

    # Top customers
    top_customers_data = (
        db.query(
            Customer.id,
            Customer.name,
            Customer.email,
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(Order.total), 0).label("total_spent"),
        )
        .join(Order, Order.customer_id == Customer.id)
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
        .group_by(Customer.id, Customer.name, Customer.email)
        .order_by(func.sum(Order.total).desc())
        .limit(top_limit)
        .all()
    )

    top_customers = [
        TopCustomer(
            customer_id=c.id,
            name=c.name,
            email=c.email,
            order_count=c.order_count,
            total_spent=round(float(c.total_spent), 2),
            avg_order_value=round(float(c.total_spent) / c.order_count, 2) if c.order_count > 0 else 0.0,
        )
        for c in top_customers_data
    ]

    return CustomerInsight(
        total_customers=total_customers,
        active_customers=active_count,
        new_customers=new_customers,
        repeat_customers=repeat_count,
        repeat_rate=round(repeat_rate, 2),
        avg_customer_spend=round(float(avg_spend), 2),
        top_customers=top_customers,
    )


def get_payment_breakdown(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[PaymentBreakdown]:
    """Get payment method usage breakdown.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.

    Returns:
        List of PaymentBreakdown entries.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)

    results = (
        db.query(
            Order.payment_method,
            func.count(Order.id).label("count"),
            func.coalesce(func.sum(Order.total), 0).label("total_amount"),
        )
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
        .group_by(Order.payment_method)
        .order_by(func.count(Order.id).desc())
        .all()
    )

    total_transactions = sum(r.count for r in results)

    return [
        PaymentBreakdown(
            method=r.payment_method,
            count=r.count,
            total_amount=round(float(r.total_amount), 2),
            percentage=round(r.count / total_transactions * 100, 2) if total_transactions > 0 else 0.0,
        )
        for r in results
    ]


def get_inventory_alerts(
    db: Session,
    threshold: int | None = None,
) -> list[InventoryAlert]:
    """Get low stock and out-of-stock item alerts.

    Args:
        db: Database session.
        threshold: Stock threshold (default from settings).

    Returns:
        List of InventoryAlert entries sorted by stock_qty ascending.
    """
    threshold = threshold or settings.LOW_STOCK_THRESHOLD

    results = (
        db.query(Item.id, Item.name, Category.name.label("category_name"), Item.stock_qty)
        .outerjoin(Category, Category.id == Item.category_id)
        .filter(Item.stock_qty != -1, Item.stock_qty <= threshold)
        .order_by(Item.stock_qty.asc())
        .all()
    )

    return [
        InventoryAlert(
            item_id=r.id,
            name=r.name,
            category=r.category_name,
            stock_qty=r.stock_qty,
            status="out_of_stock" if r.stock_qty == 0 else "low_stock",
        )
        for r in results
    ]


def get_profit_loss(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
) -> ProfitLoss:
    """Get profit and loss overview.

    Args:
        db: Database session.
        start_date: Start date.
        end_date: End date.

    Returns:
        ProfitLoss with revenue, expenses, and breakdown.
    """
    start_dt, end_dt = _get_date_range_with_defaults(start_date, end_date)

    # Revenue from completed/non-cancelled orders
    revenue_data = (
        db.query(
            func.coalesce(func.sum(Order.total), 0).label("total_revenue"),
            func.coalesce(func.sum(Order.tax_amount), 0).label("total_tax"),
            func.coalesce(func.sum(Order.discount_amount), 0).label("total_discounts"),
        )
        .filter(
            Order.created_at.between(start_dt, end_dt),
            Order.status != "cancelled",
        )
        .first()
    )

    total_revenue = float(revenue_data.total_revenue or 0)
    total_tax = float(revenue_data.total_tax or 0)
    total_discounts = float(revenue_data.total_discounts or 0)

    # Expenses
    expense_results = (
        db.query(
            Expense.category,
            func.coalesce(func.sum(Expense.amount), 0).label("amount"),
        )
        .filter(Expense.date.between(start_dt, end_dt))
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    total_expenses = sum(float(e.amount) for e in expense_results)

    expense_breakdown = [
        ExpenseBreakdownItem(
            category=e.category,
            amount=round(float(e.amount), 2),
            percentage=round(float(e.amount) / total_expenses * 100, 2) if total_expenses > 0 else 0.0,
        )
        for e in expense_results
    ]

    gross_profit = total_revenue - total_expenses
    profit_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0.0

    return ProfitLoss(
        total_revenue=round(total_revenue, 2),
        total_expenses=round(total_expenses, 2),
        gross_profit=round(gross_profit, 2),
        profit_margin=round(profit_margin, 2),
        total_tax_collected=round(total_tax, 2),
        total_discounts_given=round(total_discounts, 2),
        net_revenue=round(total_revenue - total_discounts, 2),
        expense_breakdown=expense_breakdown,
    )


def get_shift_summaries(
    db: Session,
    shift_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[ShiftSummaryItem]:
    """Get shift performance summaries.

    Args:
        db: Database session.
        shift_id: Specific shift to get summary for.
        start_date: Start date filter.
        end_date: End date filter.

    Returns:
        List of ShiftSummaryItem entries.
    """
    query = db.query(Shift).order_by(Shift.opened_at.desc())

    if shift_id:
        query = query.filter(Shift.id == shift_id)
    else:
        if start_date:
            start_dt = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
            query = query.filter(Shift.opened_at >= start_dt)
        if end_date:
            end_dt = datetime.combine(end_date, datetime.max.time(), tzinfo=timezone.utc)
            query = query.filter(Shift.opened_at <= end_dt)

    shifts = query.all()
    summaries = []

    for shift in shifts:
        # Revenue from orders in this shift
        order_data = (
            db.query(
                func.count(Order.id).label("total_orders"),
                func.coalesce(func.sum(Order.total), 0).label("total_revenue"),
            )
            .filter(Order.shift_id == shift.id, Order.status != "cancelled")
            .first()
        )

        total_orders = order_data.total_orders or 0
        total_revenue = float(order_data.total_revenue or 0)

        # Expenses in this shift
        total_expenses = float(
            db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(Expense.shift_id == shift.id)
            .scalar() or 0
        )

        # Cash difference for cash orders
        cash_revenue = float(
            db.query(func.coalesce(func.sum(Order.total), 0))
            .filter(Order.shift_id == shift.id, Order.payment_method == "cash", Order.status != "cancelled")
            .scalar() or 0
        )
        expected_closing = shift.opening_cash + cash_revenue - total_expenses
        cash_diff = (shift.closing_cash - expected_closing) if shift.closing_cash is not None else 0.0

        summaries.append(
            ShiftSummaryItem(
                shift_id=shift.id,
                opened_at=shift.opened_at,
                closed_at=shift.closed_at,
                status=shift.status,
                total_orders=total_orders,
                total_revenue=round(total_revenue, 2),
                total_expenses=round(total_expenses, 2),
                net=round(total_revenue - total_expenses, 2),
                opening_cash=shift.opening_cash,
                closing_cash=shift.closing_cash,
                cash_difference=round(cash_diff, 2),
            )
        )

    return summaries
