from dataclasses import dataclass

from task_manager.application.protocols.database import DatabaseGateway, UoW
from task_manager.domain.services.to_do_test_users_services import UserService


@dataclass
class NewUserDTO:
    username: str
    hashed_password: str


class CreateUser:
    def __init__(
            self,
            database: DatabaseGateway,
            user_service: UserService,
            uow: UoW,
    ):
        self.database = database
        self.user_service = user_service
        self.uow = uow

    async def __call__(self, user: NewUserDTO) -> int:
        user = await self.user_service.create_user(user)

        await self.database.add_user(user)
        await self.uow.commit()
        return user.id
