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
claimed_by: run 9/10/2026, 1:01:00 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34511427139
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

**Cohort C1 — the A–C surname block of the sixty-six** (`forename_agrees`, `rivals[]` non-empty,
purchaser spelling beginning A, B or C). Ruled 2026-09-10. **Nine upheld, eight refused** —
matched 112 → 104, ruled 71 → 89, unruled 66 → 49; seven cards cleared and an eighth reduced,
fifteen register rows, 1,520.00 acres and $1,984.00 taken back off them.

| upheld | refused |
|---|---|
| ANDREWS DAVID, ARCHER WILLIAM B, BEAUBIEN MARK, BOWEN ERASTUS, BROWN WILLIAM H, CARPENTER PHILO, CHAPMAN CHARLES H, COOK JOSIAH P, COOK THOMAS | ALLEN WILLIAM, ANDREWS WILLIAM, BALLARD THOMAS, BENNETT WILLIAM, BLAKE LEVI, BROWN WM, BURDICK PAUL, CLARK JOHN K |

**What the cohort taught, and the next block should use it.** *Cohort B's line — does the town
hold the man more than once — survives, but it is no longer sufficient.* A forename agreeing IN
FULL is what a crowded surname produces by accident, so what decided all seventeen is whether one
of the town's documents carries a token THE REGISTER'S ROW ALSO CARRIES. Eight of the nine
upholds have one; every refusal has none.

*The strongest such token in this block was the SCHOOL-SECTION SALE.* Six of the nine upholds
buy town lots or blocks in section 16 in October 1833, and the town's own 1833 tax list, poll
book or election record holds the same man in the same season. **Check the sale date against the
tax list of 1833 first** — it is faster than the directories and it is decisive when it fires.

*A count of readings is not a weight of evidence.* ALLEN WILLIAM is refused with three rows on
his card, because Fergus 1839 (saloon, North Canal), Fergus 1843 (shipcarpenter, Wolcott) and
Norris 1844 (shipwright, Wolcott) cannot all be one man; COOK THOMAS is upheld on three rows
because they are one trade at one street across eleven years. Ask whether the rows are
CONSISTENT, not how many there are.

*The register refuses its own proposals twice in this block, and that is new.* BROWN WM is
refused because the same register writes BROWN WILLIAM H when it has the initial — omission is
the source speaking. CLARK JOHN K is refused because `ls0897` and `ls0898` are the SAME entry
read from two volumes and the two volumes spell the purchaser JOHN K and JOHN R. **Look for
one-entry-two-volumes pairs before ruling on a middle initial**: `volume`/`page`/`purchase_no`
disagreeing on an identical tract and date is the signature.

*Two independent printings make an initial safe; one does not.* ARCHER WILLIAM B upheld (paper
and death notice both print the B), BROWN WILLIAM H upheld (two Democrat readings eight days
apart), against cohort B's ROWLEY/HURD refusals where the initial pair was the whole record.

### NEXT

1. **Cohort C2 — the D–H surname block.** DAVIS GEORGE, DAVIS JOHN, EGAN WILLIAM B, FOOT JOHN,
   GOODRICH EBENEZER, HADDOCK EDWARD H, HALL GEORGE, HAMILTON RICHARD J, HANDY HENRY S, HARMON
   CHARLES L, HARMON CHAS L, HARMON ELIJAH D, HARMON ISAAC, HARMON ISAAC D, HUBBARD ELIJAH K,
   HUBBARD GURDON S, HUNTER EDWARD E — seventeen, the same size as C1. Two things to carry in:
   the four HARMON spellings and the two HUBBARDs are where the one-entry-two-volumes check of
   C1 will earn its keep, and HUNTER EDWARD E is the fuller reading of a spelling cohort A
   already upheld, so read that ruling before re-deciding it.
2. **Cohort C3 — the J–Z remainder**, thirty-two spellings.

Read T-1001 before either: an empty `rivals[]` means "no namesake OF THAT SPELLING", so a
cohort-C surname block should be gathered by eye as well as by `namesake.py`.

**Remaining after cohort C1: 49 unruled** (`resident_crosswalk.json` → `ruled`). This ticket
closes when that number is zero, and says so with the number.
