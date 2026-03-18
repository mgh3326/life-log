# life-log

Personal life logging system for workouts, coffee brews, and more.

## Quick Start

```bash
uv sync
cp .env.example .env
make dev        # API on :8766
make mcp        # MCP server on :8767
```

## API Endpoints

- `GET /health` — Health check
- `POST /api/workouts` — Log a workout
- `POST /api/coffee` — Log a coffee brew
- `GET /api/workouts/streak` — Workout streak info
- `GET /api/workouts/report/weekly` — Weekly workout report

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full details.
