---
id: T-0596
title: The research-spend ratchet measures a finding aid in units it can never earn, so the Newberry ceiling climbs by a volume every read
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-03
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The research-spend ratchet measures a finding aid in units it can never earn, so the Newberry ceiling
climbs by a volume every read.

**What the ratchet does.** `tools/measure_research_spend.py` counts, per research domain, the named units
READ and the ones RULED ON, and `check.sh` fails when a domain's unspent count passes its ceiling in
`tools/research_spend_baseline.json`. It exists because the owner asked, on 2026-09-03, "i see lots of
research being done and some apparent findings from parsing but there are not outputs or updates to the
household and resident data it seems, should i be concerned?" He was right, and the ratchet is the answer.

**Why `newberry_index` cannot answer it.** A Newberry card is a pointer to a book, not a statement about a
person. `tools/read_newberry_index.py --check` FAILS if the source id ever appears behind a resident,
household, structure or reconstruction record, and `crosswalk.json` holds zero merges by rule, because the
index is nothing but surnames and a shared surname is a lead. So a card can never move from `read` to
`ruled on`, and the ceiling was raised from 2,619 to 4,646 by T-0578 for that reason alone. Volumes 3 and 4
(T-0579, T-0580) will raise it again by roughly as much, and each raise will say the same thing.

**Two smaller measurement faults the same raise exposed.**
- `count_read` walks every JSON in the domain but the crosswalks, so `precision_sample.json`'s 80 hand-
  adjudicated rows are counted as 80 more things read — they are re-readings of records already counted.
- `count_spent` only sees a crosswalk ruling that carries an id anchor, so this crosswalk's one pass and
  five written refusals count as zero. A refusal IS an adjudication; that is the whole discipline of
  T-0505.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- The domain registry (`data/research/domains.json`) says, per domain, what its spend UNIT is — a name
  ruled on, or something else — and the ratchet reads it rather than assuming.
- A finding-aid domain is measured on what it actually produces: the works its Chicago cards point at and
  whether each has been opened or ticketed (`follow_up.json` already carries the ranking, and `reachable`
  already says whether a work can be opened). Failing when it reads a volume and mints no ticket is the
  useful version of this alarm.
- The precision sample stops counting as read; state the corrected figure for both volumes.
- An unanchored crosswalk refusal counts as an adjudication, or the ratchet says out loud why it does not.
- Every existing ceiling is restated under the new units in one commit, and `newberry_index`'s stops being
  a number that only ever goes up.

**Effort.** S — the counting is one file and the registry already has a place to say this.

**Links:** T-0578 (the raise that exposed it) · T-0570 · T-0562 · T-0505 (the refusal discipline) ·
`tools/measure_research_spend.py` · `tools/research_spend_baseline.json` `raised[]`.
