---
id: T-1373
title: Dev is red at desktop part 12: T-1347's 308 trade households are written outside data/residents/households/, so the People directory counts them and the manifest cannot, and the smoke's count assertion only knows to add the re-admitted
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-19
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Dev is red at desktop part 12: T-1347's 308 trade households are written outside data/residents/households/, so the People directory counts them and the manifest cannot, and the smoke's count assertion only knows to add the re-admitted.

**Acceptance:** `SMOKE_VIEWPORT=desktop SMOKE_STAGE=12` is green on dev, with the count
assertion holding the directory to a sum it can actually name — every layer that mints a
person outside `data/residents/households/`, not just the re-admitted.

**Found by** T-1370's run, 2026-09-19, on the first desktop part-12 leg run after
T-1347 (#1503) merged. Both failures are DEV's: that branch mints no person and changes
no byte under `data/residents/`, `renderers/web/js/people.js` or `data/town_census.json`.

```
FAIL desktop 1280x800: the People directory lists the town, and its count is the file's and the manifest's
     — {"rows":80,"api":2626,"file":2626,"stated":2626,"manifest":2144,"readmitted":174}
FAIL desktop 1280x800: the tavern-keeper pill narrows the list to tavern keepers
     — {"all":2626,"matched":8,"pressed":"","offTrade":[],"rows":8,"cleared":2626}
```

**The first, and the arithmetic is exact.** The assertion holds
`stated === manifest + readmitted`: 2,626 against 2,144 + 174 = 2,318. The shortfall is
**308** — precisely the trade households T-1347 minted into
`data/residents/reconstructed_trades/`, a directory that did not exist one commit earlier
(309 files on `origin/dev`, 0 on `origin/dev~1`). The manifest is derived from
`data/residents/households/` and cannot see that layer, which is deliberate and is the same
shape as T-1172's re-admissions — but the assertion was taught about the re-admitted only,
so a THIRD off-manifest layer reads to it as a card that reached the town by an unknown path.
The stage's own `--check` is green; this is the count assertion not knowing about a layer,
not a reproduction failure.

**The second** fails on one clause only: `pressed` is empty, so the pill's `aria-pressed`
never took. Everything else in that check passes — `matched` 8, `rows` 8, no off-trade rows,
`cleared` back to 2,626. Not investigated here.

**Confirming it is dev's, not the branch that found it:** `git diff origin/dev...HEAD` is
empty for `data/residents/`, `people.js` and `town_census.json`, and part 12 was **73 passed,
0 failed** on the same branch before `origin/dev` was merged into it. The only thing that
changed between the green reading and the red one was the merge.

## The second one, investigated (T-1375, 2026-09-19)

`pressed` is empty because **the pill the assertion reaches for no longer exists**.
`renderers/web/js/people.js` offers the TOP TEN trades by count as pills and everything else
through the `More` select; the smoke looks for
`.pill[data-filter="occupation"][aria-pressed="true"]`. T-1347's reconstructed trades and
T-1344's women and children have rewritten that top ten —

    domestic 76 · boarding-house keeper 40 · laundress 34 · carpenter 26 · clerk 26
    labourer 26 · dressmaker 25 · milliner 21 · attorney 15 · merchant 14

— and tavern keeper, with 8, has dropped out of it. `dir.filter('occupation','tavern_keeper')`
still works, which is why the other four clauses of that check pass; only the DOM lookup for a
pill fails, and it fails correctly.

So the fix is not to swap in a trade that happens to be in today's top ten — that is the same
trap one reconstruction stage later. Either drive the row through the `More` select when the
trade is not a pill, or have the smoke pick its trade off `people.json`'s own top ten and
assert against that.

Re-measured on this branch at `sha256:f8037d0f341c23d0`, desktop part 12: the same two
failures and no others, with parts 13 at both viewports green (115 passed, 0 failed each).
