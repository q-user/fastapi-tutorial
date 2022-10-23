from pathlib import Path

from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import settings

templates = Jinja2Templates(directory=f"{settings.BASE_DIR}/templates")
general_pages_router = APIRouter()


@general_pages_router.get('/')
async def home(request: Request):
    return templates.TemplateResponse("general_pages/homepage.html", {"request": request})
