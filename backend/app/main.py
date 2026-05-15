from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import error_response
from app.modules.catalog.router import router as catalog_router
from app.modules.cart.router import router as cart_router
from app.modules.orders.router import router as orders_router

app = FastAPI(title="ShopLite API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(orders_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, __):
    return error_response(
        code="VALIDATION_ERROR",
        message="Invalid request payload or query parameters",
        http_status=422,
    )


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
