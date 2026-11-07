#!/usr/bin/env python3
"""
Criteria 4 (appeal path) and 5 (bad input), which run_eval.py cannot express.

    python app.py                                  # in one terminal
    python run_eval_extra.py --label before        # in another

run_eval.py only POSTs dict bodies to /submit. Criterion 4 needs a submit and
then an appeal against the content_id that came back; criterion 5 needs a JSON
list and invalid JSON, which are not dicts. So this does those two, three
trials each, and writes results/run_extra_<date>_<label>.md with the real output
and a pass/fail per trial.
"""

import argparse
import datetime as dt
import json
import time

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"
TEXT = ("I walked down to the harbor this morning and the fog hadn't lifted, so the "
        "boats looked like they were floating in milk. My grandfather used to say "
        "that fog was the sea thinking.")


def log():
    return requests.get(f"{URL}/log", timeout=30).json()["entries"]


def criterion_4(trial):
    out = {"appeals": [], "checks": {}}
    ok = True
    ids = []
    for i in range(10):
        r = requests.post(f"{URL}/submit", timeout=90,
                          json={"text": f"{TEXT} Trial {trial} piece {i}.",
                                "creator_id": f"eval_appeal_{trial}_{i}"})
        ids.append(r.json().get("content_id"))
    before = {e["content_id"]: e for e in log() if e.get("content_id") in ids and e.get("event") != "appeal"}
    for cid in ids:
        r = requests.post(f"{URL}/appeal", timeout=30,
                          json={"content_id": cid, "reasoning": "I wrote this myself."})
        out["appeals"].append({"status": r.status_code, "body": r.json()})
        ok &= r.status_code == 200
    after = log()
    appeal_entries = [e for e in after if e.get("event") == "appeal" and e.get("content_id") in ids
                      and e.get("status") == "under_review"]
    out["checks"]["appeal_entries_found"] = f"{len({e['content_id'] for e in appeal_entries})}/10"
    ok &= len({e["content_id"] for e in appeal_entries}) == 10
    unchanged = all(
        next(e for e in after if e.get("content_id") == cid and e.get("event") != "appeal") == before[cid]
        for cid in ids)
    out["checks"]["original_decisions_unchanged"] = unchanged
    ok &= unchanged

    n_before = len([e for e in after if e.get("status") == "under_review"])
    r = requests.post(f"{URL}/appeal", timeout=30,
                      json={"content_id": "no-such-id", "reasoning": "typo"})
    n_after = len([e for e in log() if e.get("status") == "under_review"])
    out["unknown_id"] = {"status": r.status_code, "body": r.json(),
                         "new_under_review_entries": n_after - n_before}
    ok &= r.status_code == 404 and n_after == n_before
    return ok, out


def criterion_5(trial):
    cid = f"eval_bad_{trial}"
    cases = [
        ("missing text", {"json": {"creator_id": cid}}),
        ("empty text", {"json": {"text": "", "creator_id": cid}}),
        ("whitespace-only text", {"json": {"text": "   \n\t ", "creator_id": cid}}),
        ("non-string text", {"json": {"text": 12345, "creator_id": cid}}),
        ("missing creator_id", {"json": {"text": TEXT}}),
        ("body is a JSON list", {"json": [TEXT]}),
        ("invalid JSON", {"data": "{not json", "headers": {"Content-Type": "application/json"}}),
        ("100,000-character text", {"json": {"text": "word " * 20000, "creator_id": cid}}),
    ]
    rejections_before = len([e for e in log() if e.get("event") == "rejected"])
    results, ok = [], True
    for name, kwargs in cases:
        try:
            r = requests.post(f"{URL}/submit", timeout=120, **kwargs)
            try:
                body = r.json()
            except ValueError:
                body = None
            has_error = isinstance(body, dict) and "error" in body
            passed = 400 <= r.status_code < 500 and has_error
            results.append({"case": name, "status": r.status_code, "json_error": has_error,
                            "body": body if not has_error else body["error"], "pass": passed})
        except Exception as exc:  # noqa: BLE001
            passed = False
            results.append({"case": name, "status": None, "error": str(exc), "pass": False})
        ok &= passed
    new_rejections = len([e for e in log() if e.get("event") == "rejected"]) - rejections_before
    ping = requests.post(f"{URL}/ping", json={"message": "hi"}, timeout=10).status_code
    ok &= new_rejections >= 8 and ping == 200
    return ok, {"cases": results, "new_rejection_entries": new_rejections, "ping_after": ping}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    report = {}
    for name, fn in (("4. appeal path", criterion_4), ("5. bad input", criterion_5)):
        report[name] = []
        for trial in range(1, args.trials + 1):
            passed, detail = fn(trial)
            print(f"{name} trial {trial}: {'PASS' if passed else 'FAIL'}")
            report[name].append({"trial": trial, "pass": passed, **detail})
            time.sleep(61)  # keep per-minute limits (per-IP for no-creator rows) from interfering

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"run_extra_{stamp}{'_' + args.label if args.label else ''}.md"
    lines = [f"# Extra run log — {args.label}", "",
             "- Produced by: `run_eval_extra.py::main` (`criterion_4`, `criterion_5`)", ""]
    for name, trials in report.items():
        lines += [f"## {name}", "", "| Trial | Pass |", "|---|---|"]
        lines += [f"| {t['trial']} | {t['pass']} |" for t in trials]
        lines += ["", "```json", json.dumps(trials, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
