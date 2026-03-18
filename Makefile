.PHONY: dev mcp test lint format migrate

dev:
	uvicorn app.main:app --host 0.0.0.0 --port 8766 --reload

mcp:
	python -m app.mcp_server.main

test:
	pytest tests/ -v

lint:
	ruff check app/ tests/
	ruff format --check app/ tests/

format:
	ruff check --fix app/ tests/
	ruff format app/ tests/

migrate:
	alembic revision --autogenerate -m "$(msg)"
	alembic upgrade head
