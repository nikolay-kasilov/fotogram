"""Модуль для запуска FASTAPI."""
from pathlib import Path

from fastapi import FastAPI

from users.routing import router as users_router
from settings import settings
from posts.routing import router as posts_router

def create_app() -> FastAPI:
    if not Path(settings.PATH_FILES).is_dir():
        Path(settings.PATH_FILES).mkdir()
    return FastAPI()


app = create_app()
app.include_router(users_router, prefix="/api/v1", tags=["api/v1"])
app.include_router(posts_router, prefix="/api/v1", tags=["api/v1"])


@app.get("/")
def read_root() -> dict[str, str]:
    """Тестовый эндпоинт.

    Returns
    -------
        dict[str, str]: тестовый словарь.

    """
    return {"Hello": "World"}
