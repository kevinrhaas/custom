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

## Known future work, in the ticket queue rather than here

- The 1879 registry and its years of arrival (its own ticket).
- A structured death-date field on a resident. Six records now carry a date of death **in
  prose**, because a `died` block is new schema surface for the residents layer and is a
  decision for a pass that owns that layer, not for a source reading.
