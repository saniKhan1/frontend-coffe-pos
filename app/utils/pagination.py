"""Reusable pagination helper for list endpoints."""

from __future__ import annotations

import math
from typing import Any, TypeVar

from sqlalchemy.orm import Query

T = TypeVar("T")


def paginate(query: Query, page: int = 1, per_page: int = 20) -> dict[str, Any]:
    """Apply pagination to a SQLAlchemy query and return paginated result.

    Args:
        query: SQLAlchemy query object.
        page: Current page number (1-indexed).
        per_page: Number of items per page.

    Returns:
        Dictionary with ``items``, ``total``, ``page``, ``per_page``, ``total_pages``.
    """
    page = max(1, page)
    per_page = min(max(1, per_page), 100)  # Cap at 100 items per page

    total = query.count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1

    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }
