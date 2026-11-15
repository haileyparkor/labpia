# 팀 계약 (v1.1)

## 담당

| 담당 | 사람 | 파일 |
|---|---|---|
| 리드 | haileyparkor | `app.py`, `db.py`, `schema.sql`, `base.html`, `style.css` |
| A | cslfdlbia | `reagents.py`, `templates/reagents/*` |
| B | chloehj-png | `qr.py`, `templates/qr/*`, `static/js/*`, `static/css/qr.css` |

## URL

| 기능 | URL |
|---|---|
| CSV 업로드 | `GET/POST /admin/reagents/import` |
| QR 라벨 | `GET /admin/qr/label/<id>` |
| 태그 연결 | `GET/POST /admin/qr/tags/link` |
| 스캔 화면 | `GET /scan` |
| QR 조회 | `GET /q/<token>` |

## DB

- 기존 `supplies` 8컬럼 유지
- 추가: `qr_code`, `rfid_epc`, `cas_number`, `concentration`, `volume`, `opened_at`, `expires_at`, `hazard_class`
- `qr_code` 자동 생성 (`Q` + 10자), `rfid_epc` 는 실물 태그 스캔으로만 입력
- 중복 기준: `(name, location, cabinet_number)` → CSV 에서 **건너뛰기**

## CSV

- 인코딩: UTF-8(BOM) 우선, 실패 시 cp949
- 필수: `name, category, location, cabinet_number, quantity`
- 전체 검증 후 오류가 1건이라도 있으면 저장하지 않음
- 결과: `총 N행 · 추가 N · 건너뜀 N · 실패 N`

## Git

- `main` 직접 push 금지
- 브랜치: `feat/reagent-csv`, `feat/qr-rfid`
- PR 전 `git pull --rebase origin main`
- merge 순서: 기준선 → A → B
