---
id: T-0878
title: Wright's 1834 registration is three per cent long in y: the School Section's mile measures 1658.65 m north-south and 1603.04 m east-west on the same fit
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Wright's 1834 registration is three per cent long in y: the School Section's mile measures 1658.65 m north-south and 1603.04 m east-west on the same fit.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found while working T-0797, and it is a fact about the FIT rather than about the sheet.

Section 16 is a statute mile square — 1609.344 m — and its north-east corner, State and
Madison, is GCP G1 of `data/traces/gcp/wright_1834_nara_hup_gcps.json`. Measuring the
section's own outer lines on the registered scan, through that fit:

| | measured | mile | departure |
|---|---|---|---|
| east-west | 1603.04 m | 1609.344 m | -6.30 m (-0.39 %) |
| north-south | 1658.65 m | 1609.344 m | **+49.31 m (+3.06 %)** |

The x scale is right to four tenths of one per cent over a mile. The y scale is three per
cent long — **more than the width of any block in the grid**, and eight times the fit's own
16.19 m RMS.

The registration already predicted the direction of this: it measured 5.2 per cent x/y
anisotropy on this scan against 3.7 per cent on the BPL copy and wrote that "the extra
stretch is in the long axis, along which the manuscript was torn and backed". What is new
is the SIZE of it at the bottom of the sheet, measured against a length that is known
exactly rather than against control points.

T-0797 anchored its grid on the section rather than on the paper, so nothing it committed
is wrong. But every OTHER trace off this sheet is placed by the fit alone.

**Acceptance:** state whether the eight-point global affine should stand, and if not what
replaces it — a y-scale correction, a second-order term, or control at the sheet's foot,
which the section's south-west corner and the two reserved corners now supply. Measure the
change on the committed traces before adopting it; a datum that moves is a bigger event
than a fit that is known to be long, and `tools/rederive_datum.py` is the gate that will
say so.
