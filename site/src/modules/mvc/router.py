from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.modules.mvc.services import LandingService

router = APIRouter(prefix="")

landing_service = LandingService()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return landing_service.get_home_page(request)
