from typing import Annotated

from fastapi import UploadFile, Form

from files.models import FileModel
from users.services import CurrentUser
from posts.schemas import PostSchema
from database import session_factory

async def create_post(current_user: CurrentUser, content: Annotated[str, Form()],
                file: UploadFile) -> None:
    with session_factory() as session:
        extension = file.filename.split('.')[-1]
        file = FileModel(extension=extension)
        session.add(file)
        session.flush()
        print(file.uuid)
        # with open("") as f:
        #     s = await file.read()
