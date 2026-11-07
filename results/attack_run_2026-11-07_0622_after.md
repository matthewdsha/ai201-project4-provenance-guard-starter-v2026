# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-07 06:22
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `ab128572-5fc4-4682-9b5c-736bdd60e5b9` | unsure | 0.483 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `af19b41a-fa3e-475f-a68d-1cbd70e6566b` | unsure | 0.448 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `ef6f5ee4-67cc-448f-8b0c-e87776d01f66` | unsure | 0.488 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a5bd7f89-7312-4e29-9582-c5565c36276f` | unsure | 0.707 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `69a702a5-0267-4db8-8b0f-25e5227ba388` | human | 0.262 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `d5de65cc-9059-4175-ae60-d54d971edd30` | unsure | 0.437 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `575fd44f-35f0-4f11-b130-783535e7e578` | unsure | 0.543 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `52232914-d79b-404e-be32-c6f46564ec7b` | unsure | 0.598 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `be84203a-c745-4eaa-90ee-b4af62862d06` | unsure | 0.590 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0ad7ca5b-4173-421a-9774-1b1e359bf301` | ai | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f9f4c932-8968-46d4-ad21-c38c9d6f4933` | unsure | 0.604 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `7de8e08b-d0e1-41c7-ae39-d0a2efa5f7be` | ai | 0.820 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `89053a05-3384-4991-ab30-23d86313db6a` | ai | 0.844 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `6d50b5fa-8755-4be5-ae20-00259f7ad157` | ai | 0.779 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `7ab0dc5a-8f7d-4ecd-af0c-6226d12593b9` | ai | 0.831 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `dc6017b8-b5d4-453f-842d-e83d9aa48198` | unsure | 0.690 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `2b81afd8-ceb7-41f2-900d-be1bd92f9d9b` | unsure | 0.591 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `9ffc9c9a-ca03-4214-8068-e433401ed558` | unsure | 0.524 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `eeb88075-2fad-4c0c-8065-4cab51d57e4f` | unsure | 0.431 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `8967c652-d228-492e-a81a-304bf0095371` | human | 0.203 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1f763bd3-fe52-4cda-ad4b-ee1d151f6d73` | unsure | 0.629 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c55bdeb6-d862-4b2d-97a1-e99a1fe8e41e` | unsure | 0.541 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4a4fff0e-b359-4f94-abb6-4b2ce6ef473a` | unsure | 0.506 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `99cc21c2-b41d-420a-92ba-1dae5313da1a` | unsure | 0.583 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `0ae76819-bbdc-407c-a16b-a8f267769752` | unsure | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `22c6dea6-400d-4055-b57e-82f53d14d480` | human | 0.264 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `baaf1e87-8f7e-4b39-8a81-4e860247dbde` | human | 0.264 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9bd77575-343c-47c5-b577-5c480aed9cc3` | human | 0.264 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b27a1df7-ece3-41b5-990c-ad537ce471a5` | human | 0.264 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f2a7312-c69d-4890-be16-cdac67202ee9` | human | 0.264 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "ab128572-5fc4-4682-9b5c-736bdd60e5b9",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.483,
  "model_score": 0.1635,
  "style_score": 0.8025,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "af19b41a-fa3e-475f-a68d-1cbd70e6566b",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4478,
  "model_score": 0.5943,
  "style_score": 0.3012,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "ef6f5ee4-67cc-448f-8b0c-e87776d01f66",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.488,
  "model_score": 0.6662,
  "style_score": 0.3099,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "a5bd7f89-7312-4e29-9582-c5565c36276f",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7069,
  "model_score": 0.6114,
  "style_score": 0.8025,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "69a702a5-0267-4db8-8b0f-25e5227ba388",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2619,
  "model_score": 0.3212,
  "style_score": 0.2025,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "d5de65cc-9059-4175-ae60-d54d971edd30",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.437,
  "model_score": 0.5727,
  "style_score": 0.3012,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "575fd44f-35f0-4f11-b130-783535e7e578",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5431,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "52232914-d79b-404e-be32-c6f46564ec7b",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5979,
  "model_score": 0.2452,
  "style_score": 0.9507,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "be84203a-c745-4eaa-90ee-b4af62862d06",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5902,
  "model_score": 0.7042,
  "style_score": 0.4762,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "0ad7ca5b-4173-421a-9774-1b1e359bf301",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8817,
  "model_score": 0.9792,
  "style_score": 0.7841,
  "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f9f4c932-8968-46d4-ad21-c38c9d6f4933",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6038,
  "model_score": 0.6175,
  "style_score": 0.59,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "7de8e08b-d0e1-41c7-ae39-d0a2efa5f7be",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8199,
  "model_score": 0.7387,
  "style_score": 0.9012,
  "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "89053a05-3384-4991-ab30-23d86313db6a",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8439,
  "model_score": 0.8051,
  "style_score": 0.8827,
  "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "6d50b5fa-8755-4be5-ae20-00259f7ad157",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7795,
  "model_score": 0.8329,
  "style_score": 0.7262,
  "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "7ab0dc5a-8f7d-4ecd-af0c-6226d12593b9",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8307,
  "model_score": 0.8005,
  "style_score": 0.8609,
  "label": "This may have been written with an AI tool, but our check can be wrong, especially for plain, simple writing and for people writing in a second language. If you wrote this yourself, you can appeal using the content ID in this response. Your appeal will be recorded and the submission marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "dc6017b8-b5d4-453f-842d-e83d9aa48198",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6895,
  "model_score": 0.8814,
  "style_score": 0.4975,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "2b81afd8-ceb7-41f2-900d-be1bd92f9d9b",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5914,
  "model_score": 0.8816,
  "style_score": 0.3012,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "9ffc9c9a-ca03-4214-8068-e433401ed558",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5239,
  "model_score": 0.3223,
  "style_score": 0.7255,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "eeb88075-2fad-4c0c-8065-4cab51d57e4f",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4313,
  "model_score": 0.4625,
  "style_score": 0.4,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "8967c652-d228-492e-a81a-304bf0095371",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2035,
  "model_score": 0.2044,
  "style_score": 0.2025,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "1f763bd3-fe52-4cda-ad4b-ee1d151f6d73",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6286,
  "model_score": 0.5943,
  "style_score": 0.6629,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c55bdeb6-d862-4b2d-97a1-e99a1fe8e41e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5411,
  "model_score": 0.4998,
  "style_score": 0.5824,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "4a4fff0e-b359-4f94-abb6-4b2ce6ef473a",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5059,
  "model_score": 0.6401,
  "style_score": 0.3716,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "99cc21c2-b41d-420a-92ba-1dae5313da1a",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5832,
  "model_score": 0.5583,
  "style_score": 0.6081,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "0ae76819-bbdc-407c-a16b-a8f267769752",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. That doesn't mean anything is wrong with it. Plenty of people's own work lands here, and you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "22c6dea6-400d-4055-b57e-82f53d14d480",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "baaf1e87-8f7e-4b39-8a81-4e860247dbde",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "9bd77575-343c-47c5-b577-5c480aed9cc3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "b27a1df7-ece3-41b5-990c-ad537ce471a5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "5f2a7312-c69d-4890-be16-cdac67202ee9",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
