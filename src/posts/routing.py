from fastapi import APIRouter

from posts.services import create_post, like_post

router = APIRouter(prefix="/posts", tags=["posts"])
router.post("/create/")(create_post)
router.post("/{post_id}/like/")(like_post)
