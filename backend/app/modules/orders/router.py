from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import error_response
from app.modules.cart.router import COOKIE_NAME
from app.modules.orders import service
from app.modules.orders.schemas import OrderDetailOut, OrderOut, OrderSummaryOut

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("", response_model=list[OrderSummaryOut], status_code=200)
def get_orders(
    cart_id: str | None = Cookie(default=None, alias=COOKIE_NAME),
    db: Session = Depends(get_db),
):
    return service.get_orders(db=db, cart_id=cart_id)


@router.get("/{order_id}", response_model=OrderDetailOut, status_code=200)
def get_order(
    order_id: int,
    cart_id: str | None = Cookie(default=None, alias=COOKIE_NAME),
    db: Session = Depends(get_db),
):
    try:
        return service.get_order_by_id(db=db, order_id=order_id, cart_id=cart_id)
    except service.OrderServiceError as exc:
        return error_response(code=exc.code, message=exc.message, http_status=exc.http_status)


@router.post("", response_model=OrderOut, status_code=201)
def place_order(
    cart_id: str | None = Cookie(default=None, alias=COOKIE_NAME),
    db: Session = Depends(get_db),
):
    try:
        return service.place_order(db=db, cart_id=cart_id)
    except service.OrderServiceError as exc:
        db.rollback()
        return error_response(code=exc.code, message=exc.message, http_status=exc.http_status)