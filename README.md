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

**Moment 3**

- *What I asked for:* After running my five criteria three times, I had Claude check my verdicts against the targets in `criteria.md` and argue against any generous reading, since "met" is the comfortable answer.
- *What came back:* It agreed with MISSED on criteria 1, 2, 3 and 5, because each target has to hold in every trial and none did. It pushed back on criterion 4: MET is correct, but the target only checks ten appeals on valid ids, so it is the easiest of my five and passing it says little. It also argued against lowering any missed target, since a number I missed stays where it is and gets diagnosed.
- *What I changed:* Nothing in `criteria.md`. I wrote in the run log that criterion 4 is the generous one, and I diagnosed each miss instead of revising it.

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

**Every attack, with its outcome and mark** (before the improvement; the same
table is in `results/attack_run_2026-11-07_0559_before.md`, which also has the
content IDs):

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.483 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.448 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.488 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.707 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.262 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.437 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.543 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.598 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.590 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.604 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.820 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.844 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.779 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.831 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.690 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.591 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.524 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.431 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.203 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.629 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.541 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.506 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.583 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | human | 0.250 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | human | 0.306 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.749 | HELD |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.749 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | ai | 0.811 | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

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

`python run_eval.py --label before` (criteria 1 to 3, `results/run_2026-11-07_0604_before.md`)
and `python run_eval_extra.py --label before` (criteria 4 and 5,
`results/run_extra_2026-11-07_0610_before.md`). Three trials each, nothing
changed in between. Criteria 4 and 5 need an appeal after a submit and a JSON
list / invalid JSON body, which `run_eval.py` can't send, so I extended the
harness with `run_eval_extra.py` and wrote the scenarios for 1 to 3 in `scenarios.py`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Plain human writing never called AI | ≤ 1 of 10 labelled ai, none of the 4 plain | 4/10 (all 4 plain) | 4/10 (all 4 plain) | 4/10 (all 4 plain) | MISSED |
| 2. Score spread | AI paragraph ≥ 0.40 above human | gap 0.328 | gap 0.328 | gap 0.328 | MISSED |
| 3. Label coverage | 3 of 3 labels; clear AI gets ai, clear human gets human, all trials | 3 labels, but clear AI got unsure | same | same | MISSED |
| 4. Appeal always changes status | 10/10 appeals 200 and logged, original unchanged, unknown id 404 | 10/10 | 10/10 | 10/10 | MET |
| 5. Bad input never crashes | 8 of 8 get a 4xx with a JSON error, each logged, /ping answers | 7/8 | 7/8 | 7/8 | MISSED |

Scores were identical in all three trials for criteria 1 to 3. The model signal
did not vary between runs on this machine. The 4 flagged inputs in criterion 1
are texts 1 to 4, the plain ones, at combined scores 0.827, 0.834, 0.880 and
0.847. Every plain paragraph was accused and none of the six informal ones was.
For criterion 5, the 100,000-character `text` came back 200 instead of a 4xx, so
no rejection entry was written for it (7 new rejection entries, not 8).

**Real output from one trial** (trial 1), pasted as text. Criteria 1 to 3 came
from `run_eval.py::main` (the `/submit` response via `app.py::submit`); criteria
4 and 5 from `run_eval_extra.py::criterion_4` and `::criterion_5`.

*Criterion 1: false positives (texts 1 to 4 are the plain ones)*
```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8266,
    "model_score": 0.778,
    "style_score": 0.8752,
    "sent": "I get up at six every day. I make tea and I sit by the window. My stre"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8335,
    "model_score": 0.8294,
    "style_score": 0.8375,
    "sent": "Last year I started a new job in a new city. At first I was afraid. I "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8795,
    "model_score": 0.7768,
    "style_score": 0.9821,
    "sent": "My sister has a small shop that sells fruit. She opens it at eight and"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8466,
    "model_score": 0.6932,
    "style_score": 1.0,
    "sent": "The park near my school has a big lake. In summer many people come the"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.318,
    "model_score": 0.3349,
    "style_score": 0.3012,
    "sent": "Honestly the worst part of moving flat wasn't the boxes, it was findin"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4718,
    "model_score": 0.5219,
    "style_score": 0.4216,
    "sent": "I've been learning to bake bread for about a year now and I still can'"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2759,
    "model_score": 0.2506,
    "style_score": 0.3012,
    "sent": "We drove up to Whitby in my dad's ancient Volvo, which smells permanen"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2888,
    "model_score": 0.2763,
    "style_score": 0.3012,
    "sent": "Not gonna lie, I almost quit the choir twice this term. Rehearsals run"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3683,
    "model_score": 0.4353,
    "style_score": 0.3012,
    "sent": "My grandfather kept bees behind the garage and never wore a veil, whic"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3685,
    "model_score": 0.5345,
    "style_score": 0.2025,
    "sent": "Tuesday I missed the train because I went back for my umbrella, and it"
  }
]
```

*Criterion 2: score spread (AI paragraph, then human paragraph)*
```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6597,
    "model_score": 0.7246,
    "style_score": 0.5947,
    "sent": "Effective communication is a cornerstone of successful teamwork in any"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3314,
    "model_score": 0.3101,
    "style_score": 0.3527,
    "sent": "I'll be honest, the team meeting yesterday was a mess. Priya turned up"
  }
]
```

*Criterion 3: label coverage (clear AI, clear human, plain human, lightly edited AI)*
```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6597,
    "model_score": 0.7246,
    "style_score": 0.5947,
    "sent": "Effective communication is a cornerstone of successful teamwork in any"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3314,
    "model_score": 0.3101,
    "style_score": 0.3527,
    "sent": "I'll be honest, the team meeting yesterday was a mess. Priya turned up"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8335,
    "model_score": 0.8294,
    "style_score": 0.8375,
    "sent": "Last year I started a new job in a new city. At first I was afraid. I "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6223,
    "model_score": 0.6536,
    "style_score": 0.591,
    "sent": "Good communication is a cornerstone of successful teamwork in any mode"
  }
]
```

*Criterion 4: appeal path*
```json
{
  "criterion_4_trial_1": {
    "appeal_statuses": [
      200,
      200,
      200,
      200,
      200,
      200,
      200,
      200,
      200,
      200
    ],
    "checks": {
      "appeal_entries_found": "10/10",
      "original_decisions_unchanged": true
    },
    "first_appeal_response": {
      "content_id": "aae5cedd-224a-4856-87bb-628ca14ab430",
      "message": "We've recorded your appeal and marked this submission as under review.",
      "status": "under_review"
    },
    "unknown_id": {
      "status": 404,
      "body": {
        "error": "unknown_content_id",
        "message": "No submission has that content_id. Check it for typos."
      },
      "new_under_review_entries": 0
    }
  }
}
```

*Criterion 5: bad input*
```json
{
  "criterion_5_trial_1": {
    "cases": [
      {
        "case": "missing text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "empty text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "whitespace-only text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "non-string text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "missing creator_id",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "body is a JSON list",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "invalid JSON",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "100,000-character text",
        "status": 200,
        "json_error": false,
        "pass": false
      }
    ],
    "new_rejection_entries": 7,
    "ping_after": 200
  }
}
```

**Diagnoses**

Verdicts against my `criteria.md` targets: criteria 1, 2, 3 and 5 are
**MISSED**, criterion 4 is **MET**.

How I decided each one, checking every trial against the number in `criteria.md`:
1. **MISSED:** the target was none of the 4 plain paragraphs and at most 1 of 10 called "ai", and all 4 plain ones were, in every trial.
2. **MISSED:** the target was a gap of at least 0.40, and the gap was 0.328 in every trial, which is under.
3. **MISSED:** all three labels did appear, but the target also needed the clearly-AI paragraph to get "ai", and it got "unsure" in every trial.
4. **MET:** in every trial all 10 appeals returned 200, all 10 `under_review` entries were in the log, the originals were unchanged, and the unknown id returned 404 with no new entry. The one thing I'd call generous is that it only tests ten appeals on valid ids, so it is the easiest of my five targets.
5. **MISSED:** the target was 8 of 8 refused with a 4xx and logged, and the 100,000-character text got 200 in every trial, so 7 of 8. Scores were identical in all three trials
for criteria 1 to 3, so no trial rescued a target and no trial broke one. I did
not revise any criterion: all five could be measured, so a miss is a miss.

**Criterion 1, plain human writing called AI (4 of 4 plain, target 0).**
Stage: signal one and signal two together; the combining rule and the label
mapping pass the mistake straight through. The four plain paragraphs scored
0.78, 0.83, 0.78 and 0.69 on the model signal and 0.88, 0.84, 0.98 and 1.00 on
the style signal. Both read short, common-word sentences as machine-like: gpt2
finds them predictable, and the style signal sees even sentence lengths (spread
0.29 on the plain sample) and almost no punctuation variety (0.11). My cap only
helps when one signal reads human, and here both lean AI, so the average (0.83
to 0.88) clears the 0.75 threshold. This is the false-positive risk I named in
Milestone 1, and it happened to every plain input I tried. The six informal
paragraphs were not accused (combined 0.28 to 0.47), so the signals are
separating plain from messy, not machine from human.

**Criterion 3, label coverage, and criterion 2, score spread (gap 0.328, target
0.40; clear AI got "unsure").** Stage: both signals, on the AI paragraph. The
chatbot-style paragraph scored only 0.72 on the model signal (modern chatbot
text is not especially predictable to a 2019 model) and 0.59 on the style
signal (spread 0.39, punctuation 0.22, in the middle, not extreme). Combined
0.66, which is "unsure", so the clearly-AI input never reached "ai". Worse, the
plain human paragraph in the same run scored 0.83, **higher** than the AI
paragraph. That inversion is the same problem as criterion 1 seen from the other
side: neither signal measures "machine-written", they measure "plain". The
lightly edited AI paragraph scored 0.62, close to the unedited 0.66, so small
word swaps barely moved it. All three labels are reachable, but "ai" is reached
by plain human text more reliably than by AI text.

**Criterion 5, bad input (7 of 8).** Stage: the route. `app.py::submit` has an
emptiness check and nothing on length, so a 100,000-character `text` returned
200. `detector.py` silently truncates to 400 tokens, which hides the problem:
the oversized text was scored and labelled from its first ~300 words, and no
rejection was logged for it. The mechanism is a missing size cap in the route.

**Broken attacks (16 of 56), by mechanism.**
- *Signal two moved by cheap shape changes (EV02, EV03, EV06, EV07, EV09, and
  part of PI02).* EV02 (broken-up sentences), EV06 (one very long and one very
  short sentence) and EV03 (a pasted quotation) pushed sentence spread up (0.85,
  1.19, 0.44) or added punctuation kinds (quotes), dropping the style score to
  0.30 or 0.31. EV09 bolted a human opening onto AI text and the whole-text
  averages fell to 0.48. EV07 (punctuation padding) became one sentence, so
  `style_signal` returned its neutral 0.5 fallback. This is the blind spot I
  named: it cannot read, it only measures shape, and shape is cheap to change.
- *Signal one fooled by surprising tokens (EV01, EV04, EV08, PI02, MF03, MF04).*
  Typos (EV01) raised perplexity so the model score fell to 0.16 even though
  the style signal still read AI at 0.80. Unusual words (EV04) dropped it to
  0.61; combined 0.707, just under 0.75, and it would have been caught at my
  starter threshold of 0.65. Raising the AI threshold to 0.75 turned that one
  from a catch into a miss, which is the trade I chose. EV08 is a 65-character
  text: too little for the model signal to say anything (0.25) while the style
  signal read 0.95. The fake `SYSTEM:` prefix in PI02 moved both signals to
  0.20: gpt2 was surprised by the odd prefix, and the short opening sentences
  raised spread. The injection did not work by instruction. There is no model
  following instructions here, it worked as noise at the start of the text.
- *EV05 (heavy human editing)* scored 0.32 on the model signal and 0.20 on the
  style signal, so both signals read it as human. At that point the text is
  partly human, and these signals have nothing finer to look at.
- *False positives (FP02 to FP05).* Same stage and mechanism as criterion 1:
  both signals lean AI on formal, plain, rubric-style or technical human text
  (model 0.74 to 0.83, style 0.73 to 0.90, combined 0.78 to 0.84).
- *Junk input accepted (MF03 control characters, MF04 only punctuation).*
  Stage: the route. Neither has real words in it, but both pass the emptiness
  check. gpt2 scored them 0.00 and 0.01 (maximally surprising) and the combined
  0.25 and 0.31 labelled them "human", which is a confident label on nothing.
  The route should refuse input with no real words.

**Pattern.** The 16 broken attacks and 4 missed criteria are really three
problems, not twenty:
1. **Both signals measure plainness, not provenance.** This explains criterion
   1, criterion 3's inversion (plain human 0.83, AI paragraph 0.66), criterion
   2's gap, and FP02 to FP05. The cap in the combining rule cannot fix it,
   because the two signals agree with each other.
2. **Each signal can be moved on purpose by something cheap:** shape edits for
   signal two (EV02, 03, 06, 07, 09) and odd tokens at the start for signal one
   (EV01, 04, 08, PI02). The combining rule averages them, so fooling one is
   enough to land in "unsure" or "human".
3. **The route trusts its input** (criterion 5, MF03, MF04): no length cap and
   no check for real words.

The matching improvement for the next section has to come from this list. The
first is the one that matters most to writers, since it is the one that accuses
them, and it is the hardest to fix with the signals I have.


---

## The Improvement

**What I changed:** one change, input validation in the route, before either
signal sees the text (`app.py::submit`, limits in `config.py`):
- `MAX_TEXT_CHARS = 20000`: longer text is refused with a 413 `text_too_long`.
- `MIN_REAL_WORDS = 5`: text with fewer than five real words (a word with at
  least two letters) is refused with a 400 `not_enough_words`.
Both refusals are written to the audit log as rejections. The signals, the
weights and the thresholds are unchanged.

**Which diagnosis pointed at it:** the third problem in my diagnosis, "the route
trusts its input". Criterion 5 failed because the route had no size cap
(100,000 characters returned 200), and MF03 and MF04 got a confident "human"
label on text with no real words in it. I chose this over the other two changes
because it is the only one whose effect I can attribute cleanly. Reweighting or
moving the threshold would change the false-positive numbers and the evasion
numbers at once, and I would not be able to say which change did what.

### Attack Run — After

`python run_attacks.py --set attack_set --label after`
(`results/attack_run_2026-11-07_0622_after.md`), marked with the same rules as
before.

| Family | Before (held / broke) | After (held / broke) |
|---|---|---|
| evasion | 1 / 9 | 1 / 9 |
| false_positive | 4 / 4 | 4 / 4 |
| prompt_injection | 5 / 1 | 5 / 1 |
| malformed | 18 / 2 | 20 / 0 |
| flood_same_creator | 12 / 0 | 12 / 0 |
| **Total** | **40 / 16** | **42 / 14** |

Exactly five attack rows changed and nothing else moved:

| ID | Before | After |
|---|---|---|
| MF03 control characters | 200, "human" 0.25 (broke) | 400 `not_enough_words` (held) |
| MF04 only punctuation | 200, "human" 0.31 (broke) | 400 `not_enough_words` (held) |
| MF05 4,000-character single word | 200, "unsure" 0.75 | 400 `not_enough_words` |
| MF06 emoji only | 200, "unsure" 0.75 | 400 `not_enough_words` |
| MF08 60,000 characters | 200, "ai" 0.81 | 413 `text_too_long` |

Two of those were broken and are now held. MF05, MF06 and MF08 were already
held (no crash, no confident wrong claim), but a refusal is a better answer than
a score on nothing. A rejection from the after run, as logged:

```json
{"timestamp": "2026-11-07T12:22:23+00:00", "creator_id": "attacker_MF03", "event": "rejected", "status": "rejected", "reason": "not_enough_words", "real_words": 2, "min_words": 5}
{"timestamp": "2026-11-07T12:22:23+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "text_too_long", "length": 57640, "max_length": 20000}
```

Every attack after the improvement, in the same format (also in
`results/attack_run_2026-11-07_0622_after.md`):

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.483 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.448 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.488 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.707 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.262 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.437 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.543 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.598 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.590 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.604 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.820 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.844 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.779 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.831 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.690 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.591 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.524 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.431 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.203 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.629 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.541 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.506 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.583 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.264 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

**Criteria, before and after** (three trials each; criteria 1 to 3 from
`run_eval.py --label after`, `results/run_2026-11-07_0623_after.md`; criteria 4
and 5 from `run_eval_extra.py --label after`,
`results/run_extra_2026-11-07_0629_after.md`):

| Criterion | Target | Before (Run 1 / 2 / 3) | After (Run 1 / 2 / 3) | Verdict before | Verdict after |
|---|---|---|---|---|---|
| 1. Plain human writing never called AI | ≤ 1 of 10, none of the 4 plain | 4/10 · 4/10 · 4/10 | 4/10 · 4/10 · 4/10 | MISSED | MISSED |
| 2. Score spread | gap ≥ 0.40 | 0.328 · 0.328 · 0.328 | 0.328 · 0.328 · 0.328 | MISSED | MISSED |
| 3. Label coverage | 3 labels, clear AI gets ai | clear AI got unsure, all trials | same | MISSED | MISSED |
| 4. Appeal always changes status | 10/10, 404 on unknown id | 10/10 · 10/10 · 10/10 | 10/10 · 10/10 · 10/10 | MET | MET |
| 5. Bad input never crashes | 8 of 8 4xx, JSON error, logged | 7/8 · 7/8 · 7/8 | 8/8 · 8/8 · 8/8 | MISSED | MET |

Real output, criterion 5, trial 1 of the after run
(`run_eval_extra.py::criterion_5`):

```json
{
  "criterion_5_trial_1": {
    "cases": [
      {
        "case": "missing text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "empty text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "whitespace-only text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "non-string text",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "missing creator_id",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "body is a JSON list",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "invalid JSON",
        "status": 400,
        "json_error": true,
        "pass": true
      },
      {
        "case": "100,000-character text",
        "status": 413,
        "json_error": true,
        "pass": true
      }
    ],
    "new_rejection_entries": 8,
    "ping_after": 200
  }
}
```

**Did it help, and how do I know:** it fixed what it was aimed at and nothing
else. Criterion 5 went from 7/8 to 8/8 in all three trials, the 100,000-character
text now gets a 413 and a rejection entry (8 new entries, up from 7), and two
broken attacks (MF03, MF04) are now held. I know the change did only that because
the other 51 attack rows and every score in criteria 1 to 3 are identical
before and after, to four decimal places. That is also the limit of it: the 14
attacks that still broke, and criteria 1, 2 and 3, are the signal problems, and
input validation cannot touch them. The false accusations of plain writers, the
worst outcome in the set (FP03, called "ai" at 0.844), are exactly as they were.

The cost of the change is on the other side: a genuine very short submission is
now refused. FP08 ("Went for a run. Legs hurt. Worth it.", 7 words) still gets
through, but a four-word piece would not, and a writer submitting a haiku-length
caption gets a 400 instead of a label. I think that is the right trade, since a
label on four words means nothing, but it is a trade, and the five-word minimum
is my choice, not something I measured.

---

## What's Still Broken

I stopped because this unit asks for one change measured properly. I chose
input validation, which fixed criterion 5 and two attacks and left every signal
problem exactly where it was. Fourteen attacks still break and three criteria
are still missed. They fall into three groups, each with the same fix and the
same reason I didn't make it.

**1. Plain and formal human writing is called AI (FP02, FP03, FP04, FP05;
criterion 1; criterion 3's clear-AI-gets-"ai" check; criterion 2's gap).** I
would stop treating "ai" as a verdict the two signals can reach alone. Both
signals measure plainness, so no weight or threshold separates a plain writer
from a chatbot: FP03 is called "ai" at 0.844 and my AI paragraph only scores
0.66. The honest fix is a better first signal (a newer model than gpt2, or text
the writer can be compared against) and a human check before any "ai" label. I
didn't do it because it is a different project from this one, and because
moving the threshold to protect FP03 would let nearly all AI text through
(EV10, the only evasion that held, scored 0.88).

**2. Cheap shape edits fool signal two (EV02, EV03, EV06, EV07, EV09).** I
would score sentence-length spread on the median rather than the mean, treat
quoted text separately so a pasted quotation doesn't add punctuation kinds, and
replace the neutral 0.5 for a one-sentence text with something that can't be
dragged to the middle by padding. I stopped because each of those is its own
change to measure, and I can't tell from five inputs that they would hold on
text I haven't seen.

**3. Odd tokens fool signal one, and the combining rule averages it in (EV01,
EV04, EV05, EV08, PI02).** I would score signal one on the middle of the text
rather than its first 400 tokens (the `SYSTEM:` prefix in PI02 moved both
signals), and ignore tokens that aren't real words so typos don't count as
surprise (EV01). EV04 is also a cost I chose: at my earlier threshold of 0.65 it
would have been caught at 0.707, and I raised the threshold to 0.75 to protect
real writers. EV05 (heavy human editing) I would leave alone, because at that
point the text is partly human and I don't think the signals should claim
otherwise. I stopped for the same reason as group 2.

**The trade I'd make if this ran for real:** I would go toward fewer wrong
accusations and accept more AI text getting through, by never letting the
signals alone produce an "ai" label and sending those cases to a person. The
site's honest writers and moderators would pay for that, because more AI text
gets through and someone has to read the flagged cases, but that is a cost I
would rather the site carry than an international student whose own essay is
called AI with an appeal nothing re-checks.

---

<!-- ═══════════════════════ UNIT 9 — DEPLOY AND INSTRUMENT ═══════════════════════ -->

## Capstone

**What This Extends**

This extends Provenance Guard, the Flask service from the last two units. It
already takes text at `POST /submit`, scores it with gpt2 (`detector.model_signal`)
and a stylometry signal (`stylometry.style_signal`), combines them in
`scoring.combine_signals`, labels it, and writes a decision or a rejection to
`logs/audit.jsonl`. It also rate-limits `/submit`, rejects bad input, and has
an attack set and an eval harness. What is new this unit is the operational
layer around it: a run path anyone can follow, a structured log that records how
long each request took, and measured numbers for what a run costs.

**The Shape**

I am doing **A, deploy and instrument**, on **Path B (local with logs)**. I'm
adding three things. First, per-request timing in `app.py::submit`: how long the
gpt2 signal took, how long the stylometry signal took, and the whole request,
written as fields on every log line, including the lines for rejected requests.
Second, a start command in RUNNING.md that I test from a clean checkout, with the
Python version, the pinned dependencies and the size of the gpt2 download, plus a
committed log from a real session. Third, a measurement script that sends
a fixed set of submissions and reports time per run and memory, so that
What It Costs rests on a number I measured.

**Out of scope.** I am not changing the signals, the combining rule, the
thresholds or the labels: the three groups in What's Still Broken stay broken,
and this unit's criteria are about the operational layer, not detection quality.
I am not hosting it anywhere, because gpt2 needs far more than the 512 MB the
free tier gives and Path B is worth the same. I am not building a dashboard or
adding a metrics service: the log file and one script are the instrumentation.

**Size check.** Timing fields, the measurement script and the RUNNING.md test
are each under thirty minutes, and none of them touches the scoring path, so I
expect about ninety minutes in total.

**Running It**

Path B, local with logs. The full instructions, with the environment table, are
in [RUNNING.md](RUNNING.md). The short version:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt     # Python 3.11 to 3.13; I tested 3.13.7
python detector.py                  # once: downloads gpt2, 525 MB
python app.py                       # serves http://127.0.0.1:5000
```

`python app.py` loads gpt2 before it answers, so `/health` takes about four to
six seconds to come up. After that every submission, the first included, takes
tens to hundreds of milliseconds (before the change in The Improvement,
the model loaded inside the first `/submit` and that request took six to seven
seconds). I
I tested the steps from a fresh `git clone` in a separate folder, following
RUNNING.md as written: a new virtual environment, `pip install -r
requirements.txt` (it installed the same versions listed in RUNNING.md, in about
30 seconds), `python detector.py`, then `python app.py`. `/health` answered, a
real submission returned a label, an empty text was rejected, and each left a
line in that clone's own `logs/run.jsonl`. Two things made that test easier than
a first-time install would be: pip had the packages cached, and the gpt2 model
was already in my Hugging Face cache, so the 525 MB download did not happen. I
did not time or test those two downloads.

**Instrumentation**

Every `/submit` and `/appeal` request appends one JSON line to
`logs/run.jsonl`, written by `app.py::_log_request` through `runlog.write`. I
kept it separate from `logs/audit.jsonl`: the audit log records decisions and
keeps its nine fields, and this log records how the service ran. Each line has:

| Field | What it holds |
|---|---|
| `timestamp` | UTC, to the millisecond |
| `request_id` | a new uuid per request |
| `route`, `status_code` | what was called and the HTTP status |
| `outcome` | `ok`, or the error code the route returned (`missing_text`, `rate_limited`, ...) |
| `input_chars`, `creator_id` | what came in. I log the length, not the text, so the log never holds a writer's submission |
| `guess`, `combined_score` | what came out (successful `/submit` only) |
| `total_ms`, `model_ms`, `style_ms` | the whole request, the gpt2 stage, and the stylometry stage |

Rejections go through the same hook, so a refused request leaves a line too. I
produced the entries below in one deliberate session
(`AI201_RUN_LOG=logs/session_2026-11-11.jsonl python app.py`, then ten
submissions, five bad requests and two appeals), and they are the whole file,
pasted as text. Lines 1 to 10 are successful submissions, 11 to 15 are rejected
inputs, 16 is an appeal that worked, and 17 is an appeal for an id that does not
exist. The failures are lines 11 to 15 and 17. Nothing errored on the server
side, so there is no 5xx entry; the rate-limit 429s appear in the larger
`logs/run.jsonl`, which came from the attack run.

```json
{"timestamp": "2026-11-11T23:49:56.603+00:00", "request_id": "f47c3f26-ef8d-4fa0-90a5-36d47e3eb37d", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 150, "creator_id": "session_01", "total_ms": 6006.7, "model_ms": 6000.4, "style_ms": 0.4, "guess": "unsure", "combined_score": 0.649}
{"timestamp": "2026-11-11T23:49:56.672+00:00", "request_id": "76f55af3-07e5-49d4-abdb-a293df32fde6", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 175, "creator_id": "session_02", "total_ms": 62.4, "model_ms": 61.5, "style_ms": 0.1, "guess": "ai", "combined_score": 0.851}
{"timestamp": "2026-11-11T23:49:56.746+00:00", "request_id": "81200624-8222-4800-aca7-976a25eab434", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 178, "creator_id": "session_03", "total_ms": 71.6, "model_ms": 71.0, "style_ms": 0.1, "guess": "unsure", "combined_score": 0.665}
{"timestamp": "2026-11-11T23:49:56.814+00:00", "request_id": "6302f508-75b1-488d-ba34-26af96e53e71", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 217, "creator_id": "session_04", "total_ms": 67.1, "model_ms": 66.5, "style_ms": 0.1, "guess": "ai", "combined_score": 0.849}
{"timestamp": "2026-11-11T23:49:56.878+00:00", "request_id": "e666f921-5b14-4b0e-9004-f34dc0f26f73", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 161, "creator_id": "session_05", "total_ms": 62.2, "model_ms": 61.5, "style_ms": 0.1, "guess": "unsure", "combined_score": 0.583}
{"timestamp": "2026-11-11T23:49:56.929+00:00", "request_id": "098af8b0-c7ed-4c0d-a055-68292422fa9a", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 200, "creator_id": "session_06", "total_ms": 48.8, "model_ms": 48.0, "style_ms": 0.1, "guess": "unsure", "combined_score": 0.695}
{"timestamp": "2026-11-11T23:49:56.991+00:00", "request_id": "60b09ac6-4fd3-4d93-a1bd-99df46ebfc59", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 149, "creator_id": "session_07", "total_ms": 60.5, "model_ms": 59.7, "style_ms": 0.1, "guess": "unsure", "combined_score": 0.697}
{"timestamp": "2026-11-11T23:49:57.056+00:00", "request_id": "5ea707cd-f973-48d2-a773-751c0bf78fba", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 160, "creator_id": "session_08", "total_ms": 63.6, "model_ms": 62.9, "style_ms": 0.1, "guess": "unsure", "combined_score": 0.593}
{"timestamp": "2026-11-11T23:49:57.127+00:00", "request_id": "7673c0d9-aedd-4d67-90d4-37c0d446faca", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 202, "creator_id": "session_09", "total_ms": 68.9, "model_ms": 68.0, "style_ms": 0.1, "guess": "ai", "combined_score": 0.953}
{"timestamp": "2026-11-11T23:49:57.180+00:00", "request_id": "e7d7ffbf-1d84-4a2f-9649-674479ed6adb", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 140, "creator_id": "session_10", "total_ms": 51.4, "model_ms": 50.5, "style_ms": 0.1, "guess": "unsure", "combined_score": 0.427}
{"timestamp": "2026-11-11T23:49:57.183+00:00", "request_id": "dcdb0fbe-40ab-4b78-8464-2597c780e920", "route": "/submit", "status_code": 400, "outcome": "invalid_json", "input_chars": null, "creator_id": null, "total_ms": 0.8}
{"timestamp": "2026-11-11T23:49:57.185+00:00", "request_id": "13b59939-d9d2-448c-a3fa-6c795e7b6357", "route": "/submit", "status_code": 400, "outcome": "missing_text", "input_chars": 0, "creator_id": "session_bad", "total_ms": 0.4}
{"timestamp": "2026-11-11T23:49:57.187+00:00", "request_id": "8f0a4186-1899-4d52-98ae-318e932afecd", "route": "/submit", "status_code": 400, "outcome": "missing_creator_id", "input_chars": 150, "creator_id": null, "total_ms": 0.4}
{"timestamp": "2026-11-11T23:49:57.190+00:00", "request_id": "99cfa96a-26fc-4f95-acd3-c02f1e9f1c5b", "route": "/submit", "status_code": 400, "outcome": "not_enough_words", "input_chars": 19, "creator_id": "session_bad", "total_ms": 0.5}
{"timestamp": "2026-11-11T23:49:57.192+00:00", "request_id": "68a10631-495f-4eae-be92-eac3ca941219", "route": "/submit", "status_code": 413, "outcome": "text_too_long", "input_chars": 30000, "creator_id": "session_bad", "total_ms": 0.6}
{"timestamp": "2026-11-11T23:49:57.197+00:00", "request_id": "5796ab73-9d38-416d-a358-6b055cd5495a", "route": "/appeal", "status_code": 200, "outcome": "ok", "input_chars": null, "creator_id": null, "total_ms": 3.3}
{"timestamp": "2026-11-11T23:49:57.201+00:00", "request_id": "414cac6c-34a2-46e7-b3a2-f1463d3c3ec9", "route": "/appeal", "status_code": 404, "outcome": "unknown_content_id", "input_chars": null, "creator_id": null, "total_ms": 1.5}
```

What the entries show: line 1 took 6,007 ms and is almost all `model_ms`, because
it was the first request after a start and loaded the model. Lines 2 to 10 took
49 to 72 ms each. `style_ms` is 0.1 to 0.4 ms on every line, so gpt2 is the whole
cost of a run. Rejected requests took under a millisecond, because the route
refuses them before it calls gpt2.

**What It Costs**

The real cost of a run here is seconds of compute and memory on my own machine.
There is no API spend, because gpt2 runs locally, and no token count to read off
a bill.

**How I measured it.** `python measure.py` starts the service with the
documented command (debug off, so there is one process), sends one cold
request, then twenty warm requests, which is five each of four texts of about
20, 60, 150 and 300 words, and times each with `time.perf_counter()` around the
HTTP call on the same machine (an M1 MacBook, 8 GB, CPU only). It reads the
service's memory with `ps` before the model loads, after the cold request, and
after the warm ones. I ran it twice; the full tables are in
`results/measure_2026-11-11_1742.md` and `results/measure_2026-11-11_1750.md`.

| Measure | Run 1 | Run 2 |
|---|---|---|
| Cold request (loads gpt2) | 7,478 ms | 5,934 ms |
| Warm mean (20 requests) | not recorded | **180 ms** |
| Warm median | 325 ms | 170 ms |
| Warm p95 | 651 ms | 327 ms |
| Memory, loaded | 438 MB | 818 MB |

Run 1 did not record a mean, so I added one to `measure.py` before run 2. The two
runs disagree by about a factor of two on latency, and I did not run anything
else to explain that, so I read the cost as a range: **about 0.2 to 0.3
seconds per warm submission** (run 2's mean of 0.18 s up to run 1's median of
0.33 s). Length matters more than that spread: in run 2 the mean was 64 ms for
about 20 words and 356 ms for about 300.

**Per run:** 0.18 s of compute in run 2, and 0.33 s as the upper end from run 1.
Before the preload change in The Improvement, a cold start added
another 6 to 7.5 s inside the first request once per process start, and the process
holds roughly 440 to 820 MB while it runs. Memory grew from 438 to 722 MB across
run 1's warm requests but fell from 818 to 780 MB in run 2, so I have no
evidence of a leak.

**A hundred submissions a day:**

- 100 × 0.18 s = **18 s** of compute a day on run 2's mean
- 100 × 0.33 s = **33 s** a day at the slower end
- plus one cold start each time the service is started: 6 to 7.5 s inside the first request as measured here, and about 3.5 to 6 s before `/health` answers after the change in The Improvement

For a hundred people a day, one submission each, that is 18 to 33 seconds of
compute and no spend, far inside what one laptop can do. The cost that matters is not the compute but
the 525 MB model and the roughly 800 MB of memory it needs to stay loaded,
which is why this does not fit a 512 MB free host.

**Run Log and Verdicts**

I wrote the five criteria in [criteria.md](criteria.md) ("Unit 9 criteria") and
committed them before any of this was run. `run_criteria.py` runs all five once,
starting a fresh `AI201_DEBUG=0 python app.py` for each criterion as the
criteria say; I ran it three separate times (`--run 1`, `--run 2`, `--run 3`)
with nothing changed in between. Everything each run produced is saved in
`results/criteria_run_<n>/` (the service's own request log and audit log for
each criterion) and `results/criteria_run_<n>.json` (what the client saw).
Criterion 2 asks for three restarts, so run 1, 2 and 3 are its three restarts.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Warm latency | p95 ≤ 500 ms, 20 of 20 return 200 | p95 225 ms, 20/20 ok | p95 244 ms, 20/20 ok | p95 197 ms, 20/20 ok | MET |
| 2. Cold start | first submission ≤ 8,000 ms, 200 | 4,331 ms, HTTP 200 | 4,927 ms, HTTP 200 | 4,510 ms, HTTP 200 | MET |
| 3. Request log complete | exactly 37 lines for 37 requests, all checks | 37/37 lines, 0 problems | 37/37 lines, 0 problems | 37/37 lines, 0 problems | MET |
| 4. Memory bounded | ≤ 1,000 MB after 100 and ≤ +100 MB from 50 to 100 | 653 MB at 50, 645 MB at 100 (-8) | 642 MB at 50, 634 MB at 100 (-8) | 640 MB at 50, 645 MB at 100 (+5) | MET |
| 5. Bad path | 10 of 10 exact refusals, ≤ 50 ms, none 429/500 | 10/10 correct, health 200 | 10/10 correct, health 200 | 10/10 correct, health 200 | MET |

All five were met in all three runs. Nothing missed, so there is nothing to
diagnose; the section after the output below says which targets I set too loose.

Two things I changed to run this, neither of which touches the scoring path: I
added an `AI201_AUDIT_LOG` environment variable in `config.py` (like
`AI201_RUN_LOG`) so the roughly 170 audit entries each run produces stay out of
`logs/audit.jsonl`, and the harness takes the process id from the process it
started instead of `$!`, which is the same process.

### Real output, from run 1

**Criterion 1: warm latency.** Produced by `run_criteria.py::criterion_1`, which
times each `requests.post` to `/submit` with `time.perf_counter()`. The 20 timings
in milliseconds, all HTTP 200, p95 (the 19th fastest) 225.0:

```
[187.2, 157.4, 154.1, 225.0, 162.6, 154.9, 216.9, 172.6, 213.7, 254.9, 187.0, 205.1, 158.9, 149.8, 156.3, 159.0, 160.6, 155.4, 157.4, 162.4]
```

**Criterion 2: cold start.** Produced by `run_criteria.py::criterion_2`, the first
`/submit` to a fresh process:

```
{"cold_ms": 4330.7, "status": 200}
```

**Criterion 3: the request log.** Written by `app.py::_log_request` through
`runlog.write` into `results/criteria_run_1/crit3_run.jsonl`, checked by
`run_criteria.py::criterion_3`. The file has 37 lines. These are line 1, then
lines 21 to 37 (the ten bad requests, then the seven from `crit3_burst`, the last
two of which are the rate-limit 429s):

```json
{"timestamp": "2026-11-12T00:13:49.692+00:00", "request_id": "03c1d386-4495-41d8-bd5e-b66ad75c782f", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 246, "creator_id": "crit3_valid_01", "total_ms": 4528.6, "model_ms": 4522.0, "style_ms": 0.3, "guess": "ai", "combined_score": 0.806}
...
{"timestamp": "2026-11-12T00:13:51.328+00:00", "request_id": "58fc9b8d-8dc6-460d-80f4-be4a41a34865", "route": "/submit", "status_code": 400, "outcome": "missing_text", "input_chars": null, "creator_id": "crit3_b01", "total_ms": 0.6}
{"timestamp": "2026-11-12T00:13:51.330+00:00", "request_id": "15dc5136-1a0c-4bc0-83c4-b9736f87be88", "route": "/submit", "status_code": 400, "outcome": "missing_text", "input_chars": 0, "creator_id": "crit3_b02", "total_ms": 0.4}
{"timestamp": "2026-11-12T00:13:51.332+00:00", "request_id": "8a5d767c-f68c-4ac2-978e-d3a46b5c58eb", "route": "/submit", "status_code": 400, "outcome": "missing_text", "input_chars": 4, "creator_id": "crit3_b03", "total_ms": 0.4}
{"timestamp": "2026-11-12T00:13:51.334+00:00", "request_id": "a2df009f-9b86-4b4e-b2f9-fb8308eb3a15", "route": "/submit", "status_code": 400, "outcome": "missing_text", "input_chars": null, "creator_id": "crit3_b04", "total_ms": 0.3}
{"timestamp": "2026-11-12T00:13:51.335+00:00", "request_id": "d992e7f9-a694-41e9-b26a-01e4206cba90", "route": "/submit", "status_code": 400, "outcome": "missing_creator_id", "input_chars": 246, "creator_id": null, "total_ms": 0.3}
{"timestamp": "2026-11-12T00:13:51.337+00:00", "request_id": "dbbab450-9418-4d1c-add7-d0f71f989f3b", "route": "/submit", "status_code": 400, "outcome": "invalid_json", "input_chars": null, "creator_id": null, "total_ms": 0.4}
{"timestamp": "2026-11-12T00:13:51.339+00:00", "request_id": "dfd0c28f-9a72-4bf2-8882-820410b3ef31", "route": "/submit", "status_code": 400, "outcome": "invalid_json", "input_chars": null, "creator_id": null, "total_ms": 0.5}
{"timestamp": "2026-11-12T00:13:51.341+00:00", "request_id": "32f7a09d-fa42-479b-8b11-f6f86b856a1d", "route": "/submit", "status_code": 413, "outcome": "text_too_long", "input_chars": 100000, "creator_id": "crit3_b08", "total_ms": 0.4}
{"timestamp": "2026-11-12T00:13:51.342+00:00", "request_id": "270414fa-4bbd-46cc-863a-5edaa96ec500", "route": "/appeal", "status_code": 404, "outcome": "unknown_content_id", "input_chars": null, "creator_id": null, "total_ms": 0.3}
{"timestamp": "2026-11-12T00:13:51.343+00:00", "request_id": "1af68472-6423-4731-baee-57b7829406f6", "route": "/appeal", "status_code": 400, "outcome": "missing_reasoning", "input_chars": null, "creator_id": null, "total_ms": 0.1}
{"timestamp": "2026-11-12T00:13:51.416+00:00", "request_id": "6a9f542b-cb06-4df2-9bf8-95465d900a9c", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 246, "creator_id": "crit3_burst", "total_ms": 72.3, "model_ms": 71.7, "style_ms": 0.1, "guess": "ai", "combined_score": 0.806}
{"timestamp": "2026-11-12T00:13:51.491+00:00", "request_id": "d7b27081-bb50-46fd-9be6-98b44a027ded", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 246, "creator_id": "crit3_burst", "total_ms": 73.3, "model_ms": 72.7, "style_ms": 0.1, "guess": "ai", "combined_score": 0.806}
{"timestamp": "2026-11-12T00:13:51.568+00:00", "request_id": "685cdde8-d29d-453f-abe9-1a6951f1ca2b", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 246, "creator_id": "crit3_burst", "total_ms": 75.9, "model_ms": 75.2, "style_ms": 0.1, "guess": "ai", "combined_score": 0.806}
{"timestamp": "2026-11-12T00:13:51.642+00:00", "request_id": "69e82080-dfc6-481c-ad9e-55f0453149d6", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 246, "creator_id": "crit3_burst", "total_ms": 71.9, "model_ms": 71.2, "style_ms": 0.1, "guess": "ai", "combined_score": 0.806}
{"timestamp": "2026-11-12T00:13:51.713+00:00", "request_id": "d098fd73-20d6-4a0b-98dd-b799e9661f17", "route": "/submit", "status_code": 200, "outcome": "ok", "input_chars": 246, "creator_id": "crit3_burst", "total_ms": 69.9, "model_ms": 69.2, "style_ms": 0.1, "guess": "ai", "combined_score": 0.806}
{"timestamp": "2026-11-12T00:13:51.715+00:00", "request_id": "e23d94f5-bdff-4b26-9552-20c1d495f852", "route": "/submit", "status_code": 429, "outcome": "rate_limited", "input_chars": 246, "creator_id": "crit3_burst", "total_ms": 0.4}
{"timestamp": "2026-11-12T00:13:51.717+00:00", "request_id": "549c2f93-c3a1-40d6-a4a0-6b154ad592b7", "route": "/submit", "status_code": 429, "outcome": "rate_limited", "input_chars": 246, "creator_id": "crit3_burst", "total_ms": 0.3}
```

**Criterion 4: memory.** Produced by `run_criteria.py::criterion_4`, which reads
`ps -o rss=` for the service's process three times a second apart after request
50 and after request 100 and keeps the largest:

```
{"mb_after_50": 652.8, "mb_after_100": 644.6, "growth_mb": -8.2, "non_200": []}
```

**Criterion 5: the bad path.** Produced by `run_criteria.py::criterion_5`. Each
line is one of the ten requests: what I wanted, what came back, the time in
milliseconds, and the `outcome` on the matching line of the service's own log:

```json
{"case": "1 body is not JSON", "want": [400, "invalid_json"], "got": [400, "invalid_json"], "ms": 9.1, "logged_outcome": "invalid_json", "ok": true}
{"case": "2 body is a JSON list", "want": [400, "invalid_json"], "got": [400, "invalid_json"], "ms": 2.1, "logged_outcome": "invalid_json", "ok": true}
{"case": "3 text missing", "want": [400, "missing_text"], "got": [400, "missing_text"], "ms": 3.2, "logged_outcome": "missing_text", "ok": true}
{"case": "4 text is empty", "want": [400, "missing_text"], "got": [400, "missing_text"], "ms": 2.2, "logged_outcome": "missing_text", "ok": true}
{"case": "5 text is only spaces", "want": [400, "missing_text"], "got": [400, "missing_text"], "ms": 2.5, "logged_outcome": "missing_text", "ok": true}
{"case": "6 text is 12345", "want": [400, "missing_text"], "got": [400, "missing_text"], "ms": 2.2, "logged_outcome": "missing_text", "ok": true}
{"case": "7 text is null", "want": [400, "missing_text"], "got": [400, "missing_text"], "ms": 2.6, "logged_outcome": "missing_text", "ok": true}
{"case": "8 creator_id missing", "want": [400, "missing_creator_id"], "got": [400, "missing_creator_id"], "ms": 1.8, "logged_outcome": "missing_creator_id", "ok": true}
{"case": "9 text of 20,001 characters", "want": [413, "text_too_long"], "got": [413, "text_too_long"], "ms": 1.9, "logged_outcome": "text_too_long", "ok": true}
{"case": "10 four words", "want": [400, "not_enough_words"], "got": [400, "not_enough_words"], "ms": 1.5, "logged_outcome": "not_enough_words", "ok": true}
```

### Which targets were set too loose

Because nothing missed, the useful finding is how far inside each target the
system landed:

| Criterion | My target | Measured in the three runs | Tighter target I would set |
|---|---|---|---|
| 1. Warm p95 | 500 ms | 197, 225, 244 ms | **300 ms**: about 20% above the slowest run |
| 2. Cold start | 8,000 ms | 4,331, 4,510, 4,927 ms | **6,000 ms**: but see the note below |
| 4. Memory ceiling | 1,000 MB | 634 to 653 MB | **750 MB** |
| 4. Memory growth, 50 to 100 | +100 MB | -8, -8, +5 MB | **+25 MB** |
| 5. Refusal time | 50 ms | 7.8 to 9.3 ms slowest of ten | **15 ms** |

Criterion 3 is already exact (37 of 37) and cannot be tightened.

Two of my earlier expectations were wrong. I said criteria 1 and 4 were the ones
likely to miss, because my two `measure.py` runs had a p95 of 190 and 570 ms for
this text length and memory went from 438 to 722 MB. In these runs the same
paragraph gave a p95 of 197 to 244 ms and memory did not grow at all. I did not
find out why the two harnesses disagree. One candidate is that `measure.py` also
sends 300-word texts, which allocate more, but I did not test that. Criterion 2
passed with room because I time back-to-back restarts, where the operating
system still has the model files cached; the criterion says it does not test a
first start after a reboot, which would be slower, and I did not measure one.

**The Improvement**

**The pattern in the data.** No criterion missed, so there is no failure to
trace. What the numbers do show is one stage that is far more expensive than
everything else: `detector.py::_load`, which loads gpt2 lazily on its first call,
so the load happens inside the first `/submit` after every start. In run 1 that
request took 4,331 ms against a warm p95 of 225 ms, and in
`results/startup_before.md` it took 6.3 to 6.5 s against about 0.15 s warm, over
forty times as long. The mechanism is that the cost belongs to the process
starting, but the request path pays it, so whoever submits first after a restart
or deploy waits about six seconds. It is also the target I said I would tighten
first (criterion 2, 8,000 ms down to 6,000 ms), and the tighter target would be
missed on the slower of my two harnesses. The two harnesses disagree by about two
seconds on this number (4.3 to 4.9 s in `run_criteria.py`, 6.3 to 6.5 s in
`measure_startup.py`) and I did not find out why.

**The one change.** In `app.py::preload_detector`, called from `main()`, the
service now loads gpt2 and scores one throwaway sentence before it starts
answering. The first version loaded the model only, and the first `/submit` then
still took 335 to 1,978 ms because the first forward pass has its own start-up
cost, so I added the throwaway scoring. It is about twenty lines and does not
touch the signals, the combining rule or the labels. If the model cannot load it
prints that and carries on, so `/submit` still answers 503
`detector_unavailable` as before. In debug mode only the Flask worker loads the
model, not the reloader parent. `measure_startup.py` times three restarts
(`results/startup_before.md` and `results/startup_after.md`).

### Startup, before and after

Before:

| Restart | Until /health answers | model loaded at /health | First /submit | Start until first label | HTTP |
|---|---|---|---|---|---|
| 1 | 327 ms | False | 6,415 ms | 6,742 ms | 200 |
| 2 | 324 ms | False | 6,512 ms | 6,836 ms | 200 |
| 3 | 320 ms | False | 6,285 ms | 6,606 ms | 200 |
| median | 324 ms | | 6,415 ms | 6,742 ms | |

After:

| Restart | Until /health answers | model loaded at /health | First /submit | Start until first label | HTTP |
|---|---|---|---|---|---|
| 1 | 5,785 ms | True | 102 ms | 5,886 ms | 200 |
| 2 | 3,788 ms | True | 154 ms | 3,942 ms | 200 |
| 3 | 3,674 ms | True | 155 ms | 3,829 ms | 200 |
| median | 3,788 ms | | 154 ms | 3,942 ms | |

### Criteria, before and after

Before: the three runs already shown above, unchanged.

After (the whole set rerun three times, nothing else changed in between; these
are `--run 4`, `5` and `6`, saved in `results/criteria_run_4` to `_6`):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Warm latency | p95 ≤ 500 ms, 20 of 20 return 200 | p95 199 ms, 20/20 ok | p95 186 ms, 20/20 ok | p95 265 ms, 20/20 ok | MET |
| 2. Cold start | first submission ≤ 8,000 ms, 200 | 117 ms, HTTP 200 | 226 ms, HTTP 200 | 452 ms, HTTP 200 | MET |
| 3. Request log complete | exactly 37 lines for 37 requests, all checks | 37/37 lines, 0 problems | 37/37 lines, 0 problems | 37/37 lines, 0 problems | MET |
| 4. Memory bounded | ≤ 1,000 MB after 100 and ≤ +100 MB from 50 to 100 | 641 MB at 50, 642 MB at 100 (+1) | 641 MB at 50, 638 MB at 100 (-3) | 737 MB at 50, 648 MB at 100 (-89) | MET |
| 5. Bad path | 10 of 10 exact refusals, ≤ 50 ms, none 429/500 | 10/10 correct, health 200 | 10/10 correct, health 200 | 10/10 correct, health 200 | MET |

| Criterion | Before (runs 1 to 3) | After (runs 4 to 6) |
|---|---|---|
| 1. Warm p95 | 225, 244, 197 ms | 199, 186, 265 ms |
| 2. First submission | 4,331, 4,927, 4,510 ms | 117, 226, 452 ms |
| 4. Memory after 100 | 645, 634, 645 MB | 642, 638, 648 MB |
| 4. Growth 50 to 100 | -8, -8, +5 MB | +1, -3, -89 MB |

### Did it help?

**Yes on what I aimed at, and it cost something elsewhere.**

- **The first submission after a start went from 4.3 to 6.5 s to 0.1 to 0.5 s**
  (criterion 2, and 6,415 ms to 154 ms median in `measure_startup.py`). Every
  criterion still passes, so the verdicts do not change.
- **The wait did not disappear, it moved.** `/health` used to answer in about
  0.3 s and now takes a median 3.8 s, because the load happens before the
  service starts answering. Anything that waits for the service to come up, a
  deploy or a health check or me, now waits those seconds. The time from
  starting the process until a writer has a label fell from a median 6.7 s to
  3.9 s; I measured that and did not explain why it is shorter than the load plus
  the first request used to be.
- **An idle service now holds the model.** Before, the process sat near 40 MB
  until the first request. Now it holds 586, 686 and 779 MB right after
  `/health` answers, measured on three restarts. That matters for exactly the
  reason this project cannot go on a 512 MB host.
- **Nothing else got better.** Warm latency is within noise (p95 186 to 265 ms
  against 197 to 244 ms before), and run 6 shows the memory reading is noisier
  than I treated it: 737 MB after request 50 and 648 MB after 100, an 89 MB
  swing in a run where the service did nothing different. It dropped, so the
  run passed, but the same swing upward would have been within 11 MB of missing
  the 100 MB growth target, so that target is looser than the noise I now know
  about, and a pass does not show that memory is stable.
- **Criterion 2 now passes trivially.** It waits for `/health` and then times
  the first submission, so moving the load before `/health` removes it from what
  the criterion measures. The honest comparison is the startup table above, which
  includes the wait. If I kept this change I would rewrite criterion 2 to time
  from process start to the first label, and I have not.

**What's Still Broken**

No criterion was missed. All five were met in all six runs, three before the
preload change and three after, so there is no missed criterion to say what I
would do about. What is still broken is that my targets were set too loose to
find anything, and one of them no longer measures what it was meant to:

- **Criterion 1, warm latency:** 500 ms against a measured p95 of 186 to 265 ms.
  I would tighten it to **300 ms**.
- **Criterion 2, first submission:** 8,000 ms against 117 to 452 ms after the
  change. This is the one that is now blind: it times the first submission after
  `/health` answers, and I moved the model load to before that. I would make it
  time from starting the process until the first label, with a target of
  **6,000 ms**. That would have failed before the change (a median 6,742 ms in
  `results/startup_before.md`) and passes after it (3,942 ms), which is the
  difference I actually care about.
- **Criterion 4, memory:** I would tighten the ceiling from 1,000 MB to
  **750 MB** and the growth allowance from 100 MB to **25 MB**. Run 6 swung 89 MB
  between request 50 and 100 with nothing different happening, so a 25 MB target
  would need the median of several readings, not one.
- **Criterion 5, refusal time:** 50 ms against a slowest refusal of 9.3 ms. I
  would tighten it to **15 ms**.
- **Criterion 3** is exact (37 lines for 37 requests) and cannot be tightened.

I did not change these in `criteria.md`. I only know they are loose because of
the results, and moving a target after seeing the results is the one move this
unit says not to make; each of them is also its own change to build and measure.
Two things I did not explain are still open: the two harnesses disagree by about
two seconds on the old cold-start number, and the time from starting the process
to the first label came out shorter after the change than I expected. Detection
quality, the subject of units 7 and 8, is untouched and is described in the
unit 8 section above.

**If I had another unit, the first thing I would do** is rewrite criterion 2 to
time from process start to the first label with a 6,000 ms target, and rerun it.
I would do that one first because it is the only criterion that covers startup,
my preload change made it pass without measuring the trade I made (a slower
`/health` for a fast first request), and it is a few lines to change.

**How I Used AI**

**Moment 1**

- *What I asked for:* After the five criteria were written, I asked Claude how it felt about them as a set.
- *What came back:* It said they were solid but too safe. By its reading only criteria 1 and 4 could plausibly miss, criteria 3 and 5 overlapped on the same bad inputs, and nothing tested two requests arriving at once, which it called the failure most likely to break a service that runs on its own. It suggested replacing the logging check with a concurrency criterion.
- *What I changed:* Nothing. I kept all five as written and committed them. All five then passed every run, so its point stands: no criterion I wrote tests simultaneous requests, and I do not know whether the service survives them.

**Moment 2**

- *What I asked for:* Once all five criteria were met, I asked Claude to choose and make the one improvement, since there was no miss to point it at.
- *What came back:* It chose preloading gpt2 at startup. The reason was the data: the first `/submit` after a start took 4.3 to 6.5 s against about 0.15 s for every other request, because the model loads inside that request. It also said the wait would move rather than disappear. Its first version loaded the model only, and the first request still took 335 ms to 2 s until it added a throwaway scoring.
- *What I changed:* I kept the change and ran the whole criteria set three more times. The README reports what it cost as well as what it fixed: `/health` now takes a median 3.8 s to answer, an idle service holds 586 to 779 MB, and criterion 2 passes without measuring the load.

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
