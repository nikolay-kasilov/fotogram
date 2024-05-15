from fastapi import APIRouter
from posts.services import create_post

router = APIRouter(prefix="/posts", tags=["posts"])
router.post("/create/")(create_post)
