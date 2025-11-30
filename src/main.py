import asyncio
from contextlib import asynccontextmanager

import uvloop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.client import init_hf_model
from src.core.common import get_app_version
from src.core.config import settings
from src.core.error import init_global_errors
from src.core.middleware import init_process_time_tracing
from src.data import init_db, run_migration
from src.route.health import router as _health_router
from src.route.image import router as _image_router


@asynccontextmanager
async def lifespan(fa: FastAPI):
    logger.info("lifespan(): starting up...")

    await run_migration()
    await init_hf_model()
    yield  # startup complete
    # any shutdown code here
    logger.info("lifespan(): shutting down...")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = FastAPI(
    title="Tensor App",
    version=get_app_version(),
    debug=settings.debug,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_global_errors(app)
init_db(app)
init_process_time_tracing(app)

routers = [
    _health_router,
    _image_router,
]
for router in routers:
    app.include_router(router)
