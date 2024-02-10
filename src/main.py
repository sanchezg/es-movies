from fastapi import FastAPI

from src.application.controllers import router
from src.container import Container


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(router)
    return app


app = create_app()
