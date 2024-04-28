from dishka import make_async_container, Scope
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from .auth_di import get_current_active_user
from .dependencies import CoreProvider
from ..api import root_router


def create_app() -> FastAPI:
    app = FastAPI()
    provider = CoreProvider()  # change after adding fastapi-user
    provider.provide(
        get_current_active_user, scope=Scope.REQUEST
    )  # change after adding fastapi-user
    container = make_async_container(provider)
    setup_dishka(container, app)
    app.include_router(root_router)
    return app
