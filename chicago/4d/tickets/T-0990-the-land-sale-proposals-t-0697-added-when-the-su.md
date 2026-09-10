---
id: T-0990
title: The land-sale proposals T-0697 added when the surname rule widened are unruled: rule them one cohort per run, and the run that closes a cohort files the next
state: open
epic: META
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
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

### NEXT

1. **Cohort B — the twenty-four with NO namesake at all** (`rivals[]` empty). The mechanical
   rule fired on a surname the layer holds exactly once, which is T-0700's and T-0850's
   original shape; the SPENCER WILLIAM G refusal is the precedent that governs most of them.
2. **Cohort C — the sixty-six remaining `forename_agrees` proposals with namesakes.** Take
   them in two or three runs by surname block, not all at once.

**Remaining after cohort A: 90 unruled** (`resident_crosswalk.json` → `ruled`). This ticket
closes when that number is zero, and says so with the number.

