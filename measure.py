#!/usr/bin/env python3
"""
Measure what a run of Provenance Guard costs.  <- UNIT 9, SHAPE A

    python measure.py

Starts the service itself with the documented command (`python app.py`, on a
spare port, debug off so there is one process to measure), sends a fixed set
of submissions, and writes results/measure_<time>.md with:

  - the cold request (the first one, which loads gpt2) on its own,
  - warm requests: median, p95 and max, overall and by text length,
  - the service's memory before and after, and the model's size on disk,
  - one rejected request, so the failure path is exercised too.

Every request also lands in logs/run.jsonl, written by the service, with its
own model_ms and style_ms. That file is the run record.
"""

import os
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

import config

PORT = 5051
URL = f"http://127.0.0.1:{PORT}"
WARM_ROUNDS = 5  # each of the four lengths this many times -> 20 warm requests

_SENTENCES = [
    "I went to the market on Saturday morning and bought apples, bread and a little cheese.",
    "The vendor was friendly, and we talked about the weather for a good while.",
    "Then I walked home slowly because the sun had finally come out after a week of rain.",
    "My sister called while I was cooking, and I burned the onions listening to her news.",
    "We decided to eat on the porch, even though the chairs still needed painting.",
    "Later the neighbours stopped by with a pie, and nobody got any work done.",
]


def paragraph(n_sentences: int) -> str:
    return " ".join(_SENTENCES[i % len(_SENTENCES)] for i in range(n_sentences))


# Four lengths: about 20, 60, 150 and 300 words.
TEXTS = {
    "short (~20 words)": paragraph(1),
    "medium (~60 words)": paragraph(4),
    "long (~150 words)": paragraph(10),
    "very long (~300 words)": paragraph(20),
}


def rss_mb(pid: int) -> float:
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True)
    return int(out.stdout.strip() or 0) / 1024


def model_size_mb() -> float | None:
    folder = Path.home() / ".cache" / "huggingface" / "hub" / f"models--{config.DETECTOR_MODEL.replace('/', '--')}"
    if not folder.exists():
        return None
    # Follow the snapshot links, so each blob is counted once.
    blobs = folder / "blobs"
    return sum(f.stat().st_size for f in blobs.iterdir() if f.is_file()) / 1024 / 1024


def p95(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))]


def timed_post(creator: str, text: str) -> tuple[int, float]:
    started = time.perf_counter()
    resp = requests.post(f"{URL}/submit", json={"text": text, "creator_id": creator}, timeout=120)
    return resp.status_code, (time.perf_counter() - started) * 1000


def main() -> int:
    env = {**os.environ, "PORT": str(PORT), "HOST": "127.0.0.1", "AI201_DEBUG": "0"}
    server = subprocess.Popen([sys.executable, "app.py"], cwd=config.ROOT, env=env,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                requests.get(f"{URL}/health", timeout=1)
                break
            except requests.ConnectionError:
                time.sleep(0.5)
        else:
            print("The service did not start.")
            return 1

        rss_start = rss_mb(server.pid)

        # The cold request: the first one loads the model.
        status, cold_ms = timed_post("measure_cold", TEXTS["medium (~60 words)"])
        rss_loaded = rss_mb(server.pid)
        if status != 200:
            print(f"Cold request returned {status}; stopping.")
            return 1

        # Warm requests. A fresh creator_id each time keeps clear of the rate limit.
        by_length = {name: [] for name in TEXTS}
        counter = 0
        for _ in range(WARM_ROUNDS):
            for name, text in TEXTS.items():
                counter += 1
                status, ms = timed_post(f"measure_warm_{counter:02d}", text)
                if status != 200:
                    print(f"Warm request {counter} returned {status}; stopping.")
                    return 1
                by_length[name].append(ms)
        rss_end = rss_mb(server.pid)

        # The failure path: a request the route refuses.
        reject = requests.post(f"{URL}/submit", json={"text": "", "creator_id": "measure_bad"}, timeout=30)
    finally:
        server.terminate()
        server.wait(timeout=15)

    warm = [ms for values in by_length.values() for ms in values]
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out = config.ROOT / "results" / f"measure_{stamp}.md"
    size = model_size_mb()
    lines = [
        f"# Measurement run {stamp}",
        "",
        f"Command: `python measure.py` (starts `python app.py` on port {PORT}, debug off).",
        f"Python {sys.version.split()[0]}, model `{config.DETECTOR_MODEL}`"
        + (f", {size:.0f} MB on disk." if size else "."),
        "",
        "| Measure | Value |",
        "|---|---|",
        f"| Cold request (first, loads gpt2) | {cold_ms:,.0f} ms |",
        f"| Warm requests sent | {len(warm)} |",
        f"| Warm median | {statistics.median(warm):,.0f} ms |",
        f"| Warm p95 | {p95(warm):,.0f} ms |",
        f"| Warm max | {max(warm):,.0f} ms |",
        f"| Memory at start (before model) | {rss_start:,.0f} MB |",
        f"| Memory after cold request | {rss_loaded:,.0f} MB |",
        f"| Memory after warm requests | {rss_end:,.0f} MB |",
        f"| Rejected request (empty text) | HTTP {reject.status_code}, `{reject.json().get('error')}` |",
        "",
        "## Warm latency by text length",
        "",
        "| Text | n | Median | p95 |",
        "|---|---|---|---|",
    ]
    for name, values in by_length.items():
        lines.append(f"| {name} | {len(values)} | {statistics.median(values):,.0f} ms | {p95(values):,.0f} ms |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWritten to {out.relative_to(config.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
