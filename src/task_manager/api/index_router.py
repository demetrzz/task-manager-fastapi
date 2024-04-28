from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request

from task_manager.application.protocols.database import DatabaseGateway, UoW

index_router = APIRouter(route_class=DishkaRoute)


@index_router.get("/")
async def index(
    request: Request,
    database: FromDishka[DatabaseGateway],
    uow: FromDishka[UoW],
) -> dict:
    return {}
