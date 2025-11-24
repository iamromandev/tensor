import uuid
from pathlib import Path

import imageio
import torch
from diffusers import StableDiffusionPipeline
from diffusers.utils import logging
from loguru import logger

from src.core.factory import SingletonMeta


class ImageClient(metaclass=SingletonMeta):
    _initialized: bool = False
    _pipline: StableDiffusionPipeline

    def __init__(self) -> None:
        if self._initialized:
            return

        logger.debug(f"{self._tag}|__init__():")

        self._dir: Path = Path("media/image")
        self._dir.mkdir(parents=True, exist_ok=True)

        logging.set_verbosity_info()

        logger.debug(f"{self._tag}|__init__(): StableDiffusionPipeline Creating")
        self._pipline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5-pruned",
            torch_dtype=torch.float32,
            safety_checker=None
        ).to("cpu")
        logger.debug(f"{self._tag}|__init__(): StableDiffusionPipeline Created")

        self._initialized = True

    @property
    def _tag(self) -> str:
        return self.__class__.__name__

    async def run(
        self, prompt: str, steps: int, width: int, height: int
    ) -> str:
        logger.debug(f"{self._tag}|run(): prompt={prompt}")

        result = self._pipline(
            prompt,
            num_inference_steps=steps,
            width=width,
            height=height
        )

        img = result.images[0]

        file_path = f"{self._dir}/{uuid.uuid4()}.png"
        imageio.imwrite(file_path, img)

        return file_path
