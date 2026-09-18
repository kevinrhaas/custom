---
id: T-1144
title: Converge the resident layer after the standing truth tickets: zero synthesis and mint drift, no false Chicago resident, and no 1835 claim above its dated evidence
state: claimed
epic: META
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-09-15
closed: null
pr: null
claimed_by: run 9/18/2026, 10:41:14 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35363076082
---

Converge the resident layer after the standing truth tickets: zero synthesis and mint drift, no false Chicago resident, and no 1835 claim above its dated evidence.

**Measured on `dev`, 2026-09-15.** A fresh resident synthesis would change 150 files although
`synthesis_drift_baseline.json` is empty. The documented and letter-list mint checks would change
41 and 798 files respectively, but `check.sh` invokes `synthesize_resident_research.py --check`
under both labels instead of the passes whose output the labels promise. A green generic synthesis
therefore does not mean either cohort agrees with its derivation.

This is the convergence pass, not a second ticket for each source-reading question. It consumes
the standing truth tickets after they land: T-1129 (four Bear Creek people are not Chicago
residents), T-1115 (uncertainty brackets), T-1121 (Leonard C. Hugunin), T-1136 (presence brackets),
T-1137 (one writer deleting another's findings), T-0662/T-0691 (the two mint drifts), and T-1145
(dated roles, which supplies T-0991's honest home for pre-scene occupations). If one is still open,
do not re-decide it here: state the dependency and leave this ticket open.

**Acceptance:**

1. Run all three writers against throwaway copies, review their exact diffs, and make the
   committed resident layer a fixed point: synthesis drift 0, documented-mint drift 0 and
   letter-list-mint drift 0. Do not bless drift with a nonzero baseline.
2. Correct `check.sh` so each label invokes its own writer's `--check`/drift contract. A self-test
   changes one output of each writer and proves the matching gate fires.
3. Rebuild away Mary Durbin, John Simmons, John Vincent and Cery Logdson unless a new independent
   Chicago source is committed; no resident may rest solely on church readings whose
   `at_chicago` values are all false.
4. Apply the bracket, name and writer-ownership repairs from T-1115, T-1121, T-1136 and T-1137
   through the generators, never as hand edits. Re-run every affected presence and identity rule.
5. `audit_scene_window_trades.py --check` reaches zero after T-1145: a pre-scene or later role may
   remain dated on the person, but it cannot call itself an attested 1 July 1835 occupation.
6. Rebuild `index.json`, sidecars, town census, published residents and the final resident audit;
   the closing report gives the exact household/person/grade deltas and names every retired id's
   redirect. Relevant resident and ticket gates pass.

**Owner review, 2026-09-17 — added acceptance** (the owner asked that the research-spend tickets
be reviewed and enhanced before the reconstruction bands below them run):

7. The convergence report names, per person, which of the plural `roles[]` (T-1145) and which
   home/work/other locations (T-1147) reach 1 July 1835, so the sign-off ticket T-1157 can read
   coverage per axis off one table rather than re-deriving it.
8. The `reconstructed` grade stays at zero in this ticket and the three writers refuse to emit it:
   reconstruction begins only at T-1167 under its own programme file, never inside a mint.
9. Every household `present_on_scene_date: uncertain` keeps the dated evidence leg that made it
   uncertain (the last appearance and its date) as a structured field, because T-1159 classifies
   the 893 uncertain presences by that date.

**Stop condition:** the three resident derivations agree byte-for-byte with the tree and every
standing confirmed false/overstated resident assertion has either moved or gained new evidence.

**Links:** T-0660 · T-0662 · T-0691 · T-0838 · T-0991 · T-1115 · T-1121 · T-1129 · T-1136 · T-1137 · T-1145.


## IT WAS FOLDED INTO T-1157 AND THE GATE REFUSED IT (2026-09-17)

Same refusal as T-1241, and the same invariant. `research_spend_ledger.py` holds that *a
unit may only defer to work that is still going to happen*, and unresolved research units
name THIS TICKET BY ID as the work they wait on. Closing it as folded made those units defer
to finished work, and `measure_research_spend.py --check` failed on every one.

**A ticket that research units defer to by id cannot be consolidated away** — not without
repointing every unit that names it, which is a bigger and riskier change than a shorter
queue is worth. That is the real constraint on tightening this band, and it is worth knowing
before anyone tries again.

**The tightening that DOES apply:** run this in the SAME PASS as T-1157 and T-1241. The drift
checks here are the sign-off report's evidence section, not a separate expedition, and one run
produces all three.


## ACCEPTANCE 8 IS DONE, AND THE TICKET STAYS OPEN (2026-09-18)

`tools/refuse_reconstructed_grade.py`, gated in `check.sh` as *"no research writer can
mint a reconstructed resident"* with its self-test beside it, and called by all four
writers of `data/residents/` on the way out — `synthesize_resident_research.py`,
`mint_documented_residents.py`, `mint_letter_list_residents.py`,
`mint_placed_residents.py`.

The refusal runs in EVERY mode, including `--check` and `--report`, so a mint is red on
the same rule its write is. What it checks is the **call**, not the import: a refusal
imported and never called is the failure shape it exists for, so `WIRED_WRITERS` names
the exact call each writer must carry and `--check` fails if one goes missing.

What it deliberately leaves alone: per-attribute `confidence: "reconstructed"` — the
`{"value": null, "confidence": "reconstructed", "note": "Not attested."}` block on one
field of a real attested person. That is a statement about a fact, not about whether the
person existed; hundreds of committed records carry it and refusing it would be wrong.
The self-test asserts that distinction directly, so a later tightening cannot quietly
widen the refusal onto it.

Measured before the wiring and unchanged after it: `synthesize_resident_research.py
--check` 1,282 people, 410 attested, 872 inferred, 0 reconstructed; documented mint 39
minted / 96 refused, no drift; placed mint 5 minted / 165 refused, no drift; letter-list
mint the standing 798 (T-0691's, untouched here). Proved end-to-end as well as by
self-test: `mint_documented_residents.record()` was monkeypatched to grade one person
`reconstructed` and `build()` refused all 39, naming each household.

This was the one acceptance clause that does not wait on anything — and it is the one the
bands below need FIRST, because T-1167 is what turns the grade on. The boundary is now one
line per writer to see, and the reconstruction generator T-1167 brings simply does not
call it.

**Why the ticket is still open.** Acceptance 1 is not reachable today: letter-list-mint
drift is 798 files, that drift is T-0691's, and T-0691 is `blocked-tech` behind T-0660 —
which is still `open` at row 2 of the queue. Per this ticket's own rule, that dependency
is stated rather than re-decided here. Acceptances 3 and 5 are satisfied on `dev` and were
re-measured today: Mary Durbin, John Simmons, John Vincent and Cery Logdson hold no
household or person record, and `audit_scene_window_trades.py --check` reads 0 standing
rows and re-derives. Acceptance 2 was closed by T-1228 except for the letter-list slot,
which is acceptance 1's blocker again. What remains for the convergence run is 1, 2's last
slot, 6, 7 and 9 — and the note above still holds: take it in the same pass as T-1157 and
T-1241.

`claimed_by` is cleared with this, and the `claim/t-1144` marker released: nobody holds
this ticket.


## ACCEPTANCE 9 IS DONE, AND THE TICKET STAYS OPEN (2026-09-18, second pass)

`tools/derive_presence_evidence_leg.py`, gated in `check.sh` as *"every uncertain
presence carries the dated evidence leg under it"* with its self-test beside it, and
carried through all four mints by `tools/resident_mint_carry.py`.

820 uncertain presences, 820 legs, **779 of them dated**: 733 a dated reading of the
person, 43 the far end of a cited source's SPAN, 3 an arrival bound, 41 no date at or
before the scene date. The leg is derived from the blocks the card already holds —
`press_evidence`, `civic_evidence`, `book_evidence`, `church_evidence`,
`census_evidence`, `profile_facts`, `letter_list_returns`, `roles[]`, `arrival` — and
never from prose.

**The tiers are the honesty, and they are asserted.** A sighting outranks a span even
when the span reaches further, because the role's own note says that bound is the
source's and not the man's: a Democrat run covering 1833-11 to 1835-08 is not a sighting
in August. And a reading is NOT clipped to the scene date — a source that says `1835`
does not say which half, so `reaches` stays 1835-12-31, `includes_scene_date` is true,
and the card states that it pins no last sighting before the day. 102 legs are in that
position. Clipping them would have been a confidence upgrade by arithmetic, which is
the thing this field exists to prevent; the self-test holds both rules.

**The field may not outlive the verdict.** A leg is written only under `uncertain` and
removed when the presence is settled — `--check` holds both halves, and
`resident_mint_carry.py --self-test` proves a mint that now derives `present` does not
get the leg back.

`tools/export_borderline_roster.py` was the reason to do this: its
`last_dated_appearance()` reached into `present_on_scene_date.note` with a regular
expression, which found a date on the handful of notes that happened to print one and
fell back to the arrival bound for the rest. It reads the derived field now — one
implementation — and each R1 row carries `describes_date` (the source's own words),
`dated_evidence_reaches` (the comparable day) and `dated_evidence_includes_scene_date`.
T-1159's 814 R1 rows are 773 dated where they were a scattering before. The resident
card prints the leg under the presence row and names which of the three kinds it is.

**Why the ticket is still open.** Acceptance 1's letter-list slot and the last slot of
acceptance 2 are one and the same, they are **T-1222's** — read that ticket, it holds
the measurement — and they are not a hand's turn: `mint_letter_list_residents.py
--check` reports 798 files, of which 648 differ in nothing but the five keys the
synthesis owns, 81 are households the mint no longer derives, 54 are ids the name
splitter now mints differently and 14 are genuinely mint-owned. T-0662 read that drift
and found byte-identity to be the WRONG CONTRACT for a pass that is not the last writer
of its files; the shape it wants is T-1228's field-level ownership settlement, and
`data/research/check_gate_baseline.json` carries the row saying exactly that. It is
re-measured and unchanged today, and this pass did not make it worse.

Acceptances 6 and 7 remain, and they are a pass of their own: 7 is a per-person table
of which `roles[]` and which locations reach 1 July 1835, and this ticket's leg is the
presence axis of it — `days_before_scene_date` and `includes_scene_date` are the two
columns that axis needs, so 7 now has one of its three axes derived rather than
re-argued.

**A WARNING PAID FOR HERE.** `node tools/ticket.mjs restamp T-1144` does not re-stamp a
ticket's dates — it RENUMBERS it, and it renumbered this one to T-1305 mid-run. That is
the one edit this ticket's own tombstone note forbids: research units defer to T-1144 BY
ID, and `measure_research_spend.py --check` fails on every one of them the moment the id
moves. It was reverted in the same minute (the `site/` mirror is generated and
gitignored, so nothing escaped). To leave this ticket open with its claim released, edit
`claimed_by` and `claimed_run` by hand, as the pass before this one did.

`claimed_by` is cleared with this: nobody holds this ticket.
