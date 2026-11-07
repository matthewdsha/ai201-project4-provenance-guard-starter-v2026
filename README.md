# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A submission takes seven steps from arriving to the label a reader sees.

1. **Arrives** at `POST /submit` as JSON `{text, creator_id}`. Nothing is judged yet.
2. **Input check** (`app.py`). Adds a refusal for bad input: a non-JSON body, a missing or blank `text` or `creator_id`, or text too short to score gets a 400 with a plain error code.
3. **Signal one** (`detector.model_signal`). Adds `model_score`: how predictable a local language model (gpt2) finds the text. Higher means more likely AI.
4. **Signal two** (`stylometry.style_signal`). Adds `style_score`: the shape of the text (sentence-length spread and punctuation variety). Higher means more likely AI.
5. **Combine** (`scoring.combine_signals`). Adds `combined_score`, one 0–1 number from the two signals.
6. **Label** (`scoring.score_to_label`). Adds `guess` (`human`, `unsure` or `ai`) and `label`, the plain-language sentence the writer sees.
7. **Log, then answer.** `audit.log_decision` writes the decision with a new `content_id` and `status: decided`. The response returns the label, both signal scores and the `content_id`. If the writer disagrees, `POST /appeal` with that `content_id` appends an appeal entry and sets the status to `under_review`. The original decision is never overwritten.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity under gpt2 (`detector.py`): how surprised a language model is by each next word, squashed onto 0–1. Low perplexity gives a high AI score.

**Why that might differ between human and AI writing:** A model writes by picking likely next words, so its output is easy for a model to predict. Human prose has odd word choices and specifics a model doesn't expect.

**What it can't see:**
- **Predictable is not the same as machine-written.** Plain, common-word, short-sentence human writing scores as AI: non-native writers, younger writers, anyone writing simply on purpose. My plain human samples scored 0.66 against 0.80 for clearly AI text.
- **Famous or memorised text reads as machine-like.** The opening of Darwin's *Origin of Species* scored 0.65, probably because gpt2 has seen it. Formal prose does not automatically read human.
- **Edits shift the score a little, not a lot.** Lightly editing AI text moved it from 0.80 to 0.70.
- **It only reads the first ~300 words** (400 tokens), so anything later is invisible.
- **gpt2 is old.** Text from a modern model is not especially predictable *to gpt2*.

### Signal two — the style signal

**What it measures:** The shape of the text (`stylometry.py`), not its meaning. Two measures, each scaled to 0–1 and flipped so higher means more AI, then combined 0.6 / 0.4:
- **Sentence-length spread** (standard deviation ÷ mean of sentence length). Low means more AI. At or above 0.65 reads fully human; at or below 0.25 fully AI. Weight 0.6.
- **Punctuation variety:** how many of nine mark kinds (commas, semicolons, colons, dashes, brackets, quotes, `!`, `?`) appear at all. Narrow means more AI. At or above 0.45 of the kinds reads fully human. Weight 0.4.
- **Type-token ratio is computed but not scored.** On my inputs it ran the wrong way: the AI sample had the more varied vocabulary (0.89 against 0.86 for clearly human). With five samples that is an observation, not a finding, but I won't score on a measure pointing the wrong way.
- A text under two sentences has no spread, so it gets a neutral 0.5.

**Why that might differ between human and AI writing:** "Most likely next word" pushes generated prose toward even, mid-length sentences. Human writing is lumpier.

**What it can't see:**
- **It cannot read.** Meaning is invisible to it.
- **Plain human writing looks even.** A plain paragraph I wrote with short sentences and no commas scored **0.97**, higher than the AI text (0.80). Short, simple sentences are exactly what this measures as machine-like.
- **Cheap shape edits fool it.** Typos, chopped-up sentences, a pasted quotation or inserted fragments make AI text look lumpy.
- **Genre confuses it.** Lists, legal text, and technical or children's writing have uniform shape for innocent reasons.
- **Short texts are noisy.** The 0.65 / 0.25 scaling points are my reading of five inputs, not a calibrated standard.

The two blind spots are different (word choice vs shape), but they overlap on the one group that matters most: plain human writing is wrongly accused by both.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** The expensive mistake is accusing a real writer, so it takes both signals to agree before anyone is called AI. The combined score is a 50 / 50 average of the two. But if either signal alone is below the human threshold, the combined score is capped just under the AI threshold. When the signals split, the writer lands in "unsure", never "AI". The cost is that AI text that fools one signal gets through. I accept that.

**What the rule can't do:** It cannot rescue someone both signals get wrong. A plain human paragraph scored 0.66 and 0.97, so it combines to about 0.81, the same as clearly AI text. Averaging and capping don't help when both signals are wrong in the same direction. Only the thresholds can, and moving them also lets AI text through.

**The numbers:** Weights 0.5 / 0.5 (`config.py`). Cap on the combined score: `AI_THRESHOLD - 0.01`, applied when `min(model, style) < HUMAN_THRESHOLD`. Thresholds: `HUMAN_THRESHOLD` 0.35 and `AI_THRESHOLD` 0.75 (see Label Variants), so the cap is 0.74.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

The opening of Darwin's *Origin of Species* (formal human writing). The model signal scored it **0.65**: gpt2 finds it predictable, probably because it is a famous text it has seen. The style signal scored it **0.37**: the sentences are long and uneven and the punctuation is varied, so it looks human. The two disagree about which side of the line it is on.

The rule averages them to **0.51**, which is "unsure". The cap did not apply, since the lower score (0.37) is just above the human threshold of 0.35. The averaging alone kept a human text out of "AI". The tie goes to "unsure", not "AI".

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.75 | We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything. |
| high-confidence AI | 0.75 – 1.00 | This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review. |

The score is the combined score (higher means more likely AI). The ranges come from `scoring.label_ranges()` and the cutoffs are `HUMAN_THRESHOLD = 0.35` and `AI_THRESHOLD = 0.75` in `config.py`. I raised the AI cutoff from the starter's 0.65 because 0.65 would have labelled a plain human paragraph (combined 0.63) one notch from AI, and a false accusation costs more than a missed detection.

**Why I worded the "unsure" one this way:**

It is the label a real writer is most likely to get on their own work, so it opens with what we don't know ("We can't tell"), not with a suspicion. It then says plainly that nothing is wrong and nothing needs doing, so the writer isn't left wondering whether they've been accused. It doesn't mention AI as the likely cause or quote a number.

The AI label is hedged on purpose, too: it says "may have been" and that the check "can be wrong, especially for plain, simple writing and for people writing in a second language", because those are the writers it is most likely to get wrong. It only promises what the service does: an appeal is recorded and the submission is marked for review. Nothing re-checks it automatically and no reviewer exists inside this service, so the label doesn't say a person will look.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The meeting went fine. We talked about the budget and the schedule for next month. Most people agreed that we should wait before making a decision. I think that is probably the right call for now. Dana said she would send the notes by Friday. I will check with Sam about the room. We can meet again in two weeks if nothing changes.", "creator_id": "matt"}'
```

```json
{
  "confidence": 0.8132,
  "content_id": "a8d83f8a-c0a9-4793-addc-69d263493fe6",
  "guess": "ai",
  "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.",
  "model_score": 0.6595,
  "style_score": 0.9668
}
```

*(The text is one of my test paragraphs, a plainly written human one. It is also the false-positive case: it comes back "ai", which is why the appeal below exists.)*

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "a8d83f8a-c0a9-4793-addc-69d263493fe6", "reasoning": "I wrote this myself. I keep my sentences short and simple on purpose."}'
```

```json
{
  "content_id": "a8d83f8a-c0a9-4793-addc-69d263493fe6",
  "message": "We've recorded your appeal and marked this submission as under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8132,
      "content_id": "a8d83f8a-c0a9-4793-addc-69d263493fe6",
      "creator_id": "matt",
      "guess": "ai",
      "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.",
      "model_score": 0.6595,
      "status": "decided",
      "style_score": 0.9668,
      "timestamp": "2026-10-31T02:22:53+00:00"
    },
    {
      "content_id": "a8d83f8a-c0a9-4793-addc-69d263493fe6",
      "creator_id": "matt",
      "event": "appeal",
      "reasoning": "I wrote this myself. I keep my sentences short and simple on purpose.",
      "status": "under_review",
      "timestamp": "2026-10-31T02:22:53+00:00"
    }
  ]
}
```

The log is append-only: the original decision (`status: decided`) is untouched, and the appeal sits after it with `status: under_review`.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I had Claude check my criteria in `criteria.md` before I built anything. First I took my false-positive criterion ("at most 1 of 10 of my own pieces labelled high-confidence AI") and asked for the message a real writer would send if they were the one person that rate allows, without being told whether my number was right. Then I had it read all five against the grading rubric and tell me whether someone who didn't write them could run each one without asking me.
- *What came back:* The writer's message was from an international student whose scholarship essay was flagged and whose appeal had gone unanswered with a Friday deadline. It showed that my 1 in 10 was an average over a set where only 4 pieces were plain, so the one allowed miss could land on a plain or second-language writer, who gets flagged every time and whose only recourse is an appeal that nothing re-checks. The rubric read found that criteria 1 to 3 pointed at "my own pieces" and "my calibration inputs", which a stranger couldn't get hold of.
- *What I changed:* I tightened criterion 1 so none of the plain pieces may be labelled high-confidence AI, and rewrote its "why" to say the allowance can't be spent on the writers with the least room to argue back. I reworded criteria 1 to 3 so each says what to submit and what to check.

**Moment 2**

- *What I asked for:* I had a fresh Claude agent with no context read only my three label texts and say, as the writer, what it would think each one said about it and what it would do next.
- *What came back:* The human and unsure labels landed as I meant them to. The AI label read as an accusation even with the hedging. Naming "plain, simple writing" and "second language" as reasons the check might be wrong could read as being told one's writing is the problem. "Recorded" and "marked for review" could sound ominous, and finding the content ID is left to the writer.
- *What I changed:* Nothing in the label text yet. The check showed me the problem, but I haven't decided how to reword it, and the 0.81 false positive on plain writing stays however the label is worded. I've left it as an open item.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
A real writer submits a few pieces an hour, so 5 a minute leaves room for a
burst of retries and 50 a day is far more than one person writes. A script
mapping my thresholds with a thousand variations is stopped after 5 in the
first minute and would need about 20 days to send a thousand. I didn't go lower because each 429 punishes a legitimate writer who resubmits after an edit.

**What a caller counts as:** the `creator_id` in the request body, falling back to the caller's IP address when it's missing or invalid. Per-creator limits don't penalise a shared household address. The weakness is that a script can rotate `creator_id` values to get a fresh quota each time, so this limiter slows a single identity and doesn't stop a determined attacker.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15` (full report: `results/flood_2026-11-07_0530.md`)

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

10 of 15 were rate limited, and each rejection appears in `GET /log` with
`reason: rate_limited`.

---

## Attack Run — Before

Full table with every attack, status, content ID, score and verdict:
`results/attack_run_2026-11-07_0559_before.md`. 56 attacks sent with
`python run_attacks.py --set attack_set --label before`.

**How I marked them.** Thresholds are 0.35 / 0.75.
- *evasion* and *prompt_injection* inputs built from AI text: **HELD** only if the service still said "ai" (or, for injections that targeted something other than the label, if that target stayed intact). Anything that got "human" or "unsure" for AI text is **BROKE**.
- *false_positive*: **HELD** if the writer was not accused ("human" or "unsure"); **BROKE** if the label was "ai".
- *malformed*: **HELD** if the service refused cleanly or scored without crashing and without a confident claim; **BROKE** if junk got a confident label.
- *flood*: **HELD** if the limiter cut in.

| Family | Attacks | Held | Broke | Broke: which |
|---|---|---|---|---|
| evasion | 10 | 1 | 9 | EV01–EV09 (only EV10, the repeated stanza, was still called "ai") |
| false_positive | 8 | 4 | 4 | FP02, FP03, FP04, FP05 called "ai": four real writers accused |
| prompt_injection | 6 | 5 | 1 | PI02 (fake SYSTEM line) came back "human" 0.203 |
| malformed | 20 | 18 | 2 | MF03 (control characters) and MF04 (only punctuation) got a confident "human" |
| flood_same_creator | 12 | 12 | 0 | 5 got 200, then 7 got 429 |
| **Total** | **56** | **40** | **16** | |

Notes on the held rows: no attack caused a 500. RQ10 and RQ11 returned 429
because the malformed rows all share my IP address and had used up its 5 per
minute, so those two never reached my route. They are not evidence the route
handles form-encoded bodies. MF08 (60,000 characters) was accepted and scored
"ai" 0.811 from only its first 400 tokens, so there is no size cap.

**Ten audit log entries from the run** (`GET /log`, pasted as text. The first
four are the false accusations, then evasions and junk that got "human", the one
evasion that held, a rate-limit rejection from the flood rows, and a rejected
request from my own route; rejections carry fewer fields than decisions):

```json
{"combined_score": 0.8439, "content_id": "d8459e4a-6535-4977-a1a0-cdef7b53d1a2", "creator_id": "attacker_FP03", "guess": "ai", "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.", "model_score": 0.8051, "status": "decided", "style_score": 0.8827, "timestamp": "2026-11-07T11:59:28+00:00"}
{"combined_score": 0.8307, "content_id": "6e37fbd6-e96d-4cd7-a737-4ff88929e129", "creator_id": "attacker_FP05", "guess": "ai", "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.", "model_score": 0.8005, "status": "decided", "style_score": 0.8609, "timestamp": "2026-11-07T11:59:28+00:00"}
{"combined_score": 0.8199, "content_id": "63387ae0-190d-4e40-b95d-6b63d4cab183", "creator_id": "attacker_FP02", "guess": "ai", "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.", "model_score": 0.7387, "status": "decided", "style_score": 0.9012, "timestamp": "2026-11-07T11:59:28+00:00"}
{"combined_score": 0.7795, "content_id": "c8c18d5d-29db-4d98-b269-e3302cb9603d", "creator_id": "attacker_FP04", "guess": "ai", "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.", "model_score": 0.8329, "status": "decided", "style_score": 0.7262, "timestamp": "2026-11-07T11:59:28+00:00"}
{"combined_score": 0.2619, "content_id": "eb3dd420-4311-42cc-8215-3786292d65ce", "creator_id": "attacker_EV05", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.3212, "status": "decided", "style_score": 0.2025, "timestamp": "2026-11-07T11:59:28+00:00"}
{"combined_score": 0.2035, "content_id": "03a6d973-c836-4295-b577-52e2a3c54e26", "creator_id": "attacker_PI02", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.2044, "status": "decided", "style_score": 0.2025, "timestamp": "2026-11-07T11:59:29+00:00"}
{"combined_score": 0.25, "content_id": "e4a1a0db-50e4-4faf-9c81-cdfa313f7ee6", "creator_id": "attacker_MF03", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.0, "status": "decided", "style_score": 0.5, "timestamp": "2026-11-07T11:59:29+00:00"}
{"combined_score": 0.3056, "content_id": "f7cf214f-1578-4b6c-b72c-373518687383", "creator_id": "attacker_MF04", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.0112, "status": "decided", "style_score": 0.6, "timestamp": "2026-11-07T11:59:29+00:00"}
{"combined_score": 0.8817, "content_id": "5caea615-d6e3-4e43-bbb6-189dcf0bb6e3", "creator_id": "attacker_EV10", "guess": "ai", "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.", "model_score": 0.9792, "status": "decided", "style_score": 0.7841, "timestamp": "2026-11-07T11:59:28+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "5 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-07T11:59:30+00:00"}
{"creator_id": "attacker_MF01", "event": "rejected", "reason": "missing_text", "status": "rejected", "timestamp": "2026-11-07T11:59:29+00:00"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03**, `d8459e4a-6535-4977-a1a0-cdef7b53d1a2`: a non-native English speaker
writing carefully about their first month in a new country came back "ai" with a
combined score of 0.844, the highest false accusation in the set. Their plain,
short sentences are exactly what my two signals read as machine writing. The
writer is told their work "may have been written with an AI tool" for being
careful in their second language, and the only recourse is an appeal.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
