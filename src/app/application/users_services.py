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
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def new_user(
        database: DatabaseGateway,
        uow: UoW,
        username: str,
) -> int:
    user = user_schemas.User(username=username)
    database.add_one(user)
    uow.commit()
    return user.id


def create_user(
        database: DatabaseGateway,
        uow: UoW,
        user: user_schemas.UserCreate,
):
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
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
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

