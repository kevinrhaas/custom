# The Old Settlers of Chicago — the Calumet Club's receptions

The owner's ask, 2026-09-03: *"there was a group called the old settlers club and they
have some names can you research them and their meetings and add residents accordingly
make sure you include citations"* — with a pointer to
<https://chicagology.com/goldenage/goldenage063/>. Ticket **T-0554**.

## What this is

The Calumet Club of Chicago, organised 1878, invited every surviving resident of Chicago
"prior to the 1st day of January, 1840" who had been of age by then to an annual
reception, and the Chicago Tribune printed the rosters, the speeches and the year's
deaths. Those receptions are a **source series**, and this directory reads it.

| file | what it holds |
|---|---|
| `receptions.json` | one row per reception — date, venue, host, where its roster is printed, how many names it carries, and `roster_read` |
| `death_notices.json` | Fergus's 757 death notices of Chicago's old settlers, ages at death kept verbatim beside the birth window each one implies (T-0574) |
| `death_notices_crosswalk_1835.json` | those notices against the 1835 residents layer, and Wentworth's roll of 1882 held against Fergus's list |
| `coverage.json` | what has been read out of a page and where it stops |
| `people.json` | every name on the two rolls read so far, `as_read`, matched against the residents layer, with the ladder rung this source **proposes** |
| `crosswalk.json` | the identity decisions: merges, probables, refusals, each with the rule that fired |
| `claims.json` | what the documents say *about the town*, each with its verbatim quote |
| `text/` | the three 1882 Tribune documents as the page reprints them, so every quote can be rebuilt |

`tools/old_settlers.py --build | --check | --self-test | --apply-citations` owns all of
it. The gate rebuilds the JSON out of the committed text, refuses a quote that differs by
a character, refuses a source id that does not resolve, and refuses a merge that has not
been written onto the resident record it names.

## The two things to read before using this

**1. The club's criterion is not the scene date.** A guest had to be here before 1 January
1840 — not on 1 July 1835. So no name here mints a resident and no name here regrades one.
Under the ratified ladder (T-0513) a later recollection *corroborates, enriches and dates*;
`people.json` carries a **proposed** rung with its reason for T-0513 to consolidate and
T-0514/T-0515 to apply. Only an OS1 or OS2A merge is written onto a record, and what it
writes is a citation and a caveat, never a grade.

**2. The reading is transcription-mediated.** This project has not opened the Tribune of
1882. Every name is carried exactly as the page prints it — `Aux. 25`, `William H. stow`,
`Chiengo`, `Carter, 1. B.` — and the three Tribune source records keep `verified: false`
until someone reads the newspaper itself.

## What is read, and what is not

Read: the fourth annual reception of **18 May 1882** — 128 printed guest entries (the
report's own count is 118, and both numbers are carried) and John Wentworth's roll of
**40** old settlers dead since 1 January 1881. Twelve of those 168 names are people the
residents layer already holds; six of the twelve gained a date of death.

Not read, and declared in `receptions.json`: the **first** reception of 27 May 1879, whose
printed proceedings (*Early Chicago*, Calumet Club, 1879; Internet Archive
`earlychicagorece00calu`) carry a registry of 149 settlers **with their years of arrival** —
the one roster in the series that dates its people, and the richest thing still unread
here. The receptions of 1880 and 1881 are declared from the 1882 report's own arithmetic
and their Tribune reports have not been located.

## The second list: Fergus's death notices (T-0574)

`tools/read_fergus_obits.py --build | --check | --self-test` owns
`death_notices.json`, `death_notices_crosswalk_1835.json` and the domain's byte-for-byte
copy of the transcription. This is the same **genre** as the receptions and a different
**list**: Robert Fergus printed an OBITUARY in his 1896 reprint of the *Directory of the
City of Chicago for 1843* — "Names, places, dates, and ages at death of some of Chicago's
Old Settlers" — and 757 entries were read out of K. Torp's 2007 transcription of it.

**Why it was worth a run: an age at death is a birth year.** 725 entries carry a death
date and 608 a printed age, and 598 of them yield a window the birth falls in — 165 of
those narrow enough to name a single year. Nothing else this project has read dates its
people that way. The residents layer is shorter of birth years than of names, and the
crosswalk offers twenty of them.

**The trap, and it is the whole reason to read this section before using the file.** The
list's own header admits it names "some of Chicago's Old Settlers, prior to 1843, **and
other well-known citizens who arrived after 1843**, together with others prominently
connected with Illinois history". So presence here establishes *nothing* about arrival —
not before 1843, and certainly not residence on 1 July 1835. Gov. Richard Yates, Henry
Ward Beecher, Marquette and La Salle are all printed in it. Every record carries
`places_in_1835: false` with the admission quoted verbatim, and the crosswalk repeats it
above the first match, because a reader meeting a matched name is exactly the reader who
will forget it.

**The arithmetic is this project's, not the page's**, so every birth window is `inferred`
and carries its own subtraction written out. An age printed to the day ("aged 82-2-15") is
exact; an age in years and months ("a. 48-6", and the fractions "89½" and "24 2/3", which
are months the volume elsewhere spells out) gives a window of a month; a bare age in years
gives a window of a year, and therefore two candidate birth years. Where the age is
truncated in the transcription ("aged 5-"), hedged ("aged about 50"), or the death carries
no year, **no window is derived** and the record says which of those it was.

Four entries print a date of birth outright — Daniel O'Hara, John Phillips, John Harrison
Whistler and Ellen Marion Kinzie. Those are `documented`, and there the subtraction becomes
a *check*. Three of the four agree. The fourth misses by **one day**: Fergus gives Ellen
Kinzie's birth as 20 December 1804 and her age at death as 55-7-11, which counts back from
1 August 1860 to the 21st. A one-day gap is what two different conventions for counting the
day of death look like, and it is recorded rather than reconciled.

### Read beside the receptions, as the ticket asked

Wentworth's roll of forty old settlers dead since 1 January 1881 and Fergus's list are two
compilations of the same kind of fact, made fourteen years apart by different hands, and
Fergus's runs late enough to cover Wentworth's years. Held against each other on surname
and first initial: **five agree**, **two pairs are the rule's doing and not one man**
(Mark and Medore Beaubien, Harlow and Henry R. Kimball — recorded rather than dropped,
because a reader running the same rule meets the same pair), and **one is a real
disagreement**: both lists spell Simon Doyle, Wentworth kills him in September 1881 and
Fergus in November 1851. Neither is corrected against the other; this project has opened
neither printed page. **Thirty-two of Wentworth's forty are not in Fergus at all**, which
is evidence of nothing — his list is explicitly "some of" the old settlers, so a silence
in it is a silence.

### What the crosswalk says, and what it does not

847 residents tried; 34 meet exactly one entry, 11 are ambiguous, 4 are contested by two
residents apiece and no match is made, and 126 are refused for surname-only agreement. 32
matches could carry a date of death and 20 a birth year — including Thomas J. V. Owen, the
Indian agent, who died 15 October 1835 aged 34½ and was therefore born in 1801, three and
a half months after the scene date. **The file changes no resident record.** Under the
ratified ladder a later compilation corroborates, enriches and dates; T-0513 consolidates
and T-0514/T-0515 apply.

One entry is left as printed and flagged rather than corrected: "Seipp, Conrad, brewer,
died January 28, 1590" is a slip for 1890, and no birth is derived from a year earlier
than the earliest death the volume means to print.

## Known future work, in the ticket queue rather than here

- The 1879 registry and its years of arrival (its own ticket).
- A structured death-date field on a resident. Six records now carry a date of death **in
  prose**, because a `died` block is new schema surface for the residents layer and is a
  decision for a pass that owns that layer, not for a source reading.
