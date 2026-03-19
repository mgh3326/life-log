FROM python:3.13-slim AS builder

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:/root/.local/bin:$PATH"

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev

FROM python:3.13-slim AS final

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends bash curl && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --uid 10001 appuser
COPY --from=builder /app/.venv /app/.venv
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8100 8101

# Command is typically provided via docker-compose or run command.
# But providing a default for completeness.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100"]
