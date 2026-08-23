#!/usr/bin/env python3
"""Which horizontal run a roof climbs, per archetype — the one thing a pitch needs
before it can be gated on the ridge it produces.

WHY THIS EXISTS (T-0145). `tools/family_bands.py` samples a pitch inside the family's
authored `N:12-M:12` band and wants to keep the resulting ridge inside the family's
authored `ridge_ft` band. The ridge is `eave + run x tan(pitch)`, and the `run` is the
only part of that the crosswalk does not author: it is the archetype's, because the
archetype decides which way the ridge points and whether a plane covers half the span
or all of it. So the run is named here, once, for the five archetypes the reconstructed
parcels instantiate.

THIS FILE DUPLICATES ARCHETYPE ARITHMETIC AND THAT IS ONLY SAFE BECAUSE IT IS CHECKED.
Retyping a rule into a second file is the exact fault `tools/family_bands.py` was
written to end. What makes it defensible here is that the copy cannot drift in silence:
`tools/measure_ridge_band.py` computes the ridge from THIS model and reads the ridge the
committed GLB actually carries — the top of the `roof` material, which is the ridge and
not the chimney over it — and fails when the two disagree by more than the roof's own
board thickness. The model is a claim about the generators and the gate tests it every
commit. If an archetype changes how its roof is set out, the gate goes red here before
anything downstream believes a wrong number.

WHAT EACH ARCHETYPE DOES, and where it does it:

  frame_dwelling      `_roof` -> `MeshBuilder.add_gable_roof(..., ridge_along_x=True)`.
                      "The ridge runs parallel to the facade, always" — the module says
                      so in as many words — so the span is the DEPTH, and `add_gable_roof`
                      grows the rectangle by its overhang on all four sides BEFORE it
                      raises the ridge, so the run is (depth + 2 x overhang) / 2.
  frame_tavern        `ridge_along_x=(w >= d)` — the ridge runs down the LONG axis, so
                      the span is the short one, grown the same way.
  log_dwelling        `_ridge_along_x(x0, y0, x1, y1)` is `(x1-x0) >= (y1-y0)`: the same
                      long-axis rule, so the span is the short one.
  frame_storefront    `_ridge_along_x(p)` is `not p.gable_front`, so the RECORD decides:
                      a gable front turns the ridge across the plan (span = depth), and
                      eaves to the street leaves it along the plan (span = width)... and
                      it is the other way round from how it reads, because
                      `ridge_along_x=True` means the ridge runs along x and the roof
                      therefore falls across y. Span = DEPTH when `gable_front` is false,
                      WIDTH when it is true.
  outbuilding         its OWN roof builder, and the one that does not grow the plan:
                      "THE OVERHANG CONTINUES THE SLOPE rather than being pinned at the
                      eave height", so the ridge stands over the building's own centre
                      line and the overhang adds nothing to the height. `roof_run_m`
                      names the run directly — half the span across the ridge for a
                      gable, the whole span for a shed — and `ridge_along_x` is
                      `width >= depth`, the long-axis rule.

A shed roof has no ridge; its high eave is what `ridge_ft` has to be read against, and
the run is the whole span rather than half of it. That is the same number the family's
`ridge_ft` band means for a family whose roof line is "gable or shed", and those families
author no pitch anyway (see `family_bands.pitch_band_deg`), so nothing is sampled for
them — the gate still measures them.
"""

from __future__ import annotations

# `MeshBuilder.add_gable_roof`'s default overhang, which `frame_tavern` and
# `frame_storefront` already name as a constant of their own for the same reason.
GABLE_OVERHANG_M = 0.25

# The archetypes whose roof is built by `MeshBuilder.add_gable_roof`, and how each
# decides which way the ridge points. `True` means the ridge runs along x, so the roof
# falls across y and the span is the DEPTH.
def _ridge_along_x(archetype: str, width_m: float, depth_m: float,
                   gable_front: bool | None) -> bool:
    if archetype == "frame_dwelling":
        return True                                   # parallel to the facade, always
    if archetype == "frame_storefront":
        return not bool(gable_front)                  # the record decides
    return width_m >= depth_m                         # frame_tavern, log_dwelling


def ridge_run_m(archetype: str, roof_type: str, width_m: float, depth_m: float,
                gable_front: bool | None = None) -> float | None:
    """The horizontal distance from the eave to the ridge, or None if not modelled."""
    if archetype == "outbuilding":
        if roof_type == "shed":
            # `OutbuildingParams.shed_axis` derives the fall from the open sides and
            # defaults to 'y'; a reconstructed anonymous outbuilding has no open side,
            # so the fall is front-to-back and the run is the whole depth.
            return depth_m
        # `ridge_along_x = width >= depth`; the ridge runs down the long axis, so the
        # plane covers half of the SHORT one.
        return (depth_m if width_m >= depth_m else width_m) / 2.0
    if archetype not in ("frame_dwelling", "frame_tavern", "frame_storefront",
                         "log_dwelling"):
        return None
    along_x = _ridge_along_x(archetype, width_m, depth_m, gable_front)
    span = (depth_m if along_x else width_m) + 2 * GABLE_OVERHANG_M
    return span if roof_type == "shed" else span / 2.0
