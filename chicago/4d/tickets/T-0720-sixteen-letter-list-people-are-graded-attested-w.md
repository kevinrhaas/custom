---
id: T-0720
title: Sixteen letter-list people are graded attested with no research row and a note that says the opposite: the ladder and the synthesis programme disagree about the same card
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Sixteen letter-list people are graded attested with no research row and a note that says the opposite: the ladder and the synthesis programme disagree about the same card.

Found by T-0508 while running the resident-research programme's own tool.

`tools/synthesize_resident_research.py` is the programme's authority for grading a
`letter_list_only` person: with no research row the person is `inferred` and carries
`resident_subtype: projected_resident`; with a corroborated row the person is `attested`.
Sixteen people on dev today are `letter_list_only`, carry NO research row, and are graded
`attested` anyway — albert_shepherd, ambrose_joshua, barry_john_s, bradford_harriet,
brooks_gardner, chapman_chas_h, cole_parker_m, crawford_james, fitzgerald_thos, lee_george,
mack_stephen, matthews_james_g, neff_r_a, rogers_edward_a, simons_e, winson_wm — and
murray_alonzo is a seventeenth, of the same shape, from before the convergence rung.

Each of them still carries the note the synthesis wrote: *"PROJECTED RESIDENT. Documented in
Chicago post-office evidence but not independently corroborated strongly enough for attested
circa-1835 residence."* The grade and the note on one card say opposite things, and a reader
gets whichever the card shows them first.

**Running the synthesizer demotes all seventeen back to `inferred`**, which would revert
T-0699's convergence rung inside whatever PR happened to run the tool. T-0508 therefore
restored the seventeen to exactly what dev has and changed no grade at all, and filed this.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

One rule wins and the other is written down as beaten. Either the ladder's convergence rung
supersedes the synthesis programme's letter-list rule for these people — in which case
`synthesize_resident_research.py` stops demoting a person the ladder has ruled on, and says
so — or the synthesis rule stands and the seventeen go back to `inferred`. Whichever way it
goes, the note is rewritten to agree with the grade on all seventeen cards, and running
`tools/synthesize_resident_research.py` twice in a row moves nothing.
