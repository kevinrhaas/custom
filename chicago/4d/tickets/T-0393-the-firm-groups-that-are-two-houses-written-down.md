---
id: T-0393
title: The firm groups that are two houses, written down so no later sweep merges them
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0338
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Piece 3 of 4 of **T-0338 — Thirty-one groups of firms share a partner surname and only one
of them has been judged**. The parent keeps the full ask; this ticket owns one slice of it.

The groups `firm_surnames()` puts together that are NOT one house. Nothing merges here; the
work is the written record, and it is worth a run because the next sweep that groups on the
surname will find these again and the file has to be able to answer it. T-0391 opened
`refused_firm_merges` for exactly this; three entries stand in it already.

The candidates:

    the Kinzies — J. H., John S. and R. A., three men of one family
    P. F. Peck against P. F. W. Peck · F. G. Blanshard against G. Blanshard
    Dr. J. B. Barnard against Dr. J. H. Barnard · G. W. Keeney against W. Keeney
    M. H. Kennicott against Wm. H. Kennicott · J. H. Mulford against [J. I. Mulford]
    J. Curtiss, L. Curtiss and L. G. Curtiss · Charles Taylor against Wm. H. Taylor
    Brown the painter against W. H. Brown
    the 'store' group — New York Clothing Store, Peter Cohen's store, W. Kimball's New
      Store — which share no partner at all, only the word
    the 'hotel' group — the Eagle Hotel against the blacksmith shop opposite the Chicago
      Hotel — same shape, an anchor mistaken for a partner
    the two Chicago & St. Joseph packets, schooner Llewellyn against schooner Phillips

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Every group above stands in `refused_firm_merges` with the reason it is two, in the shape
  T-0391 established (`into`, `from`, `witnesses`, `kind`, `refused_because`).
- The 'store' and 'hotel' groups additionally record that `firm_surnames()` grouped them on
  a common WORD and not a partner, so the failure is legible if the function changes.
- The gazetteer recompiles green; no business count changes, and the PR says so.

Links: T-0338 (the parent), T-0391 (which opened the file).
