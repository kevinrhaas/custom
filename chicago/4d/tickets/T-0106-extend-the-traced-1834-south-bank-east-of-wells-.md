---
id: T-0106
title: Extend the traced 1834 south bank east of Wells so the claimed docks can stand
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-19
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Found by T-0062: the committed south-bank trace in
`data/terrain/epochs/e1834_harbor_cut/river.geojson` ends at Wells (local e ≈ 390),
so the wharf layer cannot place a deck anywhere on the reach between Wells and the
Dearborn drawbridge — `peck_store`, `harmon_loomis_store` and `thomas_church_store` qualify under the
T-0062 river-trade rule and the generator refuses them as drawings with exactly that
reason (see `data/wharves/river_landings.json` § refused; Church's would also need
the frontage cap re-measured once the trace reaches it). The trace is a derivation
from the georeferenced 1834 sheet, not a thing to freehand: extend it from the same
source the existing bank vertices came from, with the same provenance.

**Acceptance:** the traced south bank of the main stem reaches the Dearborn
drawbridge; `tools/generate_river_wharves.py` then draws Peck's and Harmon & Loomis's
landings with no rule change and no stacked feet; check.sh green.

**Links:** T-0062 · data/wharves/river_landings.json § refused · docs/LIBERTIES.md L145.
