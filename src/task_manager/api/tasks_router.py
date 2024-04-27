from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from task_manager.application.protocols.database import DatabaseGateway, UoW
from task_manager.application.schemas import User
from task_manager.application.schemas.task_schemas import TaskAdd, TaskCompletion, TaskBase
from task_manager.application.tasks_services import add_one_task, get_users_tasks, update_task, InvalidTask, NoPermission
from task_manager.main.auth_di import get_current_active_user

tasks_router = APIRouter()


@tasks_router.get("")
async def get_tasks(
        database: Annotated[DatabaseGateway, Depends()],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        tasks = get_users_tasks(database, current_user.id)
    except InvalidTask:
        raise HTTPException(status_code=404, detail="This user doesnt have any tasks")
    return tasks


@tasks_router.post("")
async def add_task(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        task: TaskAdd,
        current_user: Annotated[User, Depends(get_current_active_user)]

) -> TaskBase:
    return add_one_task(database, uow, task, current_user.id)


@tasks_router.patch("/{id}")
async def edit_task_completion(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        current_user: Annotated[User, Depends(get_current_active_user)],
        id: int,
        task: TaskCompletion,

) -> TaskBase:
    try:
        task = update_task(database, uow, current_user.id, id, task)
    except InvalidTask:
        raise HTTPException(status_code=404, detail="Task not found")
    except NoPermission:
        raise HTTPException(status_code=400, detail="You are not author or assignee of this task")
    return task
