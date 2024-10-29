from enum import Enum
from pydantic import BaseModel, EmailStr

from db.models.user import GenderEnum, UserORM






class UserCreateSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    gender: str
    password: str
    latitude: float
    longitude: float

    def to_userOrmModel(self, password: str) -> UserORM:
        return UserORM(
            email=str(self.email),
            first_name=self.first_name,
            last_name=self.last_name,
            gender=GenderEnum(self.gender),
            password_hash=password,
            latitude=self.latitude,
            longitude=self.longitude,
        )