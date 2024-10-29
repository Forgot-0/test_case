from datetime import datetime
from enum import Enum
import json
from fastapi import Form, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, ValidationError, model_validator

from db.models.user import GenderEnum, UserORM






class UserCreateSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    gender: str
    password: str
    latitude: float
    longitude: float

    def to_ormModel(self, password: str) -> UserORM:
        return UserORM(
            email=str(self.email),
            first_name=self.first_name,
            last_name=self.last_name,
            gender=GenderEnum(self.gender),
            password_hash=password,
            latitude=self.latitude,
            longitude=self.longitude,
        )

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class UserShema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    gender: str
    latitude: float
    longitude: float
    created_at: datetime

    @classmethod
    def from_ormModel(cls, user_orm: UserORM) -> 'UserShema':
        return cls(
            email=user_orm.email,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            gender=user_orm.gender.value,
            latitude=user_orm.latitude,
            longitude=user_orm.longitude,
            created_at=user_orm.created_at
        )

class ListUsersShema(BaseModel):
    users: list[UserShema] | None


class UserFilters(BaseModel):
    gender: str | None = Query(default=None)
    first_name: str | None = Query(default=None)
    last_name: str | None = Query(default=None)


class UserOrder(BaseModel):
    order_by: str | None = Query(default=None)