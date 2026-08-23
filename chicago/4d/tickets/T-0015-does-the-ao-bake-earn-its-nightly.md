---
id: T-0015
title: Does the AO bake earn its nightly
state: claimed
epic: PIPELINE
requested_by: loop
seen: false
effort: M
legacy_id: B-A1
parent: null
opened: 2026-08-17
closed: null
pr: null
claimed_by: run 8/23/2026, 8:12:16 AM CT
blocked_on: null
needs_bake: false
---

Does the AO bake earn its nightly? Measure what AO actually contributes to the shipped
frame vs what the nightly costs. Deep history: § B-A1 (~8434).

**Acceptance:** a measured yes (keep, with numbers) or no (retire the step, with numbers).

---

## MEASURED 2026-08-23 — the answer is NO, and the question had a false premise

**There is no nightly AO cost to earn.** `--ao` is opt-in on `generators/build.py`
and *nothing passes it*: not `tools/bake.sh` (which forwards `"$@"`), not
`chicago-4d-bake.yml` (`./tools/bake.sh` and `./tools/bake.sh --only …`), not
anything else in the repo. The flag has been opt-in-and-never-opted-in.

| the ticket asks | measured |
|---|---|
| what AO contributes to the shipped frame | **nothing** — 0 of 345 master GLBs carry an `occlusionTexture`; every manifest entry that records the field says `baked_ao: false` (251 false, 94 absent, 0 true) |
| what the nightly costs for it | **nothing** — the nightly never bakes AO |
| what it *would* cost | **+137 %** build time on one asset: 1,457 ms → 3,454 ms (`sauganash_hotel`, direct Blender, 512×512, 48 samples), and **+4.4 %** file size, 94,420 → 98,580 bytes. Across 345 assets that is roughly **+11 minutes** of nightly |
| what it *would* contribute | **less than nothing today** — see below |

**And it has broken while nobody was running it.** The bake itself still works —
in memory the AO reads min 0.000, max 1.000, **mean 0.2158** over 262,144 texels,
which *corroborates* the docstring's long-standing "mean 0.265, too dark, it is a
geometry problem" rather than contradicting it. But the texture that reaches the
GLB is **entirely black, min 0 and max 0**, confirmed with two independent PNG
decoders. Switching `--ao` on today would not ship the too-dark AO the docstring
warns about; it would ship a fully-occluded one, and `assets/manifest.json` would
record `baked_ao: true` for it.

### What was done about it

Nothing was retired. Deleting `--ao` would foreclose the low-poly AO cage the
docstring describes as the real fix, and that is a direction call rather than a
measurement — so this run made the situation *honest and loud* instead:

- `assert_ao_survived_export()` refuses a GLB whose occlusion texture carries no
  occlusion, checked on the **exported bytes**. Demonstrated firing (`rc=1`) on
  the real asset before it was trusted; the default path is untouched (`rc=0`).
- The `bake_ao` docstring claimed "`--ao` exists so the path stays exercised".
  It is not exercised and it does not work. Corrected, with both measurements.
- `tools/bake.sh`'s header said `--no-bake` skips "AO baking", which read as
  though AO were on by default. Corrected.
- The export loss is **T-0158**, with the eliminations already done recorded so
  nobody repeats them (it is not the object's selection state).

### The decision left to the owner

Retire-or-fix is genuinely open and is not the loop's call: **T-0158** fixes the
export, and the AO cage remains the documented plan for making AO worth having
at all. What is now settled is that the current path earns nothing, costs nothing
because it never runs, and can no longer fail quietly.
