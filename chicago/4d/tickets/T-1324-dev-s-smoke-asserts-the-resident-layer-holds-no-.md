---
id: T-1324
title: Dev's smoke asserts the resident layer holds no reconstructed person, and since T-1314 it holds three: the retargeted K18 check is stale again
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Dev's smoke asserts the resident layer holds no reconstructed person, and since T-1314 it holds three: the retargeted K18 check is stale again.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured on a steward runner, 2026-09-18, on `steward/t-1311-…` whose diff touches no
resident file at all (`git diff origin/dev...HEAD -- data/residents` is empty):

    FAIL  desktop 1280x800: the invented-name programme left nothing behind on this layer
          — 3 reconstructed people in the manifest, 0 on hh_inf_cooper_north_04,
            name_basis present: false

`data/residents/index.json` on `origin/dev` reads
`counts.by_grade.reconstructed: 3`, written by T-1314 (#1453) when stage
`named_families` seated the three people the 1840 census counts in a bridged head's
house. So the assertion is inherited red, not caused by the branch that found it.

The assertion is T-0524's retarget of the retired K18 check: T-0489 removed the
invented-name population, `reconstructed` went to 0, and rather than delete a
passing-shaped check T-0524 turned it round to assert the OPPOSITE promise — that the
programme left nothing behind. T-1167 then made `reconstructed` a GRADE THE PROJECT
WRITES ON PURPOSE, with a stage, a basis and a seed on every person, and twelve more
stages queued behind it. The promise the check states is no longer the project's.

What must NOT happen is the thing T-0524 itself forbids: deleting the check because it
is in the way. What the layer promises now is narrower and still worth a gate — no
reconstructed person without a stage, a basis and a seed, and no `name_basis` block
coming back — which is what `reconstruct_residents_1835.py --check` already refuses
record by record. The smoke's job is to prove the CARD says it.

**Acceptance:** the assertion states the promise the reconstruction programme actually
makes, reads the count from the manifest rather than hardcoding one (it will move on
every stage from T-1171 to T-1178), and the PR says which promise replaced which.
Desktop part 3 runs green on `--published`. No check deleted without the sentence
T-0524 requires.

**Links:** T-0524 · T-0489 · T-1167 · T-1314 · `tools/smoke_renderer.mjs` ·
`tools/dev-smoke-state.mjs`.
