from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from .basemodel import Base
from datetime import datetime
from sqlalchemy import DateTime, func


class User(Base):
    __tablename__ = "users_alembic"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
