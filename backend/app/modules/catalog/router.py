from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import error_response
from app.modules.catalog import service
from app.modules.catalog.schemas import ProductOut

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


@router.get("/products", response_model=list[ProductOut], status_code=200)
def get_products(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    try:
        return service.get_products(db=db, limit=limit, offset=offset)
    except Exception:
        return error_response(
            code="CATALOG_LIST_FAILED",
            message="Unable to fetch products",
            http_status=500,
        )
