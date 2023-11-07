from fastapi import HTTPException

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.schemas.task_schemas import TaskAdd, TaskBase, TaskCompletion


def get_users_tasks(
        database: DatabaseGateway,
        user_id: int,
):
    tasks = database.get_tasks_by_user_id(user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="This user doesnt have any tasks")
    return list(map(TaskBase.model_validate, tasks))


def add_one_task(
        database: DatabaseGateway,
        uow: UoW,
        task: TaskAdd,
        user_id: int
) -> TaskBase:
    task = database.add_one_task(task, user_id)
    uow.commit()
    database.refresh_one(task)
    return task


def update_task(
        database: DatabaseGateway,
        uow: UoW,
        user_id: int,
        task_id: int,
        task: TaskCompletion
) -> TaskBase:
    db_task = database.query_task_by_id(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if user_id != db_task.author_id and user_id != db_task.assignee_id:
        raise HTTPException(status_code=400, detail="You are not author or assignee of this task")
    db_task.completed = task.completed
    uow.commit()
    database.refresh_one(db_task)
    return db_task
