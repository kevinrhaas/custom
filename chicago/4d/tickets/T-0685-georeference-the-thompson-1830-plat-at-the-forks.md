---
id: T-0685
title: Georeference the Thompson 1830 plat at the forks and measure its bank against the Wright 1834 line for the owner's ruling
state: open
epic: GROUND
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-0453
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Georeference the Thompson 1830 plat at the forks and measure its bank against the Wright 1834 line for the owner's ruling.

Piece 2 of 2 of **T-0453 — The river banks are traced from Wright 1834 and the owner reads the Thompson plat differently at Wolf Point**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

This piece carries T-0453's acceptance 1, 2 and 3.

**Why it is its own run.** `data/sources/thompson_plat_1830.json` records the
sheet as a PARAMETER SOURCE — "no open high-resolution archival scan located",
the surviving artifact a Canal Commissioners' working copy, and the standing
instruction "read for its stated figures, never traced for geometry". There are
no Thompson GCPs in `data/traces/gcp/` (only Wright 1834 and Hathaway 1834), so
the plat cannot be measured against the Wright line until it has been fitted to
the same frame the datum was fitted in — which is a run's work by itself, of the
same shape as `tools/rederive_datum.py`'s fit, with its own residuals to report.

**Acceptance:**

1. The Thompson plat is georeferenced into EPSG:26916 through committed ground
   control of the same form as `data/traces/gcp/wright_1834_gcps.json`, with the
   fit's residuals reported. If the sheet will not carry a fit at a useful
   residual, that is the finding and it is recorded rather than forced.
2. Its bank at the forks is traced and committed **beside** the Wright 1834
   line, not over it — both readable, each with its source.
3. The disagreement is measured in metres at named eastings, the way T-0444
   measures the West Division's spacings, and reported rather than characterised.
4. The owner rules which is the planform of record, and the ruling is written
   into the ticket with the measurement in front of it. If they differ by less
   than the ±20 m the file already declares, that is a pass and the finding is
   that there was nothing to fix.
5. Nothing moves. Moving the bank re-derives every waterline test in the project
   and that is its own unit of work.
