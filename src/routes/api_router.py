from fastapi import APIRouter
from .building import router as building_router
from .industry import router as industry_router
from .company import router as company_router

api_router = APIRouter(prefix="/api")

api_router.include_router(building_router, tags=["building"])
api_router.include_router(industry_router, tags=["industry"])
api_router.include_router(company_router, tags=["company"])
