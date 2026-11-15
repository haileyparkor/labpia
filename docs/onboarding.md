# 온보딩

세 명 모두 이 순서로 시작합니다.

## 0. 준비

- GitHub 계정과 이 저장소의 쓰기 권한
- Python 3.12
- git

## 1. clone

```bash
git clone https://github.com/haileyparkor/labpia.git
cd labpia
```

## 2. 커밋 신원 설정

```bash
git config user.name "<본인 GitHub 아이디>"
git config user.email "<GitHub에 등록한 이메일>"
```

이메일이 GitHub 계정에 등록되어 있지 않으면 커밋이 본인 것으로 표시되지 않습니다.

## 3. 실행 환경

일반 PC:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

이 서버처럼 `ensurepip is not available` 오류가 나면 [setup.md](setup.md)의 우회 방법을 쓰세요.

## 4. DB와 실행

```bash
python seed.py
python app.py
```

접속: `http://127.0.0.1:5000`
원격 서버라면 VS Code **PORTS** 탭에서 5000을 포워딩하세요.

## 5. 내 브랜치 만들기

```bash
git switch main
git pull --rebase origin main
git switch -c feat/reagent-csv   # A: chloehj-png
git switch -c feat/qr-rfid       # B: cslfdlbia
```

## 6. 첫 PR (연습)

1. 문서 오타 하나를 고칩니다.
2. `bash scripts/check.sh` 실행
3. commit → push
4. GitHub에서 **Draft PR** 생성
5. 상대방이 리뷰 → 리드가 merge

## 7. 매일 작업 루틴

```bash
git switch main
git pull --rebase origin main
git switch <내 브랜치>
git rebase main
# 작업
bash scripts/check.sh
git add <내 파일만>
git commit -m "feat(reagent): ..."
git push
```

PR을 올리기 전에는 항상 `git pull --rebase origin main`으로 최신 main을 반영하세요.

## 8. 막히면

- 오류: [troubleshooting.md](troubleshooting.md)
- 규칙: [workflow.md](workflow.md)
- 내 기능 명세: [features/](features/)
- 그래도 안 되면 PR에 코멘트로 질문 (DM보다 PR 코멘트가 기록에 남습니다)
