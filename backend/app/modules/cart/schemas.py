from decimal import Decimal

from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(default=1, ge=1)


class CartLineOut(BaseModel):
    product_id: int
    name: str
    description: str | None = None
    quantity: int = Field(ge=1)
    stock: int = Field(ge=0)
    unit_price: Decimal
    line_total: Decimal


class CartOut(BaseModel):
    cart_id: str
    items: list[CartLineOut]
    total_quantity: int = Field(ge=0)
    total_amount: Decimal