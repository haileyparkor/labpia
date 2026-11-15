# 문제 해결

## `ModuleNotFoundError: No module named 'flask'`

원인: 시스템 Python으로 실행했습니다.

```bash
# 방법 1
source .venv/bin/activate
python app.py

# 방법 2
.venv/bin/python app.py
```

## `ensurepip is not available`

원인: `python3.12-venv` 미설치.

해결: [setup.md](setup.md)의 "해결 1" 또는 "해결 2".

## 링크가 안 열림 / 연결 거부

확인 순서:

```bash
ss -ltnp | grep :5000
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5000/
```

- 서버 프로세스가 없으면 → `python app.py`로 실행
- 서버는 있는데 브라우저에서 안 되면 → VS Code **PORTS** 탭에서 5000 포워딩
- `Address already in use` → 다른 포트 사용

```bash
.venv/bin/python -c "from app import app; app.run(port=5001)"
```

## `이미 supply.db 가 있어 실행을 중단했습니다`

원인: `seed.py`의 안전장치. 기존 데이터를 지우지 않으려고 중단합니다.

해결:

```bash
# 데이터를 버려도 될 때만
rm supply.db
.venv/bin/python seed.py
```

## `git push`가 거부됨

```text
! [rejected] ... (fetch first)
```

해결:

```bash
git pull --rebase origin main
bash scripts/check.sh
git push
```

`main`에는 force push하지 않습니다.

## merge conflict

- 충돌 파일의 **소유자**가 해결합니다.
- 내 파일이 아니면 직접 고치지 말고 PR 코멘트로 요청합니다.
- 해결 후:

```bash
git add <파일>
git rebase --continue
```

## `.moran/`이 git status에 보임

`.gitignore`에 `.moran/`이 있습니다. 보인다면 이미 추적 중인 파일입니다.

```bash
git rm -r --cached .moran
```

파일 자체는 디스크에 남습니다.

## CSV가 깨져 보임 (한글)

- UTF-8(BOM) 또는 cp949로 저장되었는지 확인
- 업로더는 UTF-8 우선, 실패 시 cp949로 읽습니다.
- 엑셀에서 "CSV UTF-8"로 저장하는 것을 권장

## `UNIQUE constraint failed: supplies.qr_code`

원인: QR 토큰 충돌(매우 드묾).

해결: `db.assign_qr_code()`를 사용하면 충돌 시 재시도합니다.
직접 `UPDATE supplies SET qr_code = ...`를 작성하지 마세요.

## QR은 되는데 RFID가 안 됨

확인:

1. 태그가 **UHF ISO 18000-6C**인가 (13.56MHz NFC 스티커는 불가)
2. 스캐너가 **HID 키보드 모드**인가
3. PC 입력 언어가 **영문**인가 (한글 IME가 켜져 있으면 값이 깨짐)
4. EPC가 대문자 hex로 저장되었는가
5. `rfid_epc`에 실제로 연결되어 있는가

## 스캔 값이 두 번 입력됨

원인: 접미사(Suffix)가 `CR+LF`로 설정됨.

해결: 스캐너 설정에서 접미사를 **CR(Enter) 하나**로 변경.

## `flask` 개발 서버가 두 번 실행됨

원인: `debug=True`의 자동 reloader.

스크립트/테스트에서는 다음처럼 실행:

```bash
.venv/bin/python -c "from app import app; app.run(port=5000, use_reloader=False)"
```
