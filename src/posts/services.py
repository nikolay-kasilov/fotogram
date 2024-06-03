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
    ResponsePostsSchema, CommentWithUserSchema, CommentsOutputSchema
from settings import settings
from users.models import User
from users.schemas import UserSchema
from users.services import CurrentUser


def get_posts(current_user: CurrentUser, user_id: int | None = None) -> ResponsePostsSchema:
    with session_factory() as session:
        query = session.query(Post).options(selectinload(Post.images),
                                            selectinload(Post.author),
                                            selectinload(Post.likes))

        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            query = query.filter(Post.author_id == user_id)
        posts = query.all()
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
                count_comments=len(post.comments)
            )
            for post in posts
        ]
        return ResponsePostsSchema(posts=posts_schemas)


def get_comments(current_user: CurrentUser, post_id: int):
    with session_factory() as session:
        comments = session.query(Comment).options(
            selectinload(Comment.user)).filter(
            Comment.post_id == post_id).all()
        comments_schemas = [
            CommentWithUserSchema(
                id=comment.id,
                user=UserSchema(username=comment.user.username,
                                fullname=comment.user.fullname,
                                birthday=comment.user.birthday,
                                signup_at=comment.user.signup_at,
                                last_activity=comment.user.last_activity,
                                bio=comment.user.bio,
                                avatar=comment.user.avatar),
                post_id = post_id,
                content=comment.content,
                created_at=comment.created_at,
                owner=current_user == comment.user,
            )
            for comment in comments
        ]
        return CommentsOutputSchema(comments=comments_schemas)


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
