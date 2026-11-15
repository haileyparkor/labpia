# labpia — 보평고 비품관리 시스템

Flask + SQLite 기반 과학실 비품 관리 시스템입니다.

## 빠른 시작

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

## 구조

| 파일 | 역할 | 소유 |
|---|---|---|
| `app.py` | Flask 앱, 기존 라우트 | 리드 |
| `db.py` | DB 연결·초기화·코드 정규화 | 리드 |
| `schema.sql` | DB 스키마 | 리드 |
| `reagents.py` | CSV 업로드 | A |
| `qr.py` | QR/RFID | B |
| `docs/team-contract.md` | URL·DB·CSV 계약 | 리드 |

## 협업 규칙

- `main` 직접 push 금지 → `feat/<기능>` 브랜치 + PR
- 공통 파일(`app.py`, `db.py`, `schema.sql`, `base.html`, `style.css`)은 리드만 수정
- PR 전 `bash scripts/check.sh`
- `supply.db`, `.venv/`, `__pycache__/` 는 커밋하지 않음

자세한 내용은 [docs/team-contract.md](docs/team-contract.md) 를 참고하세요.
