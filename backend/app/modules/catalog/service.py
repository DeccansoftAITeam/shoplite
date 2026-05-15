from sqlalchemy.orm import Session

from app.modules.catalog import repository
from app.modules.catalog.models import Product


def get_products(db: Session, limit: int = 20, offset: int = 0) -> list[Product]:
    return repository.list_products(db=db, limit=limit, offset=offset)


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return repository.get_by_id(db=db, product_id=product_id)
