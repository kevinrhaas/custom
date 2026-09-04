---
id: T-0678
title: T39N R14E sections 16, 21 and 29 stop at the land-sales database's 150-row ceiling and its search cannot narrow below a section: find a route to the rest of the 1833 town-lot sales
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0610
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

T39N R14E sections 16, 21 and 29 stop at the land-sales database's 150-row ceiling and its search cannot narrow below a section: find a route to the rest of the 1833 town-lot sales.

Piece 2 of 2 of **T-0610 — Three sections of T39N R14E were truncated at the land-sales database's 150-row ceiling, and the ring townships are unread: finish the Illinois land tract sales around Chicago**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**What the T-0677 pass established about the search surface, so the next run does not
re-establish it.** The Illinois State Archives' public-domain form (`pubdomsrch.jsp`)
offers exactly three searches and no fourth: by section/township/range/meridian, by
township/range/meridian, and by county — and the page itself says the county option
"cannot be used in combination with any other search criteria". The result page carries
no paging control, no offset parameter and no sort parameter; the only other inputs on
either form are the hidden `srchType=domain` and `fromPage=pubDomSrch`. **Section is the
finest legal-description grain the database offers, so a section that returns 150 rows
cannot be narrowed by any query this source accepts.**

The rows come back ordered by purchaser, and the ceiling therefore cuts the alphabet:
section 16 returns BARCKENBILE CHRISTIA through HALE JOHN and stops. Everything from
HALE onward is unread, and all 150 rows it does return are October 1833 — the school
section's town-lot sale — so the unread remainder is 1833 town lots too, not the
1848-52 sales the T-0557 note supposed.

Two routes that do NOT work, both tested:
- **The name form.** `name=HALE` returns 150 rows and is itself truncated; the name
  search replaces the legal-description query rather than narrowing it, so it answers
  Illinois-wide. Descending a prefix trie from H to Z over the whole state's register
  is thousands of queries, not one run's work.
- **Purchase-number enumeration.** Section 16's 150 rows are scattered over purchase
  numbers 367309-369743 (plus 376893-895) in thirteen runs, interleaved with other
  sections, so covering the remainder means fetching several thousand detail pages
  through the reader proxy.

So this ticket is a SOURCE problem, not a query problem. The likely routes are the BLM
GLO patent records for T39N R14E, or the canal commissioners' / county's own ledger of
the October 1833 town-lot sale — a different deposit, read the way the other document
domains are read.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
