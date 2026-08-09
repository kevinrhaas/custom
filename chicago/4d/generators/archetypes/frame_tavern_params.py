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
        confidence=confidences,
    )
    p.validate()
    return p
