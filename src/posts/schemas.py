from datetime import datetime

from pydantic import BaseModel

from users.schemas import UserSchema


class PostSchema(BaseModel):
    id: int
    images: list[str]
    content: str
    author_id: int
    author_name: str
    created_at: datetime
    count_likes: int
    liked: bool
    count_comments: int


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

class CommentWithUserSchema(BaseModel):
    id: int
    user: UserSchema
    post_id: int
    content: str
    created_at: datetime
    owner: bool


class CommentsOutputSchema(BaseModel):
    comments: list[CommentWithUserSchema]
