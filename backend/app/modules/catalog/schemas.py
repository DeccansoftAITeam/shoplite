from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductOut(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price: Decimal
    stock: int = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)
