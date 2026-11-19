# Week 2 Assessment: Data + SQL + APIs

Order Analytics and Customer API for a retail client.

| Task | Folder | Database | What it covers |
|---|---|---|---|
| 1 | task1 | retail_db | SQL analysis: JOIN, HAVING, CTE, ROW_NUMBER, LAG, JSONB |
| 2 | task2 | perf_db | EXPLAIN ANALYZE before/after index, parameterised query, constraints |
| 3 | task3 | retail_orm_db | SQLAlchemy models, pooling, Alembic, transactions, MongoDB |
| 4 | task4 | customer_api_db, customer_api_test_db | FastAPI, API key, HMAC webhook, fetch_all client, pytest |

## Decisions
- Separate database per task, so Alembic autogenerate starts from an empty database.
- Task 2: parameterised query (%s), so the input '1 OR 1=1' returns 0 rows.
- Task 3: place_order uses one transaction with a row lock; any error rolls back everything.
- Task 4: API key checked with hmac.compare_digest (401 missing, 403 wrong); webhook uses HMAC-SHA256 on the raw body.
- Secrets are kept in .env files, which are not committed.

## How to run
- Task 4 API: python -m uvicorn main:app --reload
- Task 4 tests: python -m pytest -v
