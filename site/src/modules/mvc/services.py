from fastapi.responses import RedirectResponse

from src.common.templates import templates
from src.models.orders.models import Order
from src.models.orders.repository import OrderRepository
from src.models.products.repository import ProductRepository


class SiteViews:

    async def get_home_page(self, request):
        return templates.TemplateResponse(request=request, name="index.html")

    async def get_login_page(self, request):
        return templates.TemplateResponse(request=request, name="login.html")

    async def login(self, request, username, password):
        request.session['user_id'] = username
        return RedirectResponse(url="/dashboard", status_code=303)

    async def logout(self, request):
        request.session.pop("user_id", None)
        return RedirectResponse(url="/login", status_code=303)

    async def get_dashboard(self, request, db):
        user_id = request.session.get("user_id")
        products = await ProductRepository.get_all(db)
        orders = await OrderRepository.get_all_by_user_id(db, user_id)

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "username": user_id,
            "orders": orders,
            "products": products
        })

    async def add_order(self, request, db, product_id, quantity):
        product = await ProductRepository.get_one(db, product_id)
        await OrderRepository.create(db, Order(
            user_id=request.session.get("user_id"),
            product_id=product.id,
            qty=quantity
        ))
        return RedirectResponse(url="/dashboard", status_code=303)


    async def remove_order(self, request, db, order_id):
        await OrderRepository.delete(db, await OrderRepository.get_order_by_id(db, order_id))
        return RedirectResponse(url="/dashboard", status_code=303)
