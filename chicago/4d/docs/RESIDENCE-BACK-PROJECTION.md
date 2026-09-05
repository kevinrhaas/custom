# Back-projection, the other half — what an 1835 HOME does with a door printed after 1835

*Policy. Written for **T-0669**, 2026-09-04, which `docs/ADDRESS-BACK-PROJECTION.md`
clause 2 names as the place the residence question gets answered. The tool is
`tools/back_project_residences.py`, the ledger is
`data/research/directories/residence_back_projection.json`, the liberty is **L223**, and
the gate is two steps in `tools/check.sh`.*

## Why there are two documents and not one clause

T-0633 wrote the business half. Its clause 2 refuses, by name, an address the volume
itself prints as a residence — its own `res` or `bds` — on the ground that "positioning a
home from a later door is the same mechanism aimed at a different question". This document
answers that question, and the first thing it has to settle is whether it is a different
question at all.

**It is, in exactly two places.** Everything else here is T-0633's rule, imported rather
than re-argued: the same 1835 street layer, the same table of names 1835 holds and names
it does not, the same folding of a printed word onto a table key, the same refusal to
deal a roof, and the same `reconstructed` ceiling. Two passes reading `Michigan ave`
differently would be a worse fault than either reading, so the code imports the tables
instead of copying them and `--self-test` asserts the two passes never both place.

The two departures are stated as clauses, so a reader can disagree with the argument and
not merely with the outcome.

### R2 — a home needs no attested trade, where a business does

The business pass's clause 1 refuses a person the 1835 corpus gives no trade, and it is
right to: there is no business for a later door to place, and minting one out of an 1844
directory is the single thing that pass may never do. It is also that pass's largest
refusal by a distance.

**A residence is not that claim.** Everybody the town holds lived somewhere in it. An
absent occupation says nothing about whether a man had a house; it says the papers of
1835 did not print his trade. So this pass's population is *every* residence-printed
address, and the difference is not marginal: **35 of these 43** are people the 1835 record
gives no trade, whom the business pass had already refused at its clause 1 before its
clause 2 ever looked at them. **Four of the seven placements below are people with no
1835 trade at all** — which is to say R2 is not a technicality, it is most of the yield.

The ticket was filed against the six the business pass's clause 2 actually reached, and
estimated the yield at "small". That estimate was a consequence of the clause ordering
rather than of the corpus.

### R5 — a face, and never a point, where a business may reach a crossing

The business pass resolves `cor.` and `near` onto the point where two committed
centrelines meet, and grades the weaker of those two `anchored`. This pass declines the
point for a home, always, and the reason is two facts about what the volume is saying:

1. **The corner is a fact about the 1840s grid, not about the ground.** Every residence
   entry that prints a corner prints it against a street NUMBER — `res 208 Clark, n.-w.
   cor Adams`, `res 62 Adams near State`. Chicago numbered its streets after 1835. The
   corner is how the 1843 volume tells its reader which of two hundred Clark Street doors
   it means, and reading it back is reading a finding aid as a survey.
2. **A house moves more than a shopfront does.** A shopfront is capital sunk into one
   street's trade; a lodging is a month's rent, and `bds` says so on its face. Carrying a
   point back eight years would be this policy claiming most exactly where its evidence is
   thinnest, which is the inversion the confidence model exists to prevent.

So a residence reaches the FACE and stops. Where the volume names a second street, the
record says so in the note and takes nothing from it.

## The five clauses

Evaluated in the order written, and the record says which one decided it.

**R1 — the address is printed as a residence.** `res`, `bds`, `boards`. That is this
pass's whole population, and the business pass reads the rest. Between them every later
address on the layer is ruled on.

**R2 — no trade is required**, for the argument above. This clause refuses nothing; it is
here because it is the departure, and a clause that only ever permits still has to be
stated to be disagreed with.

**R3 — an 1835 placement always wins.** A household carrying a real `lives_at` is left
exactly where it is and the later address moves nothing. None of the 43 is in that
position today, which is itself the measurement: **20 of 825 households carry a real
`lives_at`** and not one of them is a person a directory prints a home address against.

**R4 — the address has to be a street, on the 1835 grid, under that name.** The business
pass's clause 3, plus three refusals only a home produces, and each is tested BEFORE any
street name is looked for — which is the load-bearing detail:

- **A named house.** `bds Lake House` contains the word *Lake*, and the Lake House is a
  hotel on the north side nowhere near Lake Street. `res Fort Dearborn` contains
  *Dearborn*, and the fort stands at the river mouth, not on Dearborn Street. Resolving
  either as a street face would be a placement invented out of a collision between a
  building's name and a street's. Seven entries are refused this way — five public
  houses, the government reservation, and the fort — and the reservation is 1835
  ground the town holds and still not a street. One of the five is only reached because
  the sign table is scanned against a re-spaced copy of the line: Fergus prints `bds
  American TemperanceHouse` with the space dropped, and a word with no boundary in front
  of it is invisible to `\bhouse\b`. It was refused either way — as a bare personal name
  — which is the kind of right answer for the wrong reason a refusal ledger exists to
  make visible.
- **A household, named by its head.** `bds Mrs. Post`, `bds John Gray`, `bds Michael
  McDonald` — eight of them, two printed with a title and six bare. Where that person
  is himself in this town the two records could be joined, but that is a crosswalk between
  two people, not an address read back.
- **`res same`.** Fergus's back-reference to the line above. The crosswalk that fed this
  layer carried the two words without their antecedent, so there is no address here at
  all, and supplying the neighbouring entry's street would be reading the volume's
  typography as evidence about the ground. Two entries.

And a ward is not a street: `res 3d Ward, south of Jackson` divides the Chicago of 1843,
which was not incorporated until 1837.

R4's second half is the business rule verbatim, and it is where the ticket's own estimate
was wrong: **a qualifier naming a street the town does not have refuses the whole
address**, not just the qualifier. Giles Spring's `res 62 Adams near State` was expected
to survive on State. It does not, and it should not: the volume says his house was on
Adams, and moving him to State would place him where it does not say he was. Three
addresses resolve a head street and are then refused on a qualifier — Henry G. Hubbard on
La Salle (Madison), Hibbard Porter on Clark (Adams), and John P. Simpson on Canal (Adams
and Jackson).

**R5 — the grade is `reconstructed`, the note says how many years back, the placement is
a face, and no `lives_at` is written.** `tools/back_project_residences.py --self-test`
asserts all four rather than the prose promising them.

## What it reaches, measured 2026-09-05

| outcome | count |
|---|---|
| residence addresses adjudicated | **43** — 29 printed `res`, 14 printed `bds` |
| **placed on a face** | **7**, of which 4 are people with no 1835 trade |
| already better placed (R3) | 0 |
| refused | 36 |

Five faces are reached — **Clark, Lake, Market, Randolph and Washington** — and the seven
are J. H. Collins on Lake, Dr William Bradshaw Egan, Samuel Mills and James M. Morrison on
Clark, L. W. Montgomery on Market, J. B. Jordan on Washington and High Es Jones, who
boarded on Randolph in 1839 at a corner this policy declines to take.

**`lives_at` real values before 7 placements: 20. After: 20.** It did not move and was not
meant to, for the reason `docs/STREET-FACE-ADOPTION.md` limit 3 gives and L218 repeats:
dealing a household to one roof on a face is an allocation, not a reading, and stacking
that on an address already carried back eight years would be two inventions under one
chip. `works_at` is untouched at 50. What seven households gained is a face, on the
record, graded and dated and reversible — and thirty-six gained a written refusal where
they previously had a business pass's ruling on a question nobody had asked about them.

## The two passes may both rule, and may never both place

A residence-printed address against a person with no 1835 trade is refused by the
business pass at *its* clause 1 — there is no business to position — and adjudicated here
on its own merits. That is two rulings on two questions, and the card shows both, because
hiding the first would leave a reader wondering why one address has two verdicts and
seeing only one. Three of the 43 stand off in the business pass instead (Daniel Elston,
Gholson Kercheval and Augustine Taylor carry a real `works_at`), and a stand-off is not a
placement. The invariant the gate holds is the narrow one: **no printed address is
*placed* by both policies.**

## Where it reaches a reader

The Evidence panel's *The town's people* section, on the household's own card, under the
directory entry the address was read out of — the outcome, the face, the grade, whether
the volume printed `res` or `bds`, and the note saying how many years it was carried.
**All 43 are shown, refusals included**, for the reason `residents.js` already gives about
the crosswalks' three match statuses: a card showing only the seven would be reporting this
pass's successes and hiding its arithmetic.

Nothing is drawn, and L2 is the precedent for saying so in those words.

## What would settle it

A source inside the scene year that says where somebody slept. The 1835 poll and tax
lists and the land-sales tracts are all closer to the year than a directory is, and any
one of them that houses one of these seven supersedes this pass under R3 without an
argument. The eight `bds <a person>` entries would fall to a person-to-person crosswalk
rather than to a new source, and the seven named places to a building identification — both
are ordinary work this policy declines to do inside one pass, not open questions.
