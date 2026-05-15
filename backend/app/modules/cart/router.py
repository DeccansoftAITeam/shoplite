from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import error_response
from app.modules.cart import service
from app.modules.cart.schemas import CartItemCreate, CartOut

COOKIE_NAME = "cart_id"

router = APIRouter(prefix="/api/cart", tags=["cart"])


def set_cart_cookie(response: Response, cart_id: str) -> None:
    response.set_cookie(
        key=COOKIE_NAME,
        value=cart_id,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24 * 30,
    )


@router.get("", response_model=CartOut, status_code=200)
def get_cart(
    response: Response,
    cart_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    cart, resolved_cart_id, _ = service.get_cart(db=db, cart_id=cart_id)
    set_cart_cookie(response, resolved_cart_id)
    return cart


@router.post("/items", response_model=CartOut, status_code=200)
def add_item(
    payload: CartItemCreate,
    response: Response,
    cart_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    try:
        cart, resolved_cart_id, _ = service.add_item(
            db=db,
            cart_id=cart_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
    except service.CartServiceError as exc:
        db.rollback()
        return error_response(code=exc.code, message=exc.message, http_status=exc.http_status)

    set_cart_cookie(response, resolved_cart_id)
    return cart


@router.delete("/items/{product_id}", response_model=CartOut, status_code=200)
def delete_item(
    product_id: int,
    response: Response,
    cart_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    cart, resolved_cart_id, _ = service.remove_item(db=db, cart_id=cart_id, product_id=product_id)
    set_cart_cookie(response, resolved_cart_id)
    return cart