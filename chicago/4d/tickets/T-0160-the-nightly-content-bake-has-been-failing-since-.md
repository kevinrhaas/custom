---
id: T-0160
title: "The nightly content bake has been failing since 2026-08-22: the passthrough baseline no longer matches what a fresh bake compresses"
state: open
epic: PIPELINE
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-23
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

`chicago-4d-bake.yml` refuses to publish and has done for at least a day. Recent
runs, all `push`-triggered:

| run | branch | outcome |
|---|---|---|
| #248 | steward/t-0135-worst-stand | failure (2026-08-22 23:26Z) |
| #251 | **dev** | failure (2026-08-23 06:39Z) |
| #252 | steward/t-0014-ground-faces-the-sky | failure |
| #253 | **dev** | failure (2026-08-23 10:49Z) |
| #254, #255 | steward/t-0015-ao-nightly | failure |

It fails the same way every time — a fresh full bake produces derivatives that
disagree with `web_derivative_baseline.json`:

```
FAIL  recon_1835_blk_south_water_wells_d6_01__inferred_1835.glb: banked in
web_derivative_baseline.json as a decided master passthrough and it is
compressed now. That is a repair, not a discovery — re-run
tools/measure_web_derivatives.py --write-baseline in the commit that made it (K38)

REFUSING TO PUBLISH — the derivatives this would mirror do not answer for
themselves against the masters in the tree.
```

**What it does and does not mean.** It does NOT mean the shipped site is wrong:
`check.sh`'s own derivative gate passes on the committed `assets/web/` (345
pairs), and every PR has been merging on a green `gate`. What is broken is the
ability to *rebuild the town and publish the result* — so the nightly content
bake produces nothing, and any parcel that needs a fresh full bake to land will
hit this.

**Why it has gone unnoticed:** the bake only runs on pushes touching generators,
`tools/bake.sh` or asset paths, and the runs that hit it were on steward branches
whose PRs merged on `gate` alone. Run #253 failed on `dev` itself and nothing
surfaced it.

The remedy the failure names is `tools/measure_web_derivatives.py
--write-baseline`, but the message is emphatic that this belongs "in the commit
that made it" — so the first question is WHAT moved the passthrough set, not how
to re-bank it. A blind re-bank would launder whatever changed.

Found while running a full rebake for T-0015, which hit the identical failure
locally before the CI runs were looked at — so it reproduces off CI too.

**Acceptance:** `chicago-4d-bake.yml` completes and publishes on `dev`. Whatever
moved the passthrough set is identified and named — a compressor version, a
generator change, an option — and the baseline is re-banked with that cause
recorded, not merely to make the gate stop complaining. If the mismatch turns out
to be legitimate drift with no single cause, that is a recorded finding too. A
green run on `dev` is the demonstration, not a green run on a branch.
