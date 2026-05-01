#!/usr/bin/env bash
# startup.sh - launch frontend + backend stack with venv and readiness checks

set -e
set -o pipefail

# --- LOAD ENV CONFIG ---
source "$(dirname "$0")/.env"

# --- FRONTEND ---
echo "[INFO] Starting frontend (npm run dev)..."
cd "$FRONTEND_PATH"
npm run dev &
FRONTEND_PID=$!

# --- BACKEND: Activate Python environment ---
echo "[INFO] Activating Python environment..."
source "$VENV_PATH/bin/activate"

# --- BACKEND: Start Wine server ---
echo "[INFO] Starting Wine server..."
wine server -p &
WINE_SERVER_PID=$!

# --- BACKEND: MT5 bridge ---
echo "[INFO] Starting MT5 Linux bridge via Wine..."
export WINEPREFIX
wine "$PYTHON_EXE" -m mt5linux &
MT5_PID=$!

# --- BACKEND: Wait for MT5 bridge readiness ---
echo "[INFO] Waiting for MT5 bridge to be ready on port $MT5_PORT..."
until nc -z localhost $MT5_PORT; do
    sleep 1
done
echo "[INFO] MT5 bridge is ready."

# --- BACKEND: FastAPI server ---
echo "[INFO] Starting FastAPI backend (Uvicorn)..."
cd "$BACKEND_PATH"
uvicorn main:app --reload &
UVICORN_PID=$!

# --- MONITOR ---
echo "[INFO] Frontend PID: $FRONTEND_PID"
echo "[INFO] Wine server PID: $WINE_SERVER_PID"
echo "[INFO] MT5 bridge PID: $MT5_PID"
echo "[INFO] Uvicorn PID: $UVICORN_PID"

wait
