import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Form, UploadFile
from starlette.responses import Response

from database import session_factory
from files.models import FileModel
from posts.models import Like, Post
from settings import settings
from users.services import CurrentUser


async def create_post(current_user: CurrentUser,
                      content: Annotated[str, Form()],
                      files: list[UploadFile]) -> None:
    with session_factory() as session:
        post = Post(content=content, created_at=datetime.now(),
                    author=current_user)
        session.add(post)
        session.flush()
        for file in files:
            ext = file.filename.split(".")[-1]
            file_uuid = uuid.uuid4()
            file_path = settings.PATH_FILES / (str(file_uuid) + "." + ext)
            file_bytes = await file.read()
            with file_path.open(mode="wb") as f:
                f.write(file_bytes)
            file_model = FileModel(uuid=file_uuid, extension=ext,
                                   post_id=post.id)
            session.add(file_model)
        session.commit()


def like_post(current_user: CurrentUser, post_id: int, like: bool) -> Response:
    with session_factory() as session:
        user_like = session.query(Like,
                                  ).filter(
            Like.post_id == post_id,
            Like.user_id == current_user.id,
        ).first()
        if like and user_like or not like and not user_like:
            return Response(status_code=200)
        if not user_like:
            user_like = Like(post_id=post_id, user_id=current_user.id)
            session.add(user_like)
            session.commit()
            return Response(status_code=200)
        if user_like:
            session.delete(user_like)
            session.commit()
            return Response(status_code=200)

