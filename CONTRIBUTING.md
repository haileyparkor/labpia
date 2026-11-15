# 기여 안내

처음이면 [docs/onboarding.md](docs/onboarding.md)부터 읽으세요.

## 핵심 규칙

- `main` 직접 push 금지 → `feat/<기능>` 브랜치 + PR
- 공통 파일(`app.py`, `db.py`, `schema.sql`, `base.html`, `style.css`)은 리드만 수정
- PR 전 `bash scripts/check.sh`
- `supply.db`, `.venv/`, `__pycache__/`, `.moran/` 커밋 금지

## 문서

| 문서 | 내용 |
|---|---|
| [docs/README.md](docs/README.md) | 문서 지도 |
| [docs/onboarding.md](docs/onboarding.md) | 시작 순서 |
| [docs/setup.md](docs/setup.md) | 실행 환경 |
| [docs/team-contract.md](docs/team-contract.md) | 역할·URL·DB 계약 |
| [docs/workflow.md](docs/workflow.md) | 브랜치·PR·충돌 |
| [docs/troubleshooting.md](docs/troubleshooting.md) | 오류 대응 |
| [docs/features/](docs/features/) | A/B 기능 명세 |
