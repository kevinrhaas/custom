---
id: T-0684
title: The river tracer would regrade two committed confidences on its next run, and no gate would notice
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Found while reading the Thompson plat for T-0452.

`tools/trace_river.py` is the generator that writes
`data/terrain/epochs/e1834_harbor_cut/hydrology.geojson`, whose own `_doc` says
"do not hand-edit". On the `north_side_slough` feature the generator and the
committed file disagree about two gradings:

| field | `tools/trace_river.py` | committed `hydrology.geojson` |
|---|---|---|
| `width_confidence` | `reconstructed` | `inferred` |
| `depth_confidence` | `conjectural` | `reconstructed` |

**Nothing catches this.** `trace_river.py --check` is deliberately outside
`tools/check.sh` — it needs the BPL IIIF scan over the network — so the drift can
sit indefinitely, and the next deliberate re-run would silently REGRADE two
committed confidences in opposite directions. Regrading a confidence without a
reading is the one thing the provenance model does not allow, and here it would
happen as a side effect of a re-trace nobody was auditing.

Which of the two is right is the actual question, and it is a reading, not a
merge: `width_confidence` describes a width measured off Wright's drafted band
(so `inferred` looks right and the generator looks stale), and
`depth_confidence` describes a depth the file itself calls invented (so
`conjectural` looks right and the committed file looks stale). If so, neither
copy is wholly correct and the fix is one line in each.

**Acceptance:**

1. Each of the two fields is decided on its own reading, and the reasoning is
   written where a reader meets it.
2. Generator and committed file agree afterwards, by construction — not by two
   independent edits that could drift again.
3. Whether `trace_river.py --check` can join a gate (even an advisory one that
   skips cleanly when the network is absent, which its docstring says it already
   degrades to) is decided in writing. A generator no gate ever compares against
   is how this happened.
4. `tools/check.sh` green.
