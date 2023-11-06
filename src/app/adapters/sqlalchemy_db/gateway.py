from sqlalchemy.orm import Session

from app.adapters.sqlalchemy_db import models
from app.application.schemas import user_schemas, task_schemas
from app.application.protocols.database import DatabaseGateway
from app.application.schemas.user_schemas import UserInDB


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_one(self, one) -> None:
        self.session.add(one)
        return

    def refresh_one(self, one):
        self.session.refresh(one)
        return one

    def query_user_by_username(self, username: str) -> UserInDB | None:
        return self.session.query(models.User).filter(models.User.username == username).first()

    def add_one_task(self, task: task_schemas.TaskSchemaAdd, id: int):
        print(task)
        task = models.Task(**task.model_dump(), author_id=id)
        self.session.add(task)
        return
