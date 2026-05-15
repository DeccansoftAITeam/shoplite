from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.cart import repository
from app.modules.cart.models import Cart
from app.modules.cart.schemas import CartLineOut, CartOut
from app.modules.catalog import service as catalog_service


class CartServiceError(Exception):
    code = "CART_ERROR"
    http_status = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ProductNotFoundError(CartServiceError):
    code = "PRODUCT_NOT_FOUND"
    http_status = 404


class ProductOutOfStockError(CartServiceError):
    code = "PRODUCT_OUT_OF_STOCK"
    http_status = 409


def get_or_create_cart(db: Session, cart_id: str | None) -> tuple[Cart, bool]:
    resolved_cart_id = cart_id or str(uuid4())
    cart = repository.get_cart_by_cart_id(db=db, cart_id=resolved_cart_id)
    if cart is not None:
        return cart, False

    cart = repository.create_cart(db=db, cart_id=resolved_cart_id)
    db.flush()
    return cart, True


def get_cart(db: Session, cart_id: str | None) -> tuple[CartOut, str, bool]:
    cart, created = get_or_create_cart(db=db, cart_id=cart_id)
    db.commit()
    db.refresh(cart)
    return serialize_cart(cart), cart.cart_id, created


def add_item(db: Session, cart_id: str | None, product_id: int, quantity: int) -> tuple[CartOut, str, bool]:
    product = catalog_service.get_product_by_id(db=db, product_id=product_id)
    if product is None:
        raise ProductNotFoundError(f"Product {product_id} not found")
    if product.stock <= 0:
        raise ProductOutOfStockError(f"Product {product_id} is out of stock")

    cart, created = get_or_create_cart(db=db, cart_id=cart_id)
    repository.add_or_increment_item(
        db=db,
        cart=cart,
        product_id=product.id,
        quantity=quantity,
        unit_price=product.price,
    )
    db.commit()
    db.refresh(cart)
    return serialize_cart(cart), cart.cart_id, created


def remove_item(db: Session, cart_id: str | None, product_id: int) -> tuple[CartOut, str, bool]:
    cart, created = get_or_create_cart(db=db, cart_id=cart_id)
    repository.remove_item(cart=cart, product_id=product_id)
    db.commit()
    db.refresh(cart)
    return serialize_cart(cart), cart.cart_id, created


def get_existing_cart(db: Session, cart_id: str | None) -> Cart | None:
    if cart_id is None:
        return None
    return repository.get_cart_by_cart_id(db=db, cart_id=cart_id)


def clear_cart(cart: Cart) -> None:
    repository.clear_items(cart)


def serialize_cart(cart: Cart) -> CartOut:
    lines: list[CartLineOut] = []
    total_quantity = 0
    total_amount = Decimal("0.00")

    for item in sorted(cart.items, key=lambda current: current.id):
        product = item.product
        if product is None:
            continue

        line_total = item.unit_price * item.quantity
        total_quantity += item.quantity
        total_amount += line_total
        lines.append(
            CartLineOut(
                product_id=item.product_id,
                name=product.name,
                description=product.description,
                quantity=item.quantity,
                stock=product.stock,
                unit_price=item.unit_price,
                line_total=line_total,
            )
        )

    return CartOut(
        cart_id=cart.cart_id,
        items=lines,
        total_quantity=total_quantity,
        total_amount=total_amount,
    )