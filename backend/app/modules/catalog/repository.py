from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.catalog.models import Product


def list_products(db: Session, limit: int, offset: int) -> list[Product]:
    stmt = select(Product).order_by(Product.id).offset(offset).limit(limit)
    return list(db.scalars(stmt).all())
