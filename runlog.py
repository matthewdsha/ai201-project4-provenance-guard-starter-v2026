"""
The request log: one JSON line per request in logs/run.jsonl.

Separate from audit.py on purpose. The audit log is the record of decisions and
keeps its nine-field shape. This one is the record of how the service ran:
what came in (route, input length), what came out (status, outcome) and how
long it took. It never stores the submitted text.
"""

import json
import threading
from datetime import datetime, timezone

import config

_lock = threading.Lock()


def write(**fields) -> dict:
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"), **fields}
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    with _lock:
        with config.RUN_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
