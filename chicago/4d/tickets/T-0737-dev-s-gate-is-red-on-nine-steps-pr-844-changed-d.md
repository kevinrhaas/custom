---
id: T-0737
title: dev's gate is red on nine steps: PR #844 changed data/residents/ without regenerating the sidecar and the eight cohort/ladder files derived from it
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

dev's gate is red on nine steps: PR #844 changed data/residents/ without regenerating the sidecar and the eight cohort/ladder files derived from it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0517**, which could not merge on a green gate because of it. **This blocks every
run on this app**, so it is the first thing to fix.

**The finding.** `./tools/check.sh` fails on `dev` at `85d650116`, with no working-tree changes
at all. Nine steps, all downstream of the residents layer:

```
   ^ sidecars derived from data/ failed
   ^ the 75-person real-resident research cohort is fixed failed
   ^ the second non-overlapping 75-person research cohort is fixed failed
   ^ the third non-overlapping 75-person research cohort is fixed failed
   ^ the thirteenth research cohort is fixed failed
   ^ the fourteenth research cohort is fixed failed
   ^ the fifteenth research cohort is fixed failed
   ^ the civic, church, press and book residents re-derive from the ladder failed
   ^ the regraded residents re-derive from the ladder too failed
```

Each says the same thing in its own words:

```
python3 tools/compile_scene.py --all --check
   DRIFT: data/sidecars/1835/people.json is not what the dataset compiles to
python3 tools/select_resident_research_pilot.py --gate
   data/research/residents/pilot_75_cohort.json is stale; regenerate without --gate
```

**The cause.** `85d650116` — "T-0510: cohort 15 — 76 people looked for" (#844) — is the last
merge into `dev` and it changed `data/residents/`. Eight cohort/ladder files and one scene
sidecar are DERIVED from that layer and were not regenerated in the same commit, which is the
rule `check.sh` exists to enforce. Reproduce on a clean checkout of `dev`: no local edits are
needed and the two commands above fail immediately.

**Why it is not just "run the regenerators".** The sidecar is pure derivation and safe to
rebuild. The cohort files are not obviously so: a cohort is a SELECTION over the residents
layer, several landed research tickets cite cohort membership by number, and a blind
regeneration could reshuffle who is in which cohort and silently orphan those citations. That
question — does regenerating a cohort preserve its membership? — is what this ticket has to
answer before it regenerates anything.

**The ask.**

1. `python3 tools/compile_scene.py --all` for the sidecar, which is uncontroversial.
2. For each of the eight cohort/ladder files: regenerate, and DIFF the result. If membership is
   stable and only derived counts move, land it. If membership moves, stop and say so — that is
   a finding about the cohort tools, not a file to overwrite.
3. Whatever the outcome, close the hole that let it through: #844's PR gate did not catch what
   `check.sh` catches in seconds.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- `./tools/check.sh` exits 0 on `dev` with a clean tree.
- Every regenerated cohort file's membership is either unchanged, or its change is stated in
  the PR with the research tickets that cite it named.

**Links:** T-0517 (blocked by this) · T-0510 / PR #844 (the merge that introduced it)
