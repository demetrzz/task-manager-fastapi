from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.schemas import User
from app.application.schemas.task_schemas import TaskSchemaAdd
from app.application.tasks_services import add_one_task
from app.application.users_services import get_current_active_user

tasks_router = APIRouter()


# @tasks_router.get("/tasks")
# def get_tasks(
#         database: Annotated[DatabaseGateway, Depends()],
#         uow: Annotated[UoW, Depends()],
#         current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     tasks = get_users_tasks(database, uow, current_user.username)
#     return tasks


@tasks_router.post("")
def add_task(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
        task: TaskSchemaAdd,
        current_user: Annotated[User, Depends(get_current_active_user)]

):
    task = add_one_task(database, uow, task, current_user.id)
    return {"task": task}
#
#
# @tasks_router.patch("/{id}")
# async def edit_task(
#     id: int,
#     task: TaskSchemaEdit,
#     uow: UOWDep,
# ):
#     await TasksService().edit_task(uow, id, task)
#     return {"ok": True}
