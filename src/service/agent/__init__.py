from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from src.client import AgentClient, get_agent_client
from src.service.agent.agent import AgentService


async def get_agent_service(
agent_client: Annotated[AgentClient, Depends(get_agent_client)]
) -> AsyncGenerator[AgentService]:
    yield AgentService(
        agent_client=agent_client
    )
