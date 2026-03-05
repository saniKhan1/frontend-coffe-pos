"""Audit logging middleware for tracking data changes."""

import json
from datetime import datetime, timezone

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.database import SessionLocal
from app.models.audit_log import AuditLog
from app.utils.logger import get_logger

logger = get_logger("audit")

# Methods that create/modify/delete data
AUDIT_METHODS = {"POST", "PATCH", "PUT", "DELETE"}

# API path prefix to audit
AUDIT_PREFIX = "/api/v1/"

# Paths to skip auditing (like dashboard read-only endpoints)
SKIP_PATHS = {"/api/v1/dashboard/"}


class AuditMiddleware(BaseHTTPMiddleware):
    """Records audit log entries for all CUD (Create/Update/Delete) API operations.

    Captures the entity type, action, request body, response body, client IP,
    and user agent for each mutating API request.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Only audit mutating requests to API endpoints
        if request.method not in AUDIT_METHODS or not request.url.path.startswith(AUDIT_PREFIX):
            return await call_next(request)

        # Skip dashboard and other read-only paths
        if any(request.url.path.startswith(skip) for skip in SKIP_PATHS):
            return await call_next(request)

        # Parse entity type from path: /api/v1/{entity_type}/...
        path_parts = request.url.path.strip("/").split("/")
        entity_type = path_parts[2] if len(path_parts) > 2 else "unknown"
        entity_type = entity_type.replace("-", "_").title().rstrip("s")  # e.g., "categories" -> "Category"

        # Determine action
        action_map = {"POST": "create", "PATCH": "update", "PUT": "update", "DELETE": "delete"}
        action = action_map.get(request.method, "unknown")

        # Try to get entity ID from path
        entity_id = None
        if len(path_parts) > 3:
            try:
                entity_id = int(path_parts[3])
            except (ValueError, IndexError):
                pass

        # Read request body
        request_body = None
        try:
            body_bytes = await request.body()
            if body_bytes:
                request_body = body_bytes.decode("utf-8")
        except Exception:
            pass

        # Execute the actual request
        response = await call_next(request)

        # Log to audit table (only for successful operations)
        if 200 <= response.status_code < 400:
            try:
                db = SessionLocal()
                audit_entry = AuditLog(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    action=action,
                    old_values=None,  # Would require pre-fetch for updates/deletes
                    new_values=request_body,
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent", "")[:500],
                    timestamp=datetime.now(timezone.utc),
                )
                db.add(audit_entry)
                db.commit()
                db.close()
                logger.info(f"Audit: {action} {entity_type} (id={entity_id}) from {request.client.host if request.client else 'unknown'}")
            except Exception as e:
                logger.error(f"Failed to write audit log: {e}")

        return response
