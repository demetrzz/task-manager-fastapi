from datetime import timedelta, datetime

from dishka import FromDishka
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from task_manager.application.protocols.database import DatabaseGateway
from task_manager.domain.schemas import user_schemas
from task_manager.main.config import Config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


async def create_access_token(user: user_schemas.UserInDB,
                              config: FromDishka[Config]):
    print(config)
    print("====================================")
    expire = datetime.utcnow() + timedelta(minutes=config.token_expires)  # 'function' object has no attribute
    # 'token_expires'
    to_encode = {"sub": user.username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.jwt_secret, algorithm=config.sha_algorithm)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


async def get_current_user(
    database: FromDishka[DatabaseGateway],
    config: FromDishka[Config]
) -> user_schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            str(oauth2_scheme), config.jwt_secret, algorithms=[config.sha_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await database.query_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    database: FromDishka[DatabaseGateway],
    config: FromDishka[Config]
) -> user_schemas.User:
    current_user = await get_current_user(database, config)
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user