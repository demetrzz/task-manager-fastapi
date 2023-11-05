from sqlalchemy.orm import Session

from app.adapters.sqlalchemy_db import models
from app.application.schemas import user_schemas
from app.application.protocols.database import DatabaseGateway
from app.application.schemas.user_schemas import UserInDB


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, user: user_schemas.User) -> None:
        self.session.add(user)
        return

    def refresh_user(self, user):
        self.session.refresh(user)
        return user

    def query_user_by_username(self, username: str) -> UserInDB | None:
        return self.session.query(models.User).filter(models.User.username == username).first()
