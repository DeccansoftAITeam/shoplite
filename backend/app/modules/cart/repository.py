from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.cart.models import Cart, CartItem


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_cart_by_cart_id(db: Session, cart_id: str) -> Cart | None:
    stmt = (
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .where(Cart.cart_id == cart_id)
    )
    return db.scalar(stmt)


def create_cart(db: Session, cart_id: str) -> Cart:
    cart = Cart(cart_id=cart_id)
    db.add(cart)
    db.flush()
    return cart


def add_or_increment_item(
    db: Session,
    *,
    cart: Cart,
    product_id: int,
    quantity: int,
    unit_price,
) -> CartItem:
    existing_item = next((item for item in cart.items if item.product_id == product_id), None)
    if existing_item is None:
        existing_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        db.add(existing_item)
        cart.items.append(existing_item)
    else:
        existing_item.quantity += quantity
        existing_item.unit_price = unit_price

    cart.updated_at = utc_now()
    db.flush()
    return existing_item


def remove_item(cart: Cart, product_id: int) -> bool:
    item = next((existing for existing in cart.items if existing.product_id == product_id), None)
    if item is None:
        return False

    cart.items.remove(item)
    cart.updated_at = utc_now()
    return True


def clear_items(cart: Cart) -> None:
    cart.items.clear()
    cart.updated_at = utc_now()