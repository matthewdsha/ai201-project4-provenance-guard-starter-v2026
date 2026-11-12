# Acceptance criteria — Provenance Guard

> **Unit 9's five criteria are at the bottom of this file**, under "Unit 9 criteria". Everything above them is from units 7 and 8 and is kept exactly as written.

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives: plain human writing is never called AI

Submit 10 paragraphs of human-written text to `/submit`, at least 4 of them deliberately plain (short sentences, common words, the way a second-language writer might write). At most 1 of the 10 is labelled high-confidence AI, and none of the plain ones is; at worst they land in "unsure". This has to hold in each of three trials, not on average.

**Why this target:** On a writing site a wrong accusation costs a real person a lot and a missed detection costs the site a little. The plain inputs are the ones that matter most: signal one is most likely to accuse plain and second-language writers, they get flagged every time they submit rather than once, and my appeal path only records the complaint, since nothing re-checks it. So the target is zero, not "one in ten", for those writers.

## 2. Score spread: clearly-AI and clearly-human text are far apart

Submit one paragraph pasted from an AI chatbot's reply and one human-written paragraph with a clearly personal voice (informal, specific, a bit messy). The AI paragraph's combined score (`confidence` in the response) is at least 0.40 higher than the human one, in each of three trials.

**Why this target:** If the two sit close together, the thresholds are cutting through noise and every label is a coin flip. My unsure band is 0.40 wide (0.35 to 0.75), so a gap of 0.40 means the clear cases at least sit on opposite sides of it. It is a single pair, not a rate, so it checks the best case: if even that is close, nothing else will separate.

## 3. Label coverage: all three labels are reachable and land where they should

Submit four inputs: a clearly AI paragraph, a clearly human one, a plainly written human one, and a lightly-edited AI paragraph (an AI paragraph with a few words swapped). All three labels (`human`, `unsure`, `ai`) appear at least once across them. The clearly AI paragraph gets `ai` and the clearly human one gets `human` in all three trials.

**Why this target:** A label no input can produce is a gap in my ranges, not a design choice. This also checks that signal two actually varies: a stub style signal that always returns 0.5 would make the human label unreachable.

---

## 4. The appeal path: an appeal always changes status and is always recorded

For 10 appeals on valid content_ids, all 10 return 200, all 10 add an `appeal` entry to the audit log with `status: under_review`, and the original decision entry is unchanged. An appeal on an unknown content_id returns 404 and writes no `under_review` entry.

**Why this target:** The appeal is the only thing between a wrong accusation and nothing at all, so it has to work every time, not most of the time. The 404 clause covers the typo case, where a silent failure would look like a broken endpoint, and the unchanged original is what makes the log an audit trail.

---

## 5. Bad input: malformed requests never crash the service

Eight bad submissions get a 4xx with a JSON `error` code, none gets a 500, and each leaves a rejection entry in the log: missing `text`, empty `text`, whitespace-only `text`, non-string `text`, missing `creator_id`, a body that is a JSON list, invalid JSON, and a 100,000-character `text`. `/ping` still answers afterwards.

**Why this target:** A crash on malformed input is one of the most common real failures, and unit 8's attack set will send exactly these. A 500 means my handler broke rather than refused. Logging the rejection matters because an attack that leaves no trace can't be diagnosed.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 9 criteria — the operational layer

These five test what this unit added: the run path, the structured log
(`logs/run.jsonl`) and the numbers `measure.py` reports. None of them is about
how well the detector tells human from AI; that is units 7 and 8, and I am not
changing it this unit. Each one is run in three trials, and a trial that misses
the target is a miss.

**How every criterion is run.**
- The machine is an M1 MacBook, 8 GB, CPU only, Python 3.13.7. The millisecond
  and megabyte targets are for this machine; on another one the numbers would
  differ with nothing wrong in the system.
- The service is started with `AI201_DEBUG=0 python app.py`. Without that,
  debug mode starts a reloader parent and a worker, which are two processes
  with very different memory. The gpt2 model is already on disk, and no other
  copy of this service is running.
- "Warm" means after the first `/submit` of that process.
- Requests are sent one at a time, in the order given, with the `requests`
  library. Timing is `time.perf_counter()` around the `requests.post` call.
- Every request has its own `creator_id` (for example `crit_01`, `crit_02`)
  unless a criterion says otherwise, so the rate limit of 5 a minute per
  creator does not get involved.
- Only `/submit` and `/appeal` write to `logs/run.jsonl`. Calls to `/health`
  and `/ping` leave no line and are not counted anywhere below.

## 1. Warm latency: a typical submission comes back in half a second

After one warm-up request, send 20 submissions of the same paragraph (the
10-sentence paragraph that `measure.py` in this repository builds with
`paragraph(10)`, about 150 words) and time each. The 19th-fastest of the 20 (the p95) is at most **500
ms**, and all 20 return 200. In each of three trials, each on a freshly
started service.

**Why this target:** My two measurement runs put the p95 for a text this long at
190 ms and 570 ms, so the run-to-run spread is about two to three times and 500
sits inside it: a target I might miss, which is the point. Under about half a
second a writer does not notice the check; at a full second they do. A looser
target such as 1,000 ms would pass even on the slow run and tell me nothing. A
stricter one such as 250 ms would be a claim about my laptop on a good day, not
about the system, because gpt2 on a CPU is the entire cost (`style_ms` is 0.1 to
0.4 ms).

## 2. Cold start: the first submission after a restart works, and within 8 seconds

Start the service, wait until `/health` answers, then send one submission of
about 60 words (`paragraph(4)` from `measure.py`) and time it. It returns 200 in
at most **8,000 ms**. Do this three times, stopping and restarting the service
each time, straight after each other. This is a restart with the model files
recently read, so the operating system still has them in its file cache. A first
start after a reboot would be slower, and this criterion does not test that.

**Why this target:** The first request is the one that loads gpt2, and it is the
request a restart or a deploy makes someone wait for. I measured 7,478, 5,934,
6,007 and 3,811 ms, all on back-to-back restarts, so 8 s leaves little room
above the slowest. A looser 15 s (the course's own estimate of "ten to twenty
seconds") would hide a regression of more than a second; a stricter 5 s would
already be missed by half of my earlier measurements and would be a claim about
a faster machine.

## 3. The request log is complete and consistent: one line per request, none missing

Start the service with `AI201_RUN_LOG` pointing at a new empty file inside a
folder that already exists (for example `logs/crit3_trial1.jsonl`; the service
creates only the default `logs/` folder, and a path in a missing folder makes
every request fail inside the log hook). Send these
37 requests, one at a time, in this order:

- 20 valid submissions of different paragraphs of 30 to 60 words.
- 10 bad requests: `text` missing, `text` empty, `text` whitespace only,
  `text` set to the number 12345, `creator_id` missing, a body that is a JSON
  list, a body that is not JSON, `text` of 100,000 characters (`"word "` repeated
  20,000 times), an appeal for a `content_id` that does not exist, and an appeal
  with no `reasoning`.
- 7 submissions, one straight after another, all with `creator_id` `crit_burst`.
  The rate limit rejects the last two.

Then read the file back. It has **exactly 37 lines**, every `request_id` is
unique, every line has `timestamp`, `route`, `status_code`, `outcome` and
`total_ms`, every successful `/submit` also has `model_ms`, `style_ms`, `guess`
and `combined_score`, and each line's `status_code` equals the status the client
received for that request, in the same order. In each of three trials.

**Why this target:** The log is the only evidence this unit produces, so a
missing line is worse than a slow request. My own README argues that a failure
that shows only as an absence is one I will never find, and the rate-limit 429
comes from an error handler rather than from the route, which is exactly the
kind of path where a hook could silently not fire. The target is exact (37 of
37) because "most requests are logged" cannot be told apart from a leak in the
logging.

## 4. Memory stays bounded: no growth across 100 submissions

Start the service in the background (`AI201_DEBUG=0 python app.py &`) and note
its process id with `$!` straight afterwards. Do not look the id up with
`lsof` on port 5000: on macOS the AirPlay Receiver (`ControlCenter`) also
listens there and shows up as a second process. Then send 100 submissions of the 150-word paragraph
from criterion 1. After request 50 and again after request 100, read the
resident memory with `ps -o rss= -p <pid>` three times, one second apart, take
the largest, and divide by 1,024 to turn kilobytes into megabytes. The reading
after 100 is at most **1,000 MB**, and it is no more than **100 MB** above the
reading after 50. In each of three trials, each on a freshly started service.

**Why this target:** This is the question I left open. In one measurement run
memory went from 438 to 722 MB over 20 requests, which looks like a leak, and in
the next it went from 818 to 780 MB, which does not. Readings on macOS wobble by
tens of megabytes, so taking the largest of three keeps one low reading from
hiding growth. If the service grows with every request it cannot run
unattended, which is the whole point of this unit's run path. The 1,000 MB
ceiling is the loaded model plus headroom on an 8 GB machine; a lower one would
fail on the 818 MB I already measured with nothing wrong, and a higher one would
stop meaning anything on this machine. Comparing request 100 to request 50
separates a model that is simply large from one that keeps growing.

## 5. The bad path: ten bad requests get the right refusal, quickly, and the service survives

Start the service, then send these ten requests, each with its own
`creator_id` except requests 1, 2 and 8, which have none. Each must return exactly the status and `error`
code in the table, none may return a 500 or a 429, each must leave a line in
`logs/run.jsonl` whose `outcome` equals that `error`, each must be answered in at
most **50 ms**, and `/health` must still answer afterwards. In each of three
trials, each on a freshly started service: requests 1, 2 and 8 are counted
against the caller's address, the limit is 5 a minute, and the counter lives in
the running process, so a second trial against the same process within a minute
would be rate limited for a reason that has nothing to do with validation.

| # | The request | Status | `error` |
|---|---|---|---|
| 1 | a body that is not JSON | 400 | `invalid_json` |
| 2 | a body that is a JSON list | 400 | `invalid_json` |
| 3 | `text` missing | 400 | `missing_text` |
| 4 | `text` is `""` | 400 | `missing_text` |
| 5 | `text` is only spaces | 400 | `missing_text` |
| 6 | `text` is the number 12345 | 400 | `missing_text` |
| 7 | `text` is `null` | 400 | `missing_text` |
| 8 | valid `text`, `creator_id` missing | 400 | `missing_creator_id` |
| 9 | `text` of 20,001 characters | 413 | `text_too_long` |
| 10 | `text` of four words, "Too short to check." | 400 | `not_enough_words` |

**Why this target:** Of the five criteria this is the one about things going
wrong. Naming the exact code matters: a 429 or a wrong 4xx is also fast, logged
and JSON, so "any 4xx" would pass without testing that validation caught the
input. The 50 ms limit exists because a refusal should happen before gpt2 runs:
in my session log the refusals took 0.4 to 0.8 ms and a real submission takes
about 60 ms or more, so 50 ms passes if validation runs first and fails if a bad
input ever reaches the model. That matters because an oversized text is the
cheapest possible way to make the service do expensive work. I chose 50 ms rather
than 5 because the point is to tell "refused up front" from "scored and then
rejected", and a timing target tight enough to fail on laptop noise would test
the laptop.
