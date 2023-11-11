from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.application.protocols.database import DatabaseGateway, UoW
from app.application.schemas.user_schemas import Token, User, UserCreate
from app.application.users_services import authenticate_user, create_user, InvalidCredentials
from app.main.auth_di import create_access_token, get_current_active_user

users_router = APIRouter()


@users_router.post("/registration")
def registration(
        user: UserCreate,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> Token:
    try:
        user = create_user(database, uow, user)
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Username already in use")
    return create_access_token(user)


@users_router.post("/token")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        database: Annotated[DatabaseGateway, Depends()],
) -> Token:
    try:
        user = authenticate_user(database, form_data.username, form_data.password)
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token(user)


@users_router.get("/me")
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    return current_user
