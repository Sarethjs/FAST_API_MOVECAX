from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/routes')


@router.get('/')
async def find_best_route():
    pass