from .exceptions import InvalidCredentials
from .protocols.database import DatabaseGateway, UoW
from passlib.context import CryptContext
from .schemas import user_schemas
from ..adapters.sqlalchemy_db import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(
        database: DatabaseGateway,
        uow: UoW,
        user: user_schemas.UserCreate,
):
    db_user = database.query_user_by_username(user.username)
    if db_user:
        raise InvalidCredentials
    user = models.User(
        username=user.username, hashed_password=pwd_context.hash(user.hashed_password)
    )
    database.add_user(user)
    uow.commit()
    return user


def authenticate_user(
        database: DatabaseGateway,
        username: str,
        password: str
):
    user = database.query_user_by_username(username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise InvalidCredentials
    return user
