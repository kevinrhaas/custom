"""Parameters for the log_dwelling archetype — pure Python, NO bpy import.

Same split, and for the same reason, as frame_tavern_params: tools/check.sh imports
this module on every commit to prove that every scene-included record still resolves
into buildable parameters, and it has to do that in a bare Python 3.11 with no
Blender in the sandbox.

## What this archetype has to cover

Hewn log was the commonest construction at the forks in 1835, and the three buildings
this archetype was written for differ in exactly the ways the parameters expose:

- **Wolf Point Tavern** — "partly log and partly frame" (chicagology/prefire273,
  describing Wentworth's house), so a log core with a frame extension. It was *low*;
  the retrospective images that show it tall are not evidence. Its one genuinely
  distinctive documented feature is the **painted sign of a wolf hung outside** by
  about 1833, which is what `sign` is for.
- **Samuel Miller's house** — "log cabin with a two-storey frame addition fronting the
  river" (DRLOIH), corroborated by the 1833 view showing "a two-story building and
  adjoining log cabin" on the north bank. So: `frame_addition` on the `front` side,
  two storeys, over a single-storey log core.
- **Rev. Jesse Walker's meeting house** — Wau-Bun: "a small square log building,
  originally designed for a school-house". No additions, no sign, square in plan. The
  plain case, and the one that proves the archetype degrades to nothing-but-a-cabin.

See docs/research/03-structures-north.md §2.1, §2.2 and §3.1 for the evidence and its
disagreements.

## What it deliberately does not cover

The `frame_addition` is a *massing* addition — a clapboarded block sharing the log
core's footprint bbox. It is not a general-purpose second archetype: a building that is
mostly frame with a log wing is a `frame_tavern` (the Sauganash), and one that is
mostly log with a frame piece is a `log_dwelling`. Which side of that line a record
falls on is a research judgement and belongs in the record's `archetype`, not in a
parameter.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Confidence values as they are written into the _CONFIDENCE glTF attribute.
# See docs/GLB-CONTRACT.md. Duplicated from frame_tavern_params rather than imported
# so that neither params module can break the other's import in the commit gate.
CONFIDENCE_VALUE = {"attested": 0.0, "inferred": 0.5, "reconstructed": 1.0}

# Only the two roof forms this archetype actually builds. A log dwelling with a
# gambrel roof in 1835 Chicago would be a claim, not a default, so the archetype
# refuses it loudly rather than quietly substituting a gable.
LOG_ROOF_TYPES = ("gable", "shed")

# How a signboard is displayed. `bracket` is an arm off the wall; `sapling_pole` is
# a slender trunk set in the ground with a cross-arm at its head, which is what the
# Wolf Point sources describe and what its engraving draws. See `sign_mount`.
SIGN_MOUNTS = ("bracket", "sapling_pole")

# What may be painted on a board. Deliberately an enumeration rather than free text:
# the value drives an outline this module owns, so a record naming a device the
# archetype cannot draw has to be refused rather than silently given a blank board.
SIGN_DEVICES = (None, "wolf")

ADDITION_SIDES = ("front", "end")

# The form attributes whose VALUE this archetype reads. See the same set in
# frame_tavern_params for the argument; the short version is that an attribute
# outside it cannot move a vertex, so the record states something the mesh does
# not contain and `tools/validate.py` makes the record say which.
#
# Note the two spellings this set made visible rather than tolerant. The Wolf
# Point record wrote `frame_extension` and `signage`; the parameters are
# `frame_addition` and `sign`. Neither name is wrong on its own and neither
# resolver ever complained, which is exactly why a documented frame half and a
# documented painted sign went unbuilt without anything saying so. The record was
# renamed to this vocabulary on 2026-08-10 and re-baked in the same slice; the set
# is what found it, and it is what will find the next one.
#
# `chimney` was a third one of those, caught the same way and fixed on 2026-08-10.
# Every record in the dataset states `chimneys`, a COUNT; this module read a
# boolean called `chimney` that no record has ever contained, so `from_phase` took
# its default and every log building got exactly one stack whatever the record
# said. Samuel Miller's house says two. The parameter is now `chimneys` and it is
# the count.
# `finish_key` and `roof_condition` are NOT in this set and must not be, although the
# archetype now reads both (T-0007). This set names FORM attributes — what a phase
# states about the building — and those two live in the record's `reconstruction`
# block, the 665-roof programme's own ledger, one level above the phase. That is why
# no archetype could read them for as long as `from_phase` took only a phase, and it
# is what `docs/RESEARCH/materials.md` §4 finding 4 was pointing at.
CONSUMED = frozenset({
    "stories", "wall_height_m", "roof_type", "roof_pitch_deg", "construction",
    "loft", "chimneys", "sign", "sign_mount", "sign_device", "frame_paint",
    "frame_addition", "frame_addition_side", "frame_addition_width_m",
    "frame_addition_depth_m", "frame_addition_stories", "frame_addition_height_m",
})

# See frame_tavern_params for the argument. `perimeter`: the footprint outline
# meets the terrain at local z = 0, the base of the walls.
GROUND_CONTACT = "perimeter"


class ParamError(ValueError):
    """A structure record cannot be resolved into valid archetype parameters."""


@dataclass
class LogDwellingParams:
    """A hewn-log building, optionally with a frame addition, a loft and a sign.

    Dimensions are metres and describe the WHOLE building including any frame
    addition, because that is what a footprint polygon means. The addition is
    carved out of the footprint bbox, never bolted onto the outside of it — a
    building that overflows its own recorded footprint is a lie the renderer
    cannot detect.
    """

    # massing
    width_m: float
    depth_m: float
    stories: int = 1
    wall_height_m: float = 2.5
    roof_type: str = "gable"
    # 35, not the frame_tavern's 38 and emphatically not the 42 this started at: a
    # cabin is shallow in plan and low in the wall, so a steep pitch puts more roof
    # above the eave than there is wall below it and the building stops reading as
    # low. Wolf Point Tavern is described as low and that has to survive the roof.
    roof_pitch_deg: float = 35.0
    construction: str = "log"

    # a sleeping or storage loft under the roof. From outside this is a gable-end
    # opening and nothing else, which is honest: a loft leaves no other external
    # trace, and inventing a dormer would be adding evidence.
    loft: bool = False

    # How many stacks the building carries. Log dwellings here were heated, so the
    # default is one, and the record supplies the number. Where each one stands is
    # the archetype's: the first goes against the log core's gable end, and a second
    # goes on the frame addition if there is one — which is the reasoning Miller's
    # record gives for counting two, "a stack in each element" — or against the
    # opposite gable if there is not. Nothing about a stack's position, size or
    # material is attested for any of these buildings; docs/LIBERTIES.md owns that.
    chimneys: int = 1

    # the frame addition. `front` puts it against the facade (Miller's house, the
    # two-storey block "fronting the river"); `end` extends the building sideways
    # (Wolf Point Tavern, "partly log and partly frame").
    frame_addition: bool = False
    frame_addition_side: str = "front"
    frame_addition_width_m: float = 6.0
    frame_addition_depth_m: float = 4.0
    frame_addition_stories: int = 2
    frame_addition_height_m: float | None = None
    frame_paint: str = "unpainted"

    # A hanging signboard, as a string naming what was painted on it. The value
    # exists so the sidecar can say what the board carried; whether the mesh draws
    # the device is `sign_device`'s question and not this one's.
    sign: str | None = None

    # HOW THE BOARD WAS DISPLAYED, added 2026-08-21 for T-0072. `bracket` is what
    # this archetype built from the start — a board on an arm off the wall beside
    # the door, an arrangement nothing attests and which was chosen because it is
    # what a tavern sign usually is. `sapling_pole` is what the Wolf Point sources
    # actually describe: "the wolf sign was hung on a sapling" (chicagology's Wolf's
    # Point note, chicagology_prefire273), which is a slender trunk set in the ground
    # and not a wall bracket, and which the 2026-08-18 owner brief's engraving of the
    # tavern draws as a mast-tall pole with a cross-arm and the board flying from it.
    # A record has to choose; the default stays `bracket` so no other building moves.
    sign_mount: str = "bracket"

    # WHETHER THE DEVICE IS PAINTED ON THE BOARD, and it is a separate attribute
    # from `sign` for the reason gallows_braced is separate from gallows_frames: the
    # subject is one claim and the drawing is another, and they are evidenced
    # differently. `None` leaves the board blank, which is what every board in this
    # dataset was until T-0072 and what docs/LIBERTIES.md L25 argued for. `wolf`
    # paints a flat canine silhouette, and a record turning it on is claiming only
    # THAT a wolf was painted there — the outline is the archetype's own and owes
    # docs/LIBERTIES.md an entry.
    sign_device: str | None = None

    # The finish the 665-roof programme dealt this building, and how weathered its
    # roof is. NOT form attributes — they live in the record's `reconstruction`
    # block, which is why `from_phase` takes the record — and until T-0007 they were
    # read by `generators/inferred_placeholder.py` alone, so a weathered roof and a
    # fresh one were the same pixel on every archetype building in the town
    # (docs/RESEARCH/materials.md §4 finding 4). None on every named or documented
    # building, which carries no reconstruction block and therefore keeps exactly the
    # colours it had. `common/materials.py` is what turns either into a surface.
    finish_key: str | None = None
    roof_condition: str | None = None

    # per-attribute confidence, keyed by the attribute name in the record
    confidence: dict = field(default_factory=dict)

    def conf(self, attr: str, default: str = "reconstructed") -> float:
        """The _CONFIDENCE float for one attribute."""
        return CONFIDENCE_VALUE[self.confidence.get(attr, default)]

    def worst_conf(self, *attrs: str) -> float:
        """Least-confident wins — the contract's rule for geometry driven by
        several attributes."""
        return max((self.conf(a) for a in attrs), default=1.0)

    @property
    def addition_height_m(self) -> float:
        if self.frame_addition_height_m is not None:
            return self.frame_addition_height_m
        return 2.55 if self.frame_addition_stories == 1 else 4.7

    def validate(self) -> None:
        if not 2.0 <= self.width_m <= 40.0:
            raise ParamError(f"width_m {self.width_m} outside plausible range 2-40 m "
                             f"for a log building")
        if not 2.0 <= self.depth_m <= 40.0:
            raise ParamError(f"depth_m {self.depth_m} outside plausible range 2-40 m "
                             f"for a log building")
        if self.stories not in (1, 2):
            raise ParamError(f"stories {self.stories} not in 1..2 — a log core of "
                             f"three storeys is not a thing at the forks in 1835")
        if not 1.8 <= self.wall_height_m <= 7.0:
            raise ParamError(f"wall_height_m {self.wall_height_m} outside 1.8-7 m")
        if self.stories == 1 and self.wall_height_m > 3.6:
            raise ParamError(f"wall_height_m {self.wall_height_m} is two storeys' worth "
                             f"of wall on a one-storey record; set stories or the height")
        if self.roof_type not in LOG_ROOF_TYPES:
            raise ParamError(
                f"roof_type '{self.roof_type}' not in {LOG_ROOF_TYPES}. log_dwelling "
                f"builds gable and shed only; a hip or gambrel roof on a log building "
                f"here would be an invention, so it is refused rather than substituted")
        if not 15.0 <= self.roof_pitch_deg <= 55.0:
            raise ParamError(f"roof_pitch_deg {self.roof_pitch_deg} outside 15-55 deg")
        if self.construction != "log":
            raise ParamError(
                f"construction '{self.construction}' is not log — a mostly-frame "
                f"building belongs to the frame_tavern archetype, and which side of "
                f"that line a building falls on is a research judgement, not a default")
        for k, v in self.confidence.items():
            if v not in CONFIDENCE_VALUE:
                raise ParamError(f"confidence['{k}'] = '{v}' is not a confidence level")
        if self.sign is not None and not str(self.sign).strip():
            raise ParamError("sign is present but empty — omit it or say what it showed")
        if self.sign_mount not in SIGN_MOUNTS:
            raise ParamError(
                f"sign_mount '{self.sign_mount}' not in {SIGN_MOUNTS} — how a board "
                f"was displayed is evidence, so an unknown mounting is refused "
                f"rather than defaulted to the commonest one")
        if self.sign_device not in SIGN_DEVICES:
            raise ParamError(
                f"sign_device '{self.sign_device}' not in {SIGN_DEVICES} — this "
                f"archetype draws only the devices whose outline it owns")
        if self.sign_device is not None and self.sign is None:
            raise ParamError(
                "sign_device is set with no sign — a device is painted ON a board, "
                "so the board has to be stated first")
        if not isinstance(self.chimneys, int) or isinstance(self.chimneys, bool):
            raise ParamError(f"chimneys {self.chimneys!r} is not a whole number — the "
                             f"record states a count, not whether there was one")
        # Two is the ceiling because two is the number this archetype can place with
        # an argument behind it: one on the log core, one on the frame addition. A
        # third stack would have to go somewhere invented for no stated reason, and
        # a log pen at the forks carrying three is a claim a record should make
        # explicitly rather than have an archetype guess at.
        if not 0 <= self.chimneys <= 2:
            raise ParamError(f"chimneys {self.chimneys} outside 0..2 for a log dwelling; "
                             f"this archetype places one at the core's gable and one on "
                             f"the frame addition, and has nowhere argued to put a third")
        if self.chimneys > 1 and not self.frame_addition and self.width_m < 4.0:
            raise ParamError(f"two stacks on a {self.width_m} m log pen with no frame "
                             f"addition would stand within a metre of each other")
        if self.frame_addition:
            self._validate_addition()

    def _validate_addition(self) -> None:
        if self.frame_addition_side not in ADDITION_SIDES:
            raise ParamError(f"frame_addition_side '{self.frame_addition_side}' "
                             f"not in {ADDITION_SIDES}")
        if self.frame_addition_stories not in (1, 2):
            raise ParamError(f"frame_addition_stories {self.frame_addition_stories} "
                             f"not in 1..2")
        if not 1.8 <= self.addition_height_m <= 7.0:
            raise ParamError(f"frame addition height {self.addition_height_m} "
                             f"outside 1.8-7 m")
        if self.frame_addition_width_m > self.width_m:
            raise ParamError("frame addition is wider than the footprint it sits in")
        if self.frame_addition_depth_m > self.depth_m:
            raise ParamError("frame addition is deeper than the footprint it sits in")
        # The addition is carved out of the footprint, so what is left has to still be
        # a building. 2 m is about the smallest single-pen log room anyone lived in.
        if self.frame_addition_side == "end":
            if self.width_m - self.frame_addition_width_m < 2.0:
                raise ParamError(
                    f"an end addition {self.frame_addition_width_m} m wide leaves only "
                    f"{self.width_m - self.frame_addition_width_m:.2f} m of log core "
                    f"inside a {self.width_m} m footprint; widen the footprint or "
                    f"record the building as frame")
        elif self.depth_m - self.frame_addition_depth_m < 2.0:
            raise ParamError(
                f"a front addition {self.frame_addition_depth_m} m deep leaves only "
                f"{self.depth_m - self.frame_addition_depth_m:.2f} m of log core "
                f"inside a {self.depth_m} m footprint; deepen the footprint or "
                f"record the building as frame")


def from_phase(phase: dict, record: dict | None = None) -> LogDwellingParams:
    """Resolve one structure phase into generator parameters.

    Reads only the attested `value` of each form attribute plus its confidence.
    Footprint dimensions come from the phase footprint polygon's bounding box — the
    polygon is authoritative, width and depth are derived.
    """
    form = phase.get("form", {})

    def val(attr, default=None):
        a = form.get(attr)
        return default if a is None else a.get("value", default)

    def conf(attr, default="reconstructed"):
        a = form.get(attr)
        return default if a is None else a.get("confidence", default)

    poly = phase.get("footprint", {}).get("polygon") or []
    if len(poly) < 3:
        raise ParamError("footprint polygon needs at least 3 points")
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    width, depth = max(xs) - min(xs), max(ys) - min(ys)

    # `dock` is excluded from the sweep because this builder never reads it, the same
    # exclusion `frame_storefront_params` makes and for the same reason: a dock
    # statement selects a deck on the RENDERER's wharf layer
    # (tools/generate_river_wharves.py), not a metre of this mesh, and
    # generators/mesh_inputs.py hashes exactly what the builder can see — "only a
    # value the generator reads counts". Without it, stating the landing at Robert
    # Kinzie's store (T-0107) would have marked that GLB stale on the day the
    # statement was authored, on a runner with no Blender, when not one of its
    # vertices could move. The storefront archetype learned this on the five South
    # Water stores (T-0062); this is the log archetype carrying the same lesson.
    # `reconstruction` is the 665-roof programme's own block: it is present on every
    # anonymous or household roof it dealt and absent from every named building.
    recon = (record or {}).get("reconstruction") or {}
    confidences = {a: conf(a) for a in form if a != "dock"}
    confidences["footprint"] = phase.get("footprint", {}).get("confidence", "reconstructed")

    stories = int(val("stories", 1))
    sign = val("sign")

    p = LogDwellingParams(
        width_m=round(width, 3),
        depth_m=round(depth, 3),
        stories=stories,
        wall_height_m=float(val("wall_height_m", 2.5 if stories == 1 else 4.6)),
        roof_type=str(val("roof_type", "gable")),
        roof_pitch_deg=float(val("roof_pitch_deg", 35.0)),
        construction=str(val("construction", "log")),
        loft=bool(val("loft", False)),
        chimneys=int(val("chimneys", 1)),
        frame_addition=bool(val("frame_addition", False)),
        frame_addition_side=str(val("frame_addition_side", "front")),
        frame_addition_width_m=float(val("frame_addition_width_m",
                                         round(width * 0.5, 3))),
        frame_addition_depth_m=float(val("frame_addition_depth_m",
                                         round(depth * 0.5, 3))),
        frame_addition_stories=int(val("frame_addition_stories", 2)),
        frame_addition_height_m=(None if val("frame_addition_height_m") is None
                                 else float(val("frame_addition_height_m"))),
        frame_paint=str(val("frame_paint", "unpainted")),
        sign=(None if sign is None else str(sign)),
        sign_mount=str(val("sign_mount", "bracket")),
        sign_device=(None if val("sign_device") is None
                     else str(val("sign_device"))),
        # The programme's own finish deal, read off the record rather than the
        # phase. `wall_finish` in `common/materials.py` states the order these are
        # applied in and why a stated coating outranks them.
        finish_key=recon.get("finish_key"),
        roof_condition=recon.get("roof_condition"),
        confidence=confidences,
    )
    p.validate()
    return p
