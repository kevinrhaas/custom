---
id: T-1034
title: The 619 town lots propose 69 new purchaser matches and nobody has ruled on one: adjudicate them in cohorts as T-0990 did, and bring the land_sales ceiling back down from 869
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-11
closed: null
pr: null
claimed_by: run 9/11/2026, 12:15:15 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34626225713
---

The 619 town lots propose 69 new purchaser matches and nobody has ruled on one: adjudicate them in cohorts as T-0990 did, and bring the land_sales ceiling back down from 869.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- the cohort is NAMED in the claim commit, and every spelling in it carries a ruling in
  `data/research/land_sales/resident_rulings.json` — `upheld` or `refused`, each with its
  `checked_against` and its reasoning;
- `python3 tools/read_land_sales.py --build` and `python3 tools/spend_land_sales.py` are
  re-run, and what moved is itemised in `data/research/land_sales/README.md`;
- the five derived files a retraction moves are re-run in the same pass —
  `export_resident_audit.py --build`, `consolidate_resident_evidence.py --build`,
  `consolidate_town_cards.py --apply`, `compile_scene.py --all` — because `check.sh`
  reports them one failing step at a time (T-0990 cohort C3's lesson);
- `bash tools/check.sh` green;
- the ceiling comes down as far as the cohort earns, with `measure_research_spend.py
  --tighten land_sales`, and the PR says how far and why not further;
- **the run that closes a cohort names the next one here before it closes.** This ticket
  closes when the crosswalk's `ruled` block reads zero unruled, and says so WITH the count
  — never on "there was nothing left".

---

## COHORT LOG — this ticket stays OPEN until the crosswalk's `ruled` block reads zero unruled

Same shape as T-0990's: a cohort is a run, the run that finishes one names the next here
rather than opening a second ticket for it. The full reasoning per cohort is in
`data/research/land_sales/README.md`; this log is the ledger.

### DONE

**Cohort A — the twenty whose PERSON already carries a ruling under another spelling of
the same name.** Ruled 2026-09-11. **Nineteen upheld, one refused** — `ruled` 89/1/48/72 →
**108/1/49/52**; matched 162 → 161, entries carried 619 → 618, one card retracted
(`wright_truman_g`, lot 7 of block 5, $900). Acres are unchanged because a town lot has
none: the register prints `0000.00` in the acres column for every one of the 619.

| upheld | refused |
|---|---|
| BOTSFORD J K, CARPENTER P, EGAN W B, EGAN WILLIAM, FULLERTON A N, GOODHUE J C, HAMILTON R J, HUBBARD E K, HUBBARD GORDON S, KIMBERLY E S, KINZIE ROBERT, MARSH S, MERRILL G W, MULFORD J H, NEWBERRY W L, PRICE JERE, SHERMAN S W, TAYLOR E D, TEMPLE J T | WRIGHT T |

**What the cohort taught, in one line each** (the argument is in the domain README):

*The precedent is not the ruling.* Nineteen carry a token the fuller spelling also carried;
WRIGHT T carries none, and Fergus 1839 prints both Truman G. and Timothy Wright. Ask what
the token is before reaching for the precedent.

*The register's SEQUENCE is a check, and the June 1836 town sale hands it to you.* These
are lots entered block by block over ten days, so EGAN WILLIAM — no middle initial, and a
rival EGAN WILLIAM G in the same book — is decided by standing in block 45 on 25 June
between WILLIAM B's lots 5 and 7. The section deposits can rarely do this; a ring tract has
no neighbours in the book.

*The town's own paper can be the source of the mis-spelling.* The Democrat prints "Gordon
S. Hubbard" in the notice electing him a trustee, so HUBBARD GORDON S is not a second man.

*Three spellings the crosswalk does not propose are left open on purpose* — GOODHUE G J,
KIMBERLY EDWARD, NEWBERRY WALTER S. Each may be a misreading of a spelling already ruled
on, and a ruling can only be made on a proposal the crosswalk holds. The Newberry one is
noted on T-0396.

*The ceiling is not the measure of this ticket.* `measure_research_spend.py` anchors
rulings through `crosswalk.json` and cannot see `resident_crosswalk.json`, so twenty
judgements moved the meter by one and the ceiling came down 869 → 868. That is T-0962's
blind spot alive in this domain; the crosswalk's own `ruled` block is the number to read.

Filed on the way past: nothing. Every card the cohort touched was clean or already
carrying a ticket, and the one open question found (Walter S. Newberry) was added to
T-0396 rather than filed, per the queue's FILING RULE.

### NEXT

**Cohort B — the twenty-four remaining proposals with an empty `rivals[]`.** Named in the
domain README with the list. Then the twenty-eight with a namesake, by surname. 52 unruled.
