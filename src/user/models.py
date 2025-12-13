from datetime import datetime
from sqlalchemy import false

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column()
    data: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    password_salt: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(server_default="")
    email_verified: Mapped[bool] = mapped_column(server_default=false())
    random_string: Mapped[str] = mapped_column(server_default="")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"{self.id} {self.nickname} {self.data} {self.email} {self.email_verified}"

