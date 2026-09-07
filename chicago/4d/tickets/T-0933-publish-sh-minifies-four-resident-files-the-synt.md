---
id: T-0933
title: publish.sh minifies four resident files the synthesizer writer pretty-prints, so tools/check.sh goes red on any run that publishes
state: open
epic: PIPELINE
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

`bash tools/publish.sh` on an **untouched `dev`** turns `bash tools/check.sh` red. No branch
is involved. Reproduced at `f581e15b9`:

```
git checkout dev && git status --short        # clean
bash chicago/4d/tools/publish.sh              # exit 0
python3 chicago/4d/tools/synthesize_resident_research.py --drift
  FAIL site/chicago/4d/data/residents/households/hh_adams_william_h.json has drifted …
  FAIL site/chicago/4d/data/residents/households/hh_miller_john.json      has drifted …
  FAIL site/chicago/4d/data/residents/households/hh_murphy_john.json      has drifted …
  FAIL site/chicago/4d/data/residents/index.json                          has drifted …
```

**The four files are semantically identical either way.** Parsed and compared as JSON, the
published form and the committed form are equal objects. The whole difference is
formatting: `data/residents/index.json` is 496,413 bytes committed and 394,615 published,
because one is indented and the other is on one line.

**Two owners write the same four paths and disagree about whitespace.**
`synthesize_resident_research.py` writes them pretty-printed; `tools/publish.sh` transforms
the residents layer into the mirror and emits them minified. T-0838's `--drift` ratchet
compares BYTES against what the writer produces, so whichever ran last decides whether the
gate is green. `dev` is committed in the writer's form, which is why `dev` is green until
somebody publishes — and publishing is the last step of every unit of work in this repo.

Restoring just those four paths to the committed form makes `--drift` green again with
nothing else changed, which is the proof that formatting is the whole of it.

**Why it is urgent rather than cosmetic.** Every PR lap in the drain band above runs
`publish.sh` and then `check.sh`. Each one will meet four red lines that have nothing to do
with its change, and the honest responses to a red gate — regenerate, or add to the
baseline — are both wrong here: regenerating re-minifies, and baselining a whitespace
difference spends the T-0838 ratchet on a non-fault and blinds it to the real drift it was
built to catch.

**Acceptance:**

1. One owner for the byte form of those four paths, stated in both tools' docstrings. Either
   the publisher stops re-writing what the writer already put in the mirror, or the writer
   emits the mirror in the publisher's form — **decide which, and say why in the code.**
2. `bash tools/publish.sh && bash tools/check.sh` twice in a row on a clean tree is green
   both times, and the second run changes no file.
3. A self-test case asserts the round trip: publish, then drift-check, green — so this
   cannot come back silently.
4. **Nothing is added to `synthesis_drift_baseline.json`.** The baseline records real
   unspent promotion; a whitespace disagreement is not that, and putting it there would
   lower a bar rather than fix a fault.
5. No resident record's CONTENT changes. If any does, that is a separate finding and it is
   reported, not folded in.

**Found by:** setting up the drain band above — the first `publish.sh` of the session went
red on a tree whose only change was five ticket files.

**NOTE FROM T-0938, 2026-09-07 — the reproduction above no longer reproduces. Verify and
close rather than re-fixing.** T-0938 took `site/chicago/4d/` off the PR surface and this
fell out with it: the mirror has ONE writer now, `tools/publish.sh`.
`synthesize_resident_research.py` and `apply_census_1840_bridges.py` both stopped writing
it and say so in their docstrings (acceptance 1 — the publisher won, and the reason is
that a generated tree should not have three authors); `site/chicago/4d/data` came off
`DRIFT_ROOTS`, because a tree that is not committed is not what the T-0838 ratchet
compares a fresh writer run against — and `_scratch`'s `copytree` would have raised on a
clone that has not published; and `apply_census_1840_bridges.py --check` stopped asserting
a mirror it no longer writes, since `check_published_residents.mjs` makes that claim over
the whole layer instead of over the rows one bridge file names.

Measured on the T-0938 branch: `bash tools/publish.sh` followed by
`python3 tools/synthesize_resident_research.py --drift` exits 0 with the baseline still
empty, and `bash tools/check.sh` is green twice in a row — and `check.sh` now runs
publish.sh itself, so every gate run IS that round trip (acceptance 2 and 3). Nothing was
added to `synthesis_drift_baseline.json` (4) and no resident record's content changed (5).

Left open because the ticket is the owner's and confirming an acceptance list belongs to
the run that takes it deliberately.
