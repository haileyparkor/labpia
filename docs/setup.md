# 로컬 실행 환경

## 표준 방법

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python seed.py
python app.py
```

## 이 서버에서 확인된 문제: ensurepip 없음

증상:

```text
The virtual environment was not created successfully because ensurepip is not
available.
```

원인: `python3.12-venv` 패키지가 설치되어 있지 않음.

### 해결 1 (권장, 시스템 변경)

```bash
sudo apt install python3.12-venv
```

이후 표준 방법으로 venv를 다시 만듭니다.

### 해결 2 (시스템 변경 없이, 이 서버에서 사용한 방법)

이미 pip가 들어 있는 venv가 하나 있다면 그 pip만 복사합니다.

```bash
python3 -m venv --without-pip .venv
cp -a <기존 venv>/lib/python3.12/site-packages/pip* .venv/lib/python3.12/site-packages/
.venv/bin/python -m pip install -r requirements.txt
```

예시:

```bash
cp -a /home/huihyeon/bphslab/.venv/lib/python3.12/site-packages/pip* \
      /home/huihyeon/labpia/.venv/lib/python3.12/site-packages/
```

## 실행

```bash
.venv/bin/python seed.py
.venv/bin/python app.py
```

venv 활성화는 필수가 아닙니다. `.venv/bin/python`을 직접 쓰면 됩니다.
그냥 `python app.py`를 쓰면 시스템 Python에는 Flask가 없어 실패합니다.

## 접속

- 같은 화면: `http://127.0.0.1:5000`
- VS Code 원격: **PORTS** 탭 → 5000 포워딩 → `http://127.0.0.1:5000`
- 서버 IP 직접: `http://<서버IP>:5000` (방화벽에 따라 막힐 수 있음)

## DB

- 기본 경로: `labpia/supply.db`
- `supply.db`는 **git에 올라가지 않습니다.**
- 다른 DB를 쓰려면 환경변수로 지정:

```bash
LABPIA_DB=/tmp/test.db .venv/bin/python -c "import db; db.init_db()"
```

### DB 초기화 (주의: 로컬 데이터 삭제)

```bash
rm supply.db
.venv/bin/python seed.py
```

이 명령은 **로컬 supply.db만** 지웁니다. 원격 저장소에는 영향이 없습니다.
실행 전에 필요한 데이터가 없는지 확인하세요.

## 테스트

```bash
bash scripts/check.sh
```

임시 DB를 사용하므로 실제 `supply.db`는 건드리지 않습니다.
