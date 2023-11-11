from app.application.exceptions import InvalidTask, NoPermission
from app.application.protocols.database import DatabaseGateway, UoW
from app.application.schemas.task_schemas import TaskAdd, TaskBase, TaskCompletion


def get_users_tasks(
        database: DatabaseGateway,
        user_id: int,
):
    tasks = database.get_tasks_by_user_id(user_id)
    if not tasks:
        raise InvalidTask
    return list(map(TaskBase.model_validate, tasks))


def add_one_task(
        database: DatabaseGateway,
        uow: UoW,
        task: TaskAdd,
        user_id: int
) -> TaskBase:
    task = database.add_one_task(task, user_id)
    uow.commit()
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
        raise InvalidTask
    if user_id != db_task.author_id and user_id != db_task.assignee_id:
        raise NoPermission
    db_task.completed = task.completed
    uow.commit()
    return db_task
