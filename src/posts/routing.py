from fastapi import APIRouter

from posts.services import create_post, like_post, create_comment, \
    delete_comment, get_posts

router = APIRouter(prefix="/posts", tags=["posts"])
router.get("/")(get_posts)
router.post("/create/")(create_post)
router.post("/{post_id}/like/")(like_post)
router.post("/{post_id}/comments/create")(create_comment)
router.delete("/{post_id}/comments/{comment_id}")(delete_comment)
