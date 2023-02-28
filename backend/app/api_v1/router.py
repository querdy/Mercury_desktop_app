from fastapi import APIRouter

from app.api_v1.endpoints import research, user

api_router = APIRouter()
api_router.include_router(research.router)
api_router.include_router(user.router)
