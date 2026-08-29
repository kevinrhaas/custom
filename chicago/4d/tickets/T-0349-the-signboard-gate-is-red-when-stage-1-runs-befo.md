---
id: T-0349
title: The signboard gate is red when stage 1 runs before it and green when stage 2 runs alone
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Measured on this runner on 2026-08-29 while gating T-0299, which changes no renderer file
and no geometry:

    SMOKE_VIEWPORT=desktop SMOKE_STAGE=1-2 --published   146 passed, 3 failed
      - the frontage layer lays all five records' walks and stands their posts
      - the board carries the record's own name, painted
      - the Sauganash's two hitching posts stand on their own ground, carrying nothing

    SMOKE_VIEWPORT=desktop SMOKE_STAGE=2   --published
      FAIL  the frontage layer lays all five records' walks and stands their posts
      pass  the board carries the record's own name, painted

Same tree, same published mirror, same viewport, minutes apart. **The board assertion is red
when stage 1 has run before it and green when stage 2 runs alone.** The first two failures
are the standing reds T-0244 and T-0243 already record; this third one is not in any ticket,
and it is the only one of the three whose verdict depends on what ran before it.

It is not this branch's: the identical 146/3 with the identical three names comes out of a
clean `origin/dev` worktree's own published mirror under `SMOKE_ROOT`, run back to back with
the branch's. It is `dev`'s.

The assertion at `tools/smoke_renderer.mjs:3989` is a conjunction of seven clauses, and six
of them are about the lettering itself. The seventh is `frontage.meshes === 62` — a count of
the frontage layer's meshes, carrying eight lines of comment recording every time the number
was moved by a street being laid. A count of meshes present in the scene is exactly the kind
of clause that can read differently depending on what an earlier stage loaded, and it is
bundled into a check whose name promises something else entirely. A visitor reading the
failure is told the painted name is wrong when the painted name is fine.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The run-order dependence is identified — which clause of the seven changes verdict, and
  what stage 1 does to it — and stated with both readings side by side.
- The gate gives the SAME verdict for stage 2 alone and stage 1-2, on an unmodified `dev`.
  Whichever verdict is correct, it is one verdict.
- If the mesh census belongs to a different question from the painted name, it is split into
  its own check with its own name, so a failure says which thing failed.
- No clause is deleted to make the two agree: a count that cannot be asserted across stages
  is re-stated, not dropped.
