from fastapi import APIRouter
from posts.services import create_post

router = APIRouter(prefix="/posts", tags=["users"])
router.post("/create/")(create_post)
