import os

from fastapi.security import OAuth2PasswordBearer

from .protocols.database import DatabaseGateway, UoW
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from .schemas import user_schemas
from ..adapters.sqlalchemy_db import models

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def create_user(
        database: DatabaseGateway,
        uow: UoW,
        user: user_schemas.UserCreate,
):
    db_user = database.query_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already in use")
    user = models.User(
        username=user.username, hashed_password=pwd_context.hash(user.hashed_password)
    )
    database.add_one(user)
    uow.commit()
    database.refresh_one(user)
    return user


def authenticate_user(
        database: DatabaseGateway,
        username: str,
        password: str
):
    user = database.query_user_by_username(username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(user: user_schemas.UserInDB):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        database: Annotated[DatabaseGateway, Depends()],
) -> user_schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = database.query_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[user_schemas.User, Depends(get_current_user)]
) -> user_schemas.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

