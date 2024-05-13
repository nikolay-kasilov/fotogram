from datetime import datetime
from uuid import UUID

from sqlalchemy import text, ForeignKey
from sqlalchemy.types import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from files.models import FileModel


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str | None]
    created_at: Mapped[datetime]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    images: Mapped[list[FileModel]] = relationship("FileModel", back_populates="posts")
    author: Mapped["User"] = relationship("User", back_populates="posts")
