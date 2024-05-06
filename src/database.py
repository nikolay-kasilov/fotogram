"""Файл для описания объекта sqlalchemy базы данных."""
from sqlalchemy import create_engine

from settings import settings

engine = create_engine(f"{settings.DB_DIALECT}://"
                       f"{settings.DB_HOST}:{settings.DB_PORT}@"
                       f"{settings.DB_USER}:{settings.DB_PASSWORD}/"
                       f"{settings.DB_NAME}")
