from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from task_manager.application.protocols.to_do_interactor_factory import InteractorFactory
from task_manager.application.to_do_create_user import NewUserDTO

to_do_users_router = APIRouter(route_class=DishkaRoute)


@to_do_users_router.post("/add_task")
async def create_task(
        ioc: FromDishka[InteractorFactory],
        data: NewUserDTO,
) -> int:
    async with ioc.create_user() as create_user_interactor:
        return await create_user_interactor(data)
