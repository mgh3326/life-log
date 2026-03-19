.PHONY: dev mcp test lint format migrate deploy-pull deploy-up deploy-down deploy-logs deploy-migrate deploy-restart deploy-status

UV_RUN = uv run
DEPLOY_COMPOSE = docker compose --env-file .env.prod

dev:
	$(UV_RUN) uvicorn app.main:app --host 0.0.0.0 --port $${API_PORT:-8766} --reload

mcp:
	$(UV_RUN) python -m app.mcp_server.main

test:
	$(UV_RUN) pytest tests/ -v

lint:
	$(UV_RUN) ruff check app/ tests/
	$(UV_RUN) ruff format --check app/ tests/

format:
	$(UV_RUN) ruff check --fix app/ tests/
	$(UV_RUN) ruff format app/ tests/

migrate:
	$(UV_RUN) alembic revision --autogenerate -m "$(msg)"
	$(UV_RUN) alembic upgrade head

deploy-pull:
	$(DEPLOY_COMPOSE) pull

deploy-up:
	$(DEPLOY_COMPOSE) up -d

deploy-down:
	$(DEPLOY_COMPOSE) down

deploy-logs:
	$(DEPLOY_COMPOSE) logs -f

deploy-migrate:
	$(DEPLOY_COMPOSE) --profile migrate run --rm migration

deploy-restart:
	$(DEPLOY_COMPOSE) restart

deploy-status:
	$(DEPLOY_COMPOSE) ps
