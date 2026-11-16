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

1. **Arrives.** A client sends `POST /submit` with JSON `{"text": "...", "creator_id": "..."}`.
2. **Checked.** The route rejects a body that isn't a JSON object, or a `text` that's missing,
   not a string, empty, over 50,000 characters, or too short to score, with a `400` instead
   of crashing. Then it assigns the submission a fresh `content_id`.
3. **Signal one — the model signal.** gpt2, running locally, measures the text's perplexity
   (how predictable it is). `detector.model_signal` squashes that onto 0–1 as `model_score`,
   where higher means more AI-like.
4. **Signal two — the style signal.** `stylometry.style_signal` measures the text's *shape*,
   not its meaning: how much sentence length varies, how much vocabulary repeats, and how
   much and what kind of punctuation it uses. That becomes `style_score`, 0–1, higher = more
   AI-like.
5. **Combine.** `scoring.combine_signals` turns the two scores into one confidence score.
6. **Label.** `scoring.score_to_label` maps that score to one of three outcomes —
   high-confidence human, unsure, high-confidence AI — with a sentence written for the
   writer, not for an engineer.
7. **Logged and returned.** The decision, both signal scores, and the label go to
   `logs/audit.jsonl`, and the writer gets the response. If they think it's wrong, they call
   `POST /appeal` with the `content_id`; that's recorded in the log and the item moves to
   `under_review` for a human to look at.

**The writer I followed through it.** Someone writing in their second language, who sticks
to common words in short, plain sentences because those are the ones they're sure of. At
step 3, gpt2 finds their text very predictable and scores it AI-like. At step 4, their even
sentence lengths and narrow vocabulary *also* look machine-like. Both signals fail in the
same direction, so no combining rule at step 5 can rescue them — averaging only helps when
the signals disagree. The only thing standing between this writer and a wrong accusation is
the wording of the label at step 6 and the appeal path at step 7.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2), measured as
perplexity and squashed onto 0–1. Low perplexity → high score → more AI-like.

**Why that might differ between human and AI writing:** A language model writes by
repeatedly picking a likely next word, so its output is text a model finds easy to predict.
People make odd word choices, take abrupt turns, and reach for the specific rather than the
typical — which surprises the model.

**What it can't see:** Who actually wrote it. Predictability isn't authorship. Plain human
writing — a second-language writer, a younger writer, anyone writing simply on purpose —
scores about as machine-like as machine writing. And the reverse: AI text prompted to use
rare words or ornate phrasing surprises gpt2 and slips through as "human."

### Signal two — the style signal

**What it measures:** The shape of the text without reading it: how much sentence length
varies, how varied the vocabulary is (type–token ratio), and how much and what kind of
punctuation is used.

**Why that might differ between human and AI writing:** Generated prose tends toward even,
mid-length sentences and a narrower band of vocabulary, because that's what "most likely next
word" produces on average. Human writing is lumpier — a three-word sentence next to a
forty-word one, a dash, a semicolon, a fragment.

**What it can't see:** Meaning. It has no idea what the text says, so anything that changes
the shape without changing the substance moves it: adding typos, chopping sentences up,
pasting in a quotation, sprinkling in dashes. That's cheap to do on purpose. It also can't
tell type–token ratio changes caused by *length* from ones caused by authorship — short texts
look more varied just because they're short.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two signals equally. But if they flatly disagree, meaning they're
0.4 or more apart, the result is capped just below the AI line, so the piece can be labelled
"unsure" at most and never "AI." Two methods disagreeing is uncertainty, and uncertainty
isn't enough to accuse someone. The cap only pushes down: a split can still land on
"human." I'd rather miss some AI text than wrongly accuse a writer.

**The numbers:**

```
combined = 0.5 × model_score + 0.5 × style_score
if |model_score − style_score| ≥ 0.4:
    combined = min(combined, 0.74)        # just under AI_THRESHOLD (0.75)
```

Inside the style signal, its three measures are weighted
`0.5 × sentence-length spread + 0.3 × expressive punctuation + 0.2 × type–token ratio`, each
first mapped onto 0–1 "AI-likeness" (`stylometry.py::style_components`). I left the model
signal's midpoint at the starter's perplexity of 45. All of the numbers live in
`config.py` (`WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`, `DISAGREEMENT_GAP`) and
`stylometry.py`.

Equal weights, because neither signal deserves more trust: the model signal accuses plain
writers, and the style signal is fooled by anything that changes the text's shape.

**Calibration** (the four Milestone 4 inputs, plus a second AI and a second human text):

| Input | model_score | style_score | combined | label |
|---|---|---|---|---|
| Clearly AI (an AI "explainer" paragraph) | 0.751 | 1.000 | 0.876 | AI |
| Clearly AI #2 (exercise explainer) | 0.936 | 0.938 | 0.937 | AI |
| Clearly human (grandmother's button tin) | 0.417 | 0.163 | 0.290 | human |
| Clearly human #2 (late bus) | 0.482 | 0.138 | 0.310 | human |
| **Plain conventional human** (second-language writer) | **0.906** | **0.756** | **0.831** | **AI ✗** |
| Lightly edited AI | 0.641 | 0.685 | 0.663 | unsure |

The plain human paragraph is the false positive from my Milestone 1 trace, and it happens
for real. Both signals read short, even sentences with common words as machine-like, so they
agree, and no combining rule can rescue a writer when both signals are wrong in the same
direction. The label wording and the appeal path are what protect this writer.

One thing calibration changed: **type–token ratio pointed the opposite way from what I
expected.** AI explainer prose scored the *highest* vocabulary variety (0.95), because it's
full of distinct abstract nouns. The plain human paragraph scored the lowest (0.76). So in my
style signal, higher type–token ratio counts as more AI-like, and it gets the smallest weight
because it's the least intuitive of the three measures.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

> *"I didn't want to go. I really didn't. But my mom said I had to go to the party because it
> was my cousin's birthday and the whole family was going to be there, so I put on my good
> shoes and got in the car. It was fine. Actually it was fun. Don't tell her that."*

`model_score` **0.891** (AI-like: the words are all common and predictable) versus
`style_score` **0.000** (human: wildly uneven sentences, contractions, punctuation). They're
0.89 apart, so the disagreement cap applies. The average, 0.446, is already below the cap,
so the result is **unsure**. That's what I want: plain vocabulary alone shouldn't get a
person accused.

The opposite split exists too, and it's the one an attacker would use. AI text with typos
added scores `model_score` **0.114**, because typos surprise gpt2, and `style_score`
**1.000**. My rule makes that **unsure** (0.557) rather than AI. That's a miss I'm choosing
to accept.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.40 | This reads like it was written by a person. Nothing in it suggests it was generated by AI. |
| unsure | 0.40 – 0.75 | We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone. |
| high-confidence AI | 0.75 – 1.00 | Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it. |

The boundaries: a score below 0.40 is human, a score from 0.40 up to but not including 0.75
is unsure, and 0.75 or above is AI. There are no gaps. The Sample Run below reaches all
three labels.

The unsure band is wide (0.35 of the scale) and sits high on purpose. It takes a strong,
agreeing signal to reach "AI."

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

Someone reading "unsure" about their own work will hear "we suspect you" unless the label
explicitly says otherwise. So it does three things:
1. It says plainly that we **can't tell**, rather than "possibly AI."
2. It says mixed results **happen a lot with genuine human writing**, so the reader knows
   this is normal and not a mark against them.
3. It says **nothing has been flagged** and no one will act on this alone, which answers
   "what happens to me now?"

It never uses "suspicious," "detected," or a percentage. The AI label is careful too: it says
"may have been," "not proof," names plain writing as a known weak spot, and points to the
appeal. A writer who gets that label wrongly should finish reading it knowing exactly what to
do.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

This is the plain human paragraph, the writer my service is most likely to get wrong. It does
get it wrong:

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I moved to this city two years ago. At first it was hard for me. I did not know many people and my English was not very good. I worked at a restaurant in the evening. In the day I went to school. Now I have some friends and I like my job. I want to finish school and get a better job. My family is proud of me.", "creator_id": "writer_04"}'
```

```json
{"confidence":0.8313,"content_id":"7d86a139-f6cf-47ff-b0be-072cc0d79fbd","guess":"ai","label":"Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.","model_score":0.9064,"status":"decided","style_score":0.7562}
```

The other two labels, from the same run:

```json
{"confidence":0.38,"content_id":"cdba9a66-f546-4d3c-ae44-51f2142091c5","guess":"human","label":"This reads like it was written by a person. Nothing in it suggests it was generated by AI.","model_score":0.4422,"status":"decided","style_score":0.3178}
{"confidence":0.4456,"content_id":"7de19f32-efb1-484c-9553-fc39d03e5642","guess":"unsure","label":"We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.","model_score":0.8913,"status":"decided","style_score":0.0}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "7d86a139-f6cf-47ff-b0be-072cc0d79fbd", "reasoning": "I wrote this myself about my first two years here. English is my second language, so I keep my sentences simple."}'
```

```json
{"content_id":"7d86a139-f6cf-47ff-b0be-072cc0d79fbd","message":"Thanks — your appeal has been recorded. A person will review this piece, and the automated result won't be used against you while they do.","original_guess":"ai","status":"under_review"}
```

An appeal against a `content_id` that doesn't exist gets a `404` and writes nothing to the
log:

```json
{"error":"not_found","message":"No submission with content_id 'not-a-real-id'. Check it matches the one you were given."}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.4456,
      "content_id": "7de19f32-efb1-484c-9553-fc39d03e5642",
      "creator_id": "writer_03",
      "guess": "unsure",
      "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
      "model_score": 0.8913,
      "status": "decided",
      "style_score": 0.0,
      "timestamp": "2026-11-16T07:23:30+00:00"
    },
    {
      "combined_score": 0.8313,
      "content_id": "7d86a139-f6cf-47ff-b0be-072cc0d79fbd",
      "creator_id": "writer_04",
      "guess": "ai",
      "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
      "model_score": 0.9064,
      "status": "decided",
      "style_score": 0.7562,
      "timestamp": "2026-11-16T07:23:30+00:00"
    },
    {
      "content_id": "7d86a139-f6cf-47ff-b0be-072cc0d79fbd",
      "creator_id": "writer_04",
      "event": "appeal",
      "reasoning": "I wrote this myself about my first two years here. English is my second language, so I keep my sentences simple.",
      "status": "under_review",
      "timestamp": "2026-11-16T07:23:40+00:00"
    }
  ]
}
```

The original decision is still there, unchanged. The appeal sits after it and moves the item
to `under_review`.

---

## How I Used AI

**Moment 1**

- *What I asked for:* How to validate the input to `/submit`. I knew it had to reject missing,
  empty and oversized text, but not how to structure the checks.
- *What came back:* A series of "check, then return a `400`" blocks, with an explanation of why
  the "is it a string" check has to come before `.strip()`. Otherwise `None.strip()` crashes
  with a `500`, the exact failure my criterion 5 rules out.
- *What I changed:* I kept the starter's `request.get_json(silent=True) or {}` instead of
  removing the `or {}`. A body that isn't JSON at all still gets a `400`, just with the "text
  is required" message. I also put `body.json`, my scratch file for testing bad inputs, in
  `.gitignore` so it never gets committed.

**Moment 2**

- *What I asked for:* With time running short, a draft of the second signal, the combining
  rule, the labels and `/appeal`.
- *What came back:* Code, plus calibration numbers on six texts. The calibration showed that
  type–token ratio runs the opposite way from the textbook assumption, and that my plain human
  paragraph is labelled AI by both signals at once.
- *What I changed:* I used AI to help me understand the existing starter code (how
  `detector.py` turns perplexity into a score, and what `audit.py` logs), then to help write
  the remaining functions and test them. I checked the draft by running it myself: submitting
  texts with curl, confirming all three labels show up, and making sure an appeal moves the
  item to `under_review` and a fake `content_id` gets a `404`.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
