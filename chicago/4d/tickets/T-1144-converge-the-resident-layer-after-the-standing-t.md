---
id: T-1144
title: Converge the resident layer after the standing truth tickets: zero synthesis and mint drift, no false Chicago resident, and no 1835 claim above its dated evidence
state: open
epic: META
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-09-15
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
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

**Stop condition:** the three resident derivations agree byte-for-byte with the tree and every
standing confirmed false/overstated resident assertion has either moved or gained new evidence.

**Links:** T-0660 · T-0662 · T-0691 · T-0838 · T-0991 · T-1115 · T-1121 · T-1129 · T-1136 · T-1137 · T-1145.
