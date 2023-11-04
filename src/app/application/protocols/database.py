from abc import ABC, abstractmethod

from app.application.schemas import User
from app.application.schemas.user import UserInDB


class UoW(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError


class DatabaseGateway(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def query_user_by_username(self, username: str) -> UserInDB:
        raise NotImplementedError
