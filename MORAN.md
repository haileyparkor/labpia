# MORAN.md — labpia (보평고 비품관리 시스템)

Flask + SQLite 기반 과학실 비품/시약 관리 앱. 3인 공동 작업, `main` 직접 push 금지.

## 실행 / 검증

```bash
# PR 전 필수
PATH=$PWD/.venv/bin:$PATH bash scripts/check.sh

# 로컬 실행
.venv/bin/python app.py          # http://127.0.0.1:5000
.venv/bin/python seed.py         # DB 없을 때만 (있으면 아무것도 안 함)

# 실제 DB 보호용 임시 DB
LABPIA_DB=/tmp/x.db .venv/bin/python app.py
```

- venv 활성화 없이 `.venv/bin/python` 으로 실행 가능
- 맨 `python app.py` 는 `No module named flask` 로 실패 (시스템 파이썬)
- 시스템에 `ensurepip` 가 없어 venv 는 `--without-pip` + pip 복사로 만든 상태. `.venv` 삭제 금지

## 소유권 — 공통 파일은 리드만 수정

| 파일 | 소유 |
|---|---|
| `app.py`, `db.py`, `schema.sql`, `templates/base.html`, `static/css/style.css` | 리드 |
| `reagents.py`, `templates/reagents/*`, `static/css/reagents.css` | A (chloehj-png) |
| `qr.py`, `templates/qr/*`, `static/css/qr.css`, `static/js/qr.js` | B (cslfdlbia) |
| `docs/**`, `README.md`, `CONTRIBUTING.md` | 리드 |

A/B는 **새 파일만 추가**한다. 공통 파일 변경이 필요하면 리드에게 요청.

## URL 계약 (바꾸면 안 됨)

| URL | 기능 |
|---|---|
| `/`, `/search`, `/supply/<id>`, `/location` | v1.0 기존 |
| `GET/POST /admin/reagents/import` | A: CSV 일괄 등록 |
| `GET /admin/qr/label/<id>`, `GET/POST /admin/qr/tags/link` | B: 라벨·태그 연결 |
| `GET /scan`, `GET /q/<token>` | B: 스캔·공개 조회 |

쓰기 URL은 전부 `/admin/...` 접두사 → 나중에 `@login_required` 를 URL 변경 없이 붙이기 위함.

## DB 규칙

- ORM 없음. `db.get_db()` (요청 스코프, `sqlite3.Row`) 사용
- 컬럼 추가는 `db.NEW_COLUMNS` 에 넣고 `init_db()` 가 `ALTER TABLE` 로 처리
- QR 발급은 **반드시** `db.assign_qr_code(conn, supply_id)`. 직접 UPDATE 금지
- 스캔 입력 정규화는 `db.normalize_code()` / `db.find_by_code()`. 자체 정규식 만들지 말 것
- QR 토큰 = `Q` + 10자(비-hex). RFID EPC = 16~64자 hex. 접두사로 자동 판별됨
- EPC는 공장 레이저 각인이라 **자동 생성 불가**

## 협업 규칙

- 브랜치: `feat/<기능>`, PR로만 merge, 설명에 `closes #<이슈번호>`
- PR 전 `bash scripts/check.sh` 통과
- 커밋 금지: `supply.db`, `.venv/`, `__pycache__/`, `.moran/`
- `main` 은 브랜치 보호 걸려 있음

## 문서 지도

- `docs/onboarding.md` — 시작 순서
- `docs/setup.md` — 환경 (ensurepip 우회법)
- `docs/team-contract.md` — 역할·URL·DB 계약
- `docs/workflow.md` — 브랜치·PR·충돌
- `docs/troubleshooting.md` — 오류 14건
- `docs/features/reagent-csv.md` — A 명세
- `docs/features/qr-rfid.md` — B 명세 + SR290 설정
- `docs/roadmap.md` — v1.1~v1.4

## 알려진 함정

- seed 12건에 `에탄올 500mL/보일랩/3`, `페놀프탈레인 용액/보일랩/3` 이 이미 있음
  → `supply.db` 에 샘플 CSV를 올리면 `추가 1 · 건너뜀 2` 가 정상. "추가 3" 은 빈 DB 기준
- 엑셀 CSV는 `cp949` 로 저장되는 경우가 많음 → `utf-8-sig` 실패 시 `cp949` 재시도
- `description`/`status` 는 `NOT NULL` → `None` 대신 `""` / `"사용 가능"`
- `rfid_epc` 는 `""` 아닌 `None` (UNIQUE 인덱스 때문)
- SR290은 UHF ISO 18000-6C만 인식. 13.56MHz NFC 스티커 불가
- QR 라벨에 인쇄되는 `LABPIA_BASE_URL` 은 고정 주소여야 함 (바뀌면 기존 라벨 무효)

## 현재 진행 상황

- v1.1 기반 완료: 공통 데이터 계층(`db.py`), 블루프린트 스텁, 문서, 스모크 테스트
- 진행 중: A = CSV 업로드(#4), B = QR/RFID(#5)
- 로그인/권한은 v1.3, 재고 실사는 v1.4
