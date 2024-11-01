from dataclasses import dataclass
from datetime import datetime, timedelta

from redis.asyncio import Redis

from db.models.user import UserORM
from exeptions.match import LimitMatchExeption, MatchAlreadyExeption, MutuallyAlreadyException, MutuallySelfExeption
from exeptions.user import NotFoundUserExeption
from repositories.matсh import SQLMathcRepository
from repositories.user import SQLUserRepository
from services.email import EmailService



@dataclass
class LimitMatchService:
    redis: Redis

    async def get_or_create(self, user_id: int) -> int:
        current_limit = await self.redis.get(user_id)

        if current_limit is None:
            now = datetime.now()
            end_of_day = datetime.combine(now.date() + timedelta(days=1), datetime.min)
            expire_time = int((end_of_day - now).total_seconds())
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
    email_service: EmailService

    async def match(self, user_id: int, user: UserORM) -> str | None:
        if user_id == user.id:
            raise MutuallySelfExeption()

        count = await self.limit_service.get_or_create(user_id=user.id)
        
        if count > 10:
            raise LimitMatchExeption()

        await self.limit_service.incr_limit(user_id=user.id)

        user_two = await self.user_repository.get_by_id(user_id=user_id)

        if not user_two:
            raise NotFoundUserExeption(user_id=user_id)

        match = await self.mathc_repositpry.get_by_users(
            user_one_id=user_id,
            user_two_id=user.id
        )

        if match:
            if match.mutually:
                raise MutuallyAlreadyException()

            if match.user_two_id == user.id:
                await self.mathc_repositpry.mutually(match=match)

                await self.email_service.send_email(user_from=user, user_to=user_two)
                await self.email_service.send_email(user_from=user_two, user_to=user)
                return user_two.email
            raise MatchAlreadyExeption()

        await self.mathc_repositpry.create(
            user_one=user,
            user_two=user_two
        )
