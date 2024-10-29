
from dataclasses import dataclass

from fastapi import Depends, UploadFile

from api.users.schemas import UserCreateSchema
from repositories.user import SQLUserRepository
from services.auth.security import create_access_token, hash_password, oauth2_scheme, verify_password, verify_token
from services.photo import add_watermark, save_avatar


@dataclass
class UserService:
    user_repository: SQLUserRepository

    async def create_user(self, user_schema: UserCreateSchema, avatar_file: UploadFile | None = None) -> None:
        if await self.user_repository.check_exsist_email(email=user_schema.email):
            raise

        password = hash_password(password=user_schema.password)

        user = user_schema.to_ormModel(password=password)
        await self.user_repository.create(user=user)

        if avatar_file:
            avatar = await add_watermark(avatar_file=avatar_file)
            await save_avatar(email=user_schema.email, avatar=avatar)

    async def get_all(self, filters: dict[str, str], order_by: str):
        users = await self.user_repository.get_list(
            filters=filters,
            orber_by=order_by
            )
        return users

    async def get_current_user(self, token: str=Depends(oauth2_scheme)):
        payload = verify_token(token=token)
        user_id: str = payload.get("id")

        user = await self.user_repository.get_by_id(user_id=user_id)
        if user: return user
        return None
    
    async def login(self, email: str, password: str) -> dict[str, str]:
        user = await self.user_repository.get_by_email(email=email)

        if verify_password(password, user.password_hash):
            accses_token = create_access_token(
                data={
                    'id': user.id,
                    "email": user.email
                }
            )
            return {'access_token': accses_token, "token_type": "access"}