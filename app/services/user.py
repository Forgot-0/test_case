
from dataclasses import dataclass
import json
from typing import Any

from fastapi import UploadFile
from redis.asyncio import Redis

from api.users.schemas import UserCreateInSchema
from db.models.user import UserORM
from exeptions.user import EmailAlreadyExistExeption, WrongPasswordExeption
from repositories.user import SQLUserRepository
from services.auth.security import create_access_token, hash_password, verify_password
from services.photo import save_avatar



@dataclass
class CacheUserService:
    redis: Redis

    async def get_cached_data(self, key: str) -> Any:
        data = await self.redis.get(key)
        if data is not None:
            return json.loads(data)
        return None

    async def set_cache_data(self, key: str, data: Any, expire: int = 3600):
        await self.redis.set(key, json.dumps(data), ex=expire)

    @staticmethod
    def convert_userOrm_to_dict(user: UserORM) -> dict[str, str]:
        return {
            'email': user.email,
            'gender': user.gender.value,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.avatar,
            'created_at': user.created_at.isoformat()
        }


@dataclass
class UserService:
    user_repository: SQLUserRepository
    cache_srvice: CacheUserService

    async def create_user(self, user_schema: UserCreateInSchema, avatar_file: UploadFile) -> None:
        if await self.user_repository.check_exsist_email(email=user_schema.email):
            raise EmailAlreadyExistExeption(email=user_schema.email)

        password = hash_password(password=user_schema.password)

        user = user_schema.to_ormModel(password=password)
        user.avatar=f'avatars/{user.email}'
        await self.user_repository.create(user=user)

        if avatar_file:
            await save_avatar(email=user_schema.email, avatar_file=avatar_file)

    async def get_all(self, user: UserORM, filters: dict[str, str], order_by: str) -> dict[str, str] | str:
        key = f'{user.location.data}_{filters}_{order_by}'
        
        
        cache_data = await self.cache_srvice.get_cached_data(key=key)

        if cache_data:
            return cache_data

        users = await self.user_repository.get_list(
            user=user,
            filters=filters,
            orber_by=order_by,
            )

        data = [CacheUserService.convert_userOrm_to_dict(user) for user in users]
        await self.cache_srvice.set_cache_data(key=key, data=data)

        return data

    async def login(self, email: str, password: str) -> dict[str, str]:
        user = await self.user_repository.get_by_email(email=email)
        if verify_password(password, user.password_hash):
            accses_token = create_access_token(
                data={
                    'id': user.id,
                    "email": user.email
                }
            )
            return {'access_token': accses_token, "token_type": "bearer"}
        raise WrongPasswordExeption()