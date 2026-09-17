# The 1880s South Side epoch gets a date, and the date is argued

**Date:** 2026-09-17 · **Subject:** the representative scene date of `e1871_postfire` /
`shore_1880s_ic_edge`, the terrain epoch an 1880s Prairie Avenue scene will stand on ·
**Outcome:** 1 July 1888, decided from four sources read in full; the placeholder
1885-07-01 that `tools/check_shoreline_states.py` had been carrying as a constant is
retired and the checker now reads every dated state's date out of the record that argues
for it; no geometry was written and none was implied.

## 1. What this discharges, and what it deliberately does not

T-0473 asks for an 1880s South Side terrain and urban-ground epoch, and it opens with an
instruction before any ground is touched:

> Choose a specific representative scene date in the 1880s after checking landmark
> construction dates; document the choice.

That first clause is this document. The rest of T-0473 — the traced lake edge and rail
corridor, the graded streets and drainage, the terrain spec and heightfield a Prairie
Avenue scene stands on — is not, and the ticket has been split so that each of those is
owned by a ticket that can demonstrate it rather than by a clause in one that cannot.

**Nothing here places a building, moves a line, or writes a coordinate.** The epoch stays
`planned` and `shore_1880s_ic_edge.geometry` stays `null`. What changes is that the date
the successor tickets read their sources at is now a sourced judgement instead of a
number in a checker.

## 2. Why the date is not a formality

The 1835 scene is read at a single instant — 1 July 1835 — and everything in the dataset
is sized against it: a structure either stood on that day or is phased out of it, a
resident is either present or withheld. An epoch without such an instant cannot refuse
anything. Worse, the instant was already being *used* without being *chosen*:
`tools/check_shoreline_states.py` has been probing the 1880s at `date(1885, 7, 1)` since
T-1152 opened the state, and that figure appeared in no record, cited no source, and was
never argued. It was a placeholder doing a decision's work, which is the failure mode
this project's provenance rules exist to catch. If it had survived into the trace ticket,
the 1880s lake edge would have been fitted to a year nobody chose.

## 3. The landmark test the ticket asks for, and the disagreement it turns up

The scene the epoch is cut for is the Prairie Avenue district, and its surviving
centrepiece is H. H. Richardson's Glessner House at 1800 S. Prairie — the district's only
Richardson, a National Historic Landmark, and the one interior on the street that can be
walked today. Its construction date is therefore the binding landmark date, and **the
sources do not agree on it.** Read 2026-09-17:

| where | what it says |
| --- | --- |
| `wikipedia_glessner_house`, prose | "designed in 1885–1886 … and completed in late 1887" |
| the same page, infobox | built **1886–1887** |
| the same page, categories | "1886 establishments in Illinois"; "Houses completed in **1886**" |
| `wikipedia_prairie_avenue_district`, ¶1 | "designed and built … in **1885–1886**" |
| the same page, ¶ under *Clarke House* | "designed in 1885 … and completed in **late 1887**" |
| `wikipedia_prairie_avenue` | "designed in **1886** by architect Henry H. Richardson" |

One further sentence on the Glessner page is load-bearing and **cannot be true as
written**: *"The Glessner residence was Richardson's last work; he died three weeks after
completion."* Richardson died on 27 April 1886, so no completion in late 1887 preceded
his death by three weeks. The sentence is a garble of a real fact — the *design*, not the
building, was finished shortly before he died — and it is very likely the origin of the
1886 completion dates the same page prints elsewhere.

**This project does not resolve that spread here, and does not average it.** It has not
read Ochsner's *H. H. Richardson: Complete Architectural Works* (1984) or Drury's *Old
Chicago Houses* (1976), which are where it would be settled, and
`glessnerhouse.org/history-of-the-house` returned HTTP 404 to this session. What the
spread does is bound the answer: the house is standing by late 1887 on every reading.

## 4. The lake edge does not help choose, and that is worth knowing

`wikipedia_grant_park_chicago` carries the downtown lakefront chronology, footnoted to
Cremin's *Waterfront* in *The Encyclopedia of Chicago* (2004), pp. 864–6:

> When the Illinois Central Railroad was built into Chicago in 1852, it was permitted to
> lay track along the lakefront on a causeway built offshore from the park. The resulting
> lagoon became stagnant, and was largely filled in 1871 with debris from the Great
> Chicago Fire … In 1896, the city began extending the park into the lake with landfill,
> beyond the rail lines.

Four dated states, and the consequence for this decision is a negative one: between the
1871 fill and the 1896 extension the downtown lake edge **does not move**. Every year in
the 1880s buys the same shoreline. The date cannot be chosen on the water, and no
candidate year is bought at another's expense there.

Two things that reading *does* buy, both for the successor trace:

* the modern Grant Park and Museum Campus ground is 1896-and-later fill and is a
  quarter-century out of this epoch — exactly the failure T-0473's acceptance names;
* **it is a downtown reading and not a Prairie Avenue reading.** Lake Park lay between
  Randolph and present Roosevelt Road; Prairie Avenue's blocks are a mile further south.
  Nothing read here says where the Illinois Central ran at 18th Street or where the water
  stood off it. That gap is stated in the record so the next ticket meets it rather than
  inherits an over-stretched line.

## 5. The candidates, and why 1 July 1888

| candidate | for | against |
| --- | --- | --- |
| **1885-07-01** | the incumbent probe date | Argued by nothing. Precedes even the earliest reading of the Glessner completion. It is the placeholder this document retires. |
| **1886-07-01** | the strongest documentary pull in the decade: the *Encyclopedia of Chicago* carries an elite mapping made to 1886 alone — Conzen & Knox, *Chicago's Prairie Avenue Elite in 1886* — which is the nearest thing to a dated house-by-house roster of the street, and `wikipedia_prairie_avenue` dates the street's maturity to the same year ("By 1886 the finest mansions in the city … stood on Prairie Avenue") | On 1 July 1886 the centrepiece is at best days old and at worst eighteen months from completion, and the scene would have to rule on § 3's spread to know which. |
| **1888-07-01** | after *both* bounds of the Glessner spread, so the scene needs no ruling on it; inside the district's own 1836–1892 construction span; after the mid-1880s build-out toward 26th–30th; before the elite's departure for the Gold Coast and the 1898 press notices of decline; same 1 July convention the 1835 scene uses | The 1886 elite mapping is two years stale against it. |
| **1892/1893-07-01** | the street's documented peak, at the Columbian Exposition, guidebooks calling it "the most expensive street west of Fifth Avenue" | Out of the decade T-0473 asks for, and on the wrong side of both the 1896 fill programme and the move north. |

**Chosen: 1 July 1888.** The decisive property is the one in the third row's first
clause — it is the earliest 1 July that clears the whole Glessner spread, so the epoch's
instant survives whichever way § 3 is eventually settled. A date chosen to be robust to an
unresolved disagreement is worth more here than a date chosen to match the best roster,
because the roster can be carried forward with its staleness stated and the disagreement
cannot be carried at all.

The 1886 mapping is not lost by this. It remains the roster the occupancy work should
compile from — two years early, and said to be.

## 6. What changed in the repository

* `data/terrain/shoreline_states.json` — `shore_1880s_ic_edge` gains `address_date`
  (1888-07-01) and `representative_date_basis`, which carries the argument above, the
  three rejected candidates with their reasons, what the choice is robust to, and three
  things it explicitly does not settle. `geometry` stays `null`; `status` stays `planned`.
* `data/terrain/epochs.json` — `e1871_postfire` gains the scene date, the sourced
  lakefront characterisation, its `research_doc`, its `sources`, and a plain statement of
  what is still owed. It stays `planned`: this bought the date, not the ground.
* `tools/check_shoreline_states.py` — the `ADDRESS_DATES` constant is gone. The checker
  resolves each epoch through the date its own state declares, requires `address_date` of
  every dated state, and refuses a date that falls outside the state's declared range.
  Three new self-tests break it three ways and require each to fail.
* Four source records written, each read in full at its URL and characterised for what it
  cannot supply as much as for what it can: `wikipedia_prairie_avenue`,
  `wikipedia_glessner_house`, `wikipedia_prairie_avenue_district`,
  `wikipedia_grant_park_chicago`. All four are tier 4 later scholarship and all four
  declare `carries_no_document`: not one of them reprints a period document.

## 7. What is still owed, and to whom

The sources read here are encyclopedias. They are adequate for choosing a year and are
adequate for nothing else — no line in this epoch may be traced from any of them
(`wikipedia_prairie_avenue_district` is graded `asset_use: orientation` for that reason).
The successor tickets split out of T-0473 need documents:

1. **The lake edge and rail corridor at the scene date**, from period cartography — the
   fire-insurance and lakefront survey mapping — reaching south past 12th Street to the
   Prairie Avenue blocks, with its own sources, confidence and bounds. Cremin's
   *Waterfront*, pp. 864–6, is the first thing to read.
2. **The graded streets, drainage and fill of the South Side at 1 July 1888**, which is
   engineering-record work and which nothing read here touches at all.
3. **The terrain spec, heightfield and extent** a Prairie Avenue scene stands on — the
   ground itself, and the only one of the three that needs a bake.

And one reading that would improve this document rather than succeed it: Ochsner 1984 and
Drury 1976 on the Glessner construction chronology. Settling § 3 would not change the
chosen date — 1888 clears both bounds — but it would let the successor say when the house
was finished instead of when it certainly was.
