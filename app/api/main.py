from fastapi import APIRouter

from app.api.controllers import user_controller

api_router = APIRouter()

api_router.include_router(user_controller.router)

