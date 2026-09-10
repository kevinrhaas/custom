---
id: T-0990
title: The land-sale proposals T-0697 added when the surname rule widened are unruled: rule them one cohort per run, and the run that closes a cohort files the next
state: claimed
epic: META
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: run 9/10/2026, 6:10:18 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34540643440
---

The land-sale proposals T-0697 added when the surname rule widened are unruled: rule them one cohort per run, and the run that closes a cohort files the next.

**FOUND BY T-0850**, which was written against a crosswalk of 35 matched spellings and
closed against one of 126. T-0700 ruled the ring deposit's nine; T-0850 ruled the first
deposit's twenty-six. In between, **T-0697** changed the mechanical rule — it stopped
requiring exactly one person of the surname and put every reading to every namesake on
`tools/namesake.py` — and **139 spellings met 124 people where 38 had met 35**. Neither
ticket was written against the hundred-odd proposals that arrived that way, and after
T-0850 the crosswalk's own `ruled` block reads **104 unruled**. They reached cards the same
way the ring's nine did: `spend_land_sales.py` writes what `matches[]` declares, and nobody
adjudicated them.

**The rule is written and does not need re-deciding** — `resident_rulings.json`'s
`the_ruling_rule`, applied twice now. A proposal is upheld only where the town's own record
carries something the register's row can be checked against BEYOND a bare name: a middle
initial both records print, a trade the purchase is what you would predict from, a second
document that brackets the entry date, or the register's own Residence column. A bare name
on each side is refused, however unlikely the coincidence looks, and a refusal RETRACTS the
paragraph the spend pass wrote.

**A cohort is a run.** T-0850 took twenty-six spellings and that was a full run: the reading
is per person, and the reasoning is hand-authored because a judgement is not a derivation.
So this is worked one bounded cohort at a time — the spellings T-0697's namesake rule
reached that carry a `rivals[]` list are the natural first one, since those are the
proposals where the layer holds a namesake and the forename alone decided.

**Acceptance,** per cohort: (state it before working — the definition of done, never
weakened to pass)

- the cohort is NAMED in the claim commit, and every spelling in it carries a ruling in
  `data/research/land_sales/resident_rulings.json` — `upheld` or `refused`, each with its
  `checked_against` and its reasoning;
- `python3 tools/read_land_sales.py --build` and `python3 tools/spend_land_sales.py` are
  re-run, and what moved is itemised in `data/research/land_sales/README.md` — matched,
  refused, cards retracted, entries and acres carried;
- `bash tools/check.sh` green;
- **the run that closes a cohort files the next cohort's ticket before it closes**, with
  the remaining count read off the crosswalk's `ruled` block. This closes when that block
  reads zero unruled, and says so with the count — never on "there was nothing left".

---

## COHORT LOG — this ticket stays OPEN until the crosswalk's `ruled` block reads zero unruled

A cohort is a run, and the run that finishes one names the next here rather than opening a
second ticket for it: the queue is meant to get shorter, and one standing ticket with a log
is fewer lines than one ticket per cohort. A run takes the cohort at the head of NEXT below,
rules it, moves it up into DONE with its counts, and names the cohort after it.

### DONE

**Cohort A — the fourteen an INITIAL decided among namesakes** (`match: initial_agrees` AND
`rivals[]` non-empty). Ruled 2026-09-10. **Eleven upheld, three refused.**

| upheld | refused |
|---|---|
| BLANCHARD F G, BLANCHARD F G AS, BLANCHARD FRANCIS G, FOOT STAN, HADDOCK E H, REED JAMES W, WRIGHT T G, BEAUBIEN J B, MONTGOMERY LOTON WM, MONTGOMERY LOTON W, HUNTER E E | GOODRICH CHAUNCEY, SMITH LIMAN, MORRISON THOS M |

**What the cohort taught, and the next run should use it.** The discriminator was in
`data/residents/directories.json` nearly every time. Where the town's card holds only an
initial, Fergus 1839, Fergus 1843 and Norris 1844 very often print the forename whole —
*Loton W. Montgomery*, *Francis Gurtrey Blanchard*, *Starr Foot*, *Truman G. Wright*,
*Edward H. Haddock* — and that printing, not the initial, is what upholds or refuses. Three
of the fourteen have no directory line at all, and all three are the refusals. **Check the
directories before writing a word of reasoning.** The register's second habit is worth as
much: it prints the same purchaser twice, once abbreviated and once in full (HADDOCK E H /
HADDOCK EDWARD H, WRIGHT T G / WRIGHT TRUMAN G, HUNTER E E / HUNTER EDWARD E, the last two
being one entry read twice with the Residence column on the fuller reading).

Filed on the way past: **T-0993**, Francis Gurtrey Blanchard's two cards.

---

**Cohort B — the twenty-four with NO namesake at all** (`rivals[]` empty). Ruled 2026-09-10.
**Twelve upheld, twelve refused** — matched 123 → 111, ruled 49 → 71, unruled 90 → 66; twelve
cards retracted, sixteen register rows, 1,549.24 acres and $2,084.04 taken back off them.

| upheld | refused |
|---|---|
| BOTSFORD JABEZ K, BOYER JOHN K, DOLE GEORGE W, FULLERTON ALEXANDER, GOODHUE JOSIAH C, KIMBALL WALTER, KIMBERLEY EDMUND S, KNICKERBACKER ABRM V, PECK P F W, SHRIGLEY JOHN, MARSH SYLVESTER, JAMISON LOUIS T | CHIPMAN ANSEL, ROBERTS EDMOND, STANLEY JOSEPH, ROWLEY HEMAN A, HURD NIRAM F, ALLISON THOMAS, SACKETT JOSHUA, OSTRANDER CATHRINE, BLAISDELL BENJAMIN, SHEPHERD ALBERT, WILCOX DE LA FAYETTE, CHURCH THOS JR |

**What the cohort taught.** *An empty `rivals[]` is not safety* — it says the layer holds the
surname once, and the register itself sells to a second Hurd and to three Robertses. The line
that decided all twenty-four is **whether the town holds the man MORE THAN ONCE**: every uphold
has a second document on the town's side, and eleven of the twelve refusals have one name-only
reading and nothing else. Six refused cards are marked `letter_list_only` in the residents layer,
which turns out to be the SPENCER WILLIAM G test written as a field — look for it first.

*A middle initial discriminates; it does not corroborate.* Three proposals agreed on a middle
initial and did not go the same way: JAMISON LOUIS T upheld because the town prints *L. T.
Jamison* twice independently, ROWLEY HEMAN A and HURD NIRAM F refused because the initial pair IS
the town's whole record. Cohort C will meet this constantly.

*The Residence column needs a town-side partner.* COOK carried DILL FRANK and LUDBY JOHN against
a poll list and a newspaper; against an uncalled-for letter (CHIPMAN ANSEL, ALLISON THOMAS) it
carries nothing.

**Before it could add, it had to restore.** PR #1055 had deleted 546 lines of
`resident_rulings.json` — T-0850's twenty-six rulings and cohort A's fourteen, forty judgements —
and every gate stayed green. Twelve cards were re-carrying retracted claims. Restored as the
union of both histories, with T-0851's firm rule intact and its absorbed PRUYNE P AND CO ruling
retired rather than deleted; the restored file rebuilds to 90 unruled, cohort A's own number,
which is the proof nothing else was lost. **A sibling slice reached the same finding in the same
hour** and shipped it as #1073/#1075 while this branch was rebasing onto it; the restoration
below is theirs, this branch's contribution is cohort B on top of it, and the gate that would
have caught #1055 is their **T-0999**.

Filed on the way past: **T-1001**, two cards for one physician and the exact surname fold that
hid the namesake.

---

**Cohort C1 — the seventeen `forename_agrees` proposals with namesakes whose surname falls in
A-C.** Ruled 2026-09-10. **Eleven upheld, six refused** — matched 112 → 106, ruled 71 → 88,
unruled 66 → 49; five cards retracted, nine register rows, 1,040.00 acres and $1,608.00 taken
back off them, against 23 rows, 1,125.71 acres and $2,943.00 that stand.

| upheld | refused |
|---|---|
| ANDREWS WILLIAM, ARCHER WILLIAM B, BEAUBIEN MARK, BENNETT WILLIAM, BOWEN ERASTUS, BROWN WILLIAM H, CARPENTER PHILO, CHAPMAN CHARLES H, CLARK JOHN K, COOK JOSIAH P, COOK THOMAS | ALLEN WILLIAM, ANDREWS DAVID, BALLARD THOMAS, BLAKE LEVI, BROWN WM, BURDICK PAUL |

**What the cohort taught, and cohort C2 should use it.**

*The `letter_list_only` field decided five of the six refusals, and it lied on one of the
upholds.* ALLEN WILLIAM, ANDREWS DAVID, BLAKE LEVI and BURDICK PAUL are each one return of
uncalled-for letters and nothing else, and they went the way cohort B's six went. CHAPMAN
CHARLES H carries the same flag and should not: three of its four `press_evidence` rows are
ordinary printings with their own locators and only one is a letter list. **Read
`press_evidence[].list`, not the flag** — filed as T-1005, which found seven cards flagged
that way.

*The register printing a purchaser twice does NOT always mean one man.* Cohort A found the
abbreviated-and-full habit (HADDOCK E H / HADDOCK EDWARD H) and it is real; C1 found where it
breaks. BROWN WILLIAM H is upheld on its middle initial, its bank and an ILLINOIS in the
Residence column; BROWN WM is REFUSED, because Fergus 1843 prints three distinct William
Browns and the layer holds one only because the layer is thin. **A spelling with no middle
initial is its own proposal and gets its own ruling**, even when a fuller spelling of the same
surname was just upheld.

*The sibling test is the cheapest one in the cohort.* ANDREWS WILLIAM upheld and ANDREWS DAVID
refused, off the same surname on the same day: one has a newspaper printing and a directory
trade, the other has a letter and a research row whose `evidence_for` is EMPTY. A
`corroborated_enrichment` outcome with nothing written in it corroborates nothing — check the
field, not the grade.

*The Residence column carried one uphold on its own back.* BENNETT WILLIAM is a G3 projected
resident — poll list of 1834, and nothing else on the card — and it is upheld because one of
its four rows states COOK and the poll list is the town-side partner cohort B said that column
needs. It is the weakest uphold in C1 and is marked so here.

Filed on the way past: **T-1004**, Erastus Bowen's card gathering two men (the 1843 veterinary
surgeon was sixteen in 1835); **T-1005**, the seven stale `letter_list_only` flags.

---

**Cohort C2 — the twenty-one `forename_agrees` proposals with namesakes, surnames D-J.** Ruled
2026-09-10. **Sixteen upheld, five refused** — matched 106 → 101, ruled 89 → 110, unruled 49 →
28; four cards retracted and one rewritten, fourteen register rows, 476.52 acres and $1,525.75
taken back off them, against 57 rows, 4,086.77 acres and $7,855.29 that stand.

| upheld | refused |
|---|---|
| DAVIS GEORGE, EGAN WILLIAM B, FOOT JOHN, GOODRICH EBENEZER, HADDOCK EDWARD H, HAMILTON RICHARD J, HANDY HENRY S, HARMON CHARLES L, HARMON CHAS L, HARMON ELIJAH D, HARMON ISAAC D, HUBBARD ELIJAH K, HUBBARD GURDON S, HUNTER EDWARD E, JONES BENJAMIN, JONES WILLARD | DAVIS JOHN, HALL GEORGE, HARMON ISAAC, JACKSON SAMUEL, JONES WILLIAM |

**What the cohort taught, and cohort C3 should use it.**

*C1's BROWN WM rule did the most work of any lesson carried forward, and it fired TWICE.* HARMON
ISAAC D upheld and HARMON ISAAC refused, two days apart on the same card; JONES WILLARD upheld
and JONES WILLIAM refused, on the same two afternoons of October 1833. Both times the barer
spelling failed for the reason Brown's did — the town's own PRINTED record holds a second man of
the name (*Harmon, Isaac Newton, with C. L. Harmon* in Fergus 1843; three William Joneses in the
same volume) and the layer holds one because the layer is thin. **HARMON CHAS L is the control
that keeps the rule from becoming "refuse every short spelling":** it is a CONTRACTION, not a
barer spelling, it carries the middle initial L, and it is upheld beside HARMON CHARLES L. C3
should ask whether the token that discriminates is missing, not whether the string is shorter.

*The trade arm is the cheapest uphold when the directory names a trade about LAND.* Fergus 1839
calls William B. Egan a *real estate dealer* and Elijah K. Hubbard a *banker*; the register
enters the first for 720 acres over four months and the second for 2,428 acres in two afternoons
of the June 1835 ring. That is the PEARSONS reasoning and it decided the cohort's two largest
carries in one reading each. **Read the 1839 trade before anything else** — it is four years
after the scene and still the closest printed trade this corpus holds.

*A refusal can come off the card's own note, free.* DAVIS JOHN needed no outside argument: the
card already says *"a 'Mr. Davis' also took over the Sauganash Hotel in 1835, and whether that is
this man is unknown … if it is not, there is a second Davis in the town."* Read the note for a
sentence like that BEFORE building a case; two of the five refusals were half-written already.

*`letter_list_only` told the truth this time.* JACKSON SAMUEL is the cohort's only flagged card,
C1's test was applied — read `press_evidence[].list`, not the flag — and the flag was right. Its
`corroborated_enrichment` row has real content, unlike C1's ANDREWS DAVID, and it still refuses:
a county history's harbour foreman arriving from Buffalo predicts no purchase. **An enrichment
that does not PREDICT the row is not a check on it.**

*Four derived files move behind a refusal and check.sh will not tell you all four at once.* A
retraction changes a card's `sources`, so `tools/export_resident_audit.py --build`,
`tools/compile_scene.py --all` and `tools/consolidate_resident_evidence.py --build` all have to
re-run, and the gate reports them one failing step at a time over three passes. Run all three
after `spend_land_sales.py` and save two laps.

Filed on the way past: nothing. Every card the cohort touched was already carrying a ticket or
was clean.

---

### NEXT

1. **Cohort C3 — the twenty-eight remaining, surnames K-Z.** Read T-1001 before starting it: an
   empty `rivals[]` means "no namesake OF THAT SPELLING", so a surname block should be gathered by
   eye as well as by `namesake.py`, and KIMBERLY EDMUND S is in this block and is T-1001's man.
   The paired spellings to rule TOGETHER, and to expect to disagree, are the ones C2's rule names:
   look for a spelling that drops a middle initial a fuller one carries, and check Fergus 1843 for
   a second man of that forename before upholding it.

**Remaining after cohort C2: 28 unruled** (`resident_crosswalk.json` → `ruled`). This ticket
closes when that number is zero, and says so with the number.
