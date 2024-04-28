from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from .dependencies import CoreProvider
from ..api import root_router


def create_app() -> FastAPI:
    app = FastAPI()
    container = make_async_container(CoreProvider())
    setup_dishka(container, app)
    app.include_router(root_router)
    return app
