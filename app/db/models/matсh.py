from sqlalchemy import ForeignKey, Index, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import BaseORM
from db.models.mixins import CreatedAtMixin


class MatchORM(BaseORM, CreatedAtMixin):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_one_id: Mapped[int] = mapped_column('user_one', Integer, ForeignKey("user.id"), nullable=False)
    user_two_id: Mapped[int] = mapped_column('user_two', Integer, ForeignKey("user.id"), nullable=False)

    mutually: Mapped[bool] = mapped_column(Boolean, default=False)


    user_one = relationship("UserORM", foreign_keys=[user_one_id], back_populates="matches_as_user_one")
    user_two = relationship("UserORM", foreign_keys=[user_two_id], back_populates="matches_as_user_two")