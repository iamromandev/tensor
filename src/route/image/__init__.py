
from fastapi import APIRouter

from .image import router as _image_router

_subrouters = [
    _image_router,
]

router = APIRouter()

for subrouter in _subrouters:
    router.include_router(subrouter)