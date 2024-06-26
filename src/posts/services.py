import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Form, UploadFile, HTTPException
from sqlalchemy.orm import selectinload
from starlette.responses import Response



from database import session_factory
from files.models import FileModel
from posts.models import Like, Post, Comment
from posts.schemas import CommentInputSchema, CommentSchema, PostSchema, \
    ResponsePostsSchema
from settings import settings
from users.services import CurrentUser


def get_posts(current_user: CurrentUser) -> ResponsePostsSchema:
    with session_factory() as session:
        posts = session.query(Post).options(selectinload(Post.images),
                                            selectinload(Post.author),
                                            selectinload(Post.likes)).all()
        posts_schemas = [
            PostSchema(
                id=post.id,
                images=list(
                    map(lambda x: x.get_filename(), post.images)),
                content=post.content,
                author_id=post.author.id,
                author_name=post.author.fullname,
                created_at=post.created_at,
                count_likes=len(post.likes),
                liked=current_user.id in map(lambda x: x.user_id, post.likes),
            )
            for post in posts
        ]
        return ResponsePostsSchema(posts=posts_schemas)


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


def create_comment(current_user: CurrentUser, post_id: int,
                   comment: CommentInputSchema) -> CommentSchema:
    with session_factory() as session:
        user_comment = Comment(
            user=current_user,
            post_id=post_id,
            content=comment.content,
            created_at=datetime.now(),
        )
        session.add(user_comment)
        session.commit()
        return CommentSchema(
            id=user_comment.id,
            content=user_comment.content,
            created_at=user_comment.created_at,
            user_id=user_comment.user_id,
            post_id=user_comment.post_id
        )


def delete_comment(current_user: CurrentUser, post_id: int,
                   comment_id: int) -> Response:
    with session_factory() as session:
        comment = session.query(Comment).filter(
            Comment.id == comment_id).filter(
            Comment.post_id == post_id
        ).first()
        if not comment:
            raise HTTPException(status_code=404,
                                detail=f"Comment with id {comment_id} not found")
        if comment.user_id != current_user.id:
            raise HTTPException(status_code=403,
                                detail="You are not permission to delete this comment")
        session.delete(comment)
        session.commit()
        return Response(status_code=204)
