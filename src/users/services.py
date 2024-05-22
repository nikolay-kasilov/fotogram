"""Функции для обработки запросов."""
import json
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import and_

from database import session_factory
from settings import settings

from .models import User, Subscribe
from .schemas import SignUpSchema, Token, UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    with (session_factory() as session):
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


def create_access_token(data: dict, expires_delta: int = 15):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)
    return encoded_jwt


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=json.dumps({"error": "Could not validate credentials"}),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        exp: int = payload.get("exp")
        token_date = datetime.fromtimestamp(exp, UTC)
        if token_date.replace(tzinfo=UTC) < datetime.now(
            UTC):
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with session_factory() as session:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            raise credentials_exception
        return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def read_users_me(
    current_user: CurrentUser,
):
    return Response(status_code=200,
                    content=current_user.fullname + " " + current_user.birthday.strftime(
                        "%B %d, %Y"))


def signup(ud: SignUpSchema) -> Response | UserSchema:
    if ud.password != ud.password_repeat:
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content=json.dumps({"error": "Passwords must match"}))
    with session_factory() as session:
        try:
            old_user = session.query(User).filter_by(
                username=ud.username).first()
            if old_user is not None:
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content=json.dumps(
                                    {"error": "Username already taken"}))
            print(old_user)
            user = User(
                username=ud.username,
                fullname=ud.fullname,
                password=get_password_hash(ud.password),
                birthday=ud.birthday,
                bio=ud.bio,
                signup_at=datetime.now(),
                last_activity=datetime.now(),
            )
        except Exception as e:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content=json.dumps(
                                {"error": f"Error creating user {e}"}))
        else:
            session.add(user)
            session.commit()
            ur = UserSchema(
                id=user.id,
                username=user.username,
                fullname=user.fullname,
                signup_at=user.signup_at,
                bio=user.bio,
                last_activity=user.last_activity,
                avatar=user.avatar,
                birthday=user.birthday,
            )
            return ur


def subscribe(current_user: CurrentUser, author_id: int) -> Response:
    with session_factory() as session:
        author = session.query(User).filter_by(id=author_id).first()
        if author is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Author not found")
        current_subscribe = session.query(Subscribe).filter(
            and_(Subscribe.subscriber == current_user,
            Subscribe.author == author)).first()
        if not current_subscribe:
            current_subscribe = Subscribe(author=author,
                                          subscriber=current_user)
            session.add(current_subscribe)
            session.commit()
        return Response(status_code=status.HTTP_200_OK)


def unsubscribe(current_user: CurrentUser, author_id: int) -> Response:
    with session_factory() as session:
        author = session.query(User).filter_by(id=author_id).first()
        if author is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Author not found")
        current_subscribe = session.query(Subscribe).filter(
            Subscribe.author == author).filter(
            Subscribe.subscriber == current_user).first()
        if current_subscribe:
            session.delete(current_subscribe)
            session.commit()
        return Response(status_code=status.HTTP_200_OK)
