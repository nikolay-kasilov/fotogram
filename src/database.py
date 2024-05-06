"""Файл для описания объекта sqlalchemy базы данных."""
from sqlalchemy import create_engine

engine = create_engine("{}://{}:{}@{}:{}/{}")
