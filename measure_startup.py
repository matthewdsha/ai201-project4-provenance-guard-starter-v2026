#!/usr/bin/env python3
"""
Time a restart: how long until the service can answer, and until it has
answered a real submission.  <- UNIT 9, THE IMPROVEMENT

    python measure_startup.py --label before
    python measure_startup.py --label after

Three times: start `AI201_DEBUG=0 python app.py` on a spare port, then record

  ready_ms   from starting the process until /health answers
  first_ms   how long the first /submit then takes
  total_ms   ready_ms + first_ms: from start until a writer has a label

The logs go to a scratch folder, not to logs/. Writes results/startup_<label>.md.
"""

import argparse
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests

import config
from measure import paragraph

PORT = 5062
URL = f"http://127.0.0.1:{PORT}"


def one_restart(scratch: Path, n: int) -> dict:
    env = {**os.environ, "PORT": str(PORT), "HOST": "127.0.0.1", "AI201_DEBUG": "0",
           "AI201_RUN_LOG": str(scratch / f"run_{n}.jsonl"), "AI201_AUDIT_LOG": str(scratch / f"audit_{n}.jsonl")}
    started = time.perf_counter()
    proc = subprocess.Popen([sys.executable, "app.py"], cwd=config.ROOT, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        while True:
            try:
                requests.get(f"{URL}/health", timeout=1)
                break
            except requests.ConnectionError:
                time.sleep(0.1)
                if time.perf_counter() - started > 120:
                    raise RuntimeError("the service did not start")
        ready_ms = (time.perf_counter() - started) * 1000
        loaded = requests.get(f"{URL}/health", timeout=5).json().get("detector_loaded")
        t = time.perf_counter()
        resp = requests.post(f"{URL}/submit", json={"text": paragraph(4), "creator_id": f"startup_{n}"}, timeout=120)
        first_ms = (time.perf_counter() - t) * 1000
    finally:
        proc.terminate()
        proc.wait(timeout=15)
        time.sleep(1)
    return {"ready_ms": ready_ms, "first_ms": first_ms, "total_ms": ready_ms + first_ms,
            "loaded_at_health": loaded, "status": resp.status_code}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    label = parser.parse_args().label
    with tempfile.TemporaryDirectory() as tmp:
        runs = [one_restart(Path(tmp), n) for n in (1, 2, 3)]
    lines = [f"# Startup timing: {label}", "",
             "| Restart | Until /health answers | model loaded at /health | First /submit | Start until first label | HTTP |",
             "|---|---|---|---|---|---|"]
    for n, r in enumerate(runs, 1):
        lines.append(f"| {n} | {r['ready_ms']:,.0f} ms | {r['loaded_at_health']} | {r['first_ms']:,.0f} ms | "
                     f"{r['total_ms']:,.0f} ms | {r['status']} |")
    lines.append(f"| median | {statistics.median(r['ready_ms'] for r in runs):,.0f} ms | | "
                 f"{statistics.median(r['first_ms'] for r in runs):,.0f} ms | "
                 f"{statistics.median(r['total_ms'] for r in runs):,.0f} ms | |")
    text = "\n".join(lines) + "\n"
    (config.ROOT / "results" / f"startup_{label}.md").write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
