from fastapi import APIRouter, Body, Depends, File, Form, Query, UploadFile
from punq import Container

from api.users.schemas import ListUsersShema, UserCreateSchema, UserFilters, UserOrder, UserShema
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


@router.get("/list", response_model=ListUsersShema)
async def get_users(
    filters: UserFilters=Depends(UserFilters),
    order_by: UserOrder=Depends(UserOrder),
    container: Container=Depends(init_container)
    ) -> ListUsersShema:
    user_service: UserService = container.resolve(UserService)
    user_list = await user_service.get_all(filters=filters, order_by=order_by)
    return ListUsersShema(
        users=[UserShema.from_ormModel(user) for user in user_list]
    )