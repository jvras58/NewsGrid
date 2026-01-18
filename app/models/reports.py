from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app2.models import User


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    topic: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    owner: Mapped["User"] = relationship(back_populates="reports")
