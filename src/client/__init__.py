from collections.abc import AsyncGenerator

from src.core.config import settings

from .cache import CacheClient
from .image import ImageClient


async def get_cache_client(
) -> AsyncGenerator[CacheClient]:
    yield CacheClient(
        cache_url=settings.cache_url
    )

async def get_image_client(
) -> AsyncGenerator[ImageClient]:
    yield ImageClient(

    )
