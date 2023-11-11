from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.schemas import User
from app.application.schemas.task_schemas import TaskAdd, TaskCompletion, TaskBase
from app.application.tasks_services import add_one_task, get_users_tasks, update_task
from app.main.auth_di import get_current_active_user

tasks_router = APIRouter()


@tasks_router.get("")
def get_tasks(
        database: Annotated[DatabaseGateway, Depends()],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return get_users_tasks(database, current_user.id)


@tasks_router.post("")
def add_task(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        task: TaskAdd,
        current_user: Annotated[User, Depends(get_current_active_user)]

) -> TaskBase:
    return add_one_task(database, uow, task, current_user.id)


@tasks_router.patch("/{id}")
def edit_task_completion(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        current_user: Annotated[User, Depends(get_current_active_user)],
        id: int,
        task: TaskCompletion,

) -> TaskBase:
    return update_task(database, uow, current_user.id, id, task)
