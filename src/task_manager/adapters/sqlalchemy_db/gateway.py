from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.adapters.sqlalchemy_db import models
from task_manager.application.schemas import task_schemas
from task_manager.application.protocols.database import DatabaseGateway
from task_manager.application.schemas.user_schemas import UserInDB


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user):
        await self.session.add(user)
        return

    async def query_user_by_username(self, username: str) -> UserInDB | None:
        return await self.session.query(models.User).filter(models.User.username == username).first()

    async def add_one_task(self, task: task_schemas.TaskAdd, user_id: int):
        task = models.Task(**task.model_dump(), author_id=user_id)
        await self.session.add(task)
        return task

    async def get_tasks_by_user_id(self, user_id: int):
        return await self.session.query(models.Task).filter(models.Task.assignee_id == user_id)

    async def query_task_by_id(self, task_id):
        return await self.session.query(models.Task).get(task_id)
