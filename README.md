# Fast Notice

## db migration
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
## install dependencies
```bash
poetry install
```

## run server
```bash
poetry run uvicorn app.main:app --reload
```