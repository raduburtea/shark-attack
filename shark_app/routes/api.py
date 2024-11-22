from fastapi import APIRouter
from src.endpoints import shark_attacks

router = APIRouter()
router.include_router(shark_attacks.router)
