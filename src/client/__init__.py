from collections.abc import AsyncGenerator

from src.core.config import settings

from .agent import AgentClient
from .cache import CacheClient


async def get_cache_client(
) -> AsyncGenerator[CacheClient]:
    yield CacheClient(
        cache_url=settings.cache_url
    )

async def get_agent_client(
) -> AsyncGenerator[AgentClient]:
    yield AgentClient(

    )
