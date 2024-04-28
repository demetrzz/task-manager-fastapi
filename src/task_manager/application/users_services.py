from .exceptions import InvalidCredentials
from .protocols.database import DatabaseGateway, UoW
from passlib.context import CryptContext
from .schemas import user_schemas
from ..adapters.sqlalchemy_db import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(
        database: DatabaseGateway,
        uow: UoW,
        user: user_schemas.UserCreate,
):
    db_user = await database.query_user_by_username(user.username)
    if db_user:
        raise InvalidCredentials
    user = models.User(
        username=user.username, hashed_password=pwd_context.hash(user.hashed_password)
    )
    await database.add_user(user)
    await uow.commit()
    return user


async def authenticate_user(
        database: DatabaseGateway,
        username: str,
        password: str
):
    user = await database.query_user_by_username(username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise InvalidCredentials
    return user
