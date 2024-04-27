from sqlalchemy.orm import Session

from task_manager.adapters.sqlalchemy_db import models
from task_manager.application.schemas import task_schemas
from task_manager.application.protocols.database import DatabaseGateway
from task_manager.application.schemas.user_schemas import UserInDB


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, user):
        self.session.add(user)
        return

    def query_user_by_username(self, username: str) -> UserInDB | None:
        return self.session.query(models.User).filter(models.User.username == username).first()

    def add_one_task(self, task: task_schemas.TaskAdd, user_id: int):
        task = models.Task(**task.model_dump(), author_id=user_id)
        self.session.add(task)
        return task

    def get_tasks_by_user_id(self, user_id: int):
        return self.session.query(models.Task).filter(models.Task.assignee_id == user_id)

    def query_task_by_id(self, task_id):
        return self.session.query(models.Task).get(task_id)
