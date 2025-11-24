from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from src.client import ImageClient, get_image_client

from .image import ImageService


async def get_image_service(
    image_client: Annotated[ImageClient, Depends(get_image_client)]
) -> AsyncGenerator[ImageService]:
    yield ImageService(
        image_client=image_client
    )
