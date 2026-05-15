from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.modules.cart import service as cart_service
from app.modules.orders import repository
from app.modules.orders.models import Order


class OrderServiceError(Exception):
    code = "ORDER_ERROR"
    http_status = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class EmptyCartError(OrderServiceError):
    code = "EMPTY_CART"
    http_status = 422


class InsufficientStockError(OrderServiceError):
    code = "INSUFFICIENT_STOCK"
    http_status = 409


def place_order(db: Session, cart_id: str | None) -> Order:
    cart = cart_service.get_existing_cart(db=db, cart_id=cart_id)
    if cart is None or not cart.items:
        raise EmptyCartError("Your cart is empty")

    total_amount = Decimal("0.00")
    for item in cart.items:
        product = item.product
        if product is None:
            continue
        if product.stock < item.quantity:
            raise InsufficientStockError(f"Insufficient stock for product {product.id}")
        total_amount += item.unit_price * item.quantity

    order = repository.create_order(db=db, cart=cart, total_amount=total_amount)
    cart_service.clear_cart(cart)
    db.commit()
    db.refresh(order)
    return order