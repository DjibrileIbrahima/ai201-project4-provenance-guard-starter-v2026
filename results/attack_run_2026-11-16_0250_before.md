# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 02:50
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `3e928b58-527c-4de8-a952-a1cc1cbce8a8` | unsure | 0.582 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `6c2628db-4f8a-4c9b-8b67-5aed4694d776` | unsure | 0.446 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `6a68a971-8d65-421c-945f-303f1c64f0a9` | unsure | 0.590 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ee54dc4a-4968-44bd-9329-6631f78f767c` | ai | 0.806 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `59e9f62b-f93c-43a9-bb3a-72573939eb74` | human | 0.393 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `14d69b72-10ea-4177-bfa3-d469f225c4cb` | unsure | 0.508 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `f3ef290f-015f-40fb-aa1f-47948b30d98e` | unsure | 0.475 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `50e91739-8773-4dbd-97c4-208457b5494d` | unsure | 0.498 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `b74c0cb6-23b5-46f5-90dd-ac9300b9662f` | unsure | 0.650 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `d031e436-79b0-4734-94e7-b9ff303c7830` | ai | 0.809 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `ad818c53-02fc-4fef-93a1-da65721a1151` | unsure | 0.641 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `b530cc8b-5797-4643-880b-f2125dfb9779` | ai | 0.775 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `6ac87cdb-476c-449b-ab1c-d3555f3e2307` | ai | 0.799 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `2b598465-d9a4-4dc8-86df-3900f086606b` | ai | 0.797 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `2cf3794d-6e7d-4f59-8c7c-afa1f9989057` | ai | 0.768 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `35051b5e-a61b-4c21-8fa9-e1a39ca0b3ac` | unsure | 0.726 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c78759eb-2e83-4fc0-8f80-2dc068b3a70c` | unsure | 0.620 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `bd128f93-55eb-448f-8662-06df83900afd` | unsure | 0.564 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `fd62bb79-35f2-42b7-8c74-add31384a0c6` | unsure | 0.526 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `65bd1a20-0f58-4301-a20d-8210bdc3c20b` | human | 0.358 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `13138cb8-f77b-4e47-945c-b00205a5d45e` | unsure | 0.600 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `239e5787-a21b-4089-9d85-db1e013bfd3e` | unsure | 0.472 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `867f7108-8aea-48b9-ac70-87446a6dee44` | unsure | 0.545 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c3d1efef-9b4b-4321-b4d1-75efa6ec33e1` | unsure | 0.617 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `1753b8b2-65f0-40af-8e8b-e3f70bf03f42` | human | 0.375 |  |
| MF04 | malformed | text is only punctuation | 200 | `0ec37cc1-b22a-4430-a41b-7d72a6b17c9c` | unsure | 0.406 |  |
| MF05 | malformed | text is a very long single word | 200 | `7e4d2193-302f-4e97-b212-32d609a74e80` | ai | 0.874 |  |
| MF06 | malformed | text is emoji only | 200 | `01dc2fbf-4e15-4101-b19f-e16242781afd` | unsure | 0.740 |  |
| MF07 | malformed | text is right-to-left script | 200 | `5c78abbc-2e4c-4672-b289-16756e22328f` | unsure | 0.728 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `71193480-bb9f-4aba-9745-3ca768078dae` | unsure | 0.495 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `a3c77354-f184-4de2-b138-9cbdb6206417` | human | 0.400 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1bbdd92a-dea0-46c0-9cbe-fa243ec11d41` | human | 0.389 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4484b3b3-b13b-4c44-91f9-96f8044b4fd2` | human | 0.389 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9a39ff28-9428-4d82-9726-60cd7d365007` | human | 0.389 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `41f52806-32bc-49a8-8d0f-d9a9bba71908` | human | 0.389 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ec2ebb02-3602-4cca-a2c5-95274a130051` | human | 0.389 |  |
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
  "content_id": "3e928b58-527c-4de8-a952-a1cc1cbce8a8",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5817,
  "model_score": 0.1635,
  "style_score": 1.0,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "6c2628db-4f8a-4c9b-8b67-5aed4694d776",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4455,
  "model_score": 0.5943,
  "style_score": 0.2967,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "6a68a971-8d65-421c-945f-303f1c64f0a9",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5901,
  "model_score": 0.6662,
  "style_score": 0.5141,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "ee54dc4a-4968-44bd-9329-6631f78f767c",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.8057,
  "model_score": 0.6114,
  "style_score": 1.0,
  "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "59e9f62b-f93c-43a9-bb3a-72573939eb74",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3931,
  "model_score": 0.3212,
  "style_score": 0.465,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
  "content_id": "14d69b72-10ea-4177-bfa3-d469f225c4cb",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5076,
  "model_score": 0.5727,
  "style_score": 0.4425,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "f3ef290f-015f-40fb-aa1f-47948b30d98e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4748,
  "model_score": 0.5862,
  "style_score": 0.3634,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "50e91739-8773-4dbd-97c4-208457b5494d",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4976,
  "model_score": 0.2452,
  "style_score": 0.75,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "b74c0cb6-23b5-46f5-90dd-ac9300b9662f",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6505,
  "model_score": 0.7042,
  "style_score": 0.5969,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "d031e436-79b0-4734-94e7-b9ff303c7830",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8088,
  "model_score": 0.9792,
  "style_score": 0.6384,
  "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "ad818c53-02fc-4fef-93a1-da65721a1151",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6411,
  "model_score": 0.6175,
  "style_score": 0.6647,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "b530cc8b-5797-4643-880b-f2125dfb9779",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7749,
  "model_score": 0.7387,
  "style_score": 0.811,
  "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "6ac87cdb-476c-449b-ab1c-d3555f3e2307",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7988,
  "model_score": 0.8051,
  "style_score": 0.7925,
  "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "2b598465-d9a4-4dc8-86df-3900f086606b",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7974,
  "model_score": 0.8329,
  "style_score": 0.762,
  "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "2cf3794d-6e7d-4f59-8c7c-afa1f9989057",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7682,
  "model_score": 0.8005,
  "style_score": 0.7359,
  "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
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
  "content_id": "35051b5e-a61b-4c21-8fa9-e1a39ca0b3ac",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7257,
  "model_score": 0.8814,
  "style_score": 0.57,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "c78759eb-2e83-4fc0-8f80-2dc068b3a70c",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6196,
  "model_score": 0.8816,
  "style_score": 0.3576,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "bd128f93-55eb-448f-8662-06df83900afd",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.564,
  "model_score": 0.3223,
  "style_score": 0.8058,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "fd62bb79-35f2-42b7-8c74-add31384a0c6",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.526,
  "model_score": 0.4625,
  "style_score": 0.5894,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "65bd1a20-0f58-4301-a20d-8210bdc3c20b",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3584,
  "model_score": 0.2044,
  "style_score": 0.5124,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
  "content_id": "13138cb8-f77b-4e47-945c-b00205a5d45e",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6004,
  "model_score": 0.5943,
  "style_score": 0.6064,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "239e5787-a21b-4089-9d85-db1e013bfd3e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4721,
  "model_score": 0.4998,
  "style_score": 0.4444,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "867f7108-8aea-48b9-ac70-87446a6dee44",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5451,
  "model_score": 0.6401,
  "style_score": 0.45,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "c3d1efef-9b4b-4321-b4d1-75efa6ec33e1",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6173,
  "model_score": 0.5583,
  "style_score": 0.6762,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "status": 200,
  "content_id": "1753b8b2-65f0-40af-8e8b-e3f70bf03f42",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.375,
  "model_score": 0.0,
  "style_score": 0.75,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "0ec37cc1-b22a-4430-a41b-7d72a6b17c9c",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4056,
  "model_score": 0.0112,
  "style_score": 0.8,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "7e4d2193-302f-4e97-b212-32d609a74e80",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8738,
  "model_score": 0.9976,
  "style_score": 0.75,
  "label": "Our checks found strong signs that this may have been generated by AI. This is an automated estimate, not proof, and it can be wrong, especially for plain or simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "01dc2fbf-4e15-4101-b19f-e16242781afd",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.74,
  "model_score": 0.9969,
  "style_score": 0.55,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "content_id": "5c78abbc-2e4c-4672-b289-16756e22328f",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.7282,
  "model_score": 0.9064,
  "style_score": 0.55,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
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
  "status": 200,
  "content_id": "71193480-bb9f-4aba-9745-3ca768078dae",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.4948,
  "model_score": 0.2395,
  "style_score": 0.75,
  "label": "We can't tell either way. Our checks gave mixed or middling results, which happens a lot with genuine human writing, so this is not a finding that AI was used. Nothing has been flagged, and no one will act on this result alone.",
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
  "status": 200,
  "content_id": "a3c77354-f184-4de2-b138-9cbdb6206417",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.3996,
  "model_score": 0.0492,
  "style_score": 0.75,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
  "content_id": "1bbdd92a-dea0-46c0-9cbe-fa243ec11d41",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3893,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
  "content_id": "4484b3b3-b13b-4c44-91f9-96f8044b4fd2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3893,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
  "content_id": "9a39ff28-9428-4d82-9726-60cd7d365007",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3893,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
  "content_id": "41f52806-32bc-49a8-8d0f-d9a9bba71908",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3893,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
  "content_id": "ec2ebb02-3602-4cca-a2c5-95274a130051",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3893,
  "model_score": 0.0287,
  "style_score": 0.75,
  "label": "This reads like it was written by a person. Nothing in it suggests it was generated by AI.",
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
