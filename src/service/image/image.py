from src.client import ImageClient
from src.core.base import BaseService
from src.data.schema.image import ImageInSchema, ImageOutSchema


class ImageService(BaseService):
    _image_client: ImageClient

    def __init__(self, image_client: ImageClient) -> None:
        super().__init__()
        self._image_client = image_client

    async def run(self, payload: ImageInSchema) -> ImageOutSchema:

        result = await self._image_client.run(
            prompt=payload.prompt,
            steps=payload.steps,
            width=payload.width,
            height=payload.height
        )
        return ImageOutSchema(output=result)
