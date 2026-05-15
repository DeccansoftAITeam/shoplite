# ShopLite – Copilot Instructions

## Stack
- **Backend**: FastAPI, SQLAlchemy 2.x, Alembic, PyTest, Python (snake_case files, PascalCase classes, UPPER_SNAKE_CASE constants)
- **Frontend**: React + Vite + TypeScript
- **Database**: SQL Server 2022 / SQLAlchemy ORM; monetary values use `DECIMAL(10,2)` and Python `Decimal` (never `float`); timestamps in UTC
- **API**: REST/JSON only; paths are plural nouns (`/api/products`, `/api/cart/items`, `/api/orders`)

## Backend Module Layout
New modules go under `backend/app/modules/<module_name>/` with exactly these five files:

```
router.py   – HTTP layer: request/response mapping, status codes
service.py  – Business rules and orchestration only
repository.py – All SQLAlchemy queries and persistence
schemas.py  – Pydantic DTOs only
models.py   – SQLAlchemy ORM entities only
```

Current modules: `catalog`, `cart`, `checkout`, `orders`, `search`.

## Layering Rule (strict)
`router → service → repository → models`

- **No raw SQL or session query construction in `service.py`** — that belongs in `repository.py`
- **No cross-module repository calls** — call the target module's service instead
- `router.py` must not import from `repository.py` or `models.py` directly

## Error Format
All non-2xx responses must use this exact shape (handled by global exception handlers in `core/errors.py`):

```json
{ "error": { "code": "UPPER_SNAKE_CASE_CODE", "message": "Human-readable English" } }
```

## Naming Conventions
- DB tables: plural `snake_case`; PK always `id`; FKs follow `<entity>_id` pattern
- API paths: plural nouns, e.g. `/api/products`
- Python: files/modules `snake_case`, classes `PascalCase`, env vars `UPPER_SNAKE_CASE`

## Key Env Vars
`DATABASE_URL`, `APP_ENV`, `API_HOST`, `API_PORT`, `CORS_ORIGINS`, `LOG_LEVEL`

## What NOT to Add
- No authentication or authorization (no JWT, sessions, login endpoints)
- No admin UI or admin-only API routes
- No payment processing (checkout creates an order with status `PLACED` only)
- No float for money — always `Decimal`
- No SQL strings in `service.py`
