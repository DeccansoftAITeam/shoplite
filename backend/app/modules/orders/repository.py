from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

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