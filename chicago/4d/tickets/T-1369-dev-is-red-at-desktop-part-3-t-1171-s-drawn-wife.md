---
id: T-1369
title: Dev is red at desktop part 3: T-1171's drawn wife lands on an evidence-only household (hh_inf_cooper_north_04), and the placeholder label no longer agrees with its asset
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Dev is red at desktop part 3: T-1171's drawn wife lands on an evidence-only household (hh_inf_cooper_north_04), and the placeholder label no longer agrees with its asset.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by** T-1347's run, 2026-09-19, on the first `SMOKE_VIEWPORT=desktop SMOKE_STAGE=3`
leg anybody has run since 2026-09-18T01:35. Two checks fail, and BOTH are dev's, not that
branch's: it changed no byte of `data/residents/households/` or `data/assets/`.

```
FAIL desktop 1280x800: nothing was drawn into an evidence-only household
     — 1 reconstructed people on hh_inf_cooper_north_04, name_basis present: true
FAIL desktop 1280x800: the placeholder label agrees with the asset it describes
```

**The first.** `hh_inf_cooper_north_04` is an *inferred* household — an evidence-only
container — and it now carries `rc_inf_cooper_north_04_wife`, drawn by T-1171's
`modelled_families` stage. The smoke's rule is that nothing may be DRAWN into a household
that exists only to hold evidence; the stage's own eligibility rules do not exclude
`hh_inf_*`. Either the rule or the stage is wrong and the two have to be reconciled — the
stage's `--check` is green, so this is a disagreement about what an inferred container is,
not a reproduction failure.

**The second** is unrelated to the residents and was not investigated here.

**Why it stood a day.** Part 3 has no reading in `dev-smoke-state.json` newer than the tree
T-1171 and T-1172 landed on. The readings are now filed: desktop 3 `fail`, desktop 13 and
mobile 13 `pass`, all on sha256:733344d4499f0392.

**Scope note (2026-09-20).** Of the two failures in the title, the second — *the placeholder
label agrees with the asset it describes* — has since been root-caused by **T-1331**: the
check reads a field that does not exist, so it has been permanently red on a typo rather
than on anything about the asset. Take the evidence-only household here and leave the label
to T-1331; the two sit together at the top of the queue. Both are among the four assertions
that have been standing red on dev, which is why every PR's smoke budget reports its legs
"already red on dev" and skips them.
