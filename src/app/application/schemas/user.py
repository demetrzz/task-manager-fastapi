from dataclasses import dataclass, field


@dataclass
class User:
    id: int = field(init=False)
    username: str
    email: str
    is_active: bool = field(default=True, init=False)


@dataclass
class UserInDB(User):
    hashed_password: str


@dataclass
class Token:
    access_token: str
    token_type: str


@dataclass
class TokenData:
    username: str
