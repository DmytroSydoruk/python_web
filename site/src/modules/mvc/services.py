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


from src.models.cart.models import CartItem
from src.models.cart.repository import CartRepository


class CartService:

    async def create_cart_item(self, user_id, db, product_id, qty):
        product = await ProductRepository.get_one(db, product_id)
        return await CartRepository.create(db, CartItem(
            user_id=user_id,
            product_id=product.id,
            qty=qty
        ))

    async def delete_cart_item(self, db, cart_item_id):
        await CartRepository.delete(
            db, await CartRepository.get_one(db, cart_item_id))


class OrderService:

    async def create_order(self, db, user_id, product_id, qty):
        product = await ProductRepository.get_one(db, product_id)
        return await OrderRepository.create(db, Order(
            user_id=user_id,
            product_id=product.id,
            qty=qty
        ))


class DashboardViews:

    def __init__(self):
        self.order_service = OrderService()
        self.cart_service = CartService()


    async def display_dashboard(self, request, db) -> templates.TemplateResponse:
        user_id = request.session.get("user_id")
        products = await ProductRepository.get_all(db)
        cart_items = await CartRepository.get_all_by_user_id(db, user_id)
        orders = await OrderRepository.get_all_by_user_id(db, user_id)
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "username": user_id,
            "orders": orders,
            "products": products,
            "cart_item_count": len(cart_items)
        })

    async def add_to_cart(self, request, db, product_id, qty) -> RedirectResponse:
        product = await ProductRepository.get_one(db, product_id)
        cart_item = await self.cart_service.create_cart_item(
            request.session.get("user_id"), db, product_id, qty
        )
        return RedirectResponse(url="/dashboard", status_code=303)

    async def remove_from_cart(self, db, cart_item_id) -> RedirectResponse:
        await self.cart_service.delete_cart_item(db, cart_item_id)
        return RedirectResponse(url="/dashboard", status_code=303)
