# A — CSV 업로드 명세

- 담당: **chloehj-png**
- 브랜치: `feat/reagent-csv`
- URL: `GET/POST /admin/reagents/import`

## 목표

엑셀에서 저장한 CSV로 시약을 한 번에 등록한다.
한 건이라도 형식이 틀리면 **아무것도 저장하지 않고** 오류 행을 알려 준다.

## 만들 파일

```text
reagents.py
templates/reagents/import.html
static/css/reagents.css   (필요할 때만)
data/reagents_sample.csv  (이미 있음, 필요하면 보강)
```

`app.py`, `db.py`, `schema.sql`, `base.html`, `style.css`는 수정하지 않습니다.

## CSV 형식

```csv
name,category,description,location,cabinet_number,quantity,status,cas_number,concentration,volume,opened_at,expires_at,hazard_class,rfid_epc
에탄올 500mL,시약,소독과 세척에 쓰는 에탄올입니다.,보일랩,3,보통,사용 가능,64-17-5,95%,500mL,2026-11-15,2027-11-15,3,
```

### 필수 컬럼

| 컬럼 | 규칙 |
|---|---|
| `name` | 비어 있으면 안 됨 |
| `category` | 비어 있으면 안 됨 (예: 시약) |
| `location` | `db.LOCATIONS` 중 하나 (`보일랩`) |
| `cabinet_number` | 정수 1~6 |
| `quantity` | `db.QUANTITIES` 중 하나 (`많음/보통/적음/없음`) |

### 선택 컬럼

| 컬럼 | 규칙 |
|---|---|
| `description` | 없으면 빈 문자열 |
| `status` | 없으면 `사용 가능` |
| `cas_number` | 자유 형식 (예: `64-17-5`) |
| `concentration` | 자유 형식 (예: `95%`) |
| `volume` | 자유 형식 (예: `500mL`) |
| `opened_at` | 있으면 `YYYY-MM-DD` |
| `expires_at` | 있으면 `YYYY-MM-DD` |
| `hazard_class` | 자유 형식 |
| `rfid_epc` | 있으면 16~64자리 hex, 대문자로 저장, 중복 불가 |

`qr_code` 컬럼은 **CSV에 넣지 않습니다.** 서버가 자동 생성합니다.

## 처리 순서

1. 업로드 파일을 바이트로 읽는다.
2. `utf-8-sig`로 디코딩, 실패하면 `cp949`로 재시도.
3. `csv.DictReader`로 모든 행을 파싱한다.
4. **모든 행을 먼저 검증한다.**
5. 오류가 1건이라도 있으면 → 저장하지 않고 오류 목록을 보여 준다.
6. 오류가 없으면 트랜잭션으로 저장한다.
   - 중복 키 `(name, location, cabinet_number)`가 있으면 **건너뛴다.**
   - 새 행은 INSERT 후 `db.assign_qr_code(conn, cursor.lastrowid)`로 QR을 부여한다.
7. 한 번에 commit 한다.

## 결과 화면

```text
총 25행 · 추가 20 · 건너뜀 3 · 실패 0
```

실패가 있으면:

```text
7행: cabinet_number 가 1~6 범위가 아닙니다 (값: 9)
12행: quantity 는 많음/보통/적음/없음 중 하나여야 합니다 (값: 조금)
```

행 번호는 **CSV 파일 기준**으로 표시합니다(헤더가 1행).

## 사용할 공통 함수

```python
from db import LOCATIONS, QUANTITIES, assign_qr_code, get_db
```

- `get_db()`: 요청 스코프 sqlite3 연결
- `assign_qr_code(conn, supply_id)`: QR 토큰 생성·저장 (commit은 직접)
- `LOCATIONS`, `QUANTITIES`: 허용 값

## 완료 조건

- [ ] `GET /admin/reagents/import` 가 200
- [ ] `data/reagents_sample.csv` 업로드 시 3건 추가
- [ ] 같은 파일을 다시 업로드하면 3건 모두 건너뜀
- [ ] 잘못된 행이 있으면 DB가 전혀 바뀌지 않음
- [ ] cp949 CSV도 읽힘
- [ ] 결과 화면에 추가/건너뜀/실패 수와 실패 행 번호가 보임
- [ ] `bash scripts/check.sh` 통과
- [ ] 공통 파일을 수정하지 않음

## 테스트 시나리오

1. 샘플 CSV 정상 업로드
2. 같은 파일 재업로드 → 건너뜀
3. `cabinet_number=9` → 실패, DB 변화 없음
4. `name` 빈 값 → 실패
5. 엑셀에서 cp949로 저장한 파일 → 정상
6. `rfid_epc` 중복 → 실패
7. 설명에 쉼표가 있는 행 → 따옴표로 감싸면 정상

## 하지 말 것

- 개별 등록 폼 (v1.2)
- 수정/삭제
- 로그인/권한
- `app.py`에 라우트 직접 추가 (blueprint는 이미 등록되어 있음)

## 자주 하는 실수

- CSV 헤더 앞뒤 공백
- 엑셀에서 한글을 cp949로 저장
- 설명에 쉼표를 넣고 따옴표를 안 씀
- 검증 전에 DB에 먼저 INSERT
- `assign_qr_code` 후 commit을 잊음
- `supply.db`를 git에 추가
