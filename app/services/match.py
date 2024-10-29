from dataclasses import dataclass

from repositories.matсh import SQLMathcRepository
from services.user import UserService



@dataclass
class LimitMathService:
    async def get_or_create(self, user_id: int, expire_time) -> int:
        ...
    
    async def incr_limit(self, user_id) -> None:
        ...



@dataclass
class MatchService:
    user_service: UserService
    mathc_repositpry: SQLMathcRepository
    # limit_service: LimitMathService

    async def match(self, user_id: int, token: str) -> None:
        # count = await self.limit_service.get_or_create(user_id=user.id)
        # if count > 10:
        #     raise

        user = await self.user_service.get_current_user(token=token)
        match = await self.mathc_repositpry.get_by_users(
            user_one_id=user_id,
            user_two_id=user.id
        )

        if match:
            if match.user_two == user.id:
                await self.mathc_repositpry.mutually()
            raise


        await self.mathc_repositpry.create(
            user_one=user.id,
            user_two=user_id
        )
