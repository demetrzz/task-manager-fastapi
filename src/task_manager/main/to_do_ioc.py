from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.adapters.sqlalchemy_db.gateway import SqlaGateway
from task_manager.application.protocols.database import UoW, DatabaseGateway
from task_manager.application.to_do_create_user import CreateUser
from task_manager.domain.services.to_do_test_users_services import UserService


class IoC:
    def __init__(self, session: AsyncSession):
        self.gateway: DatabaseGateway = SqlaGateway(session)
        self.uow: UoW = session

    @asynccontextmanager
    async def create_task(
            self
    ) -> CreateUser:
        yield CreateUser(
            database=self.gateway,
            uow=self.uow,
            user_service=UserService(),
        )
