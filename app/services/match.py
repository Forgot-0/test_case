from dataclasses import dataclass

from redis.asyncio import Redis

from db.models.user import UserORM
from repositories.matсh import SQLMathcRepository
from repositories.user import SQLUserRepository



@dataclass
class LimitMatchService:
    redis: Redis

    async def get_or_create(self, user_id: int, expire_time: int=3600) -> int:
        current_limit = await self.redis.get(user_id)

        if current_limit is None:
            await self.redis.set(user_id, 1, ex=expire_time)
            return 1

        return int(current_limit)

    async def incr_limit(self, user_id) -> None:
        await self.redis.incrby(user_id)


@dataclass
class MatchService:
    user_repository: SQLUserRepository
    mathc_repositpry: SQLMathcRepository
    limit_service: LimitMatchService

    async def match(self, user_id: int, user: UserORM) -> None:
        if user_id == user.id:
            raise

        count = await self.limit_service.get_or_create(user_id=user.id)
        
        if count > 10:
            raise
        await self.limit_service.incr_limit(user_id=user.id)

        user_two = await self.user_repository.get_by_id(user_id=user_id)

        match = await self.mathc_repositpry.get_by_users(
            user_one_id=user_id,
            user_two_id=user.id
        )

        if match:
            if match.mutually:
                raise

            if match.user_two_id == user.id:
                await self.mathc_repositpry.mutually(match=match)
                return
            raise

        await self.mathc_repositpry.create(
            user_one=user,
            user_two=user_two
        )
