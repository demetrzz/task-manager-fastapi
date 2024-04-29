from collections.abc import AsyncGenerator
from typing import cast

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession, async_sessionmaker,
)

from task_manager.adapters.sqlalchemy_db.gateway import SqlaGateway
from task_manager.application.protocols.database import DatabaseGateway, UoW
from task_manager.main.config import Config, load_config


class CoreProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=scope.APP)
    async def provide_config(self) -> Config:
        # config = await load_config()
        # config_provider = cast(Config, ConfigProvider(
        #     db_uri=config.db_uri,
        #     jwt_secret=config.jwt_secret,
        #     sha_algorithm=config.sha_algorithm,
        #     token_expires=config.token_expires
        # ))
        # return config_provider
        return cast(Config, load_config)

    @provide(scope=Scope.APP)
    async def create_async_session_maker(self) -> async_sessionmaker:
        config = await load_config()
        engine = create_async_engine(
            config.db_uri,
            echo=True,
            pool_size=15,
            max_overflow=15,
            connect_args={
                "command_timeout": 5,
            },
        )
        return async_sessionmaker(
            engine, autoflush=False, expire_on_commit=False
        )

    @provide()
    async def new_async_session(
            self,
            async_session_maker: async_sessionmaker,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide(provides=DatabaseGateway)
    async def new_gateway(self, session: AsyncSession) -> DatabaseGateway:
        yield SqlaGateway(session)

    @provide()
    async def new_uow(self, session: AsyncSession) -> UoW:
        return session
