"""Маршруты для пользователей."""
from fastapi.routing import APIRouter

router = APIRouter(prefix="/users/", tags=["users"])
router.add_route()
