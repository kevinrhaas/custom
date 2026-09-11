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
claimed_by: run 9/11/2026, 4:44:55 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34650587516
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

**Cohort B — the twenty-four remaining proposals with an empty `rivals[]`.** Ruled
2026-09-11. **Ten upheld, fourteen refused** — `ruled` 108/1/49/52 → **118/1/63/28**;
matched 161 → 147, **thirteen cards retracted** with twenty-three register rows and $45,319
of stated purchase money. Only **80 acres** move, the one quarter-section that came off
FAY H K: the other twenty-two rows are town or canal lots, and a town lot has no acreage.

| upheld | refused |
|---|---|
| FUNK ABSALOM, GARRETT A, GARRETT AUGUST, HEACOCK RUSSEL E, HEACOCK RUSSELL E, LOYD A, MCKEE DAVID, OGDEN WILLIAM B, SPRING GILES, WELLMAKER JOHN | CHURCH T JR, FAY HARRISON K, FINLEY CLEMENT A, KEYES EDWARD, MACK STEPHEN, MCGREGOR A, PEARSON HIRAM, ROBERTS E, ROBERTS EDMUND, RYAN THOMAS, SHEPHERD A, SHERWOOD S J, WILCOX DELAFAYETTE, WILSON JOHN S |

**What the cohort taught, in one line each** (the argument is in the domain README):

*T-0990's own cohort B had drawn this exact line, and it held without being bent.* Same
field, same question — does the town hold this man in anything more than a bare name? Ten
upholds each have a second document with something IN it; nine of the fourteen refusals have
one name-only reading and nothing else; four are cards the layer marks `letter_list_only`,
two of which T-0990 had already refused in another spelling.

*One line of one civic list is not enough, and it is not a rule against civic lists.* Seven
refusals rest on a single tax or poll line (the STANLEY JOSEPH shape). WELLMAKER JOHN is
UPHELD on civic lists — six readings across five domains, and a surname that appears exactly
once in all 6,849 identities, so there is no rival reading anywhere rather than none in a
thin layer. What each reading says decides it; how many there are does not.

*The sequence argument that carried cohort A cannot work here, by definition.* These
surnames appear once, so no reading of the same name stands on the block beside them.

*The register can be its own rival reading.* PEARSON HIRAM is refused because the same
volume enters PEARSONS HIRAM forty-four times, two of them town lots six days earlier in the
same sale, upheld to Hiram Pearsons — $22,410 off a card a surname fold away from him. Cohort
A's README named this one in advance.

*A middle initial can name the OTHER man.* SHERWOOD S J is the jeweler Smith J. Sherwood,
whom the corpus holds under his own name, and not the Stephen of the letter lists.

*The ceiling moved by one again, 868 → 867*, for cohort A's reason exactly: the meter cannot
see `resident_crosswalk.json`, so twenty-four judgements read as one. T-0962's blind spot,
second cohort running.

Filed on the way past, both from evidence read for this cohort: **T-1038**, the Norris 1844
jeweler line the identity layer has folded onto the letter-list Sherwood card; **T-1039**,
T-0885's row-is-not-a-parcel question asked of the town-lot volume, where four of twenty-four
purchasers turned up a lot entered twice or three times in paired and doubled prices. The
HEACOCK uphold was ADDED to **T-0884** rather than filed, per the queue's FILING RULE — it
settles the identity half of that ticket and leaves it the geometry.

### NEXT

**Cohort C — the twenty-eight left, and every one of them now has a NAMESAKE** (`rivals[]`
non-empty). Cohort B emptied the no-namesake shape, so what remains is where T-0990's C1–C3
found their refusals: the layer holds a namesake and the forename alone chose. Take them **by
surname block**, as T-0990 did — twenty-eight is more than one run can argue honestly — and
read C1's BROWN WM rule first: a spelling with no discriminating token is its own proposal
however well a fuller spelling of the same name did. The run that closes a block names the
next one here. 28 unruled.
