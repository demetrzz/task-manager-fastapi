from fastapi import APIRouter

from .index_router import index_router
from .tasks_router import tasks_router
from .users_router import users_router

root_router = APIRouter()
root_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)
root_router.include_router(
    tasks_router,
    prefix="/tasks",
    tags=["Tasks"],
)
root_router.include_router(
    index_router,
)
