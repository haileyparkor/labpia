# B — QR / RFID 명세

- 담당: **cslfdlbia**
- 브랜치: `feat/qr-rfid`
- 스캐너: SR290 (1D/2D/QR + UHF RFID ISO 18000-6C)

## 목표

1. 시약마다 QR 라벨을 만들고 인쇄한다.
2. QR 또는 RFID를 스캔하면 해당 시약 상세로 이동한다.
3. 실물 RFID 태그의 EPC를 시약에 연결한다.

## 만들 파일

```text
qr.py
templates/qr/label.html
templates/qr/scan.html
templates/qr/link.html
static/css/qr.css
static/js/qr.js   (필요할 때만)
```

`app.py`, `db.py`, `schema.sql`, `base.html`, `style.css`는 수정하지 않습니다.

## URL

| 기능 | URL | 인증 |
|---|---|---|
| QR 라벨 | `GET /admin/qr/label/<id>` | 추후 |
| 태그 연결 | `GET/POST /admin/qr/tags/link` | 추후 |
| 스캔 화면 | `GET /scan` | 공개 |
| QR 조회 | `GET /q/<token>` | 공개 |

## QR 규칙

- 토큰: `Q` + 10자 (`db.assign_qr_code`가 생성)
- QR 이미지 내용: `f"{BASE_URL}/q/{token}"`
- `BASE_URL`은 환경변수로:

```python
import os

BASE_URL = os.environ.get("LABPIA_BASE_URL", "http://127.0.0.1:5000")
```

- 라벨에 인쇄할 서버 주소가 바뀌면 기존 라벨이 깨집니다.
  학교에서 쓸 **고정 주소**를 리드에게 확인하세요.

## 라벨 페이지

`GET /admin/qr/label/<id>`

- 시약 이름, 위치, 시약장 번호, 토큰 텍스트
- QR 이미지 (`qrcode` 패키지로 PNG 생성 → `data:` URI로 HTML에 삽입)
- 인쇄 버튼
- `@media print`에서 네비게이션/버튼 숨김

```python
import base64
import io

import qrcode

img = qrcode.make(f"{BASE_URL}/q/{supply['qr_code']}")
buf = io.BytesIO()
img.save(buf, format="PNG")
data_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
```

## 스캔 페이지

`GET /scan`

- 입력창 하나에 **autofocus**
- 스캐너가 값을 입력하고 Enter를 보내면 자동 submit
- 입력값은 다음을 모두 허용:
  - 전체 URL: `http://.../q/Q7K2M9X4AB`
  - 토큰: `Q7K2M9X4AB`
  - RFID EPC: `E2806894000050...` (공백/콜론 허용)

처리:

```python
from db import find_by_code

kind, supply = find_by_code(code)
if supply is None:
    return render_template("qr/scan.html", error="찾을 수 없습니다", code=code)
return redirect(url_for("supply_detail", supply_id=supply["id"]))
```

`find_by_code`가 QR/RFID를 자동 판별합니다. 직접 정규식을 만들지 마세요.

## 태그 연결 페이지

`GET/POST /admin/qr/tags/link`

입력:

- `item_code`: 시약의 QR 토큰 또는 `/q/...` URL
- `epc`: 스캐너로 읽은 RFID EPC

처리:

1. `item_code`로 시약을 찾는다 (`db.normalize_code` + `find_by_code`, 또는 id).
2. `epc`를 `db.normalize_code`로 정규화한다 (대문자, 공백/콜론 제거).
3. 형식이 16~64자리 hex가 아니면 오류.
4. 다른 시약에 이미 연결된 EPC면 오류.
5. 같은 시약에 다시 연결하면 갱신.
6. commit 후 성공 메시지.

## SR290 설정

| 항목 | 값 |
|---|---|
| 연결 모드 | USB HID 키보드(Keyboard Wedge) |
| 접미사 | `CR` (Enter) 하나 |
| 접두사 | 없음 |
| PC 입력 언어 | 영문 |
| 스캔 모드 | 버튼 (연속 스캔은 v1.4) |

- **UHF ISO 18000-6C** 태그만 인식합니다.
- 13.56MHz NFC 스티커는 인식되지 않습니다.
- 연속 스캔은 여러 태그를 동시에 읽으므로 개별 조회에는 쓰지 않습니다.

## 완료 조건

- [ ] `/admin/qr/label/1` 이 200이고 QR이 보임
- [ ] 라벨 인쇄 시 버튼/네비게이션이 안 나옴
- [ ] `/q/<token>` 이 `/supply/<id>`로 redirect
- [ ] `/scan?code=<token>` 이 상세로 이동
- [ ] `/scan?code=<EPC>` 가 상세로 이동 (연결 후)
- [ ] 없는 코드는 친절한 "찾을 수 없습니다" 화면
- [ ] 태그 연결 후 `rfid_epc`가 DB에 저장됨
- [ ] 다른 시약의 EPC를 중복 연결하면 거부
- [ ] `bash scripts/check.sh` 통과
- [ ] 공통 파일을 수정하지 않음

## 테스트 시나리오

1. seed 데이터 1번의 `qr_code`로 라벨 페이지 열기
2. `/q/<token>` 접속 → `/supply/1`
3. `/scan?code=<token>` → `/supply/1`
4. 태그 연결 페이지에서 1번에 EPC 저장
5. `/scan?code=<EPC>` → `/supply/1`
6. 같은 EPC를 2번에 연결 → 오류
7. `/scan?code=UNKNOWN` → not found
8. 토큰에 공백/콜론을 섞어도 정상

## 하지 말 것

- EPC 자동 생성 (불가능)
- `qr_code`를 직접 UPDATE (반드시 `db.assign_qr_code`)
- 연속 스캔/재고 실사 (v1.4)
- 로그인/권한 (v1.3)

## 자주 하는 실수

- 한글 IME가 켜진 상태로 스캔 → 값 깨짐
- EPC 소문자/공백 저장 → `normalize_code` 사용
- `BASE_URL`을 `127.0.0.1`로 인쇄 → 다른 기기에서 안 열림
- 라벨 여백 부족 → 인쇄 미리보기에서 확인
- QR 토큰을 hex로 착각 → `Q`로 시작하므로 QR로 판별됨
