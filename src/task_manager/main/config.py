import os
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

DB_URI = "DB_URI"
SECRET_KEY = "SECRET_KEY"
ALGORITHM = "ALGORITHM"
ACCESS_TOKEN_EXPIRES = "ACCESS_TOKEN_EXPIRE_MINUTES"


class ConfigParseError(ValueError):
    pass


@dataclass
class Config:
    db_uri: str
    jwt_secret: str
    sha_algorithm: str
    token_expires: int


def get_str_env(key) -> str:
    val = os.getenv(key)
    if not val:
        logger.error("%s is not set", key)
        raise ConfigParseError(f"{key} is not set")
    return val


def load_config() -> Config:
    db_uri = get_str_env(DB_URI)
    jwt_secret = get_str_env(SECRET_KEY)
    sha_algorithm = get_str_env(ALGORITHM)
    token_expires = int(get_str_env(ACCESS_TOKEN_EXPIRES))
    return Config(
        db_uri=db_uri,
        jwt_secret=jwt_secret,
        sha_algorithm=sha_algorithm,
        token_expires=token_expires
    )
