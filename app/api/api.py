from fastapi import APIRouter
from app.api.endpoints import user
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(user.router, tags=['demo'], prefix=settings.API_PREFIX)


