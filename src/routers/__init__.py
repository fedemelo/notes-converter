from fastapi import APIRouter

from src.routers.factory import make_conversion_router
from src.routers.registry import CONVERSIONS

router = APIRouter()

for _conversion in CONVERSIONS:
    router.include_router(make_conversion_router(_conversion))
