from datetime import datetime
import json
from fastapi import Query
from pydantic import BaseModel, EmailStr, model_validator

from db.models.user import GenderEnum, UserORM



class UserCreateInSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    gender: GenderEnum
    password: str
    latitude: float
    longitude: float

    def to_ormModel(self, password: str) -> UserORM:
        return UserORM(
            email=str(self.email),
            first_name=self.first_name,
            last_name=self.last_name,
            gender=GenderEnum(self.gender).name,
            password_hash=password,
            location=f"POINT({self.latitude} {self.longitude})",
        )

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class UserOutShema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str | None
    gender: str
    created_at: datetime


class ListUsersOutShema(BaseModel):
    users: list[UserOutShema] | None


class UserFilters(BaseModel):
    max_distance: float = Query(default=10.0)
    gender: str | None = Query(default=None)
    first_name: str | None = Query(default=None)
    last_name: str | None = Query(default=None)


class UserOrder(BaseModel):
    order_by: str | None = Query(default=None)


class TokenOutSchema(BaseModel):
    access_token: str
    token_type: str