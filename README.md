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

## 배포 (Raspberry Pi)

이 프로젝트는 Raspberry Pi 5 (`linux/arm64`) 환경에서 Docker Compose를 사용하여 배포하도록 구성되어 있습니다.

### 첫 배포
1. `.env.prod` 파일 생성 (`.env.prod.example` 참고)
   - `DATABASE_URL`은 호스트 머신에 실행 중인 PostgreSQL을 가리켜야 합니다.
2. DB 마이그레이션 실행: `make deploy-migrate`
3. 서비스 시작: `make deploy-up`

### 업데이트 (main 브랜치 push 후)
1. 새로운 이미지 가져오기: `make deploy-pull`
2. 서비스 재시작: `make deploy-up`

### 운영 관리
- 로그 확인: `make deploy-logs`
- 상태 확인: `make deploy-status`
- 서비스 중지: `make deploy-down`
- 서비스 재시작: `make deploy-restart`
