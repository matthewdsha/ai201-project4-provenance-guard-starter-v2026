#!/usr/bin/env python3
"""
Run this unit's five criteria once.  <- UNIT 9, MILESTONE 3

    python run_criteria.py --run 1
    python run_criteria.py --run 2
    python run_criteria.py --run 3

One invocation is one run of all five criteria in criteria.md ("Unit 9
criteria"). Each criterion starts its own fresh service with
`AI201_DEBUG=0 python app.py` on port 5061, as the criteria say, and stops it
afterwards. Nothing is changed between runs.

Everything each criterion produced is kept in results/criteria_run_<n>/:

    crit<k>_run.jsonl     the service's own request log for that criterion
    crit<k>_audit.jsonl   its audit log (kept out of logs/audit.jsonl)
    ../criteria_run_<n>.json   what the client saw and the checks it made

Whether a run met a target is decided here, in the check_* functions, from the
text of the criterion. The final MET / MISSED verdict across three runs is
filled in by hand in the README.
"""

import argparse
import itertools
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

import config
from measure import paragraph, p95

PORT = 5061
URL = f"http://127.0.0.1:{PORT}"

_SENTENCES = [
    "I went to the market on Saturday morning and bought apples, bread and a little cheese.",
    "The vendor was friendly, and we talked about the weather for a good while.",
    "Then I walked home slowly because the sun had finally come out after a week of rain.",
    "My sister called while I was cooking, and I burned the onions listening to her news.",
    "We decided to eat on the porch, even though the chairs still needed painting.",
    "Later the neighbours stopped by with a pie, and nobody got any work done.",
]
# Twenty different paragraphs of 30 to 60 words: every way of choosing 3 of the 6 sentences.
PARAGRAPHS_20 = [" ".join(_SENTENCES[i] for i in combo) for combo in itertools.combinations(range(6), 3)]


class Service:
    """A fresh `AI201_DEBUG=0 python app.py`, with its logs sent to one folder."""

    def __init__(self, folder: Path, name: str):
        self.run_log = folder / f"{name}_run.jsonl"
        self.audit_log = folder / f"{name}_audit.jsonl"
        for f in (self.run_log, self.audit_log):
            f.unlink(missing_ok=True)
        env = {**os.environ, "PORT": str(PORT), "HOST": "127.0.0.1", "AI201_DEBUG": "0",
               "AI201_RUN_LOG": str(self.run_log), "AI201_AUDIT_LOG": str(self.audit_log)}
        self.proc = subprocess.Popen([sys.executable, "app.py"], cwd=config.ROOT, env=env,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                requests.get(f"{URL}/health", timeout=1)
                return
            except requests.ConnectionError:
                time.sleep(0.5)
        self.stop()
        raise RuntimeError("the service did not start")

    def stop(self):
        self.proc.terminate()
        self.proc.wait(timeout=15)
        time.sleep(1)

    def rss_mb(self) -> float:
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(self.proc.pid)], capture_output=True, text=True)
        return int(out.stdout.strip() or 0) / 1024

    def run_log_lines(self) -> list[dict]:
        if not self.run_log.exists():
            return []
        return [json.loads(l) for l in self.run_log.read_text(encoding="utf-8").splitlines() if l.strip()]


def post(path: str, **kwargs):
    """POST and time it with perf_counter around the call. Returns (response, ms)."""
    started = time.perf_counter()
    resp = requests.post(f"{URL}{path}", timeout=120, **kwargs)
    return resp, (time.perf_counter() - started) * 1000


def submit(creator: str, text) -> tuple:
    return post("/submit", json={"text": text, "creator_id": creator})


# ── Criterion 1: warm latency ────────────────────────────────────────────────

def criterion_1(folder: Path, run: int) -> dict:
    svc = Service(folder, "crit1")
    try:
        submit("crit1_warmup", paragraph(10))
        times, statuses = [], []
        for i in range(1, 21):
            resp, ms = submit(f"crit1_{i:02d}", paragraph(10))
            times.append(round(ms, 1))
            statuses.append(resp.status_code)
    finally:
        svc.stop()
    p = round(p95(times), 1)
    ok = p <= 500 and all(s == 200 for s in statuses)
    return {"passed": ok, "value": f"p95 {p:.0f} ms, {statuses.count(200)}/20 ok",
            "p95_ms": p, "times_ms": times, "statuses": statuses}


# ── Criterion 2: cold start ──────────────────────────────────────────────────

def criterion_2(folder: Path, run: int) -> dict:
    svc = Service(folder, "crit2")
    try:
        resp, ms = submit("crit2_cold", paragraph(4))
    finally:
        svc.stop()
    ms = round(ms, 1)
    return {"passed": resp.status_code == 200 and ms <= 8000,
            "value": f"{ms:,.0f} ms, HTTP {resp.status_code}", "cold_ms": ms, "status": resp.status_code}


# ── Criterion 3: the request log is complete ─────────────────────────────────

def criterion_3(folder: Path, run: int) -> dict:
    svc = Service(folder, "crit3")
    sent = []  # (label, route, status the client got)
    try:
        def record(label, route, resp):
            sent.append({"label": label, "route": route, "status": resp.status_code})

        first_id = None
        for i, text in enumerate(PARAGRAPHS_20, 1):
            resp, _ = submit(f"crit3_valid_{i:02d}", text)
            record(f"valid {i}", "/submit", resp)
            if first_id is None and resp.status_code == 200:
                first_id = resp.json()["content_id"]

        ok_text = PARAGRAPHS_20[0]
        bad = [
            ("text missing", lambda: post("/submit", json={"creator_id": "crit3_b01"})),
            ("text empty", lambda: post("/submit", json={"text": "", "creator_id": "crit3_b02"})),
            ("text whitespace", lambda: post("/submit", json={"text": "    ", "creator_id": "crit3_b03"})),
            ("text is 12345", lambda: post("/submit", json={"text": 12345, "creator_id": "crit3_b04"})),
            ("creator missing", lambda: post("/submit", json={"text": ok_text})),
            ("body is a JSON list", lambda: post("/submit", json=[1, 2, 3])),
            ("body is not JSON", lambda: post("/submit", data="this is not json",
                                              headers={"Content-Type": "application/json"})),
            ("text 100,000 chars", lambda: post("/submit", json={"text": "word " * 20000, "creator_id": "crit3_b08"})),
            ("appeal unknown id", lambda: post("/appeal", json={"content_id": "does-not-exist", "reasoning": "typo"})),
            ("appeal no reasoning", lambda: post("/appeal", json={"content_id": first_id})),
        ]
        for label, send in bad:
            resp, _ = send()
            record(label, "/appeal" if label.startswith("appeal") else "/submit", resp)

        for i in range(1, 8):
            resp, _ = submit("crit3_burst", ok_text)
            record(f"burst {i}", "/submit", resp)
    finally:
        svc.stop()

    lines = svc.run_log_lines()
    problems = []
    if len(lines) != 37:
        problems.append(f"{len(lines)} lines, expected 37")
    ids = [l.get("request_id") for l in lines]
    if len(set(ids)) != len(ids):
        problems.append("request_id values are not unique")
    always = ("timestamp", "route", "status_code", "outcome", "total_ms")
    for n, l in enumerate(lines, 1):
        missing = [f for f in always if f not in l]
        if l.get("status_code") == 200 and l.get("route") == "/submit":
            missing += [f for f in ("model_ms", "style_ms", "guess", "combined_score") if f not in l]
        if missing:
            problems.append(f"line {n} is missing {missing}")
    if [l.get("status_code") for l in lines] != [s["status"] for s in sent]:
        problems.append("logged status codes differ from the statuses the client received, or are out of order")
    rate_limited = sum(1 for s in sent if s["status"] == 429)
    return {"passed": not problems,
            "value": f"{len(lines)}/37 lines, {len(problems)} problems",
            "problems": problems, "lines_logged": len(lines), "rate_limited_seen_by_client": rate_limited,
            "client_statuses": [s["status"] for s in sent], "sent": sent}


# ── Criterion 4: memory stays bounded ────────────────────────────────────────

def criterion_4(folder: Path, run: int) -> dict:
    svc = Service(folder, "crit4")

    def reading():
        values = []
        for _ in range(3):
            values.append(svc.rss_mb())
            time.sleep(1)
        return round(max(values), 1)

    try:
        statuses, at50 = [], None
        for i in range(1, 101):
            resp, _ = submit(f"crit4_{i:03d}", paragraph(10))
            statuses.append(resp.status_code)
            if i == 50:
                at50 = reading()
        at100 = reading()
    finally:
        svc.stop()
    growth = round(at100 - at50, 1)
    return {"passed": at100 <= 1000 and growth <= 100 and all(s == 200 for s in statuses),
            "value": f"{at50:.0f} MB at 50, {at100:.0f} MB at 100 (+{growth:.0f})",
            "mb_after_50": at50, "mb_after_100": at100, "growth_mb": growth,
            "non_200": [s for s in statuses if s != 200]}


# ── Criterion 5: the bad path ────────────────────────────────────────────────

def criterion_5(folder: Path, run: int) -> dict:
    svc = Service(folder, "crit5")
    ok_text = PARAGRAPHS_20[0]
    cases = [
        ("1 body is not JSON", lambda: post("/submit", data="this is not json", headers={"Content-Type": "application/json"}), 400, "invalid_json"),
        ("2 body is a JSON list", lambda: post("/submit", json=[1, 2, 3]), 400, "invalid_json"),
        ("3 text missing", lambda: post("/submit", json={"creator_id": "crit5_03"}), 400, "missing_text"),
        ("4 text is empty", lambda: post("/submit", json={"text": "", "creator_id": "crit5_04"}), 400, "missing_text"),
        ("5 text is only spaces", lambda: post("/submit", json={"text": "     ", "creator_id": "crit5_05"}), 400, "missing_text"),
        ("6 text is 12345", lambda: post("/submit", json={"text": 12345, "creator_id": "crit5_06"}), 400, "missing_text"),
        ("7 text is null", lambda: post("/submit", json={"text": None, "creator_id": "crit5_07"}), 400, "missing_text"),
        ("8 creator_id missing", lambda: post("/submit", json={"text": ok_text}), 400, "missing_creator_id"),
        ("9 text of 20,001 characters", lambda: post("/submit", json={"text": "a" * 20001, "creator_id": "crit5_09"}), 413, "text_too_long"),
        ("10 four words", lambda: post("/submit", json={"text": "Too short to check.", "creator_id": "crit5_10"}), 400, "not_enough_words"),
    ]
    results = []
    try:
        for label, send, want_status, want_error in cases:
            resp, ms = send()
            try:
                got_error = resp.json().get("error")
            except ValueError:
                got_error = None
            results.append({"case": label, "want": [want_status, want_error], "got": [resp.status_code, got_error],
                            "ms": round(ms, 1)})
        health = requests.get(f"{URL}/health", timeout=10).status_code
    finally:
        svc.stop()
    lines = svc.run_log_lines()
    for n, r in enumerate(results):
        r["logged_outcome"] = lines[n].get("outcome") if n < len(lines) else None
        r["ok"] = (r["got"] == r["want"] and r["logged_outcome"] == r["want"][1] and r["ms"] <= 50)
    good = sum(r["ok"] for r in results)
    return {"passed": good == 10 and health == 200,
            "value": f"{good}/10 correct, health {health}", "results": results, "health_after": health,
            "lines_logged": len(lines)}


CRITERIA = [criterion_1, criterion_2, criterion_3, criterion_4, criterion_5]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run this unit's five criteria once.")
    parser.add_argument("--run", type=int, required=True, help="1, 2 or 3")
    args = parser.parse_args()

    folder = config.ROOT / "results" / f"criteria_run_{args.run}"
    folder.mkdir(parents=True, exist_ok=True)
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = {"run": args.run, "started": started, "python": sys.version.split()[0], "criteria": {}}
    for k, fn in enumerate(CRITERIA, 1):
        print(f"criterion {k} ...", flush=True)
        result = fn(folder, args.run)
        out["criteria"][str(k)] = result
        print(f"  {'PASS' if result['passed'] else 'MISS'}  {result['value']}", flush=True)
    (config.ROOT / "results" / f"criteria_run_{args.run}.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"\nWritten to results/criteria_run_{args.run}.json and results/criteria_run_{args.run}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
