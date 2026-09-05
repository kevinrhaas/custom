---
id: T-0842
title: Land the merges: fold every card ruled MERGE onto its survivor as a union with redirect stubs, and re-derive the 47 consumer gates the fold moves
state: open
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0839
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Land the merges: fold every card ruled MERGE onto its survivor as a union with redirect stubs, and re-derive the 47 consumer gates the fold moves.

Piece 2 of 3 of **T-0839 — One person, several cards: James Allen stands on four, Gurdon Hubbard on six — 39 surname clusters hold 110 cards that may be fewer people. MERGE them — a report is not the deliverable, the merged cards are — losing nothing**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** `tools/merge_resident_cards.py --apply` has landed every MERGE ruling, the
town's person count has gone DOWN from 1,404, `tools/check.sh` is GREEN, and no file that
cites a folded person id fails to resolve.

## WHAT IS ALREADY DONE, AND WHAT THIS PIECE COSTS

T-0841 shipped the machinery and the rulings: `tools/merge_resident_cards.py` with
`--candidates`, `--apply`, `--check` and a self-test, the candidate ledger at
`data/research/residents/merge_candidates.json` (37 clusters, 96 cards), and a written
ruling for every one of them at `data/research/residents/merge_rulings.json` — 29 MERGE,
2 DISTINCT, 4 UNDECIDED, 2 DEFERRED to T-0723.

**`--apply` has been RUN, and it works.** On 2026-09-05, on the branch that shipped T-0841,
it folded 49 cards onto 29 survivors, took the town from 1,404 people to 1,355, and
`python3 tools/validate.py --all` PASSED on the result — schema, provenance, date gates,
counts, the lot. That run then reverted the fold, because of what comes next.

**THE COST IS NOT THE FOLD. IT IS THE 47 GATES DOWNSTREAM.** `tools/check.sh` on a clean
`dev` is green; with the fold applied it fails 47 steps, and every one of them is a
consumer re-deriving from the residents layer. They are not all the same shape:

  * **cheap and mechanical** — `./tools/publish.sh` (the published mirror), and the
    generators whose own message names the rebuild command
    (`tools/read_st_cyr_register.py --build`, the old-settler rolls, the land-tract
    crosswalks, the directories' findings, the Newberry reading, the scene-date register,
    the identity master, the final resident audit);
  * **a real invariant to satisfy** — `4 projected residents are not inferred`. The
    union must not carry `resident_subtype`/`ladder_rule` off a folded card onto a
    survivor the ladder graded differently; that is a fix in `merge_person`, not in the
    consumer;
  * **the one that needs a DECISION, and it is why this is its own ticket** — eight
    FROZEN research cohorts (`pilot_75_cohort.json`, `pass_02..04`, `pass_13..15`) go
    stale the moment a person they name is folded. A frozen cohort is a CONTROL; you do
    not regenerate a control to make a gate go green, or the freeze records today's tree
    (which is T-0764's whole complaint). The cohorts should resolve their member ids
    THROUGH the redirect table in `data/residents/index.json` instead — a shared
    `resolve(person_id)` the cohort gates call — and that is a change to how a freeze is
    read, which the owner may want to rule on.
  * `measure_research_spend.py` also reports `directories` +2 over its ceiling once the
    cards merge, because two rulings that reached two cards now reach one.

Read `merge_rulings.json` before you start: it states the ANCHOR RULE the 29 merges rest
on, and why the Beaubien and Smith clusters are refused under the same rule.
