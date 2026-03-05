"""Request/response logging middleware."""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.utils.logger import get_logger

logger = get_logger("request_logger")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every HTTP request with method, path, status code, and duration.

    Attaches to FastAPI as middleware and records:
    - HTTP method and path
    - Client IP address
    - Response status code
    - Request processing duration in milliseconds
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            f"{request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Duration: {duration_ms}ms "
            f"- IP: {client_ip}"
        )

        # Add timing header for frontend debugging
        response.headers["X-Process-Time-Ms"] = str(duration_ms)

        return response
