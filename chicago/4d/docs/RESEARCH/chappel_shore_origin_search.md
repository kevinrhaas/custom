# Where the Eliza Chappel shore drawing came from: the external search (T-0663)

> **WHAT THIS FILE IS FOR.** T-0649 spent the sheet's internal evidence and closed the
> geometric route: the drawing is composed rather than constructed, so no drawn position
> can be inverted to a station, and the lighthouse cannot settle the subject
> (`chappel_shore_lighthouse.md`). The only route left was external — a published
> illustration has a hand, a date and a book. **This file is the record of that search:
> what was asked, of which catalogue, in which words, and what came back.** It exists so
> that the next run does not spend its budget re-asking the questions already answered
> below. A route that failed is written down as plainly as a route that worked.

**Run 2026-09-04.** The original was **not located**. That is the second branch of
T-0663's own acceptance, and this file is what that branch requires. Four candidate
publications are **eliminated**, one named candidate is **live and untested**, and six
research routes are **blocked from the runner** rather than exhausted — the difference
matters and is stated per route.

`data/sources/eliza_chappel_school_shore_view.json` is unchanged in substance:
`verified` stays **false**, `rights_status` stays **check_required**, `tier` stays 5, and
nothing in the town moves on this image. What changed is that four wrong answers are now
closed and one right-shaped question is now written down.

## 1. What is being looked for

A halftone, 640 x 368 px as deposited, cropped tight to the picture — measured row and
column means show **no white margin on any edge** and a dark bleed at the bottom, so any
printed caption was cut away before the file reached us. The signature block at the lower
left survives as roughly a 20 x 20 px smear; enlarged twelvefold under autocontrast it
resolves into nothing legible, and at 640 px across it never will. **The sheet cannot
identify itself.** Everything below therefore asks the catalogues instead.

The subject, restated for a searcher: a one-storey log building at the right with a woman
in a white apron in its doorway; girls in bonnets streaming along the bank toward her;
three canoes, one afloat with paddlers and two drawn up; a white conical lighthouse on a
low point in the left middle distance; a scatter of small gabled buildings on a flat
prairie horizon.

## 2. ELIMINATED — four publications a reader would assume this came from

Each was eliminated the same way: the digitised copy's OCR was fetched whole and its
**list of illustrations** read, rather than its text searched for the subject. A plate
that exists is listed; a plate that is not listed is not in the book.

| Publication | Copy read | What its plate list says | Verdict |
|---|---|---|---|
| A. T. Andreas, *History of Chicago*, vol. I (1884) | archive.org `historyofchicago01andr`, `_djvu.txt` (5.2 MB) | The ILLUSTRATIONS list carries exactly one Chappel entry — **"Chappel, Eliza — 206"**, a portrait, on the page where the school narrative sits. Nothing captioned school-house, shore, canoe or lighthouse. | **Not Andreas.** |
| Mary H. Porter, *Eliza Chappell Porter, a Memoir* (Chicago: Fleming H. Revell, 1892) | archive.org `elizachappellpor00port_0`, `_djvu.txt` | **No list of illustrations at all.** Every hit on *illustration*, *frontispiece*, *engraving* and *drawn by* falls either in the narrative or in the publisher's advertisements bound at the back. | **Not the memoir**, as far as the OCR can say. |
| Joseph Kirkland, *The Story of Chicago* (1892) | archive.org `storyofchicago00kirkl`, `_djvu.txt` (1.4 MB) | ILLUSTRATIONS list at OCR line 1853 — nothing captioned school, shore, lighthouse or canoe. Chappel appears only in the text at pp. 123-24 and twice in the index. | **Not Kirkland.** |
| Milo M. Quaife, *Checagou: From Indian Wigwam to Modern City, 1673-1835* (1933) | archive.org `in.ernet.dli.2015.151734`, `_djvu.txt` | No list of illustrations, no occurrence of *Chappel*, no occurrence of *lighthouse*. | **Not this copy of Quaife.** A plated copy could still be checked; this one carries neither the plates nor the name. |

The first two are the ones that mattered. Andreas is where a Chicago 1833 retrospective
engraving is *assumed* to come from, and the memoir is the one book in the world written
about this woman by her own daughter. Both are now closed.

## 3. LIVE — one named candidate, and it is untested

**William Mark Young, *Chicago's First School House*, ca. 1925.**

Young (18 March 1881, Alton, Illinois — 1 January 1946, Wilmette, Illinois) was a painter,
muralist and commercial artist who trained at the Washington University School of Fine
Arts and worked in St Louis, Chicago and Cleveland; he painted fifteen murals for the Ohio
exhibit at the 1933 Century of Progress. Prints titled ***Chicago's First School House***
are offered on the secondary market as etchings by "Wm Mark Young", dated ca. 1925 and
described as made **for Koopman, Robinson & Neumer** — a Chicago illustration-and-lettering
studio whose name also appears on Chicago advertising matchbooks of the period. Companion
titles in the same hand and vein: *First Draw Bridge Over Chicago River*, *La Salle Street
1889*, *Chicago Gateway*.

**Why it fits.** A commissioned series of historic-Chicago subjects, one hand, one
mid-1920s campaign, reproduced as halftones for a commercial client, is precisely the kind
of object a **composed-rather-than-constructed** retrospective sheet is: the artist is
arranging a story, not reconstructing a viewpoint, which is exactly what T-0649 measured
this drawing to be.

**Why it is not yet the answer, and this is the part that must not be softened.** *Nobody
on this run has seen Young's picture.* The candidate rests on two secondary-market listing
titles. It is not established that Young's schoolhouse plate shows a lighthouse, a shore,
or canoes; a "first school house" print could as easily be the 1844 Rumsey school on
Madison and Dearborn, which is the other thing that phrase is used for. **Nothing in the
project may cite Young until the picture is compared.** If it does prove to be the source,
two consequences follow at once: `describes_date` can never be earlier than a 1920s
artist's own reading of 1833, and `rights_status` becomes a live question rather than a
formality, because a ca. 1925 commercial print is not argued out of copyright on age the
way the Braunhold and Trowbridge plates are.

## 4. BLOCKED, not exhausted — the routes this runner cannot reach

Recorded so the next run does not spend its budget rediscovering the same walls.

| Route | What happened |
|---|---|
| eBay item pages (`175745610373`, `155150616147`, `155150616225`) | **403** to `WebFetch`, to `curl` with a desktop browser user-agent, and through the `r.jina.ai` reader. The listing image is where the comparison in §3 would be made. |
| WorthPoint (`worthopedia` search) | **403**. |
| HathiTrust full-text search (`babel.hathitrust.org/cgi/ls`) | **403**, Cloudflare interstitial. This is the single most valuable blocked route: a phrase search over every digitised Chicago history would settle §3 in one query. |
| Google Books API (`www.googleapis.com/books/v1/volumes`) | **429**, daily quota exhausted for the shared runner IP before this run began. |
| `loc.gov` search with `fo=json` | Did not return JSON. |
| DuckDuckGo HTML endpoint | Returned a page with no result links. |

One route was reachable and answered in the negative: the Art Institute of Chicago's
public API (`api.artic.edu/api/v1/artworks/search?q=William Mark Young`) holds **no work by
Young** — the query returns Rothko and Tobey on the name tokens alone.

## 5. Terms searched

Web search, all of them: *Eliza Chappell first school Chicago 1833 drawing log schoolhouse
illustration lighthouse* · *"Eliza Chappell Porter" memoir 1892 Mary H. Porter
illustrations plate "first school" archive.org* · *"Miss Chappell's school" OR "Chappell
school" Chicago 1833 drawing log schoolhouse lake shore canoes lighthouse illustration
Chicago History Museum* · *"first school" Chicago 1833 illustration pencil drawing children
log house lighthouse "Fort Dearborn" retrospective view artist* · *"William Mark Young"
Chicago 1925 drawings historic Chicago "first school house" series* · *"Chicago's First
School House" 1925 print artist drawing Eliza Chappell log store 1833* · *"Mark Young"
Chicago etching "Koopman" OR "Neumer" historic Chicago series prints old Chicago scenes* ·
*"Chicago's First School House" William Mark Young etching image 1833 description
lighthouse canoes* (restricted to the auction and image aggregators).

Catalogue and API queries: Wikimedia Commons file search *Chicago 1833 school Chappell*;
archive.org advanced search for *checagou quaife* and for `title:(story of chicago) AND
creator:(Kirkland)`; the four OCR fetches named in §2; the Art Institute query in §4;
Google Books phrase searches for *"first school house in Chicago"*, *"Chicago's first
school house"* and *"Miss Chappell's school"* (all 429).

## 6. What the next run should do, in this order

1. **See Young's picture.** Any machine that can reach eBay or WorthPoint settles §3 in
   one look. Compare four things: the log building at the right, the woman in the doorway,
   the conical light on a point at the left, the three canoes.
2. **Ask the catalogues under the names, not the subject** — *Young, William Mark* and
   *Koopman, Robinson & Neumer* — at the Chicago History Museum, the Newberry, and the
   Chicago Public Library's special collections. A commissioned commercial series is
   catalogued under its commissioner as often as under its artist.
3. **Ask the depositor where the scan came from.** The file arrived from the repository
   owner with a social-media filename. One sentence from whoever posted it would settle in
   a day what a catalogue sweep may not settle at all — and it is the cheapest question on
   this list, which is why it is written down rather than assumed.
4. Run the HathiTrust phrase search from anywhere it is not blocked.

Until one of those returns, the sheet stays where T-0649 left it: **tier 5, unverified,
rights unresolved, spent on nothing.**

**Links:** T-0663 · T-0649 · `chappel_shore_lighthouse.md` ·
`data/sources/eliza_chappel_school_shore_view.json` · `docs/LIBERTIES.md`.
