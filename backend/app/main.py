from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.errors import error_response
from app.modules.catalog.router import router as catalog_router

app = FastAPI(title="ShopLite API", version="0.1.0")

app.include_router(catalog_router)


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
