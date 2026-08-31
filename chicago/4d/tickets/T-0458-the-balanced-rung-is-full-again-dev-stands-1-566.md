---
id: T-0458
title: The balanced rung is full again: dev stands 1,566 triangles under a ceiling this project has twice refused to raise, and the queue's whole top band is bigger than that
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-30
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---
The `balanced` scene-detail tier's triangle ceiling in `renderers/web/js/main.js` is
1,210,000, and the release smoke reads the whole-scene worst stand at desktop 1280x800.
Measured on the steward runner on 2026-08-30, `SMOKE_VIEWPORT=desktop SMOKE_STAGE=5`
against the published mirror:

| tree | balanced, worst stand (the forks, from Wolf Point) | verdict |
|---|---|---|
| `dev` at 590e64c1 | **1,208,434** of 1,210,000 | PASS by 1,566 |
| `dev` + T-0432's four roofs | **1,210,608** of 1,210,000 | FAIL by 608 |

**Why this is a fact about the ceiling and not about T-0432.** Four roofs cost 2,174
triangles at that stand and `dev` has 1,566 to give — 0.13 % of the rung. This is
T-0098's sentence returning word for word: *"the bar had not been reached by a parcel
that overspent it; it had been reached, full stop, and the next VISIBLE parcel of any
size at all was going to fail it whatever it was."* The block comment at the definition
records five raises and one return, and it twice declined a sixth on the ground that
`T-0223`'s trim had to come first. That trim LANDED — it took the rung from 1,252,802 to
1,083,932 — and the 168,870 triangles it recovered have been spent by content in the
three days since. So the rung is full again on the far side of the trim that was supposed
to win it back, which is the new fact and the reason this is a ticket rather than a note
in a parcel.

**It is not one parcel's problem, and that is the urgent half.** QUEUE.md's top band was
reordered by the owner on 2026-08-30 specifically so the city would gain buildings, and
every ticket in it adds roofs: T-0429 is 8, T-0430 4, T-0431 4, T-0432 4, and T-0416,
T-0183, T-0384 and T-0385 more. At about 540 triangles a roof the band is worth roughly
ten thousand triangles against 1,566 of room. **Every one of them fails this gate on the
tree it merges onto**, whichever merges first — the four block tickets were dispatched as
parallel slices against one `dev` and will each read a green ceiling until they measure it.
So the band the owner ordered to the top cannot land until this is settled.

**The fork, and it is the owner's because the file says so.** The 2026-08-21 entry records
his ruling that *"a ceiling is a number this project chose rather than a claim about
1835"*; the entries after it record the discipline that a ceiling is not raised to carry
one record. Both are his. What is wanted is one line:

  (a) **Raise `balanced`** to clear the top band with stated headroom, on a fresh
      measurement, and say what retires the raise. `full` reads 907,173 of 1,400,000 and
      `light` 541,472 of 785,000 at the same stand, so the middle rung alone is squeezed —
      the same asymmetry T-0098 found, which is an argument that the LADDER is mis-shaped
      rather than that the town is too big.
  (b) **Trim first**, and name the trim. Nothing in the tickets currently orders one.
  (c) **Hold the buildings** until (a) or (b), which is what happens by default and is the
      outcome the queue reorder was written to prevent.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The fork above is put to the owner and his answer is recorded at the definition in
  `renderers/web/js/main.js`, in the block's own voice, with the measurement that earned
  it — not a number changed and a comment appended.
- Whichever way it goes, `SMOKE_VIEWPORT=desktop SMOKE_STAGE=5` is green on a tree that
  carries at least the four roofs of T-0432, measured and quoted rather than assumed.
- If it is a raise, the entry states what retires it and the `light` floor is untouched,
  which is the standing constraint on every re-budget this table has taken.

**Links:** T-0432 (the parcel that measured it) · T-0429 · T-0430 · T-0431 (the siblings
that will hit the same wall) · T-0098 · T-0223 · T-0229 · T-0241 · T-0147 · T-0149 ·
`renderers/web/js/main.js` § the detail ladder · `tools/smoke_renderer.mjs` part 5.

---

## RESOLVED BY #615, 2026-08-31 — the ceiling was already raised, on paper only

This ticket held the fork: raise the ceiling with stated headroom and a named
retirement, trim first and name the trim, or hold the buildings. The owner ruled
**raise**, and it turned out the raise had already been ruled.

T-0098 re-budgeted `balanced` from 1,210,000 to **1,225,000** on 2026-08-24 and
wrote it into the comment beside the value and into `docs/LIBERTIES.md`. It was
never written into the value: `git log -S"triangles: 1225000"` on
`renderers/web/js/main.js` was empty, so the number read 1,210,000 without
interruption from before that ruling until #615 applied it.

So the fork this ticket describes was never real. The parcel measured **1,210,608**
against a ceiling that its own records say had been lifted to 1,225,000 seven days
earlier — inside by **14,392**, not over by 608.

The 1,260,000 in the ledger's table is a different episode and does not bear on
this: T-0229 raised `balanced` with `full` on 2026-08-27 and returned it with
`full` a day later, from 1,260,000 and not from 1,225,000.

**What is still owed**, and it is T-0454's neighbour rather than this ticket's:
nothing stops the value and the ledger disagreeing again. T-0098's sizing also
still holds — this buys no room for the parcel after these, and T-0149 and T-0147
still own the trim that would win the rung back.

