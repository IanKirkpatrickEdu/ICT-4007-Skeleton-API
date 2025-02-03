from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .core import router as core_router
from .week_1 import router as week_1_router
from .week_x import router as week_x_router
from .week_y import router as week_y_router

# global route collection
api_router = APIRouter(default_response_class=JSONResponse)
api_router.include_router(core_router, prefix="", tags=[])
api_router.include_router(week_1_router, prefix="/week-1", tags=["Week 1"])
api_router.include_router(week_x_router, prefix="/week-x", tags=["Week X"])
api_router.include_router(week_y_router, prefix="/week-y", tags=["Week Y"])
