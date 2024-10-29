from dataclasses import dataclass

from sqlalchemy import select


from db.database import Database
from db.models.user import UserORM



@dataclass
class SQLUserRepository:
    database: Database

    async def create(self, user: UserORM) -> None:
        async with self.database.get_session() as session:
            session.add(user)

    async def check_exsist_email(self, email: str) -> bool:
        stmt = select(UserORM).where(UserORM.email == email).limit(1)

        async with self.database.get_read_only_session() as session:
            user_dto = await session.scalar(stmt)
            if not user_dto:
                return False
        return True
            