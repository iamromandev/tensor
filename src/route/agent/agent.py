from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from src.core.success import Success
from src.data.schema.run import RunOutSchema, RunSchema
from src.service.agent import AgentService, get_agent_service

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post(path="/run")
async def run(
    service: Annotated[AgentService, Depends(get_agent_service)],
    payload: Annotated[RunSchema, Body(...)],
) -> JSONResponse:
    output: RunOutSchema = await service.run(payload=payload)
    return Success.ok(data=output).to_resp()
