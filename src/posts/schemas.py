from datetime import datetime

from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    images: list[str]
    content: str
    author_id: int
    author_name: str
    created_at: datetime


class ResponsePostsSchema(BaseModel):
    posts: list[PostSchema]


class CommentInputSchema(BaseModel):
    content: str


class CommentSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime
