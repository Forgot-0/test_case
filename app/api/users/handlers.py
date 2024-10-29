from fastapi import APIRouter, Body, Depends, File, Form, UploadFile
from punq import Container

from api.users.schemas import UserCreateSchema
from container.init_containeer import init_container
from services.user import UserService


router = APIRouter()


@router.post("/clients/create/", response_model=None)
async def create_user(
    user_schema: UserCreateSchema=Body(...),
    avatar:UploadFile=File(...),
    container: Container=Depends(init_container)
    ) -> None:
    user_service: UserService = container.resolve(UserService)
    await user_service.create_user(
        user_schema=user_schema,
        avatar_file=avatar
    )