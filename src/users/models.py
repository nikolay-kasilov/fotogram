"""Файл моделей ORM для части работы пользователей."""
from datetime import datetime

from sqlalchemy import ForeignKey, and_
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
    comments: Mapped[list["Comment"]] = relationship("Comment",
                                                     back_populates="user")

    subscribers: Mapped[list["Subscribe"]] = relationship("Subscribe",
                                                          back_populates="subscriber",
                                                          primaryjoin="Subscribe.subscriber_id == User.id")
    subscribes: Mapped[list["Subscribe"]] = relationship("Subscribe",
                                                         back_populates="author",
                                                         primaryjoin="Subscribe.author_id == User.id")


class Subscribe(Base):
    __tablename__ = "subscribes"

    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                               primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                           primary_key=True)

    subscriber: Mapped[User] = relationship("User",
                                            foreign_keys=[subscriber_id],
                                            back_populates="subscribers")
    author: Mapped[User] = relationship("User", foreign_keys=[author_id],
                                        back_populates="subscribes")
