from dataclasses import dataclass

from sqlalchemy import select

from db.database import Database
from db.models.matсh import MatchORM
from db.models.user import UserORM


@dataclass
class SQLMathcRepository:
    database: Database

    async def create(self, user_one: UserORM, user_two: UserORM) -> None:
        match = MatchORM(
            user_one=user_one,
            user_two=user_two
        )
        async with self.database.get_session() as session:
            session.add(match)

    async def get_by_users(self, user_one_id: int, user_two_id: int) -> MatchORM | None:
        query_one = select(MatchORM).where(
            MatchORM.user_one_id == user_one_id, MatchORM.user_two_id == user_two_id).limit(1)

        query_two = select(MatchORM).where(
            MatchORM.user_two_id == user_two_id, MatchORM.user_two_id == user_one_id).limit(1)

        async with self.database.get_read_only_session() as session:
            match = await session.scalar(query_one)
            if match:
                return match

            match = await session.scalar(query_two)
            if match:
                return match

    async def mutually(self, match: MatchORM) -> None:
        match.mutually = True
        async with self.database.get_session() as session:
            session.add(match)