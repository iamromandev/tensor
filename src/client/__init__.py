from collections.abc import AsyncGenerator

import torch
from diffusers import StableDiffusionPipeline
from loguru import logger

from src.core.config import settings
from src.core.constant import IMAGE_PRETRAINED_MODEL

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

async def init_hf_model()->None:
    logger.debug("init_hf_model(): StableDiffusionPipeline loading")
    StableDiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=IMAGE_PRETRAINED_MODEL,
        torch_dtype=torch.float32
    ).to("cpu")
    logger.debug("init_hf_model(): StableDiffusionPipeline loaded")
