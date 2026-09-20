
**WIP — PR #1576, on `hold`, 2026-09-20.** The release is done and baked: all 55 placements
instantiate, the 20 built under the hold are byte-identical, the block is retired in the recipe,
the 35 GLBs are built and the mirror is published. What is NOT done is the gate: `check.sh` was
last run before six derived layers (dooryard plantings, planted rows, signboards, yard goods, lot
building material, town census) were regenerated, and the `--for-diff` smoke legs were never run.
The town-wide GLB staleness `check.sh` reports is **not** from this diff — `git diff origin/dev --
assets/manifest.json` is 315 insertions and 0 deletions, so no existing input hash moved; that is
QUEUE.md's blocking row. Next run: re-gate, run the legs, merge. The swale reading this ticket
owed was taken and is filed as T-1460.
