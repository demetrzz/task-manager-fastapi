import os
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.application.protocols.database import DatabaseGateway
from app.application.schemas import user_schemas

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("JWT env variables are not correctly set")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


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
