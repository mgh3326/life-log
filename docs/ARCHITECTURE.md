# Architecture

## Overview

**life-log** is a personal life logging system for tracking workouts and coffee brews.
Built with FastAPI + SQLAlchemy async + PostgreSQL, following the same patterns as `auto_trader`.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 17 (asyncpg) |
| Migrations | Alembic (async) |
| MCP Server | FastMCP |
| Package Manager | uv |
| Linter/Formatter | Ruff |

## Ports

| Service | Port |
|---------|------|
| life-log API | 8766 |
| life-log MCP | 8767 |
| auto_trader API | 8765 |

## Project Structure

```
app/
├── core/          # Config, DB engine, timezone helpers
├── models/        # SQLAlchemy ORM models
├── schemas/       # Pydantic request/response schemas
├── services/      # Business logic (CRUD, aggregation)
├── routers/       # FastAPI REST endpoints
└── mcp_server/    # FastMCP tools for AI assistant integration
```

## Database

- Same PostgreSQL instance as `auto_trader`, separate database `life_log`
- Owner: `mgh3326`
- Naming convention follows SQLAlchemy best practices (see `app/models/base.py`)

## Roadmap

### Phase 1 (Current)
- FastAPI REST API for workout + coffee logging
- Direct API calls for data entry/query

### Phase 2
- n8n nudge workflows (daily workout reminder, weekly report)
- Discord notifications via webhooks

### Phase 3
- MCP server → AI assistant tool integration
- Natural language log entry via Claude/ChatGPT
