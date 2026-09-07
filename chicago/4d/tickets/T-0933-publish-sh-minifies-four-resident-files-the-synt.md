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
