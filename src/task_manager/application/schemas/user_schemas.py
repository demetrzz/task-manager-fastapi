from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
