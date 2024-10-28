from datetime import datetime
from enum import Enum as PythonEnum
from xmlrpc.client import DateTime
from sqlalchemy import Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import BaseORM
from app.db.models.mixins import CreatedAtMixin


class GenderEnum(PythonEnum):
    MALE = "male"
    FEMALE = "female"


class UserORM(BaseORM, CreatedAtMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=False)
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
