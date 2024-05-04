from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from task_manager.main.di_provider import CoreProvider
# from .to_do_ioc import IoC
from task_manager.api import root_router
#from ..application.protocols.to_do_interactor_factory import InteractorFactory


def create_app() -> FastAPI:
    app = FastAPI()
    provider = CoreProvider()  # change after adding fastapi-user
    # provider.provide(IoC, scope=Scope.REQUEST, provides=InteractorFactory)
    container = make_async_container(provider)
    setup_dishka(container, app)
    app.include_router(root_router)
    return app
