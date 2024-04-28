from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from task_manager.application.protocols.database import DatabaseGateway, UoW
from task_manager.application.schemas.user_schemas import (
    Token,
    User,
    UserCreate,
)
from task_manager.application.users_services import (
    authenticate_user,
    create_user,
    InvalidCredentials,
)
from task_manager.main.auth_di import create_access_token

users_router = APIRouter(route_class=DishkaRoute)


@users_router.post("/registration")
async def registration(
    user: UserCreate,
    database: FromDishka[DatabaseGateway],
    uow: FromDishka[UoW],
) -> Token:
    try:
        user = await create_user(database, uow, user)
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Username already in use")
    return await create_access_token(user)


@users_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm, Depends()
    ],  # fix after adding fastapi-users
    database: FromDishka[DatabaseGateway],
) -> Token:
    try:
        print("here")
        user = await authenticate_user(
            database, form_data.username, form_data.password
        )
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await create_access_token(user)


@users_router.get("/me")
async def read_users_me(
    current_user: FromDishka[User],  # fix after adding fastapi-users
) -> User:
    return current_user
