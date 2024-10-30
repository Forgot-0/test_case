from fastapi import APIRouter, Body, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from punq import Container

from api.users.schemas import ListUsersOutShema, TokenOutSchema, UserCreateInSchema, UserFilters, UserOrder, UserOutShema
from container.init_containeer import init_container
from services.match import MatchService
from services.user import UserService
from services.auth.security import get_current_user


router = APIRouter()


@router.post("/clients/create/", response_model=None)
async def create_user(
    user_schema: UserCreateInSchema=Body(...),
    avatar:UploadFile=File(...),
    container: Container=Depends(init_container)
) -> None:
    user_service: UserService = container.resolve(UserService)
    await user_service.create_user(
        user_schema=user_schema,
        avatar_file=avatar
    )

@router.get("/list", response_model=ListUsersOutShema | str)
async def get_users(
    filters: UserFilters=Depends(UserFilters),
    order_by: UserOrder=Depends(UserOrder),
    user=Depends(get_current_user),
    container: Container=Depends(init_container)
) -> ListUsersOutShema | str:
    user_service: UserService = container.resolve(UserService)

    user_list = await user_service.get_all(
        user=await user,
        filters=filters.model_dump(), 
        order_by=order_by.order_by,
    )

    if isinstance(user_list, str): return user_list
    return ListUsersOutShema(
        users=[UserOutShema(**user) for user in user_list]
    )

@router.post('/login', response_model=TokenOutSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    container: Container=Depends(init_container)
) -> TokenOutSchema:
    user_service: UserService = container.resolve(UserService)
    data = await user_service.login(
        email=form_data.username,
        password=form_data.password,
    )
    return TokenOutSchema(**data)


@router.post('/clients/{id}/match/')
async def match(
    id: int,
    user=Depends(get_current_user),
    container: Container=Depends(init_container)
) -> str | None:
    match_service: MatchService = container.resolve(MatchService)
    email = await match_service.match(user_id=id, user=await user)
    if email: return email