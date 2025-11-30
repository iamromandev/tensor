import asyncio
import uuid
from pathlib import Path
from typing import Any

import torch
from diffusers import StableDiffusionPipeline
from diffusers.utils import logging
from loguru import logger

from src.core.constant import IMAGE_PRETRAINED_MODEL
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

        logger.debug(f"{self._tag}|__init__(): StableDiffusionPipeline: loading {IMAGE_PRETRAINED_MODEL}")
        self._pipline = StableDiffusionPipeline.from_pretrained(
            pretrained_model_name_or_path=IMAGE_PRETRAINED_MODEL,
            torch_dtype=torch.float32
        ).to("cpu")
        logger.debug(f"{self._tag}|__init__(): StableDiffusionPipeline: loaded {IMAGE_PRETRAINED_MODEL}")

        # logger.debug(f"{self._tag}|__init__(): loading StableDiffusionPipeline")
        # self._pipline = StableDiffusionPipeline.from_pretrained(
        #     pretrained_model_name_or_path=PRETRAINED_PRIOR_MODEL,
        #     torch_dtype=torch.float32,
        #     safety_checker=None
        # )
        # self._pipline.to("cpu")
        #
        # logger.debug(f"{self._tag}|__init__(): StableDiffusionPipeline loaded")

        self._initialized = True

    @property
    def _tag(self) -> str:
        return self.__class__.__name__

    def _on_step_end(
        self,
        total_steps: int,
        pipeline: "StableDiffusionPipeline",
        step_idx: int,
        timestep: int,
        callback_kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        # Clamp step index
        current_step = min(step_idx + 1, total_steps)
        pct: float = current_step / total_steps * 100
        logger.info(f"{self._tag}|Step {current_step}/{total_steps} ({pct:.1f}%) timestep={timestep}")

        # Optionally handle latents
        latents = callback_kwargs.get("latents")
        if latents is not None:
            logger.debug(f"{self._tag}|Latents shape: {tuple(latents.shape)}")

        return callback_kwargs

    def _generate_blocking(self, prompt: str, steps: int, width: int, height: int) -> str:
        logger.debug(f"{self._tag}|_generate_blocking(): prompt={prompt}")

        result = self._pipline(
            prompt=prompt,
            negative_prompt="",
            num_inference_steps=steps,
            width=width,
            height=height,
            callback_on_step_end=lambda *args, **kwargs: self._on_step_end(steps, *args, **kwargs),
            callback_on_step_end_tensor_inputs=["latents"],
        )

        img = result.images[0]

        file_path = f"{self._dir}/{uuid.uuid4()}.png"
        img.save(file_path)
        # imageio.imwrite(file_path, img)

        return file_path

    async def run(
        self, prompt: str, steps: int, width: int, height: int
    ) -> str:
        logger.debug(f"{self._tag}|run(): prompt={prompt}")

        file_path = await asyncio.to_thread(self._generate_blocking, prompt, steps, width, height)

        return file_path
