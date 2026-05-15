from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: Decimal
    created_at: datetime


class OrderItemOut(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class OrderSummaryOut(BaseModel):
    id: int
    status: str
    total_amount: Decimal
    created_at: datetime


class OrderDetailOut(OrderSummaryOut):
    items: list[OrderItemOut]