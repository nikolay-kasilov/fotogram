from fastapi import APIRouter

from files.services import get_file

router = APIRouter(prefix="/media_files", tags=["media_files"])
router.get("/{filename}")(get_file)
