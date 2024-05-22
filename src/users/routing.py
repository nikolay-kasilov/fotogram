"""Маршруты для пользователей."""
from fastapi import APIRouter

from users.schemas import Token, UserSchema
from users.services import login_for_access_token, read_users_me, signup, \
    subscribe, unsubscribe

router = APIRouter(prefix="/users", tags=["users"])
router.post("/signup/", response_model=UserSchema)(signup)
router.post("/login/", response_model=Token)(login_for_access_token)
router.get("/test/")(read_users_me)
router.post("/{author_id}/subscribe/")(subscribe)
router.post("/{author_id}/unsubscribe/")(unsubscribe)
