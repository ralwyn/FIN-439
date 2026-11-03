#!/bin/zsh
set -eu
LAB_DIR="${0:A:h}"
COURSE_DIR="${LAB_DIR:h}"
if [[ -x "$COURSE_DIR/.venv/bin/python" ]]; then
  LAB_PYTHON="$COURSE_DIR/.venv/bin/python"
elif [[ -x "$HOME/Desktop/FIN439/.venv/bin/python" ]]; then
  LAB_PYTHON="$HOME/Desktop/FIN439/.venv/bin/python"
else
  print "Create a virtual environment and install requirements.txt first; see README.md."
  read "REPLY?Press Enter to close."
  exit 1
fi
cd "$COURSE_DIR"
print "Open http://127.0.0.1:8503 in your browser. Ctrl+C stops this app."
exec "$LAB_PYTHON" -m streamlit run Lab17/asof_app.py --server.headless true --server.address 127.0.0.1 --server.port 8503 --browser.gatherUsageStats false
