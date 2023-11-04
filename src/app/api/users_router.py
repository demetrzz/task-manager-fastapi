from dataclasses import dataclass
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.schemas.user import Token, User
from app.application.users_services import new_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, get_current_active_user

users_router = APIRouter()


@dataclass
class SomeResult:
    user_id: int


@users_router.get("/")
def add_users(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> SomeResult:
    user_id = new_user(database, uow, "demetr", "demetr@email.com")
    return SomeResult(
        user_id=user_id,
    )


@users_router.post("/token", response_model=Token)
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        database: Annotated[DatabaseGateway, Depends()],
):
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/me/", response_model=User)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
