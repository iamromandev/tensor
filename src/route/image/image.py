from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from loguru import logger

from src.core.success import Success
from src.data.schema.image import ImageInSchema, ImageOutSchema
from src.service.image import ImageService, get_image_service

router = APIRouter(prefix="/image", tags=["image"])


@router.post(
    path="/generate",
    response_model=Success[ImageOutSchema]
)
async def generate(
    service: Annotated[ImageService, Depends(get_image_service)],
    payload: Annotated[ImageInSchema, Body(...)],
) -> JSONResponse:
    logger.debug(f"route|image|generate|payload: {payload.model_dump()}")
    output: ImageOutSchema = await service.run(payload=payload)
    return Success.ok(data=output).to_resp()
