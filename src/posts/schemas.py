from datetime import datetime

from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    filename: str
    content: str
    author_id: int
    author_name: str
    created_at: datetime

class CommentInputSchema(BaseModel):
    content: str

class CommentSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime
