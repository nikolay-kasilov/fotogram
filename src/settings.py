"""Файл, хранящий глобальные настройки проекта."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс хранящий все настройки."""

    DB_DIALECT: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        """Конфиг насйтроек."""

        case_sensitive = True
        env_file = "../.env"

settings = Settings()
(f"{settings.DB_DIALECT}://"
       f"{settings.DB_HOST}:{settings.DB_PORT}@"
       f"{settings.DB_USER}:{settings.DB_PASSWORD}/"
       f"{settings.DB_NAME}")
