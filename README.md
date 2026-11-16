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

**My limits:** 5 per minute, 60 per day, on `/submit` only (set in `config.py`, applied by
the `@limiter.limit` decorator on `app.py::submit`).

**Why those numbers and not others:**

A real writer pastes a piece, reads the label, maybe fixes something and resubmits. That's
two or three submissions in a minute at the very most, and a handful in a day. Five a minute
leaves them headroom, so a writer never sees the limit.

A script trying to map my thresholds is a different shape. To find where 0.40 and 0.75 sit,
it needs hundreds of slightly changed versions of the same text, sent as fast as possible.
At 5 a minute and 60 a day, what would take minutes takes weeks per account. I didn't go
lower than 5 because a writer who hits a `429` on their third try will assume the site is
broken. I didn't go higher than 60 a day because nobody honestly has 60 pieces of their own
to check in one day.

`/appeal` isn't limited. An appeal is the writer's way out of a wrong accusation, and
blocking it would hurt exactly the person the service most needs to protect.

**What a caller counts as:** Their `creator_id`. A request with no usable `creator_id` falls
back to the IP address (`app.py::rate_limit_key`). I chose `creator_id` because many real
writers can share one address, like a school, a library, or a household, and limiting by
address would block all of them because of one person.

The cost: `creator_id` is whatever the caller says it is. A script that makes up a new
`creator_id` for every request looks like a thousand different writers and is never
limited. That's the same reason the attack set never trips my limit, since every attack row
uses its own `attacker_<id>`. See **What's Still Broken**.

Rejections leave a trace. A `429` is logged by the error handler in `app.py`, and every
refused input (`400`) is logged by `submit`'s `refuse` helper. Both use
`audit.log_rejection`, which writes the same nine fields as a decision, with the decision
fields set to `null` and a `reason` added.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15`: 15 submissions from one `creator_id` (`flood_tester`)
in a burst. Output from `run_attacks.py::run_flood`, also saved to
`results/flood_2026-11-16_0242.md`:

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

10 of 15 were rate limited. The first five got through, which matches the limit of 5 a
minute exactly, and every request after that got a `429`.

Each `429` left a trace. Here is one of the ten rejections from `logs/audit.jsonl`, with
the same nine fields as a decision:

```json
{"timestamp": "2026-11-16T07:42:21+00:00", "content_id": null, "creator_id": "flood_tester", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

---

## Attack Run — Before

<!-- TODO: python run_attacks.py --set <attack folder> --label before
     Paste the main table from results/attack_run_<date>_before.md here, then
     fill in every blank Verdict yourself:
       - evasion (AI text built to look human): HELD if it came back "ai" or
         "unsure", BROKE if "human".
         NOTE: my combining rule caps disagreement at "unsure" ON PURPOSE, so
         an evasion landing on "unsure" counts as HELD. Say that once here.
       - false_positive (real human writing): HELD if "human" or "unsure",
         BROKE if "ai". These are the ones that matter most.
       - malformed requests: HELD if 4xx with a readable message, BROKE on 5xx.
       - flood_same_creator: HELD if some come back 429. -->

TODO: attack table

**How I judged held vs. broke:** An evasion attack *broke* only if it got labelled
**human**. My combining rule deliberately sends disagreement to "unsure", and "unsure"
never accuses anyone, so evasion that lands there counts as held. A false-positive attack
*broke* if a genuine human text got labelled **AI**. A malformed request broke if it got
anything other than a `4xx` with a readable message.

**Ten audit log entries from the run**

<!-- TODO: curl "http://127.0.0.1:5000/log?limit=200" > results/audit_extract.json
     Choose ten that show something: every false_positive labelled "ai", every
     evasion labelled "human", one or two malformed-request rejections, and one
     rate_limited rejection if the flood family tripped. -->

```json
TODO: ten entries
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

<!-- TODO: pick the false_positive input with the HIGHEST combined score
     labelled "ai". Write 2-3 sentences: what the text was, both signal
     scores, and why both signals agreed it was AI (my guess from unit 7:
     short even sentences + common words — the second-language writer). -->

TODO

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

<!-- TODO: fill MY_WRITING in scenarios.py, then: python run_eval.py --label before
     Each Run cell in results/run_<date>_before.md is already summarized
     (label counts, mean score, statuses). Copy the relevant number in.
     A target must hold in ALL THREE runs to be a MET. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Wrong accusations on my writing | ≤ 1 of 10 labelled AI | TODO | TODO | TODO | TODO |
| 2. AI vs human spread | AI mean − human mean ≥ 0.30 | TODO | TODO | TODO | TODO |
| 3. All labels reachable | each label ≥ 1×, ≥ 2 of 3 borderline → unsure | TODO | TODO | TODO | TODO |
| 4. Appeals recorded | 5/5 appeals land + fake id 404s with 0 log entries | TODO | TODO | TODO | TODO |
| 5. Bad input refused | 4/4 get 4xx, 0 get 500, `/ping` still 200 | TODO | TODO | TODO | TODO |

How each was tested: criteria 1, 2, 3 and 5 by `run_eval.py::main` against the inputs in
`scenarios.py`. Criterion 2 is the AI-set mean minus the human-set mean from the same trial.
For criterion 4, I extended `run_eval.py` with `run_appeals`. It submits each text, appeals
it with the real `content_id`, checks `GET /log` for the appeal entry, and then appeals a
made-up id and counts the log entries before and after.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

<!-- TODO: paste one trial's JSON block from results/run_<date>_before.md.
     The appeal trial is a good one: it shows content_id, status, in_log. -->

Produced by `run_eval.py::main` (the appeal rows by `run_eval.py::run_appeals`), calling
`app.py::submit` and `app.py::appeal`:

```json
TODO
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

<!-- DRAFT DIAGNOSES — these are PREDICTIONS from my unit 7 calibration.
     Keep only the ones the run confirms, put the real counts and attack IDs in,
     and delete any that didn't happen. Add one for anything unexpected.

     A. Plain human writing labelled AI (false_positive family, maybe criterion 1)
        Stage: signal one AND signal two together, then the combining rule.
        Mechanism: gpt2 finds common words in simple order very predictable,
        so model_score is high. The same text has short, even sentences and little
        expressive punctuation, so style_score is high too. The signals AGREE,
        so my disagreement cap never fires, and the 0.5/0.5 average lands above
        0.75. The cap only protects writers when the signals split.
        Check: in the logs, both scores should be above about 0.7 on these rows.

     B. AI text with typos or rare words labelled human/unsure (evasion family)
        Stage: signal one, then the combining rule.
        Mechanism: typos and unusual words are tokens gpt2 didn't expect, so
        perplexity jumps and model_score drops (0.114 on my typo test). The style signal
        still says AI, but the gap is ≥ 0.4, so the cap pulls it to "unsure" at most,
        and if model_score is low enough the average falls under 0.40 → "human".
        Check: model_score low, style_score high, gap ≥ 0.4.

     C. AI text chopped into uneven sentences / extra dashes and semicolons
        Stage: signal two.
        Mechanism: sentence-length spread is 0.5 of my style score and
        expressive punctuation 0.3. Both are pure shape, so changing the shape
        without touching the words drags style_score down.

     D. Criterion 2 spread (if missed)
        Stage: signal one on MY writing. If my own prose is plain, its
        model_score is high, which narrows the gap. Same mechanism as A. -->

TODO: write the confirmed diagnoses here, each naming the stage and the mechanism.

---

## The Improvement

<!-- DO THIS AFTER the "before" runs, not before. Recommended fix if
     diagnosis A is confirmed (it targets the costliest failure):

       config.py: AI_THRESHOLD = 0.75  →  0.85

     That's one line. The disagreement cap follows automatically because it's
     AI_THRESHOLD - 0.01. From unit 7 calibration: the plain human paragraph
     (0.831) moves to "unsure", and both clear-AI texts (0.876, 0.937) stay "ai".
     The cost: lightly edited AI between 0.75 and 0.85 now lands on "unsure".
     Also update the Label Variants table ranges (0.40 – 0.85, 0.85 – 1.00).

     Then: python run_attacks.py --set <folder> --label after
           python run_eval.py --label after
     WAIT A MINUTE between runs or restart app.py so the rate-limit counters reset. -->

**What I changed:** TODO, e.g. raised `AI_THRESHOLD` in `config.py` from 0.75 to 0.85, so
"high-confidence AI" now needs a combined score of 0.85.

**Which diagnosis pointed at it:** TODO, e.g. diagnosis A. The false positives came from the
two signals *agreeing* on plain writing at about 0.8. The disagreement cap can't help there,
so the only lever left was how high a score has to be before I accuse anyone.

### Attack Run — After

<!-- TODO: same format, from results/attack_run_<date>_after.md -->

TODO: attack table after

**Did it help, and how do I know:**

<!-- TODO: compare before vs after BY FAMILY with counts:
       - false_positive labelled "ai": before N → after M
       - evasion labelled "ai": before N → after M (expect this to DROP)
     Be honest about the trade: fewer accusations, and fewer catches. -->

TODO

---

## What's Still Broken

<!-- TODO: one paragraph per attack still getting through and per missed
     criterion. Candidates I already know about: -->

**Rotating `creator_id` walks straight past the rate limit.** The limit is per
`creator_id`, and the caller picks that freely. One script with a new id per request is
never limited. The fix is a second, looser limit per IP address next to the per-creator one
(for example 30 a minute per address), plus real accounts so `creator_id` can't be made up. I
stopped there because the attack set and `run_eval.py` both send everything from
`127.0.0.1`, so an address limit would have rate-limited my own test runs.

**Writers whose two signals agree wrongly.** No combining rule can rescue a text when both
signals are fooled the same way. A real fix is a third signal that measures something
neither of mine does. Until then, the label wording and the appeal path are what protect
these writers. TODO: confirm with the after-run counts.

**Evasion by typos or rare words.** TODO: confirm from the run. This is a blind spot of
signal one that I chose to accept. Catching it would mean trusting the style signal more,
and the style signal is the one fooled by uneven sentences in genuine human writing.

**In-memory rate-limit storage.** A restart forgets every count, and two copies of the
service wouldn't share limits. A real deployment would point `RATE_LIMIT_STORAGE` at Redis.

**The trade I'd make if this ran for real:**

I'd accept more AI text getting through in exchange for fewer wrong accusations. The site
and its readers pay for that in some undetected AI writing. Writers, and especially plain
and second-language writers, stop paying for my detector's blind spots with their
reputation.


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
