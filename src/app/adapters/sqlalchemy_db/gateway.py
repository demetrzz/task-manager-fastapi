from sqlalchemy.orm import Session

from app.adapters.sqlalchemy_db import models
from app.application.schemas import User
from app.application.protocols.database import DatabaseGateway
from app.application.schemas.user import UserInDB


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, user: User) -> None:
        self.session.add(user)
        return

    def query_user_by_username(self, username: str) -> UserInDB:
        return self.session.query(models.User).get(models.User.username == username).first()
