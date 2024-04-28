from abc import ABC, abstractmethod

from task_manager.application.schemas.user_schemas import UserInDB


class UoW(ABC):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def flush(self):
        raise NotImplementedError


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
