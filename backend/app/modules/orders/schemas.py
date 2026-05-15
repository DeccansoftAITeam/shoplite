from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: Decimal
    created_at: datetime