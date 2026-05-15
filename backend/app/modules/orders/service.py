from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.modules.cart import service as cart_service
from app.modules.orders import repository
from app.modules.orders.models import Order
from app.modules.orders.schemas import OrderDetailOut, OrderItemOut, OrderSummaryOut


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


class OrderNotFoundError(OrderServiceError):
    code = "ORDER_NOT_FOUND"
    http_status = 404


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


def get_orders(db: Session, cart_id: str | None) -> list[OrderSummaryOut]:
    if cart_id is None:
        return []

    orders = repository.list_orders_by_cart_id(db=db, cart_id=cart_id)
    return [serialize_order_summary(order) for order in orders]


def get_order_by_id(db: Session, *, order_id: int, cart_id: str | None) -> OrderDetailOut:
    if cart_id is None:
        raise OrderNotFoundError(f"Order {order_id} not found")

    order = repository.get_order_by_id_and_cart_id(db=db, order_id=order_id, cart_id=cart_id)
    if order is None:
        raise OrderNotFoundError(f"Order {order_id} not found")

    return serialize_order_detail(order)


def serialize_order_summary(order: Order) -> OrderSummaryOut:
    return OrderSummaryOut(
        id=order.id,
        status=order.status,
        total_amount=order.total_amount,
        created_at=order.created_at,
    )


def serialize_order_detail(order: Order) -> OrderDetailOut:
    return OrderDetailOut(
        id=order.id,
        status=order.status,
        total_amount=order.total_amount,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.line_total,
            )
            for item in sorted(order.items, key=lambda current: current.id)
        ],
    )