#!/bin/zsh
cd "${0:A:h}"
if [[ -x ../.venv/bin/python ]]; then
  CLASS_PYTHON=../.venv/bin/python
elif [[ -x .venv/bin/python ]]; then
  CLASS_PYTHON=.venv/bin/python
else
  echo "Install the environment using README.md first."
  exit 1
fi
exec "$CLASS_PYTHON" -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false
