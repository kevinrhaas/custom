---
id: T-1333
title: The closing convergence rebuild: index.json, the sidecars, the town census, the published residents and the final resident audit, with the exact household, person and grade deltas and every retired id's redirect, and acceptances 3, 5 and 9 stated as measured deltas rather than spot readings
state: done
epic: META
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1144
opened: 2026-09-18
closed: 2026-09-18
pr: 1477
claimed_by: run 9/18/2026, 4:02:57 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-18T22:10:23.109Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35389718070
---

The closing convergence rebuild: index.json, the sidecars, the town census, the published residents and the final resident audit, with the exact household, person and grade deltas and every retired id's redirect, and acceptances 3, 5 and 9 stated as measured deltas rather than spot readings.

Piece 1 of 2 of **T-1144 — Converge the resident layer after the standing truth tickets: zero synthesis and mint drift, no false Chicago resident, and no 1835 claim above its dated evidence**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

1. One rebuild derives the whole closing set in the manifest's order — `index.json` and its
   `merged` table, the 1835 sidecars, the town census, the published residents and the final
   resident audit — and every one of them re-derives on a clean tree afterwards. Not five
   tools run by hand in an order nobody wrote down.
2. The report states **deltas, measured**: households, persons and grades, each as a number
   with its before and after, against the tree this ticket opened on. A count with no
   baseline is not a delta and does not close this.
3. Every retired id's redirect is named and **arrives** — no dead end, no chain, no id both
   retired and live. T-1144's redirect leg (PR #1469) built `redirect_faults()` and measured
   66 redirects arriving; this ticket's rebuild keeps that at zero faults rather than
   re-proving it by hand.
4. **Acceptances 3, 5 and 9 are stated here as measured deltas, not re-asserted.** They read
   clean on 2026-09-18 — no Mary Durbin, John Simmons, John Vincent or Logdson;
   `audit_scene_window_trades.py --check` reports 0 standing rows; all 820 uncertain
   households carry their `last_dated_appearance` leg — and T-1144 banked them deliberately
   "to the closing pass to state as deltas rather than claimed closed from a spot reading".
   A spot reading repeated is still a spot reading.
5. The gate re-derives the closing set, so a later branch that moves the town tree cannot
   leave this report stale and green. If a file in the set is not in `derived_manifest.json`,
   that is a finding of this ticket, not a footnote.

**NOT IN SCOPE:** the letter-list mint's drift and the one-letter-apart identity rule. That
is T-1334, it is read by T-1222, and it is a different question from rebuilding the layer.


## DONE (2026-09-18)

`tools/report_convergence_closing.py`, gated in `check.sh` as *"every household says which
writer put it in the tree, and the sums close"* with its self-test beside it (31
assertions), writing `data/research/convergence_closing.json` and
`docs/RESEARCH/convergence-closing-2026-09.md`, listed in `tools/derived_manifest.json` and
measured into `tools/writer_inventory.json`.

**1 — one rebuild, in the manifest's order.** `--closing-set` reads
`derived_manifest.json`, selects the five, runs them in the order the manifest records and
then re-derives each one. It reads the order rather than restating it, and it fails if the
set stops being five. Measured on this branch, 11.2 s end to end, and it moved no committed
byte outside this ticket's own outputs:

    rebuild_resident_index.py --write   0.4s  ->  --check          ok
    report_convergence_closing.py --build 0.2s -> --check          ok
    compile_scene.py --all              8.6s  ->  (no verify declared)
    town_census.py                      0.0s  ->  --check          ok
    export_resident_audit.py --build    1.0s  ->  --check          ok

**2 — the deltas are measured, and the baselines are frozen.**
`data/research/convergence_closing_baseline.json` holds two readings, each taken once over
a named commit with THIS FILE'S OWN `build()` checked out into a worktree, so both ends of
every delta are measured the same way: `f7d090ebc` (2026-09-15, the tree T-1144 opened on)
and `0f3b6db5c` (2026-09-18, the commit that split it and opened this ticket). The report
reads that file and never rewrites it.

    measure                                 2026-09-15   2026-09-18   now    change
    households                                   1,281        1,258   1,258     -23
    persons                                      1,305        1,288   1,288     -17
    attested / inferred / reconstructed      419/886/0    410/875/3  410/875/3  -9/-11/+3
    retired  (all arriving)                         60           66      66      +6
    households_from_civic                          413          392     392     -21
    rebuilt_away_people_still_present                4            0       0      -4
    uncertain_presences                            832          820     820     -12
    uncertain_presences_carrying_the_leg             0          820     820    +820

A measure an older baseline is silent on prints `not measured then`, never `0` — the tree
was real and the reading was simply never taken, and a zero is a claim nobody made. The
other direction is a fault: `measure_lost_its_history` fires when a baseline records a
measure this report has stopped producing, because a renamed measure loses its history in
silence.

**4 — acceptances 3, 5 and 9 as measured deltas, not spot readings repeated.**
Acceptance 3 is the row `rebuilt_away_people_still_present`, 4 -> 0: Mary Durbin, John
Simmons, John Vincent and Cery Logdson were on cards when T-1144 opened and hold no
household or person record now. Acceptance 9 is `uncertain_presences_carrying_the_leg`,
0 -> 820: the dated evidence leg did not exist at the baseline and is derived on every
uncertain presence today, with 0 settled presences still carrying one, because the field
may not outlive the verdict. Acceptance 5 is the one measure this report does NOT derive
and it says so on its face: `audit_scene_window_trades.py --check` read 6 standing rows at
`f7d090ebc` and 0 at `0f3b6db5c`, both recorded readings from the tool that owns the rule,
and the live end needs no recording here because that tool's `--check` is its own step in
`check.sh` on every commit.

**3 — every retired id's redirect is named and arrives.** All 66, each with its merge rule,
cluster and ruling ticket, and `arrives` asked fresh from the read side: the redirect must
name a household card and a person card that are both standing, and one pointing at another
retired id is a chain, which is a dead end one hop further away. 66 of 66 arrive, zero
`redirect_does_not_arrive` faults, and T-1144's `redirect_faults()` is kept rather than
re-proved by hand.

**5 — a finding, not a footnote: the published residents layer cannot be in the manifest.**
Four of the five closing-set members carry a manifest step and this report carries one
beside them. The fifth has none because its output is the publish mirror, untracked by
design since T-0938 — the manifest resolves committed files and there is no committed file
here to resolve. Its freshness is gated instead by `check_published_residents.mjs`, which
asserts the shipped minified layer parses deep-equal to its source, file for file. The set
is covered by two mechanisms rather than one, which is worth knowing before somebody adds a
manifest row that would resolve nothing. Recorded here and in the report.
**A second, smaller one:** `compile_scene.py --all` declares no `verify` in the manifest,
so `--closing-set` prints it as undeclared rather than silently passing it. It IS gated —
`compile_scene.py --all --check` is its own step in `check.sh` — so this is a manifest
completeness gap, not a coverage gap, and it is left as found rather than widened into.

**WHAT THE ACCOUNTING FOUND, both read off committed fields and neither ruled on here.**
79 cards carry no `source_pass`: 74 are the authored core the mints were built on top of,
and **five are survivors of the retired invented-name programme** (T-0489) —
`hh_inf_cooper_north_04`, `hh_inf_joiner_north_02`, `hh_inf_physician_south_01`,
`hh_inf_tailor_north_02`, `hh_inf_tavern_keeper_north_01`. Each opens its own
`research_note` with `RECONSTRUCTED HOUSEHOLD` and no pass re-derives any of them, so a lap
that rebuilt every writer would leave all five untouched. T-1294 found one from the register
side; this is the full list. Second: **seven cards the letter-list mint minted hold no
`letter_list_only` person any more** — `hh_ambrose_joshua`, `hh_bradford_harriet`,
`hh_chapman_chas_h`, `hh_fitzgerald_thos`, `hh_murray_alonzo`, `hh_neff_r_a`,
`hh_simons_e` — a later pass found independent evidence and carried them out of the cohort.
That is **T-1334's** 798-file drift measured from the other side: re-running the mint puts
all seven back, which is a confidence downgrade by re-derivation. Named, not ruled on, and
not touched here — T-1334 is explicitly out of this ticket's scope.

**`mint_owns_reconstructed` is T-1144 acceptance 8 asked of the TREE.** The parent's first
pass wired `refuse_reconstructed_grade.py` into the four mints and proved they CALL it;
this proves the promise holds in the committed records. All three reconstructed persons
stand in `authored` cards, each with a `model`/`household_size` basis, a seed and a
`replaceable_by`.

**The self-test takes nothing off disk.** `build()` accepts its households and its index as
arguments, so all six refusals fire over in-memory fixtures. The first cut proved them by
writing a broken `index.json` and restoring it, and a gate that has to corrupt a committed
record to prove itself can leave one behind when it is interrupted.

**A NOTE FOR ANY PASS THAT CLAIMS A TICKET IN THIS BAND.** Claiming turns
`research-closing-audit-2026-09.md` and `research-signoff-2026-09.md` red on their own gate
steps, because both embed the ticket's state in their unresolved-unit tables and `claimed`
is not `open`. Do not rebuild them to chase it — release or close the claim and the two go
green on their own. Rebuilding while claimed commits the word `claimed` into two reports
and the next run has to undo it. That cost a cycle here.

