# The Michigan St tract north of Kinzie Street

T-0796 · T-1076 (the reading) · T-1079 (the seating) · T-1080 (the name, and the road — this note)

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

**And the DATE refuses it, which the size argument below only made likely.** Moses &
Kirkland set the additions in order, at line 13122 of the same volume: the canal
commissioners' addition on fractional section 15 "was platted, under the direction of the
commissioners, by Edward B. Talcott, assistant engineer, June 13, 1836, and the plat
recorded July 20" — and

> *"It was followed by 'Wolcott's' addition, North Branch addition and Wabansia
> addition."*
> — Moses & Kirkland, *History of Chicago*, vol. 1 (`moses_kirkland_history_of_chicago_v1`,
> text line 13122)

So Wolcott's Addition was laid out AFTER June 1836. Wright surveyed in 1834 and drew this
tract already platted, two years earlier. The LAND was bought in 1830 — the same volume
prices it at $130 at line 93807 — but the buying is not the platting, and it is the platting
that would put lots, an alley and a street on Wright's sheet. **Wolcott's Addition is
refused on the calendar, and the arithmetic below is now the second reason rather than the
only one.**

And the size refuses it too. Wolcott's Addition is **eighty acres**. This tract, seated, is
200.0 m by 157.4 m — **31,486 m², or 7.78 acres**, a tenth of that. Wright draws no
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
3. **The curved road — now read, and it does not name the tract either.** T-1080 traced
   it: `data/traces/michigan_st_tract_road.json`, committed as the track
   `michigan_st_tract_road`. It leaves the north bank of the Main Branch a little east of
   Market Street, crosses North Water Street and Kinzie Street, bulges west, and **ends at
   the tract's Michigan Street** — it does not run north THROUGH the tract, which was
   T-1075's premise: both drawn strokes stop inside that street's corridor and the north
   tier is ruled across with no road in it. That is an argument about what the road was FOR
   — it goes to this tract and no further, from the river — and it is not an argument about
   what the tract was called. The Green Bay road remains the obvious candidate for the
   ground the road crosses and no source in this repository fixes where that road left the
   bank.

## The seating, and what it cost

The tract is seated on the committed grid rather than pasted from the sheet's fit,
because at this tract the fit is badly local. Measured north of the committed Kinzie
line, the committed grid puts Michigan Street **138.1 m** away and Wright's fit puts it
**99.9 m** away. Thompson's 1830 plat draws exactly one tier of North Division blocks in
that span, fronting Kinzie on the south and Michigan on the north, so the span has to
hold a block plus an 80 ft street: 453 ft does and 328 ft does not.

The cost is stated rather than hidden. Seated, the tract's south border stands **60.5 m**
north of Kinzie Street where the sheet draws **22.0 m** — a 38.5 m disagreement, all of
it Wright's compression in y at his sheet's western margin. The alternative, hanging the
ladder on `kinzie`, would have kept the drawn frontage and committed a **second** Michigan
Street 38 m south of the committed one, which is the one thing the reading refuses.

## The road, and what it is evidence of

Wright's one road north of the river is drawn, seated and committed (T-1080). What it adds
to the tract's question is small and worth stating exactly, because it is tempting to make
it bigger:

- **The tract had traffic from the river.** A road drawn to it, from the bank, is a road
  somebody used. The tract is not a paper plat on the sheet alone.
- **It ends at Michigan Street.** 266 m of it, and then nothing. Whatever the tract was, the
  road served it rather than passing through on its way somewhere north.
- **It still does not name anything.** No lettering, no legend swatch of its own, and no
  source in this repository describes a road on this ground. `name_1835` on that record is
  descriptive and says so.

Both halves of T-1080's question therefore close the same way: the road is read and
committed, and the tract's name is refused — now twice over, on size and on date.
