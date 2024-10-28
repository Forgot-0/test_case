from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        comment="Дата создания записи",
    )
