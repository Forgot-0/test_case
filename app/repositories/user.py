from dataclasses import dataclass

from sqlalchemy import func, select


from db.database import Database
from db.models.user import UserORM



@dataclass
class SQLUserRepository:
    database: Database

    async def create(self, user: UserORM) -> None:
        async with self.database.get_session() as session:
            session.add(user)

    async def check_exsist_email(self, email: str) -> bool:
        query = select(UserORM).where(UserORM.email == email).limit(1)

        async with self.database.get_read_only_session() as session:
            user = await session.scalar(query)
            if not user:
                return False
        return True
            
    async def get_list(self, user: UserORM, filters: dict[str, str]=None, orber_by: str=None) -> list[UserORM] | None:
        query = select(UserORM).where(UserORM.id != user.id)

        if filters:
            if 'gender' in filters and filters['gender'] != None:
                query = query.where(UserORM.gender == filters['gender'])
            if 'first_name' in filters and filters['first_name'] != None:
                query = query.where(UserORM.first_name.ilike(f"%{filters['first_name']}%"))
            if 'last_name' in filters and filters['last_name'] != None:
                query = query.where(UserORM.last_name.ilike(f"%{filters['last_name']}%"))
            if 'max_distance' in filters and filters['max_distance'] != None:
                query = query.where(
                    func.ST_DistanceSphere(UserORM.location, user.location) <= filters['max_distance']
                )

        if orber_by:
            query = query.order_by(UserORM.created_at)

        async with self.database.get_read_only_session() as session:

            users: list[UserORM] = await session.scalars(query)
            if users: return users
        return None

    async def get_by_id(self, user_id: int) -> UserORM:
        query = select(UserORM).where(UserORM.id == user_id)

        async with self.database.get_read_only_session() as session:
            user = await session.scalar(query)
            if not user:
                raise
            return user
    
    async def get_by_email(self, email: str) -> UserORM:
        query = select(UserORM).where(UserORM.email == email)

        async with self.database.get_read_only_session() as session:
            user = await session.scalar(query)
            if not user:
                raise
            return user