"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. Higher = more varied = more human.

    The coefficient of variation of sentence length in words: standard
    deviation divided by the mean, so a long text and a short one compare.
    Roughly 0.2 is very even, 0.6+ is lumpy.

    A single sentence has no spread to measure. This returns 0.0 for it, which
    on its own would read as "perfectly even, so AI-ish" — that's wrong, so
    `style_signal` checks the sentence count first and answers neutrally.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


# Type-token ratio is measured on windows this long, then averaged, so a
# 300-word text and a 120-word text compare fairly.
TTR_WINDOW = 50


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, 0-1. Higher = more varied vocabulary.

    Plain type-token ratio falls as text gets longer, so this is a moving
    average over 50-word windows instead. Text shorter than one window gets the
    plain ratio.
    """
    ws = words(text)
    if not ws:
        return 0.0
    if len(ws) <= TTR_WINDOW:
        return len(set(ws)) / len(ws)
    ratios = [
        len(set(ws[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(ws) - TTR_WINDOW + 1)
    ]
    return sum(ratios) / len(ratios)


# The marks that vary between writers. Full stops are left out: nearly every
# sentence has one, so they carry no information.
_MARKS = [",", ";", ":", "\u2014", "\u2013", "(", '"', "!", "?"]


def punctuation_density(text: str) -> float:
    """
    Punctuation variety: how many of the interesting marks appear, 0-1.

    Counts which of commas, semicolons, colons, dashes, brackets, quotes and
    !/? show up at all (a dash is a dash either way), divided by how many kinds
    there are. Higher = wider range of punctuation = more human. This is
    variety rather than raw count: AI prose leans on commas, so count alone
    doesn't separate it.
    """
    present = {m for m in _MARKS if m in text}
    if "-" in text.replace("-", " - ").split() or " - " in text:
        present.add("\u2014")
    return len(present) / len(_MARKS)


# ── Combining them ───────────────────────────────────────────────────────────

# How each measure maps onto 0-1 "AI-ness". Chosen from looking at real
# inputs (see README, Signals and Scoring), not derived from anything: spread
# at or above SPREAD_HUMAN reads fully human, at or below SPREAD_AI fully AI.
SPREAD_HUMAN = 0.65
SPREAD_AI = 0.25
PUNCT_HUMAN = 0.45   # share of the mark kinds present that reads fully human

WEIGHT_SPREAD = 0.6
WEIGHT_PUNCT = 0.4


def _clip(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. **Higher means more likely AI.**

    Two measures, each flipped so that "evenly shaped" scores high, then a
    weighted average:

        spread   low variation in sentence length  -> high AI score
        punct    narrow range of punctuation       -> high AI score

    `type_token_ratio` is computed but NOT scored. On my test inputs it ran the
    wrong way (the AI sample had the more varied vocabulary), so folding it in
    would have added noise with a confident-looking direction.

    Fewer than two sentences gives no spread to measure, so the answer is a
    neutral 0.5 rather than a guess.
    """
    if len(sentences(text)) < 2:
        return 0.5

    spread_ai = _clip((SPREAD_HUMAN - sentence_length_spread(text)) / (SPREAD_HUMAN - SPREAD_AI))
    punct_ai = _clip(1.0 - punctuation_density(text) / PUNCT_HUMAN)

    score = WEIGHT_SPREAD * spread_ai + WEIGHT_PUNCT * punct_ai
    return round(_clip(score), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
