---
id: T-0519
title: Both dev gates are red after PR #670: two schema errors in a source record and six resident assertions in part 13
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-03
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Both dev gates are red after PR #670: two schema errors in a source record and six resident assertions in part 13.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0450's run, 2026-09-03, and it is why that PR is on `hold` rather than
merged.** PR #670 (`Merge PR #670: integrate recovered 1840 census household evidence`,
`6e72679b`, 2026-09-02 23:29 CT) left `dev` red on BOTH gates and left the published
mirror stale. None of the three is caused by any open steward branch — each was
reproduced against `origin/dev`'s own committed files.

## 1. `check.sh` — two schema errors, and they fail the dev gate

```
FAIL  source resident_research_v4_1835_census_bridge.json: rights_status:
      'research_notes' is not one of ['public_domain', 'no_known_restrictions',
      'check_required', 'cleared', 'restricted']
FAIL  source resident_research_v4_1835_census_bridge.json: type:
      'research_synthesis' is not one of ['map', 'book', 'newspaper', 'manuscript',
      'illustration', 'photograph', 'website', 'dataset', 'article', 'legal']
FAIL  2 error(s), 127 warning(s)
   ^ dataset (schema, provenance, date gates, licenses, staleness, publish) failed
```

The record was committed in `4fa63347` and is on `dev` unmodified. It is the **only
one of 250 source records** using either value: the other 249 spread over `website`
130 / `book` 76 / `dataset` 7 / `map` 7 / `article` 7 / `newspaper` 7 / `illustration`
5 / `photograph` 4 / `legal` 4 / `manuscript` 1, and `check_required` 186 /
`public_domain` 55 / `cleared` 4 / `no_known_restrictions` 3.

**Two repairs, and choosing between them is not an agent's call.** Either the schema's
vocabulary grows two terms — a synthesis this project itself produced is arguably a
kind of source the vocabulary has no word for — or the record moves to two existing
ones. The second is a statement about what may be done with the material, which is a
rights question and belongs to the owner. `docs/PROVENANCE.md` is the vocabulary this
sits under. **Whichever is chosen, the reasoning goes next to it**, because a source
record that fails its own schema is the one thing this project's honesty rules cannot
absorb quietly.

## 2. Smoke part 13 — six resident assertions, and the counts have moved

Measured at mobile 390x780 against the published mirror, one part per foreground
command:

```
FAIL  every household in the layer is on the card — 824 loaded / 824 rendered
      (no residents on the handle)
FAIL  the 956 person entries are counted — 848
FAIL  the letter-list cohort is held apart from the evidenced town — 97 evidenced /
      727 letter-list, 727 in the group, closed on mount: true
FAIL  the households no building card can reach are marked — 769 off-card /
      42 chip(s) / 727 of them letter-list
FAIL  an invented name says on the card which pool it came from
FAIL  150 resident research reviews reach resident cards — 375:
      {"corroborated_enrichment":74,"candidate_identity":62,"no_corroboration":239}
```

**The A/B that proves whose red it is.** The same command was run twice on the same
tree, the second time with `site/chicago/4d` checked out from `origin/dev` — that is,
against the mirror as `dev` itself committed it. **Identical six failures, and
identical numbers**: 824, 848, 97/727, 769/42, 375. So the smoke's expectations and
the shipped data have parted company on `dev`, and no branch did it.

Two of the six name a number outright and both are stale rather than wrong-looking:
the suite asserts **956 person entries** against 848 shipped, and **150 resident
research reviews** against 375. The direction differs — one shrank, one nearly
trebled — so this is not one edit misread twice, and the assertions should be
re-derived from what PR #670 actually intends to ship rather than nudged to match.

## 3. The mirror was left stale, and T-0450's PR carries the repair

`tools/publish.sh` on an otherwise untouched `dev` regenerates three files nobody
published: `site/chicago/4d/data/residents/households/hh_miller_john.json` and
`hh_murphy_john.json` gain their `later_census` blocks, and `hh_adams_william_h.json`
did not exist in the mirror at all. `deploy.yml` only fires on `site/**`, so that
evidence was merged but not shipped. **This half is already fixed** — T-0450's PR runs
`publish.sh` as every PR must and carries the three files with it. It is recorded here
so the cause is not looked for twice.

## Acceptance

1. `./tools/check.sh` is green on `dev`, and the source record's `type` and
   `rights_status` carry a stated reason for whichever repair was taken.
2. `SMOKE_VIEWPORT=mobile SMOKE_STAGE=13 node tools/smoke_renderer.mjs --published` is
   SMOKE PASS on `dev`, with each of the six assertions either re-derived from the
   shipped data or shown to be reporting a real regression in it.
3. Which of the two it was, per assertion, is written down. Six assertions moving at
   once is either a deliberate change of what the town holds or a fault, and the
   record should not have to guess.
