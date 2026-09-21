---
id: T-1498
title: converge_resident_layer.py --run moves 189 lines of the order book on a clean tree, so the whole-layer fixed point cannot be listed in the derived manifest's second pass
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-20
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

`tools/converge_resident_layer.py --run` (T-1398) is this project's statement of the
resident layer's rebuild order: thirteen steps, back edges recomputed from the
declarations, iterated to a fixed point. Its own `and_then` says a fixed point that
`node tools/rederive.mjs --run` undoes is not one, and names T-1363. T-1363 has now
closed the one edge it measured — the arrival stage drawing from a model the sequence
rebuilds after it — with a declared `second_pass` in `tools/derived_manifest.json`.
What is left is the reconciliation itself, and a measurement that blocks the obvious
form of it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

MEASURED on a clean `dev` tree, 2026-09-20, while closing T-1363:

    python3 tools/converge_resident_layer.py --run
      → FIXED POINT reached after 1 pass(es)
    git status --porcelain chicago/4d/data
      → M chicago/4d/data/reconstruction/1835_reconstruction_order_book.json
        (189 insertions, 189 deletions — the women_and_children block moved)

`build_order_book_1835.py --build` run ALONE on the same clean tree moved nothing, so
the drift comes from the order's own sequence and not from that tool being unstable by
itself. The tool reports a fixed point because it asks each step's `--check`, and
`build_order_book_1835.py --check` is green on either arrangement — so a file that does
not reproduce byte-for-byte passes as converged.

Why that matters beyond tidiness: the derived manifest's `_must_reproduce` refuses a
rebuild that moves a committed byte on a clean tree, which is exactly why this could not
simply be declared as the second pass. `rederive.mjs --run` is what `pr-lap.sh` calls on
every conflicting PR — listing it would churn 189 lines of the order book on merges
nobody meant to touch it in.

Done when: the order's own run is byte-stable on a clean tree (either the arrangement is
made deterministic or the drift is shown to be a real re-derivation and the committed
file is brought to it), AND `rederive.mjs --run` and `converge_resident_layer.py --run`
agree on the fixed point — one of them delegating to the other, rather than the second
pass carrying its own short tail beside a thirteen-step order that already exists.

**Related:** T-1363 (the second pass), T-1398 (the order), and the note in
`derived_manifest.json#_the_second_pass` that hands this ticket its boundary.
`readmit_borderline_roster.py` is still `placement: pending` in
`tools/writer_inventory.json` and is in the declared order as `stage_readmissions` but
in no manifest step — the same reconciliation should say where it goes.
