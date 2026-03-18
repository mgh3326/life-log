.PHONY: dev mcp test lint format migrate

dev:
	uvicorn app.main:app --host 0.0.0.0 --port $${API_PORT:-8766} --reload

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

deploy-pull:
	docker compose pull

deploy-up:
	docker compose up -d

deploy-down:
	docker compose down

deploy-logs:
	docker compose logs -f

deploy-migrate:
	docker compose --profile migrate run --rm migration

deploy-restart:
	docker compose restart

deploy-status:
	docker compose ps
