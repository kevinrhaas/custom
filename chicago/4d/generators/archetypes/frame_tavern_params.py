"""Parameters for the frame_tavern archetype — pure Python, NO bpy import.

This module is imported by tools/check.sh on every commit to validate that every
structure record can actually be resolved into generator parameters. It must stay
importable in a bare Python 3.11 with no Blender, no numpy, nothing.

The split matters: parameter validation is a per-commit concern that has to run in
seconds in every agent sandbox, while mesh generation is a content-build concern
that runs on demand with a pinned Blender. Keeping the params here is what makes
that split possible.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Confidence values as they are written into the _CONFIDENCE glTF attribute.
# See docs/GLB-CONTRACT.md.
CONFIDENCE_VALUE = {"documented": 0.0, "inferred": 0.5, "conjectural": 1.0}

ROOF_TYPES = ("gable", "hip", "shed", "gambrel")
CONSTRUCTIONS = ("balloon_frame", "braced_frame", "log", "brick", "timber_crib")

# The form attributes whose VALUE this archetype reads — the ones from_phase below
# turns into a parameter, and therefore the only ones a vertex position can depend
# on. An attribute outside this set contributes nothing the record says it should:
# the mesh either contains nothing of it or contains a fixed default in its place.
#
# Reading an attribute's CONFIDENCE is deliberately not membership. `fenestration`
# tints its geometry with the record's confidence while the shape itself is fixed
# by this module, and a tint is not a building — treating that as "consumed" would
# let the exact case this set exists to surface pass unremarked. `chimneys` was in
# that category until 2026-08-10 and is not any more: the count now decides how
# many stacks get built, so the value moves a vertex and the name belongs here.
#
# tools/validate.py holds every attribute outside it to a `geometry:` declaration
# on the record, so adding a parameter here without adding its name is a gate
# failure rather than a silently unbuilt attribute.
CONSUMED = frozenset({
    "stories", "wall_height_m", "roof_type", "roof_pitch_deg", "construction",
    "paint", "shutters", "gallery", "log_wing", "chimneys",
})

# Where this archetype touches the ground, read by tools/validate.py's ground
# contact check. `perimeter`: the whole footprint outline meets the terrain at
# local z = 0, which is what "y = 0 at the base of the walls" means in
# docs/GLB-CONTRACT.md. A building that says this and stands on ground its own
# outline does not reach is floating on one corner or buried at another.
GROUND_CONTACT = "perimeter"


class ParamError(ValueError):
    """A structure record cannot be resolved into valid archetype parameters."""


@dataclass
class FrameTavernParams:
    """A two-storey frame tavern, optionally with an attached log wing.

    Dimensions are metres. Confidence keys mirror the record's attribute
    confidences and are what the generator paints into _CONFIDENCE.
    """

    # massing
    width_m: float
    depth_m: float
    stories: int
    wall_height_m: float
    roof_type: str = "gable"
    roof_pitch_deg: float = 38.0
    construction: str = "braced_frame"

    # appearance
    paint: str = "white"
    shutters: str | None = None
    gallery: bool = False

    # How many stacks stand on the block. The COUNT comes from the record; where
    # they stand and what they are made of do not — no source describes a stack on
    # any of these buildings — so the archetype spaces them across the frontage and
    # docs/LIBERTIES.md owns the arrangement. Two is the default because two is what
    # both surviving depictions of the Sauganash show.
    chimneys: int = 2

    # the attached log wing — the Sauganash's 1829 cabin surviving as a wing.
    # See docs/RESEARCH/sauganash_hotel.md.
    log_wing: bool = False
    # Sized from the depictions: a single-pen cabin occupying roughly the left
    # third of the frontage, not a barn. Both images show it clearly subordinate
    # to the frame block.
    log_wing_width_m: float = 5.0
    log_wing_depth_m: float = 4.0
    log_wing_height_m: float = 2.35

    # per-attribute confidence, keyed by the attribute name in the record
    confidence: dict = field(default_factory=dict)

    def conf(self, attr: str, default: str = "conjectural") -> float:
        """The _CONFIDENCE float for one attribute."""
        return CONFIDENCE_VALUE[self.confidence.get(attr, default)]

    def worst_conf(self, *attrs: str) -> float:
        """Least-confident wins — the contract's rule for geometry driven by
        several attributes. A wall whose height is a guess is a guessed wall,
        even if we know it was white."""
        return max((self.conf(a) for a in attrs), default=1.0)

    def validate(self) -> None:
        if not 2.0 <= self.width_m <= 80.0:
            raise ParamError(f"width_m {self.width_m} outside plausible range 2-80 m")
        if not 2.0 <= self.depth_m <= 60.0:
            raise ParamError(f"depth_m {self.depth_m} outside plausible range 2-60 m")
        if self.stories not in (1, 2, 3):
            raise ParamError(f"stories {self.stories} not in 1..3 "
                             f"(no building in 1835 Chicago exceeded three)")
        if not 1.8 <= self.wall_height_m <= 14.0:
            raise ParamError(f"wall_height_m {self.wall_height_m} outside 1.8-14 m")
        if self.roof_type not in ROOF_TYPES:
            raise ParamError(f"roof_type '{self.roof_type}' not in {ROOF_TYPES}")
        if not 10.0 <= self.roof_pitch_deg <= 60.0:
            raise ParamError(f"roof_pitch_deg {self.roof_pitch_deg} outside 10-60 deg")
        if self.construction not in CONSTRUCTIONS:
            raise ParamError(f"construction '{self.construction}' not in {CONSTRUCTIONS}")
        # 0 is allowed and is a claim, not an absence: a record saying a building
        # had no stack gets a building with no stack. The ceiling is the number the
        # frontage can space without the stacks touching.
        if not isinstance(self.chimneys, int) or isinstance(self.chimneys, bool):
            raise ParamError(f"chimneys {self.chimneys!r} is not a whole number — the "
                             f"record states a count, not whether there was one")
        if not 0 <= self.chimneys <= 4:
            raise ParamError(f"chimneys {self.chimneys} outside 0..4; a frame block of "
                             f"these proportions cannot carry more, and a record that "
                             f"means it should say where they stood")
        for k, v in self.confidence.items():
            if v not in CONFIDENCE_VALUE:
                raise ParamError(f"confidence['{k}'] = '{v}' is not a confidence level")
        if self.log_wing:
            if self.log_wing_width_m > self.width_m:
                raise ParamError("log wing is wider than the block it attaches to")
            if not 1.8 <= self.log_wing_height_m <= 4.0:
                raise ParamError(f"log_wing_height_m {self.log_wing_height_m} outside 1.8-4 m")


def from_phase(phase: dict) -> FrameTavernParams:
    """Resolve one structure phase into generator parameters.

    Reads only the attested `value` of each form attribute plus its confidence.
    Footprint dimensions come from the phase footprint polygon's bounding box —
    the polygon is authoritative, the width/depth are derived.
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
    width, depth = max(xs) - min(xs), max(ys) - min(ys)

    # The contract pins the mesh origin to polygon coordinate (0, 0). Deriving
    # only a bounding-box SIZE and then building from the origin silently
    # translates any polygon not anchored there, so the building would stand
    # somewhere its own footprint does not describe. Refuse instead: a footprint
    # that needs an offset is asking for something this archetype does not model.
    if abs(min(xs)) > 1e-6 or abs(min(ys)) > 1e-6:
        raise ParamError(
            f"footprint polygon starts at ({min(xs)}, {min(ys)}), not the origin. "
            f"docs/GLB-CONTRACT.md pins the mesh origin to polygon coordinate (0, 0); "
            f"building from a bounding box would silently move the structure "
            f"{max(abs(min(xs)), abs(min(ys))):.2f} m from where its footprint puts it. "
            f"Re-anchor the polygon at the origin and put the offset in position.")

    confidences = {a: conf(a) for a in form}
    confidences["footprint"] = phase.get("footprint", {}).get("confidence", "conjectural")

    p = FrameTavernParams(
        width_m=round(width, 3),
        depth_m=round(depth, 3),
        stories=int(val("stories", 2)),
        wall_height_m=float(val("wall_height_m", 5.5)),
        roof_type=str(val("roof_type", "gable")),
        roof_pitch_deg=float(val("roof_pitch_deg", 38.0)),
        construction=str(val("construction", "braced_frame")),
        paint=str(val("paint", "unpainted")),
        shutters=val("shutters"),
        gallery=bool(val("gallery", False)),
        log_wing=bool(val("log_wing", False)),
        chimneys=int(val("chimneys", 2)),
        confidence=confidences,
    )
    p.validate()
    return p
