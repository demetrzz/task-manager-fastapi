from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession, async_sessionmaker,
)

from task_manager.adapters.sqlalchemy_db.gateway import SqlaGateway
from task_manager.application.protocols.database import DatabaseGateway, UoW
from task_manager.domain.models import User
from task_manager.main.config import load_config


async def create_async_session_maker() -> async_sessionmaker[AsyncSession]:
    config = load_config()
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


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = await create_async_session_maker()
    async with session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class CoreProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    async def provide_async_session(
            self
    ) -> AsyncGenerator[AsyncSession, None]:
        yield get_async_session()

    @provide()
    async def new_gateway(self, session: AsyncSession) -> DatabaseGateway:
        yield SqlaGateway(session)

    @provide()
    async def new_uow(self, session: AsyncSession) -> UoW:
        return session
