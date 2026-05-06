#!/usr/bin/env bash
# TradeCore local startup script

set -e
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  source ".env"
fi

if [ -n "${VENV_PATH:-}" ] && [ -f "${VENV_PATH}/bin/activate" ]; then
  echo "[INFO] Activating virtualenv at ${VENV_PATH}"
  # shellcheck disable=SC1091
  source "${VENV_PATH}/bin/activate"
elif [ -f ".venv/bin/activate" ]; then
  echo "[INFO] Activating local virtualenv .venv"
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
else
  echo "[WARN] No virtualenv configured. Using system python3."
fi

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

echo "[INFO] Starting TradeCore on ${HOST}:${PORT}"
echo "[INFO] Logs: ${SCRIPT_DIR}/logs/app.log"

exec uvicorn app.main:app --host "${HOST}" --port "${PORT}" --reload
