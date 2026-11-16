"""
Signal two: the style signal.

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


# ── The three measures ───────────────────────────────────────────────────────
#
# Each raw measure is on its own scale. `style_signal` maps each one onto
# 0-1 "AI-likeness" with a clamp calibrated on the Milestone 4 inputs, then
# takes a weighted average. Directions were checked against real text, not
# assumed — one of them turned out backwards from the textbook expectation.

# Punctuation that varies a lot between writers. Full stops and commas are left
# out: everyone uses them, AI included. Apostrophes are in because they catch
# contractions ("don't", "she'd"), which generated prose tends to avoid.
EXPRESSIVE_PUNCTUATION = r"[;:!?()\"'—–‘’“”]|--| - "

# Below this many sentences, spread is not evidence of anything.
MIN_SENTENCES_FOR_SPREAD = 3

# Window for the moving-average type-token ratio.
TTR_WINDOW = 40


def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: the coefficient of variation (standard
    deviation / mean) of words per sentence.

    Scale: 0 upward. 0 means every sentence is the same length; around 0.2 is
    what generated prose looked like in calibration, 0.8+ is lumpy human
    writing. **Higher = more human.**

    Fewer than two sentences has no spread to measure, so it returns 0.0 —
    and `style_signal` treats anything under MIN_SENTENCES_FOR_SPREAD as "no
    evidence" rather than as "perfectly even, so AI".
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4) if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, as a moving average over windows of
    TTR_WINDOW words (MATTR). Plain TTR falls as text gets longer; averaging
    over fixed-size windows keeps a long text and a short one comparable.
    Texts shorter than one window fall back to plain TTR.

    Scale: 0-1. Higher = more varied vocabulary.

    ⚠️ Direction, as measured: **higher = more AI**, the opposite of the usual
    assumption. Generated "explainer" prose is full of distinct abstract
    nouns (efficiency, transparency, implications) while people writing
    casually or plainly repeat "I", "it", "the" and their own small set of
    words. Plain human writing scored lowest of everything I tried.
    """
    ws = words(text)
    if not ws:
        return 0.0
    if len(ws) < TTR_WINDOW:
        return round(len(set(ws)) / len(ws), 4)
    windows = [
        len(set(ws[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(ws) - TTR_WINDOW + 1)
    ]
    return round(statistics.mean(windows), 4)


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation per 100 words: semicolons, colons, dashes,
    parentheses, ! and ?, quotation marks and apostrophes. Full stops and
    commas don't count.

    Scale: 0 upward. **Higher = more human.**
    """
    n_words = len(words(text))
    if n_words == 0:
        return 0.0
    marks = re.findall(EXPRESSIVE_PUNCTUATION, text)
    return round(100 * len(marks) / n_words, 4)


# ── Combining them ───────────────────────────────────────────────────────────

# How much each measure counts. Spread separated AI from human best in
# calibration; TTR is weakest and its direction is the least intuitive, so it
# counts least.
W_SPREAD = 0.5
W_PUNCT = 0.3
W_TTR = 0.2


def _clamp(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def style_components(text: str) -> dict:
    """Each measure mapped onto 0-1 AI-likeness. Exposed for debugging."""
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)

    # spread 0.2 -> 1.0 (AI-even), 0.8 -> 0.0 (human-lumpy). Too few
    # sentences -> 0.5, i.e. "this measure has no opinion".
    if len(sentences(text)) < MIN_SENTENCES_FOR_SPREAD:
        spread_ai = 0.5
    else:
        spread_ai = _clamp((0.8 - spread) / 0.6)

    # 0 expressive marks per 100 words -> 1.0, 6+ -> 0.0.
    punct_ai = _clamp(1 - punct / 6.0)

    # TTR 0.75 -> 0.0, 0.95 -> 1.0 (higher = more AI, see type_token_ratio).
    ttr_ai = _clamp((ttr - 0.75) / 0.20)

    return {"spread_ai": round(spread_ai, 4),
            "punct_ai": round(punct_ai, 4),
            "ttr_ai": round(ttr_ai, 4)}


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. **Higher means more likely AI.**

    A weighted average of the three measures, each first mapped onto 0-1
    AI-likeness (see `style_components`):

        0.5 x spread   +   0.3 x punctuation   +   0.2 x type-token ratio

    Directions: low spread -> AI, little expressive punctuation -> AI, high
    TTR -> AI.
    """
    c = style_components(text)
    score = W_SPREAD * c["spread_ai"] + W_PUNCT * c["punct_ai"] + W_TTR * c["ttr_ai"]
    return round(_clamp(score), 4)


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
    print(f"components               {style_components(text)}")
