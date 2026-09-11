---
id: T-1035
title: The 1843 continuity route joins 'W. H. Adams & Co' to 'R. E. W. Adams, homoeopathic physician' on one shared initial out of three
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-11
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The 1843 continuity route joins 'W. H. Adams & Co' to 'R. E. W. Adams, homoeopathic physician' on one shared initial out of three.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

MEASURED ON THIS BRANCH, against dev at 593ef0bca plus the T-1020 fix.

`agree_rule` admits a one-surname firm when ONE printed initial agrees on both sides,
and never asks how many disagree. T-1020 gave the inverted styles their initial for the
first time, and the first thing that initial did was join two Adamses who are plainly
not the same concern:

    Adams, W. H. & Co        boots, shoes and leather, Norris 1844
    R. E. W. ADAMS           homoeopathic physician, Fergus 1843, f1843_e0130

`{W, H}` meets `{R, E, W}` on W, so the route counts the firm as present in 1843. The
other eight pairings T-1020 opened are exact (W. H. Adams & Co ↔ W. H. ADAMS & CO, and
seven like it); this one is the rule's floor showing.

It matters where it is counted and not where it decides: `firms_also_printed_in_fergus_1843`
is 163 and at least one of those is wrong, while CONTINUITY — the route that names an 1835
business — is untouched, because no 1835 Adams stands against it. So this is a count to
trust less, not a record to correct.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- A stated rule for how much initial agreement a one-surname join needs when both sides
  print more than one initial — either the agreement must be of the LAST initial, or of
  every initial both sides print, or the present rule is affirmed in writing with the
  Adams pair named as the price.
- `f1843_e0130` against `Adams, W. H. & Co` falls whichever way the rule says, and the
  eight exact pairings T-1020 opened all stand.
- `firms_also_printed_in_fergus_1843` is stated before and after. `bash tools/check.sh`
  green. No bake.

---

## Added on the way past by T-1034 cohort C1 (2026-09-11): the same floor, on a PERSON

The rule this ticket is opened on is not only the firm route's. `foster_amos` carries two
directory readings — `Foster, A. H. (Jennings & F.), bds American Temperance House`
(Fergus 1843) and `Foster, A. H. of Jennings & F. res American Temperance House` (Norris
1844) — folded onto an **Amos** Foster whose whole town record is one line of the 1833 poll
list. The crosswalk's stated forename rule is *"the given name of both begins A"*: agreement
on one letter, and silence about the H that follows it. A. H. Foster boards the American
Temperance House in both books and is a partner in Jennings & Foster; nothing ties him to an
Amos, and no Amos Foster is printed in Fergus 1839, Fergus 1843, Norris 1844 or the newspaper
run at all.

**Why it belongs here rather than in its own ticket:** it is the same question — how much
initial agreement a join needs when one side prints more than the other — asked of the person
route instead of the firm route, and whatever rule this ticket states should be tested against
this pair too. The cost is already visible: the fold made a one-reading card look like a
three-domain one, which is the kind of thickness a land-sale ruling reads as corroboration.
T-1034's cohort C1 refused FOSTER AMOS after stripping it (25 register rows, $468).
