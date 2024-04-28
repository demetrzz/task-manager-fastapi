import os
from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from task_manager.adapters.sqlalchemy_db.gateway import SqlaGateway
from task_manager.application.protocols.database import DatabaseGateway, UoW


class CoreProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def create_async_session_maker(self) -> async_sessionmaker:
        db_uri = os.getenv("DB_URI")
        if not db_uri:
            raise ValueError("DB_URI env variable is not set")

        engine = create_async_engine(
            db_uri,
            echo=True,
            pool_size=15,
            max_overflow=15,
            connect_args={
                "connect_timeout": 5,
            },
        )
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False
        )

    @provide()
    async def new_async_session(
            self,
            async_session_maker: async_sessionmaker,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide()
    async def new_gateway(self, session: AsyncSession) -> DatabaseGateway:
        return SqlaGateway(session=session)

    @provide()
    async def new_uow(self, session: AsyncSession) -> UoW:
        return session
