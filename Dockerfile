# ── Build stage ────────────────────────────────────────
FROM python:3.12-slim AS builder

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml .
COPY .python-version .

# Create venv and install dependencies (no dev deps = no Sphinx packages)
# This creates the venv inside the container, not copying from host
RUN uv sync --no-dev


# ── Runtime stage ─────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="mrqadeer"
LABEL org.opencontainers.image.title="Philo Coffee Shop POS API"
LABEL org.opencontainers.image.description="FastAPI POS backend for Philo Coffee Shop"
LABEL org.opencontainers.image.source="https://github.com/mrqadeer/philo-coffee-shop"

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --create-home appuser

WORKDIR /app

# Copy only the virtual environment from builder (no source code yet for caching)
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . /app/

# Set env vars
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create data directory for SQLite database
RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
