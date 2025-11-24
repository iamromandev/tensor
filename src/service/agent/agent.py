from src.client import AgentClient
from src.core.base import BaseService
from src.data.schema.run import RunOutSchema, RunSchema


class AgentService(BaseService):
    _agent_client: AgentClient

    def __init__(self, agent_client: AgentClient) -> None:
        super().__init__()
        self._agent_client = agent_client

    async def run(self, payload: RunSchema) -> RunOutSchema:
        output = await self._agent_client.run(payload.prompt)
        return RunOutSchema(output=output)
