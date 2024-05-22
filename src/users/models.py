"""Файл моделей ORM для части работы пользователей."""
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from posts.models import Post


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    fullname: Mapped[str]
    password: Mapped[str]
    birthday: Mapped[datetime | None]
    bio: Mapped[str]
    signup_at: Mapped[datetime]
    last_activity: Mapped[datetime]
    avatar: Mapped[str | None]

    posts: Mapped[list[Post]] = relationship("Post", back_populates="author")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
