
# 보평고 비품관리 시스템 Model 1.0

Model 1.0은 NFC 기능을 제외한 **비품 검색 및 상세 정보 확인 웹 프로토타입**입니다.

## 1.0 목표

- Home 화면 제공
- 비품 검색
- 비품 상세 정보 확인
- 비품 위치 확인
- 보일랩 6개 시약장 위치를 버튼으로 선택
- 시약 잔량 확인

## 포함 기능

- `/` : Home
- `/items` : 비품 검색 및 목록
- `/items/<id>` : 비품 상세 페이지
- `/map` : 보일랩 및 6개 시약장 위치 선택

## 제외 기능

- NFC 태그 인식
- 대여·반납 기록
- 사용자 로그인
- 권한 관리
- 알림
- 통계

## 실행 방법

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python seed.py
python app.py
```

브라우저에서 다음 주소로 접속합니다.

```text
http://127.0.0.1:5000
```
