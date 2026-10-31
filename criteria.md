# Acceptance criteria — Provenance Guard

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

Of 10 pieces I wrote myself, at most 1 is labelled high-confidence AI. The 4 deliberately plain ones (short sentences, common words, the way a second-language writer would write) are never labelled high-confidence AI; at worst they land in "unsure". This has to hold in each of the three trials, not on average.

**Why this target:** On a writing site a wrong accusation costs a real person a lot and a missed detection costs the site a little, so I allow 1 in 10 overall rather than 0. But that allowance can't be spent on plain writers. They are the people signal one is most likely to accuse, they get flagged every time they submit rather than once, and my appeal path only records the complaint: nothing re-checks it. So the one miss I can afford has to land on someone with room to argue back, and for a plain writer the worst case is "unsure".

## 2. Score spread: clearly-AI and clearly-human text are far apart

Across 5 clearly AI-generated texts and 5 clearly human texts, the mean combined score of the AI set is at least 0.30 higher than the mean of the human set, and no human text scores above the lowest-scoring AI text by more than 0.10.

**Why this target:** If the two groups sit close together, the thresholds are cutting through noise and every label is a coin flip. My unsure band is 0.40 wide (0.35 to 0.75), so a gap of 0.30 means the groups at least mostly sit on opposite sides of it, and a smaller gap means the labels can't mean anything. The second clause stops a good-looking mean from hiding a human text that scores like AI.

---

## 3. Label coverage: all three labels are reachable and land where they should

My four calibration inputs (clearly AI, clearly human, plain conventional human, lightly-edited AI) produce all three labels at least once. The clearly-AI input gets high-confidence AI and the clearly-human input gets high-confidence human in all three trials. The plain human input never gets high-confidence AI.

**Why this target:** A label no input can produce is a gap in my ranges, not a design choice. The starter's own note says a stub style signal makes the human label unreachable, so this checks that signal two actually varies. I put the plain human input in because it is the false-positive case that decides my thresholds.

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
