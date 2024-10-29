from dataclasses import dataclass

from sqlalchemy import select

from db.database import Database
from db.models.matсh import MatchORM


@dataclass
class SQLMathcRepository:
    database: Database

    async def create(self, match: MatchORM) -> None:
        async with self.database.get_session() as session:
            session.add(match)

    async def get_by_user_one(self, user_id: int) -> MatchORM | None:
        query = select(MatchORM).where(MatchORM.user_one == user_id).limit(1)
        async with self.database.get_read_only_session() as session:
            match = await session.scalar(query)
            if match:
                return match

    async def set_user_two(self, match: MatchORM, user_id: int) -> None:
        match.user_two = user_id

        async with self.database.get_session() as session:
            session.add(match)