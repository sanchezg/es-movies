from logging import getLogger, config
from fastapi import FastAPI

from src.application.controllers import router
from src.container import Container
from .settings import LOGGING_CONFIG


config.dictConfig(LOGGING_CONFIG)
logger = getLogger("default")

def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(router)
    return app


app = create_app()

@app.middleware("http")
async def logger_middleware(request, call_next):
    logger.debug(f"Request: {request.url} | Method: {request.method} | Path: {request.url.path} | Query: {request.query_params} | Body: {await request.body()}")
    response = await call_next(request)
    logger.debug(f"Response: {response.status_code}")
    return response
