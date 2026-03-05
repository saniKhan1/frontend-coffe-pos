"""Dashboard analytics endpoints providing rich data for frontend dashboards."""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.dashboard import (
    CustomerInsight,
    DashboardSummary,
    HourlySales,
    InventoryAlert,
    OrderTrend,
    PaymentBreakdown,
    ProfitLoss,
    RevenueBreakdown,
    ShiftSummaryItem,
    TopCategory,
    TopItem,
)
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummary,
    summary="Get dashboard KPI summary",
)
def get_summary(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD). Default: 30 days ago"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD). Default: today"),
    db: Session = Depends(get_db),
):
    """Get overall dashboard KPI summary.

    Returns key metrics including total revenue, order count, average order value,
    customer stats, and period-over-period comparison percentages.

    If no dates are provided, defaults to the last 30 days with comparison
    against the previous 30-day period.
    """
    return dashboard_service.get_dashboard_summary(db, start_date, end_date)


@router.get(
    "/revenue",
    response_model=list[RevenueBreakdown],
    summary="Get revenue breakdown",
)
def get_revenue(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    group_by: str = Query("daily", description="Grouping: daily|weekly|monthly"),
    db: Session = Depends(get_db),
):
    """Get revenue breakdown grouped by time period.

    Each data point includes the period label, total revenue,
    order count, and average order value for that period.
    """
    return dashboard_service.get_revenue_breakdown(db, start_date, end_date, group_by)


@router.get(
    "/top-items",
    response_model=list[TopItem],
    summary="Get top-selling items",
)
def get_top_items(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=50, description="Number of items to return"),
    db: Session = Depends(get_db),
):
    """Get top-selling menu items ranked by quantity sold.

    Includes item name, category, quantity sold, revenue generated, and order count.
    """
    return dashboard_service.get_top_items(db, start_date, end_date, limit)


@router.get(
    "/top-categories",
    response_model=list[TopCategory],
    summary="Get top categories",
)
def get_top_categories(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=50, description="Number of categories to return"),
    db: Session = Depends(get_db),
):
    """Get top-performing categories ranked by revenue.

    Includes category name, distinct item count, total revenue, order count, and total quantity.
    """
    return dashboard_service.get_top_categories(db, start_date, end_date, limit)


@router.get(
    "/order-trends",
    response_model=list[OrderTrend],
    summary="Get order volume trends",
)
def get_order_trends(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    group_by: str = Query("daily", description="Grouping: daily|weekly|monthly"),
    db: Session = Depends(get_db),
):
    """Get order volume and revenue trends over time.

    Each data point includes order count, revenue, average order value,
    and counts for completed and cancelled orders.
    """
    return dashboard_service.get_order_trends(db, start_date, end_date, group_by)


@router.get(
    "/hourly-heatmap",
    response_model=list[HourlySales],
    summary="Get hourly sales heatmap",
)
def get_hourly_heatmap(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    day_of_week: int | None = Query(None, ge=0, le=6, description="Day of week (0=Sunday, 6=Saturday)"),
    db: Session = Depends(get_db),
):
    """Get hourly sales distribution for heatmap visualization.

    Returns 24 data points (one per hour, 0-23), each with order count,
    revenue, average order value, and items sold. Missing hours are filled with zeros.
    """
    return dashboard_service.get_hourly_heatmap(db, start_date, end_date, day_of_week)


@router.get(
    "/customer-insights",
    response_model=CustomerInsight,
    summary="Get customer analytics",
)
def get_customer_insights(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    top_limit: int = Query(10, ge=1, le=50, description="Number of top customers to include"),
    db: Session = Depends(get_db),
):
    """Get customer analytics and insights.

    Includes total customers, active customers, new/repeat customer counts,
    repeat rate, average spend, and a ranked list of top customers.
    """
    return dashboard_service.get_customer_insights(db, start_date, end_date, top_limit)


@router.get(
    "/payment-breakdown",
    response_model=list[PaymentBreakdown],
    summary="Get payment method breakdown",
)
def get_payment_breakdown(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """Get payment method usage breakdown.

    Shows count, total amount, and percentage for each payment method (cash/card/mobile).
    """
    return dashboard_service.get_payment_breakdown(db, start_date, end_date)


@router.get(
    "/inventory-alerts",
    response_model=list[InventoryAlert],
    summary="Get low stock alerts",
)
def get_inventory_alerts(
    threshold: int | None = Query(None, ge=0, description="Stock threshold (default from settings)"),
    db: Session = Depends(get_db),
):
    """Get items with low or zero stock.

    Returns items where stock_qty <= threshold (excludes unlimited stock items).
    Each alert includes item name, category, current stock, and status (low_stock or out_of_stock).
    """
    return dashboard_service.get_inventory_alerts(db, threshold)


@router.get(
    "/profit-loss",
    response_model=ProfitLoss,
    summary="Get profit & loss overview",
)
def get_profit_loss(
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """Get profit and loss overview.

    Includes total revenue, total expenses, gross profit, profit margin,
    tax collected, discounts given, net revenue, and expense breakdown by category.
    """
    return dashboard_service.get_profit_loss(db, start_date, end_date)


@router.get(
    "/shift-summary",
    response_model=list[ShiftSummaryItem],
    summary="Get shift performance summary",
)
def get_shift_summary(
    shift_id: int | None = Query(None, description="Specific shift ID"),
    start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """Get shift performance summaries.

    Each shift includes order count, revenue, expenses, net, cash amounts,
    and the cash difference (actual vs expected).
    """
    return dashboard_service.get_shift_summaries(db, shift_id, start_date, end_date)
