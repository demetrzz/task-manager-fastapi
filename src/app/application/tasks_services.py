from app.application.protocols.database import DatabaseGateway, UoW
from app.application.schemas.task_schemas import TaskSchemaAdd


# def get_users_tasks(
#         database: DatabaseGateway,
#         uow: UoW,
#         username: str,
# ):
#     tasks = database.get_tasks_by_username(username)


def add_one_task(
        database: DatabaseGateway,
        uow: UoW,
        task: TaskSchemaAdd,
        user_id: int
):
    task = database.add_one_task(task, user_id)
    uow.commit()
    database.refresh_one(task)
    return task
