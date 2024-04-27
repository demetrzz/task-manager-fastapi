from fastapi import APIRouter, Request

index_router = APIRouter()


@index_router.get("/")
async def index(
        request: Request,
) -> dict:
    return {}
