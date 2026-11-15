#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if ! python -c "import flask" 2>/dev/null; then
  echo "Flask가 없습니다. .venv를 활성화하거나 pip install -r requirements.txt 후 실행하세요."
  exit 1
fi

echo "[1/2] 문법 검사"
python -m compileall -q app.py db.py seed.py reagents.py qr.py tests

echo "[2/2] 스모크 테스트 (임시 DB 사용, 실제 supply.db 는 건드리지 않음)"
python -m unittest discover -s tests -v
