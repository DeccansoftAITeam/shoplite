# ShopLite Backend

FastAPI modular-monolith backend for ShopLite.

## How to run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic revision --autogenerate -m "init catalog"
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## How to seed

```bash
cd backend
.venv\Scripts\activate
python -m app.seed
```

## Folder layout

```text
backend/
  app/
    main.py
    seed.py
    core/
      config.py
      db.py
      errors.py
    modules/
      catalog/
        router.py
        service.py
        repository.py
        schemas.py
        models.py
  alembic/
    env.py
    script.py.mako
    versions/
  alembic.ini
  requirements.txt
```
