"""V1 API router aggregating all endpoint routers."""

from fastapi import APIRouter

from app.api.v1.categories import router as categories_router
from app.api.v1.items import router as items_router
from app.api.v1.addons import router as addons_router
from app.api.v1.customers import router as customers_router
from app.api.v1.orders import router as orders_router
from app.api.v1.discounts import router as discounts_router
from app.api.v1.shifts import router as shifts_router
from app.api.v1.expenses import router as expenses_router
from app.api.v1.dashboard import router as dashboard_router

router = APIRouter(prefix="/api/v1")

router.include_router(categories_router)
router.include_router(items_router)
router.include_router(addons_router)
router.include_router(customers_router)
router.include_router(orders_router)
router.include_router(discounts_router)
router.include_router(shifts_router)
router.include_router(expenses_router)
router.include_router(dashboard_router)
