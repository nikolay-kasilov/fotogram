from datetime import datetime

from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    filename: str
    content: str
    author_id: int
    author_name: str
    created_at: datetime
