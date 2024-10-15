from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.common.database import get_postgres

from src.modules.mvc.services import SiteViews, DashboardViews

from src.modules.mvc.cart.router import router as cart_router

router = APIRouter(prefix="")
router.include_router(cart_router)

site_views = SiteViews()

dashboard_views = DashboardViews()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return await site_views.get_home_page(request)


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return await site_views.get_login_page(request)


@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    return await site_views.login(request, form_data.username, form_data.password)


@router.get("/logout")
async def logout(request: Request):
    return await site_views.logout(request)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db=Depends(get_postgres)):
    return await dashboard_views.display_dashboard(request, db)


@router.post("/add-to-cart")
async def add_to_cart(
        request: Request,
        product_id: int = Form(...),
        quantity: int = Form(...),
        db=Depends(get_postgres)):
    return await dashboard_views.add_to_cart(request, db, product_id, quantity)


@router.post("/remove-from-cart")
async def remove_from_cart(
    item_id: int = Form(...),
    db=Depends(get_postgres)):
    return await dashboard_views.remove_from_cart(db, item_id)
