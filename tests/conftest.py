from unittest.mock import Mock

from _pytest.fixtures import fixture
from fastapi import FastAPI
from fastapi.testclient import TestClient
from passlib.context import CryptContext

from app.application.protocols.database import UoW, DatabaseGateway
from app.application.schemas import User, task_schemas
from app.application.schemas.user_schemas import UserInDB
from app.main import init_routers
from app.main.auth_di import get_current_active_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TEST_USER = User(id=1, username="testuser", is_active=True)
TEST_USERINDB = UserInDB(id=1, username="testuser", hashed_password=pwd_context.hash("testpassword"), is_active=True)


class MockDatabase(DatabaseGateway):
    def add_user(self, user) -> None:
        pass

    def query_user_by_username(self, username: str) -> UserInDB | None:
        pass

    def add_one_task(self, task: task_schemas.TaskAdd, user_id: int):
        pass

    def get_tasks_by_user_id(self, user_id: int):
        pass

    def query_task_by_id(self, task_id):
        pass


class MockDBForRegistration(MockDatabase):
    def query_user_by_username(self, username: str) -> UserInDB | None:
        return None


class MockDBForToken(MockDatabase):
    def query_user_by_username(self, username: str) -> UserInDB | None:
        return TEST_USERINDB


@fixture
def mock_uow() -> UoW:
    uow = Mock()
    uow.commit = Mock()
    uow.flush = Mock()
    return uow


@fixture
def mock_auth() -> User:
    return TEST_USER


@fixture(params=[MockDatabase, MockDBForRegistration, MockDBForToken])
def mock_database(request):
    return request.param()


@fixture
def client(mock_uow, mock_database, mock_auth):
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[DatabaseGateway] = mock_database
    app.dependency_overrides[UoW] = lambda: mock_uow
    app.dependency_overrides[get_current_active_user] = lambda: mock_auth
    return TestClient(app)
