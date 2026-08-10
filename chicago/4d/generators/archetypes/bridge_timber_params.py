"""Parameters for the bridge_timber archetype — pure Python, NO bpy import.

Same split, same reason, as frame_tavern_params: tools/check.sh imports this on every
commit and must not need Blender.

## What is actually documented

Two of the three 1835 crossings were log structures of the same crude specification
(docs/research/03-structures-north.md §5):

- **North Branch bridge**, built winter 1831-32 to replace Clybourn's ferry: log
  construction, **about 10 ft wide, clearing the water by about 6 ft**. A variant
  account credits Samuel Miller in 1832 near the south-east corner of Kinzie and Canal,
  "formed of stringers and only fitted for foot passengers", and says the structure was
  "useless for teams" even in the summer of 1833. But on 18 Aug 1835 the war-dance
  procession — some 800 people — "crossed the North Branch bridge", so by then it was
  more than a footway. A rebuild or widening between 1833 and 1835 is likely and
  **unattested**; the dossier lists it as an open gap.

  **Correction, 2026-08-10, made while writing the first record against this module.**
  Of those two numbers only the WIDTH survives the check. Ten feet is Charles Cleaver's,
  recalled in the *Chicago Tribune* of 29 Oct 1893 — "The abutments were built of heavy
  logs in the shallow water near the banks. These bridges were ten feet wide" — and it
  has a source record now (`chicagology_prefire252`). The six-foot clearance has none:
  the dossier tags it `[DOC]` and nothing reached states it. `DOC_CLEARANCE_M` below
  keeps the figure, because it is plausible and it is the dossier's, but the constant's
  name overstates it and `data/structures/north_branch_bridge.json` records the value as
  `inferred`. Cleaver's sentence also earns the abutments their own `documented` tag,
  which is more than the dossier's summary carried.
- **South Branch raft bridge**, winter 1832-33, near Lake Street: a floating log raft,
  same ~10 ft / ~6 ft figures. Floating is a genuinely different structure, and this
  archetype does NOT model it — a raft has no piers and no clearance in the sense used
  here. It needs its own archetype, and a record that points a floating bridge at this
  one will get a fixed-pier bridge and a false impression of solidity. Left explicit
  rather than fudged.

The 1834 Dearborn Street drawbridge is a different animal again — 200 ft, a 60-ft
double-leaf draw worked by chains — and is also out of scope here.

## The dimensional confidences run the other way round from a building

frame_tavern established that massing takes the confidence of the attributes saying
what a building WAS, not of its dimensions, because an unknown size and an unknown form
are different kinds of not-knowing. A bridge inverts the premise. "About ten feet wide,
clearing the water by about six feet, of logs" is the *entire* documented description —
the dimensions ARE the character. So `width_m` and `clearance_m` belong in the set that
drives deck and stringer confidence, while `span_m` (nobody recorded the river's width
at the crossing) and `pier_spacing_m` (nobody recorded anything about the piers) do not.
The rule is unchanged; what changes is which attributes say what the thing was.
"""

from __future__ import annotations

from dataclasses import dataclass, field

CONFIDENCE_VALUE = {"documented": 0.0, "inferred": 0.5, "conjectural": 1.0}

PIER_KINDS = ("crib", "pile")

# The documented specification, in metres, for both log bridges at the forks.
DOC_WIDTH_M = 3.05        # "These bridges were ten feet wide" — Cleaver, documented
DOC_CLEARANCE_M = 1.83    # "clearing the water by about 6 ft" — dossier only, INFERRED

# Where a structure of this archetype is anchored vertically, read by
# tools/compile_scene.py and written into the sidecar for the renderer.
# docs/GLB-CONTRACT.md pins the rule: a building sits at the base of its walls on the
# terrain, and a structure over water sits on the design water surface, because a
# bridge's one measured dimension is a clearance above the water and its piers run to a
# bed this project does not model. `bridge_timber` is the first archetype to declare it;
# anything that does not declare one is placed against the terrain as before.
VERTICAL_ANCHOR = "water"

# The form attributes whose VALUE this archetype reads. See frame_tavern_params
# for the argument. No bridge record is committed yet, so this set is a promise
# made before it can be broken rather than one being repaired.
CONSUMED = frozenset({
    "width_m", "clearance_m", "pier_spacing_m", "pier_kind", "stringer_count",
    "stringer_d_m", "plank_t_m", "abutments", "construction", "railing",
    "deck_height_m",
})


class ParamError(ValueError):
    """A structure record cannot be resolved into valid archetype parameters."""


@dataclass
class BridgeTimberParams:
    """A fixed log bridge on timber piers.

    **Local origin.** x runs along the span, y across the width, and **z = 0 is the
    design water surface**, not the ground. docs/GLB-CONTRACT.md pins a structure's
    local origin to "y = 0 at the base of the walls", which a bridge does not have —
    and the one dimension the sources actually give is a clearance above the *water*,
    so anchoring anywhere else would mean carrying the documented number as a derived
    one. The sidecar therefore has to place a bridge against the water surface rather
    than the terrain. Flagged in the module docstring of bridge_timber.py too.

    **Bearing.** The long elevation is the facade, so at `rotation_deg` 0 the deck runs
    east-west and the upstream side faces north — the same rule as a building, which is
    what keeps one convention in the renderer instead of two. A bridge over the
    north-flowing north branch is therefore near 0 or 180.
    """

    span_m: float
    width_m: float = DOC_WIDTH_M
    clearance_m: float = DOC_CLEARANCE_M
    pier_spacing_m: float = 4.5
    pier_kind: str = "crib"
    stringer_count: int = 4
    stringer_d_m: float = 0.30
    plank_t_m: float = 0.09
    abutments: bool = True
    construction: str = "log"

    # OFF by default and argued in bridge_timber.py's docstring: no source attests a
    # railing on either log bridge, and the one description we have ("formed of
    # stringers", "useless for teams") describes something cruder than a railed
    # structure. Exposed so a record with evidence can turn it on; when it is on, the
    # railing is built at whatever confidence the record gives it and nothing else
    # inherits from it.
    railing: bool = False

    # Derived in __post_init__ from clearance + structure depth unless a record
    # overrides it. Kept derived because clearance is the documented number and deck
    # height is not; storing both as independent inputs would let them disagree.
    deck_height_m: float | None = None

    confidence: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.deck_height_m is None:
            self.deck_height_m = round(
                self.clearance_m + self.stringer_d_m + self.plank_t_m, 4)

    def conf(self, attr: str, default: str = "conjectural") -> float:
        return CONFIDENCE_VALUE[self.confidence.get(attr, default)]

    def worst_conf(self, *attrs: str) -> float:
        """Least-confident wins."""
        return max((self.conf(a) for a in attrs), default=1.0)

    @property
    def bays(self) -> int:
        """How many spans between supports. At least one — a short bridge is a single
        stringer run from abutment to abutment with no pier in the water at all."""
        return max(1, round(self.span_m / self.pier_spacing_m))

    @property
    def pier_x(self) -> list[float]:
        """Centre-lines of the interior piers."""
        n = self.bays
        return [self.span_m * i / n for i in range(1, n)]

    def validate(self) -> None:
        if not 3.0 <= self.span_m <= 90.0:
            raise ParamError(f"span_m {self.span_m} outside 3-90 m. The 1834 Dearborn "
                             f"Street drawbridge was 200 ft and is a different "
                             f"archetype")
        # Before the width range check, so a transposed footprint gets told what is
        # actually wrong with it rather than "your bridge is 17 metres wide".
        if self.span_m <= self.width_m:
            raise ParamError(
                f"span_m {self.span_m} is not longer than width_m {self.width_m}. "
                f"The footprint polygon's u axis is the SPAN and its v axis is the "
                f"deck width; a polygon the other way round means the record's "
                f"footprint is rotated 90 degrees")
        if not 1.0 <= self.width_m <= 12.0:
            raise ParamError(f"width_m {self.width_m} outside 1-12 m")
        if not 0.3 <= self.clearance_m <= 6.0:
            raise ParamError(f"clearance_m {self.clearance_m} outside 0.3-6 m")
        if self.pier_kind not in PIER_KINDS:
            raise ParamError(f"pier_kind '{self.pier_kind}' not in {PIER_KINDS}")
        if not 2.0 <= self.pier_spacing_m <= 25.0:
            raise ParamError(f"pier_spacing_m {self.pier_spacing_m} outside 2-25 m")
        if not 2 <= self.stringer_count <= 12:
            raise ParamError(f"stringer_count {self.stringer_count} outside 2-12")
        if not 0.12 <= self.stringer_d_m <= 0.6:
            raise ParamError(f"stringer_d_m {self.stringer_d_m} outside 0.12-0.6 m")
        if not 0.03 <= self.plank_t_m <= 0.30:
            raise ParamError(f"plank_t_m {self.plank_t_m} outside 0.03-0.3 m")
        if self.construction not in ("log", "timber_crib"):
            raise ParamError(
                f"construction '{self.construction}' is not log or timber_crib — a "
                f"framed or iron bridge is not this archetype and not this decade")
        if self.deck_height_m is None or self.deck_height_m <= self.clearance_m:
            raise ParamError("deck_height_m must sit above the clearance line; leave "
                             "it unset and it is derived from clearance + structure")
        for k, v in self.confidence.items():
            if v not in CONFIDENCE_VALUE:
                raise ParamError(f"confidence['{k}'] = '{v}' is not a confidence level")


def from_phase(phase: dict) -> BridgeTimberParams:
    """Resolve one structure phase into generator parameters.

    The footprint polygon is the DECK outline: its u extent is the span and its v
    extent is the width. validate() rejects the transposed case rather than guessing,
    because a bridge silently rotated 90 degrees lands in the river beside its
    crossing and looks plausible from every angle except above.
    """
    form = phase.get("form", {})

    def val(attr, default=None):
        a = form.get(attr)
        return default if a is None else a.get("value", default)

    def conf(attr, default="conjectural"):
        a = form.get(attr)
        return default if a is None else a.get("confidence", default)

    poly = phase.get("footprint", {}).get("polygon") or []
    if len(poly) < 3:
        raise ParamError("footprint polygon needs at least 3 points")
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    span, width = max(xs) - min(xs), max(ys) - min(ys)

    confidences = {a: conf(a) for a in form}
    confidences["footprint"] = phase.get("footprint", {}).get("confidence", "conjectural")
    # The deck's width comes off the polygon, so a record that documents "about ten
    # feet" in prose but leaves the footprint conjectural should say so on the
    # width_m attribute. Where it does not, the footprint's confidence stands in.
    confidences.setdefault("width_m", confidences["footprint"])

    p = BridgeTimberParams(
        span_m=round(span, 3),
        width_m=round(float(val("width_m", width)), 3),
        clearance_m=float(val("clearance_m", DOC_CLEARANCE_M)),
        pier_spacing_m=float(val("pier_spacing_m", 4.5)),
        pier_kind=str(val("pier_kind", "crib")),
        stringer_count=int(val("stringer_count", 4)),
        stringer_d_m=float(val("stringer_d_m", 0.30)),
        plank_t_m=float(val("plank_t_m", 0.09)),
        abutments=bool(val("abutments", True)),
        construction=str(val("construction", "log")),
        railing=bool(val("railing", False)),
        deck_height_m=(None if val("deck_height_m") is None
                       else float(val("deck_height_m"))),
        confidence=confidences,
    )
    p.validate()
    return p
