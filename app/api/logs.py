import re
from pathlib import Path
from fastapi import APIRouter, Query

router = APIRouter()

# Matches lines written by the logging.py dictConfig formatter:
# "2026-05-06 10:23:01,123 | INFO | tradecore | Some message"
_LOG_RE = re.compile(
    r"^(?P<time>\d{4}-\d{2}-\d{2} [\d:,]+)\s*\|\s*(?P<level>\w+)\s*\|\s*(?P<name>[^|]+)\s*\|\s*(?P<msg>.+)$"
)

_LEVEL_MAP = {
    "DEBUG": "INFO",
    "INFO": "INFO",
    "WARNING": "WARN",
    "WARN": "WARN",
    "ERROR": "ERROR",
    "CRITICAL": "ERROR",
}


@router.get("/logs")
def logs(
    limit: int = Query(default=200, ge=1, le=2000),
    severity: str = Query(default="ALL", description="ALL | INFO | WARN | ERROR"),
):
    log_path = Path("logs/app.log")
    if not log_path.exists():
        return {"status": "success", "data": []}

    try:
        lines = log_path.read_text(errors="replace").splitlines()
    except OSError:
        return {"status": "error", "message": "Could not read log file"}

    items = []
    for line in reversed(lines):
        m = _LOG_RE.match(line.strip())
        if not m:
            continue
        mapped_level = _LEVEL_MAP.get(m.group("level").upper(), "INFO")
        if severity != "ALL" and mapped_level != severity:
            continue
        items.append(
            {
                "time": m.group("time"),
                "event": m.group("msg").strip(),
                "severity": mapped_level,
                "logger": m.group("name").strip(),
            }
        )
        if len(items) >= limit:
            break

    return {"status": "success", "data": items}