from enum import Enum as PythonEnum
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Enum, Integer, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import BaseORM
from db.models.mixins import CreatedAtMixin


class GenderEnum(str, PythonEnum):
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
    location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
    )

    matches_as_user_one = relationship("MatchORM", foreign_keys="[MatchORM.user_one_id]", back_populates="user_one")
    matches_as_user_two = relationship("MatchORM", foreign_keys="[MatchORM.user_two_id]", back_populates="user_two")

    