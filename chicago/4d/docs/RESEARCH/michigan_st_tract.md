# The Michigan St tract north of Kinzie Street

T-0796 · T-1076 (the reading) · T-1079 (the seating, and this note) · T-1080 (the name, and the road)
· T-1092 (re-seated on the eleven-point registration T-1091 adopted; every measured figure below
is that re-seating's, and the section at the foot says what moved)

Wright's 1834 survey draws, immediately north of Kinzie Street and east of the North
Branch, a small platted square unlike anything around it: two block columns, two block
tiers, a mid-block alley ruled through every block, lot frontages well under the
Original Town's, and an east-west street lettered **Michigan St**. Every neighbour on
that sheet is whole blocks. The owner asked what it was, on 2026-09-05: *"that must be
special"*.

## What is settled

- **Its two streets are the town's.** T-1076 read them off the 600 dpi NA/HUP sheet.
  The east-west street carried east on Kinzie's Addition's own fitted slope lands 1.7 px
  — about a metre and a half of ground — from where that Addition's Michigan Street was
  read eleven hundred pixels away. The north-south street carried south across Kinzie
  lands 16.7 m from the committed `market_north`, inside the sheet's own 16.19 m RMS.
  So Wright's second `Michigan St` is not a second street of that name, and the tract is
  platted **on the town's grid**. Only its parcel module is its own.
- **Its section is 9**, not the fractional 16 the owner read — `docs/PLSS-SECTIONS.md`
  derives the whole sheet's numbering from the committed 9/10/15/16 section corner.
  Section 9 is the canal's section, the legend's *Part of Canal Sec. No. 9*.
- **It is seated** on `michigan_north` and `market_north` by
  `tools/seat_michigan_st_tract.py`, and its two street reaches, its two alleys and its
  polygon are committed (`data/traces/michigan_st_tract_seated.json`).

## What is NOT settled: the name

**No source in this repository names this tract.** That is the state of the question and
it is not being improved by guessing at it.

One candidate is raised by the corpus and the same corpus refuses it on arithmetic:

> *"It must have been west of State street, for it was upon the eighty acres to which
> (by its help) he later established a pre-emption claim and which he bought of the canal
> commissioners for $1.25 an acre, and subdivided into the familiar 'Wolcott's
> Addition.'"*
> — Moses & Kirkland, *History of Chicago*, vol. 1, editors' footnote
> (`moses_kirkland_history_of_chicago_v1`, text line 6006)

Everything general about that fits: west of State Street, bought **of the canal
commissioners**, and therefore canal land — which is section 9, which is this tract's
section. The volume names Wolcott's Addition twice more, once in David Hunter's 1834 sale
of *"the half of Kinzie's addition to Chicago, the whole of Wolcott's addition"* to
Arthur Bronson (line 13225), and once at line 93807 on the price of the land it was laid
out upon. **None of the three gives a boundary.**

And the size refuses it. Wolcott's Addition is **eighty acres**. This tract, seated, is
202.1 m by 154.3 m — **31,182 m², or 7.71 acres**, a tenth of that. Wright draws no
platted ground adjoining it to make up the difference: north and east of it the sheet is
blank, unsurveyed, and carries the sheet's own title. So either this square is one corner
of a larger Wolcott's Addition that Wright drew only part of, or it is not Wolcott's
Addition at all, and **nothing in the corpus decides between those**.

It is therefore recorded as a candidate and nothing is graded on it. No street record,
no trace and no polygon in this project carries the name Wolcott.

## What would settle it

1. **A plat or a boundary.** Andreas on the additions north of the river; the canal
   commissioners' own sale records; the Cook County recorder's index of town plats. Any
   one of them that gives Wolcott's Addition a boundary answers this in a line.
2. **The Democrat's 1834-35 land notices.** An auction notice that lists lots by block in
   a named addition north of Kinzie would name the tract directly. The extracted issues
   in `data/research/newspapers/extracted/` have been searched for *addition*; the hits
   are Kinzie's, Dearborn, and Carpenter's, and none is north of Kinzie Street here.
3. **The curved road.** Wright draws a road as a curved double line leaving the
   Kinzie/North Water corner and running north through this tract — the only road on the
   sheet that is not a platted street apart from the fort's. It is still unread. The road
   north from the Kinzie house toward Green Bay is the obvious candidate and the sources
   that name that road's start would also place this ground.

## The seating, and what it cost

The tract is seated on the committed grid rather than pasted from the sheet's fit,
because at this tract the fit is badly local. Measured north of the committed Kinzie
line, the committed grid puts Michigan Street **138.1 m** away and Wright's fit puts it
**91.9 m** away. Thompson's 1830 plat draws exactly one tier of North Division blocks in
that span, fronting Kinzie on the south and Michigan on the north, so the span has to
hold a block plus an 80 ft street: 453 ft does and 301 ft does not.

The cost is stated rather than hidden. Seated, the tract's south border stands **62.0 m**
north of Kinzie Street where the sheet draws **15.0 m** — a 47.0 m disagreement, all of
it Wright's compression in y at his sheet's western margin. The alternative, hanging the
ladder on `kinzie`, would have kept the drawn frontage and committed a **second** Michigan
Street 38 m south of the committed one, which is the one thing the reading refuses.

## The re-seating of 2026-09-13 (T-1092)

T-1091 put the eleven-point registration of the NA sheet in force and deliberately left
the four SEATED grids — this one, the School Section, Kinzie's Addition and Wabansia's
streets — reading the eight-point fit it superseded, because moving them moves ground.
T-1092 moved them. This tract's reading was re-run by `tools/read_michigan_st_tract.py`
and re-seated by `tools/seat_michigan_st_tract.py`, both now on `fit` rather than
`retained_fit`, and every figure in this note is from that run.

WHAT MOVED, AND WHAT DID NOT. The tract is still seated on `michigan_north` and
`market_north`, so its position on the ground is unchanged in kind: the corners move
about a metre, the extent by two metres one way and three the other, and the alley
spacing off Michigan Street by under a metre. **What moves is the sheet's side of the
comparison.** Wright's drawn Kinzie-to-Michigan span reads 91.9 m through the new fit
where it read 99.9 m through the old, so the disagreement this seating pays for grows
from 38.5 m to 47.0 m. That is the same statement T-1091 made about the whole sheet —
the eleven-point fit is the better registration over the paper and a worse one in this
north-west corner, because its y scale is no longer fitted over the top quarter alone —
and it does not change which answer the project takes. Thompson's one block tier plus an
80 ft street still needs 453 ft, and 301 ft is further from holding it than 328 ft was.

THE NAME IS UNTOUCHED BY ANY OF THIS. It was refused on arithmetic and it stays refused
on arithmetic: 7.71 acres against Wolcott's Addition's eighty is the same refusal 7.78
was.
