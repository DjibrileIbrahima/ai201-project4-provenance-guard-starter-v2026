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
## 1. Wrong accusations on my own writing

Of 10 pieces I wrote myself, **at most 1** is labelled high-confidence AI — in
**every one** of the three trials.

**Why this target:** On a writing site, a wrong accusation costs the writer far more than a missed
detection costs the site: their reputation is on the line and they have to argue
their way out of it. One in ten is already a lot to ask a real person to
tolerate, so I won't allow more. It has to hold every trial, because a writer
doesn't get to average their bad day away.

---

## 2. Clearly AI and clearly human text score far apart

Across 5 clearly AI-generated texts and 5 clearly human-written texts, the
**average combined score of the AI set is at least 0.30 higher** than the
average of the human set, in all three trials.

**Why this target:** If the two sets land close together, the labels are mostly noise and the
thresholds are just picking who gets unlucky. A gap of 0.30 is the width of my
unsure band, so it means typical AI and typical human text land on opposite
sides of it rather than both in the middle.

---

## 3. All three labels are reachable

From a set of 9 inputs spread across the range (3 I expect to read as AI, 3 as
human, 3 borderline), **each of the three labels appears at least once** in
every trial, and **at least 2 of the 3 borderline inputs** land on "unsure".

**Why this target:** A label nobody can ever get is a bug in my ranges, not a design. And the
unsure band is the one that protects writers, so it has to actually catch the
cases I can't call — if borderline text gets pushed to either end instead, the
band isn't doing its job.

---

## 4. Every appeal changes status and is recorded

For 5 submissions appealed with their real `content_id`, **5 of 5** return a
success response, move to `under_review`, and appear in `GET /log` as an appeal
entry. An appeal with a made-up `content_id` returns a `404` and creates **no**
log entry.

**Why this target:** The appeal is the only thing standing between a wrong accusation and nothing at
all, so a single lost appeal is a failure — there's no acceptable rate below
100%. The fake-id check matters because an appeal that silently "succeeds"
against nothing tells the writer they've been heard when they haven't.

---

## 5. Bad input is refused, never crashes

For 4 malformed requests — empty `text`, missing `text`, `text` set to `null`,
and `text` over 50,000 characters — **4 of 4** get a `4xx` response with a
readable error message, **0** get a `500`, and the service still answers
`/ping` afterwards.

**Why this target:** A crash on malformed input is one of the most common real failures there is,
and an attacker will find it before a user does. A `500` also tells the caller
nothing about what they did wrong. Oversized text matters separately because the
model runs inline: an enormous input is a cheap way to tie the service up.

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
