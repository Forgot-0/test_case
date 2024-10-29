
from dataclasses import dataclass

from fastapi import UploadFile

from api.users.schemas import UserCreateSchema
from repositories.user import SQLUserRepository
from services.auth.security import hash_password
from services.photo import add_watermark, save_avatar


@dataclass
class UserService:
    user_repository: SQLUserRepository

    async def create_user(self, user_schema: UserCreateSchema, avatar_file: UploadFile | None = None) -> None:
        if await self.user_repository.check_exsist_email(email=user_schema.email):
            raise

        password = hash_password(password=user_schema.password)

        user = user_schema.to_userOrmModel(password=password)
        await self.user_repository.create(user=user)

        if avatar_file:
            avatar = await add_watermark(avatar_file=avatar_file)
            await save_avatar(email=user_schema.email, avatar=avatar)
