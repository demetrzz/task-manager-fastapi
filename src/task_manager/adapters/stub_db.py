from task_manager.application.schemas import User
from task_manager.application.protocols.database import DatabaseGateway
from task_manager.application.schemas.user_schemas import UserInDB


class StubDatabaseGateway(DatabaseGateway):
    def add_one_task(self, task, user_id: int):
        pass

    def get_tasks_by_user_id(self, user_id):
        pass

    def query_task_by_id(self, task_id):
        pass

    def query_user_by_username(self, username: str) -> UserInDB | None:
        pass

    def add_user(self, user: User) -> None:
        pass
