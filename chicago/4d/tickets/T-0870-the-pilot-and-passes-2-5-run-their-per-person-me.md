---
id: T-0870
title: The pilot and passes 2-5 run their per-person membership assertions on the --gate path, so a member whose letter_list_only flag moves in the tree kills the build instead of being reported
state: open
epic: PIPELINE
requested_by: steward
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

The pilot and passes 2-5 run their per-person membership assertions on the `--gate` path,
so a member whose `letter_list_only` flag moves in the tree kills the build instead of
being reported.

**Verified on `dev` at be0ee9d30, not inherited as a claim.**
`select_resident_research_pilot.main()` calls `derive()` before it looks at `--gate`, and
`derive()` raises `SystemExit` on each frozen member:

    for hid in LETTER_IDS:
        ...
        if not person.get("letter_list_only"):
            raise SystemExit(f"{hid}: no longer marked letter_list_only")

`select_resident_research_pass_2.py` has the same shape at its `member()` call
(`"{person_id}: no longer marked letter_list_only"` and the `established_profile`
counterpart), and passes 3-5 share that module's structure.

**Why this is the wrong direction of failure.** T-0764 has just settled that a snapshot
cell moving is *the research landing* and not staleness — `resident_cohort_freeze.gate`
now counts moved cells and reports them without failing. But a member's
`letter_list_only` flag moving is the same kind of event, arriving through a different
door, and it still stops the build. A cohort is a **frozen reservation of people**; what
the tree later says about those people is the finding the cohort exists to produce. The
gate should report it.

**Cohorts 13-15 already do the right thing, and theirs is the implementation to copy.**
`select_resident_research_pass_13.derive(pass_no, minting=False)` takes the flag precisely
so the assertions run when a cohort is being MINTED and not when it is being read
(T-0492, whose own comment records that running it on every call including `--gate` is
what broke the three cohorts before).

**Acceptance:**

1. The pilot and passes 2-5 scope their per-person membership assertions to the minting
   path, matching pass 13's `minting` parameter — the assertions are **moved, not
   deleted**, and a mint still refuses a member the stratum no longer describes.
2. On the `--gate` path a member whose flag has moved is **counted and named in the
   output**, in the same voice as `resident_cohort_freeze`'s moved-cell line, and the gate
   stays green.
3. A self-test case per selector proves both directions: minting refuses, gating reports.
4. `tools/check.sh` stays green with no manifest regenerated — this changes no cohort data.

**Found by:** PR #951, an independent implementation of T-0764 that #952 beat to the
merge. It named this residual and deliberately did not fold it in, because it meant
touching five selectors' selection logic in a PR about the snapshot. That reasoning holds;
the finding is kept here rather than lost with the branch. That PR filed it against
T-0854, which is a different ticket on `dev` — this is the re-filing at a free number.
