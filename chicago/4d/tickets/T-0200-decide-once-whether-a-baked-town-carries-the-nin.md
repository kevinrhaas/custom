---
id: T-0200
title: Decide once whether a baked town carries the nine renderer-drawn layers
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Decide once whether a baked town carries the nine renderer-drawn layers.

Successor to **T-0059**, which asked for one of them — a river-wharf mode of `pier_crib` — and was
withdrawn when the numbers came back. Everything below was measured by
`tools/measure_generator_half.py`, committed with T-0059's withdrawal; `--gate` fails if a figure
moves.

## The two readings

**Nine layers are drawn at load out of committed JSON, and none of them has a generator.** boats ·
enclosures · fauna · flora · frontage · residents · signage · wharves · yard. Each one has a
manifest under `data/`, a module under `renderers/web/js/` and nothing under `generators/`. So a
town assembled from GLBs alone has no fences, no signboards, no goods, no plank walks, no plants,
no boats and no docks in it. `docs/ROADMAP.md` K5 asks for "the generator half" of clauses (a),
(c) and (e) in almost the same words, three times, and the question underneath all three has never
been put once.

**And the cheapest route into the bake re-stales 346 of the 348 committed meshes.**
`generators/mesh_inputs.py` hashes `generators/build.py` into every structure asset, and
`build.py` is where the archetype table lives — so wiring in a tenth archetype costs a full rebake
before it has built a single triangle. `generators/common/*.py` costs all 348. An archetype's own
builder costs only its own meshes (2 for `pier_crib`), which is why the ticket that started this
looked small.

## What has to be decided, and it is one decision

Not "should the wharf be baked". **Is `derived at load from committed data` the ANSWER for these
layers, or a debt?** Each of the nine carries the same argument in its own record — *"a deck on
cribs is a box on boxes standing on ground and water this project already draws"* — and the
argument is a good one: the deck's height is the terrain's, sampled at load, which is T-0001's
finding, and freezing it into a GLB would put the number back beside the mesh instead of in it.
Against that: `AGENTS.md` rule 4 says *"every mesh is generated from `data/` by a command"*, and
nine layers' worth of geometry currently exists only inside a renderer.

Three honest answers, and the run that takes this picks one and writes it down:

1. **They stay renderer-drawn**, and `AGENTS.md` rule 4 gains the exception it has been operating
   under for months — with the contract that says what a second renderer would have to reimplement.
2. **They get baked**, through ONE new entry point rather than nine archetype modes — the shape
   `generators/terrain_gen.py` already has, a non-structure asset with its own inputs hash, so it
   costs no restale of anything that is not itself.
3. **They get an intermediate artifact** — the layers emit committed geometry from Python at build
   time, no Blender — which needs an argument about why two mesh authorities will not drift.

## Acceptance

The decision is written into `docs/PLAN.md` or `AGENTS.md` (not only into a ticket or a PR body),
it names all nine layers rather than one, and if it is (2) or (3) the first layer is built through
it and the other eight have a stated route. A run that builds one layer without answering the
question has not done this ticket.

**Needs the bake** if (2) is chosen; (1) and (3) do not.
