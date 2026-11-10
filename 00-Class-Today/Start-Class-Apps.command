#!/bin/zsh
set -e
cd "$(dirname "$0")/.."
mkdir -p 00-Class-Today/logs
for spec in Project2:8510 Lab19:8519; do
  folder=${spec%%:*}
  port=${spec##*:}
  if ! /usr/sbin/lsof -nP -iTCP:$port -sTCP:LISTEN >/dev/null 2>&1; then
    nohup .venv/bin/python -m streamlit run "$folder/app.py" --server.address 127.0.0.1 --server.port "$port" --browser.gatherUsageStats false >"00-Class-Today/logs/$folder.log" 2>&1 &
  fi
done
open http://127.0.0.1:8510
open http://127.0.0.1:8519
echo 'Class apps are running. Logs are in 00-Class-Today/logs.'
