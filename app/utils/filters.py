"""Date range and query filter helpers."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone


def get_date_range(
    start_date: date | None = None,
    end_date: date | None = None,
    period: str | None = None,
) -> tuple[datetime, datetime]:
    """Compute start and end datetime from provided dates or period.

    Args:
        start_date: Explicit start date.
        end_date: Explicit end date.
        period: One of ``'today'``, ``'week'``, ``'month'``, ``'year'``. Overridden by explicit dates.

    Returns:
        Tuple of (start_datetime, end_datetime) in UTC.
    """
    now = datetime.now(timezone.utc)

    if start_date and end_date:
        return (
            datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc),
            datetime.combine(end_date, datetime.max.time(), tzinfo=timezone.utc),
        )

    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start, now
    elif period == "week":
        start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, now
    elif period == "month":
        start = (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, now
    elif period == "year":
        start = (now - timedelta(days=365)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, now

    # Default: last 30 days
    start = (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
    return start, now


def get_grouping_format(group_by: str = "daily") -> str:
    """Return SQLite strftime format string for grouping.

    Args:
        group_by: One of ``'daily'``, ``'weekly'``, ``'monthly'``.

    Returns:
        strftime format string.
    """
    formats = {
        "daily": "%Y-%m-%d",
        "weekly": "%Y-%W",
        "monthly": "%Y-%m",
    }
    return formats.get(group_by, "%Y-%m-%d")
