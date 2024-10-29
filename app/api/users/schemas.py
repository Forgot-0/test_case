from enum import Enum
import json
from fastapi import Form, HTTPException, status
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

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
