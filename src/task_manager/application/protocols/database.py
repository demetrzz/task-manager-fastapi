from abc import ABC, abstractmethod
from typing import Protocol

from task_manager.domain.schemas.user_schemas import UserInDB


class UoW(Protocol):
    async def commit(self):
        pass

    async def flush(self):
        pass


class DatabaseGateway(ABC):
    @abstractmethod
    async def add_user(self, user):
        raise NotImplementedError

    @abstractmethod
    async def query_user_by_username(self, username: str) -> UserInDB | None:
        raise NotImplementedError

    @abstractmethod
    async def add_one_task(self, task, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_by_user_id(self, user_id):
        raise NotImplementedError

    @abstractmethod
    async def query_task_by_id(self, task_id):
        raise NotImplementedError
