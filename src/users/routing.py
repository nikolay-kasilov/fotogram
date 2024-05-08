"""Маршруты для пользователей."""
from fastapi import APIRouter

from users.schemas import UserSchema
from users.services import signup

router = APIRouter(prefix="/users", tags=["users"])
router.post("/signup/", response_model=UserSchema)(signup)
