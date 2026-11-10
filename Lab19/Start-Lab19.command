#!/bin/zsh
set -e
cd "$(dirname "$0")"
if [[ -x ../.venv/bin/python ]]; then
  PY=../.venv/bin/python
elif [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
else
  echo "Create a Python environment and install requirements.txt as described in README.md."
  read '?Press Return to close.'
  exit 1
fi
if /usr/sbin/lsof -nP -iTCP:8519 -sTCP:LISTEN >/dev/null 2>&1; then
  open http://127.0.0.1:8519
  exit 0
fi
exec "$PY" -m streamlit run app.py --server.address 127.0.0.1 --server.port 8519 --browser.gatherUsageStats false
