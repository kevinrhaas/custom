"""What the builder may read off a phase before it decides to build one.

TICKET T-0161. One rule lives here, and it lives here rather than in either
caller because it had FOUR restatements and one of them was missing.

`drawn_by` is a phase saying its geometry moved to another layer. The record
that started it is `data/structures/estray_pen.json`, whose note is as plain as
it gets:

    "A phase carrying this block builds NO MESH: no GLB is baked from it,
     tools/compile_scene.py writes `asset: null` into the sidecar, the renderer
     loads no asset for it and the walker is not stopped by its footprint."

`tools/validate.py`, `tools/compile_scene.py` and
`tools/generate_dooryard_plantings.py` each honoured that with their own copy of
`if ph.get("drawn_by")`. `generators/build.py` — the one program the sentence is
actually addressed to — had ZERO occurrences of the string. So the builder and
the validator disagreed about the same record and the bake sat between them:
`build.py --all` baked `estray_pen__pen_1833.glb`, `web_derivatives.sh` made a
derivative of it, and `validate.py` then failed twice, which made `check.sh` red
straight out of `tools/bake.sh`. Every full bake needed the GLB, the derivative
and three manifest entries deleted BY HAND to pass its own gate.

A predicate copied into four files is a rule in none of them: three copies
agreeing is not agreement, it is a coincidence that held until someone wrote a
fourth reader and did not know to copy it. So the copies are replaced by imports
of this one, and the fourth reader — the builder — is added.

WHY THIS FILE IS IN `common/`, which is not a filing preference. `mesh_inputs.py`
hashes `generators/build.py` and `generators/common/*.py` into every asset's
`inputs_sha256`, and deliberately does NOT hash itself ("this file computes the
hash and makes no geometry"). A rule about WHICH PHASES GET A MESH AT ALL has to
be inside that hash: change it, and what the town is made of changes, so every
asset must go stale and be rebuilt. Putting it in `mesh_inputs.py` would have
been the tidier import and would have left the rule able to move without
restaling a single asset — a hole exactly the shape of the one this ticket is
about.
"""
from __future__ import annotations


def drawn_by_another_layer(phase: dict) -> bool:
    """True when nothing should bake a mesh for this phase.

    The test is deliberately the bare truthiness of the key, which is what all
    three original readers applied: `drawn_by` is either absent, or it is a block
    that `tools/validate.py::check_drawn_by` then holds to every half of its own
    promise — the named record exists, names this structure back, is listed in
    its layer's manifest, carries no `form`, and leaves NO GLB and NO manifest
    entry behind. Validating the block's CONTENTS is that function's job and is
    not repeated here; this answers only the one question a builder asks, which
    is whether to build at all.
    """
    return bool(phase.get("drawn_by"))
