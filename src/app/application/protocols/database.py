from abc import ABC, abstractmethod

from app.application.schemas.user_schemas import UserInDB


class UoW(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError


class DatabaseGateway(ABC):
    @abstractmethod
    def add_one(self, one) -> None:
        raise NotImplementedError

    @abstractmethod
    def refresh_one(self, one):
        raise NotImplementedError

    @abstractmethod
    def query_user_by_username(self, username: str) -> UserInDB | None:
        raise NotImplementedError

    @abstractmethod
    def add_one_task(self, task, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_tasks_by_user_id(self, user_id):
        raise NotImplementedError

    @abstractmethod
    def query_task_by_id(self, task_id):
        raise NotImplementedError
