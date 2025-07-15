from fastapi import APIRouter
from app.api.v1.endpoints import comments, bugs, stories, tcases, common

router = APIRouter()

router.include_router(common.router)
router.include_router(comments.router)
router.include_router(bugs.router)
router.include_router(stories.router)
router.include_router(tcases.router)