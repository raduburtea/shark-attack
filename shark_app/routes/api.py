from fastapi import APIRouter
from src.endpoints import books

router = APIRouter()
router.include_router(books.router)
