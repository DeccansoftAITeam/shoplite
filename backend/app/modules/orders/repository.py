from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.cart.models import Cart
from app.modules.orders.models import Order, OrderItem


def create_order(db: Session, *, cart: Cart, total_amount: Decimal) -> Order:
    order = Order(cart_id=cart.cart_id, status="PLACED", total_amount=total_amount)
    db.add(order)
    db.flush()

    for item in cart.items:
        product = item.product
        if product is None:
            continue
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=product.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.unit_price * item.quantity,
            )
        )

    db.flush()
    return order


def list_orders_by_cart_id(db: Session, cart_id: str) -> list[Order]:
    stmt = select(Order).where(Order.cart_id == cart_id).order_by(Order.created_at.desc(), Order.id.desc())
    return list(db.scalars(stmt).all())


def get_order_by_id_and_cart_id(db: Session, *, order_id: int, cart_id: str) -> Order | None:
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id, Order.cart_id == cart_id)
    )
    return db.scalar(stmt)