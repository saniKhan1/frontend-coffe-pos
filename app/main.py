"""FastAPI application factory for Philo Coffee Shop POS."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.v1.router import router as v1_router
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.middleware.audit import AuditMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.seed.seed_data import seed_database
from app.utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler — runs on startup/shutdown."""
    logger.info("Starting Philo Coffee Shop POS API…")

    # Create tables (safe no-op if they already exist)
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured")

    # Auto-seed on empty database
    db = SessionLocal()
    try:
        seed_database(db)
    except Exception:
        logger.exception("Seeding failed")
        db.rollback()
    finally:
        db.close()

    yield

    logger.info("Shutting down Philo Coffee Shop POS API…")


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "Point-of-Sale REST API for Philo Coffee Shop. "
            "Manage categories, menu items, add-ons, customers, orders, "
            "discounts, shifts, expenses, and view a rich analytics dashboard."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ─── CORS ─────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ─── Custom Middleware ────────────────────────
    app.add_middleware(AuditMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # ─── Routers ──────────────────────────────────
    app.include_router(v1_router)

    # ─── Root & Health ────────────────────────────
    @app.get("/", include_in_schema=False)
    async def root():
        """Redirect root to interactive API docs."""
        return RedirectResponse(url="/docs")

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health-check endpoint."""
        return {"status": "healthy", "app": settings.APP_NAME, "version": "1.0.0"}

    return app


app = create_app()
