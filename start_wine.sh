#!/usr/bin/env bash
# run_mt5.sh - launch MT5 Linux bridge via Wine

set -e  # exit on error
set -o pipefail

# --- CONFIG ---
WINEPREFIX="$HOME/.mt5"
PYTHON_EXE="$WINEPREFIX/drive_c/users/urangani/AppData/Local/Programs/Python/Python311/python.exe"

# --- MAIN ---
echo "[INFO] Using Wine prefix: $WINEPREFIX"
export WINEPREFIX

if [ ! -f "$PYTHON_EXE" ]; then
  echo "[ERROR] Python executable not found at:"
  echo "        $PYTHON_EXE"
  exit 1
fi

echo "[INFO] Starting MT5 Linux bridge..."
wine "$PYTHON_EXE" -m mt5linux
