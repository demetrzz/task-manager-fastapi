from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request

index_router = APIRouter(route_class=DishkaRoute)


@index_router.get("/")
async def index(
        request: Request,
) -> dict:
    return {}
