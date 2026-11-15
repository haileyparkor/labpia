# 작업 흐름

## 브랜치

| 담당 | 브랜치 |
|---|---|
| A (CSV) | `feat/reagent-csv` |
| B (QR/RFID) | `feat/qr-rfid` |
| 리드 | `chore/*`, `docs/*` |

`main`에 직접 push하지 않습니다.

## 매일

```bash
git switch main
git pull --rebase origin main
git switch <내 브랜치>
git rebase main
```

작업 후:

```bash
bash scripts/check.sh
git status
git add <내 파일만>
git commit -m "feat(reagent): CSV 업로드 검증 추가"
git push
```

## 커밋 메시지

```text
feat(reagent): CSV 업로드 추가
fix(qr): EPC 공백 제거
docs: 팀 계약 갱신
chore: 의존성 추가
test: 스모크 테스트 보강
```

## PR

- 가능하면 **Draft PR**로 일찍 엽니다.
- 제목: `feat(reagent): CSV 업로드`
- 본문 템플릿의 체크리스트를 채웁니다.
- 리뷰어: 상대 담당 1명 + 리드
- merge는 리드가 합니다 (Squash merge).

## 리뷰에서 보는 것

- 내 파일만 수정했는가
- 공통 파일(`app.py`, `db.py`, `schema.sql`, `base.html`, `style.css`)을 건드리지 않았는가
- `bash scripts/check.sh`가 통과하는가
- 새 URL이 계약과 일치하는가
- 오류 메시지가 사용자에게 친절한가

## 충돌이 났을 때

1. 충돌 파일이 누구 소유인지 확인합니다 ([team-contract.md](team-contract.md)).
2. **소유자가 아닌 사람은 직접 고치지 않습니다.** PR 코멘트로 요청합니다.
3. 소유자가 main 기준으로 다시 작업하고 push합니다.
4. 내 브랜치는 `git rebase main`으로 최신화합니다.

```bash
git fetch origin
git rebase origin/main
# 충돌 해결 후
git add <파일>
git rebase --continue
```

## 공통 파일을 바꿔야 할 때

`app.py`, `db.py`, `schema.sql`, `base.html`, `style.css`는 리드만 수정합니다.
필요하면 PR에 이렇게 남기세요.

```text
공통 파일 변경 요청: db.py 에 find_by_name() 추가 필요
이유: CSV 중복 검사에 사용
```

## 절대 커밋하지 않는 것

```text
supply.db
.venv/
__pycache__/
.moran/
```

`.gitignore`에 들어 있지만 `git add -f`로 강제하지 마세요.

## merge 순서

1. 공통/문서 (리드)
2. A (CSV)
3. B (QR/RFID)

각 merge 후 `main`에서 `bash scripts/check.sh`를 실행하고, 마지막에 통합 시나리오를 확인합니다.

## 통합 시나리오 (마지막에)

1. CSV로 시약 3개 등록
2. QR 라벨 출력
3. QR 스캔 → 상세 이동
4. RFID 태그 연결
5. RFID 스캔 → 상세 이동
6. 같은 CSV 다시 업로드 → 중복 건너뜀 확인
