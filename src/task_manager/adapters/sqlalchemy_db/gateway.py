from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.adapters.sqlalchemy_db import models
from task_manager.application.schemas import task_schemas
from task_manager.application.protocols.database import DatabaseGateway
from task_manager.application.schemas.user_schemas import UserInDB


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user):
        self.session.add(user)
        return

    async def query_user_by_username(self, username: str) -> UserInDB | None:
        result = await self.session.execute(
            select(models.User).where(models.User.username == username)
        )
        return result.scalars().first()

    async def add_one_task(self, task: task_schemas.TaskAdd, user_id: int):
        task = models.Task(**task.model_dump(), author_id=user_id)
        self.session.add(task)
        return task

    async def get_tasks_by_user_id(self, user_id: int):
        result = await self.session.execute(
            select(models.Task).where(models.Task.assignee_id == user_id)
        )
        return result.scalars().all()

    async def query_task_by_id(self, task_id):
        result = await self.session.execute(
            select(models.Task).where(models.Task.id == task_id)
        )
        return result.scalars().first()
