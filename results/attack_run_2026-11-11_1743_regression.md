# Attack run — regression

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 17:43
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `a006fdfe-2e6e-4abe-b67a-af30810a8498` | unsure | 0.483 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `863c5ef2-952a-4551-bd4b-4d1bc1333df6` | unsure | 0.448 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `5a425b14-5756-4037-b96a-2c15b8bd6f75` | unsure | 0.488 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `b7eb415e-4053-4f6f-94ac-7b87c5e79f82` | unsure | 0.707 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `b82ebb9a-08c6-4dfe-95a5-0d66ca80702e` | human | 0.262 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `70d1a13a-42e6-44a6-9686-267ba3736f34` | unsure | 0.437 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `43be734f-d55b-44a4-a7d5-4a92652aaa68` | unsure | 0.543 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `17654dbd-49f6-47b1-aaf5-4608eef40f01` | unsure | 0.598 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `797bbca5-695f-48aa-818e-4b7e2f022106` | unsure | 0.590 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `205fe893-f7e9-40e0-8e6d-4785f354915b` | ai | 0.882 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `6e89641c-9f5b-4f70-a4b4-83ef3f701431` | unsure | 0.604 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `fd92039c-460a-485b-becc-feadd286b08f` | ai | 0.820 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `12ae9ffa-31c5-4b83-bb04-cdb58a0885a4` | ai | 0.844 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e65dad48-9e0f-431b-ad1b-0a9e1d7eac67` | ai | 0.779 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `a7713b79-31ca-4cc8-9039-46d9c315c866` | ai | 0.831 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `68c4844b-d8f9-467c-b7c2-5b2c4bac09ce` | unsure | 0.690 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `d85abb3e-8bd2-4748-8f18-cf7d25d3fce4` | unsure | 0.591 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `8833dde8-d53d-4615-84fe-3ff7389df15a` | unsure | 0.524 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `9dab679c-155d-4190-928a-2956d161c430` | unsure | 0.431 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `7e6378eb-fd04-42fc-8a29-7f9a90febc37` | human | 0.203 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `b53acbdd-ea1b-44c4-9339-abe52e57df80` | unsure | 0.629 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `d9d0199f-c951-4413-a829-48a1eba0bbd7` | unsure | 0.541 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ea285e0b-6997-4cf5-bcd9-f38edbe02899` | unsure | 0.506 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `efe34e72-0bb4-4338-be8c-c5aa395405d0` | unsure | 0.583 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `7973d0da-9161-4049-94dd-2513c9d0ac8e` | unsure | 0.703 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2282ca98-6ed4-4110-b06c-5a030fbb61fb` | human | 0.264 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ed72e508-41a8-4445-afe3-5c9925b91b81` | human | 0.264 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7524076b-cbcb-4c84-b86c-fb409519fba9` | human | 0.264 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `120e7169-ca65-48dc-a457-6985b5e7ccc7` | human | 0.264 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `980b7820-2c6a-4c73-bcbf-84c46166f648` | human | 0.264 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

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
  "content_id": "a006fdfe-2e6e-4abe-b67a-af30810a8498",
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
  "content_id": "863c5ef2-952a-4551-bd4b-4d1bc1333df6",
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
  "content_id": "5a425b14-5756-4037-b96a-2c15b8bd6f75",
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
  "content_id": "b7eb415e-4053-4f6f-94ac-7b87c5e79f82",
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
  "content_id": "b82ebb9a-08c6-4dfe-95a5-0d66ca80702e",
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
  "content_id": "70d1a13a-42e6-44a6-9686-267ba3736f34",
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
  "content_id": "43be734f-d55b-44a4-a7d5-4a92652aaa68",
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
  "content_id": "17654dbd-49f6-47b1-aaf5-4608eef40f01",
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
  "content_id": "797bbca5-695f-48aa-818e-4b7e2f022106",
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
  "content_id": "205fe893-f7e9-40e0-8e6d-4785f354915b",
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
  "content_id": "6e89641c-9f5b-4f70-a4b4-83ef3f701431",
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
  "content_id": "fd92039c-460a-485b-becc-feadd286b08f",
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
  "content_id": "12ae9ffa-31c5-4b83-bb04-cdb58a0885a4",
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
  "content_id": "e65dad48-9e0f-431b-ad1b-0a9e1d7eac67",
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
  "content_id": "a7713b79-31ca-4cc8-9039-46d9c315c866",
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
  "content_id": "68c4844b-d8f9-467c-b7c2-5b2c4bac09ce",
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
  "content_id": "d85abb3e-8bd2-4748-8f18-cf7d25d3fce4",
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
  "content_id": "8833dde8-d53d-4615-84fe-3ff7389df15a",
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
  "content_id": "9dab679c-155d-4190-928a-2956d161c430",
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
  "content_id": "7e6378eb-fd04-42fc-8a29-7f9a90febc37",
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
  "content_id": "b53acbdd-ea1b-44c4-9339-abe52e57df80",
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
  "content_id": "d9d0199f-c951-4413-a829-48a1eba0bbd7",
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
  "content_id": "ea285e0b-6997-4cf5-bcd9-f38edbe02899",
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
  "content_id": "efe34e72-0bb4-4338-be8c-c5aa395405d0",
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
  "content_id": "7973d0da-9161-4049-94dd-2513c9d0ac8e",
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
  "content_id": "2282ca98-6ed4-4110-b06c-5a030fbb61fb",
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
  "content_id": "ed72e508-41a8-4445-afe3-5c9925b91b81",
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
  "content_id": "7524076b-cbcb-4c84-b86c-fb409519fba9",
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
  "content_id": "120e7169-ca65-48dc-a457-6985b5e7ccc7",
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
  "content_id": "980b7820-2c6a-4c73-bcbf-84c46166f648",
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
