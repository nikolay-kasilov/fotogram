"""Функции для обработки запросов."""
from datetime import datetime

from bcrypt import hashpw
from fastapi import status
from fastapi.responses import Response

from database import session_factory
from settings import settings

from .models import User
from .schemas import SignUpSchema, UserSchema


def signup(ud: SignUpSchema) -> Response | UserSchema:
    if ud.password != ud.password_repeat:
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"error": "Passwords must match"})
    with session_factory() as session:
        try:
            user = User(
                username=ud.username,
                fullname=ud.fullname,
                password=hashpw(
                    ud.password.encode(),
                    settings.SALT.encode(),
                ).decode("utf-8"),
                birthday=ud.birthday,
                bio=ud.bio,
                signup_at=datetime.now(),
                last_activity=datetime.now(),
            )
        except Exception as e:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": ""})
        else:
            session.add(user)
            session.commit()
            ur = UserSchema(
                id=user.id,
                username=user.username,
                fullname=user.fullname,
                bio=user.bio,
                signup_at=user.signup_at,
                last_activity=user.last_activity,
                avatar=user.avatar,
                birthday=user.birthday,
            )
            return ur
