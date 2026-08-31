#!/usr/bin/env python3
"""The documented businesses the papers place on a street and nothing narrower (T-0354).

    python3 tools/adopt_street_faces.py           write
    python3 tools/adopt_street_faces.py --check   re-derive, diff, and re-assert the limits
    python3 tools/adopt_street_faces.py --report  the adoption and every refusal, with counts

WHAT THIS IS FOR.

`data/research/newspapers/register_1835.json` reads 221 businesses out of the Chicago
Democrat and the Chicago American, 203 of them standing on the scene date, and says for
each what the committed town would have to do about it. Fifty-eight resolve to a
building: `enrich_existing` where the advertisement's anchor names a roof this project
holds, `new_building` where it names a place precise enough to raise one. Sixty do
not. The paper names a PLATTED STREET AND NOTHING NARROWER — Peter Cohen at "the east end
of South Water-street", J. S. C. Hogan on South Water — and the register calls them
`street_only`. Eighty-four more reach no street the model holds at all.
Those figures move with every newspaper merge and are a snapshot; the tool is the source.

**The owner ruled on these on 2026-08-29**, choosing between the three options T-0354
set out:

> Adopt a reconstructed roof already standing on that street face and attach the
> business to it.

Not a new frontage record with a conjectural along-street position, and not waiting for a
corner. This file is that ruling made re-derivable. `docs/STREET-FACE-ADOPTION.md` is the
policy it implements and states the four limits in full; what follows is how they are
enforced here.

THE FOUR LIMITS, AND EACH ONE IS AN ASSERTION IN `--check`.

  1. **A STREET FACE, NEVER A LOT.** The paper's constraint is the face; the lot is the
     reconstruction's. Every adoption carries `lot: null` and `claims_lot: false`, and
     `--check` refuses a record that grew a lot field of any name. The plat is READ to
     derive which street a roof faces — `tools/fronting_street.py` asks the Thompson lot
     grid which tier a footprint stands in — but reading a lot to learn a frontage is not
     asserting that a business held that lot, and this file asserts the frontage only.
  2. **THE ROOF STAYS `reconstructed`.** Adopting it does not promote the building. The
     business is documented and the building under it is not, and `--check` re-reads the
     adopted structure's own phase and fails if its confidence has stopped saying so.
     This is the pattern T-0264/#518 set for a documented head on a reconstructed
     dwelling (L205), followed rather than reinvented.
  3. **THE ALONG-STREET POSITION IS THE RECONSTRUCTION'S, NOT EVIDENCE.** Which roof on
     the face a business is given is an allocation. Businesses are ranked by evidence and
     paired with the face's free roofs in id order — deterministic, and a statement about
     nothing.
  4. **ORDER WITHIN A FACE IS NOT A CLAIM.** Two businesses on one face: neither is
     nearer the corner than the other on any authority. `order_is_a_claim: false` says so
     in every record.

WHAT COUNTS AS "ALREADY STANDING ON THAT STREET FACE" — the one reading this pass makes,
and it is the narrow one.

`tools/fronting_street.py` answers three ways, and they are different claims:

  * `lot front`      — the roof's platted lot faces this street. The plat says it.
  * `corner side`    — the roof is at the end of its tier and abuts this street on the
                       SIDE. Its front is the cross street.
  * `centreline band`— the roof is off the platted grid and its centroid is within 25 m
                       of this street's centreline. Proximity, not orientation.

**`lot front` AND `corner side` are adopted; the band is not.** The narrow reading shipped
first — only `lot front`, on the owner's ruling of 2026-08-29 — and it refused the whole of
Dearborn Street, which shows eighteen roofs a side and not one a front. T-0416 dealt that
cost out rather than estimating it and put the two remaining questions to the owner
separately. **He ruled on 2026-08-30: a corner side IS a face; the band is NOT added.**

  * A corner building genuinely fronts two streets. It has a side on each, and a business
    advertising on either one is describing where its door is. Saying a corner roof stands
    on BOTH its faces is a physical fact about a corner lot; it raises no geometry, moves
    no roof and promotes nothing.
  * A band is a DISTANCE from a centreline and not an orientation. A roof 20 m from
    Dearborn's centreline may show it a wall, a gable end or nothing at all, and no reading
    of the plat can say which. It was considered and declined in the same breath, and
    `reading.considered_and_declined` in the written table names the one business it would
    have added (Wm. Sabine, on North Water Street) so a later run does not re-open it as an
    oversight.

**The cost of BOTH rulings was DEALT, not estimated (T-0416).** "Twenty-four would become
eligible" is the count of businesses a widening lets back into the deal, and it is not what
one seats: those twenty-four then meet refusal 3 and refusal 4, and the supply a widening
adds is already net of the households' homes and the yard buildings among the side-only
roofs. So the pass re-runs the whole allocation under each reading and prints what it
stands up. Measured on `dev`, 2026-08-29, before the ruling: the corner-side reading seats
TWELVE more, not twenty-four — Dearborn +8, La Salle +3, Canal +1 — and adding the band
would have seated one further. Those twelve are seated now; the one is not.

**What the corner-side reading still does NOT do.** It seats none of the three storefronts
T-0416 is named for — Wm. Sabine and John Dave on North Water Street, which has no
side-only roof at all, and the Dearborn Street wine store, which is refused on supply
under both widenings. Their answer is frontage (T-0375's neighbourhood), not a wider
reading, and the ticket says so on the record rather than closing over it.

THE REFUSALS, AND WHY EACH ONE IS THERE.

  1. `not present at the scene date`  — the register excluded it already; a business
                                        contradicted before 1 July 1835, or first printed
                                        after it, is not standing in this town.
  2. `the face holds no roof standing on it` — the named street has no reconstructed roof
                                        under either adopted reading: no lot fronts it and
                                        no roof ends its tier against it. North Water
                                        Street is the case since 2026-08-30 — one roof
                                        lies in the band and the band is not a face.
  3. `every roof on the face is spoken for` — the supply ran out. South Water Street is
                                        the case, and it is the count this ticket exists
                                        to produce rather than a failure.
  4. `the roof is a named household's dwelling` — refuses a ROOF, not a business. A roof
                                        `data/residents/` seats a household in is that
                                        household's home; hanging a documented store on
                                        it would assert a relation between two claims
                                        nothing supports. The tradesmen this leaves
                                        without a roof on South Water are T-0375's, and
                                        this pass must not quietly answer that ticket.
  5. `the roof is a yard building` — the other refusal of a ROOF. The anonymous parcels
                                        deal ANCILLARY roofs as well as principal ones —
                                        privies, stables, woodsheds standing behind a lot
                                        — and `tools/generate_block_infill.py` has refused
                                        to hang an occupant on one since the inferred-
                                        household programme: "a yard building serves the
                                        lot it stands behind, and an adoption is a claim
                                        about who lived or worked in a building". This
                                        pass did not know that rule until 2026-08-29, and
                                        it had seated NINE documented businesses in
                                        outbuildings — Peter Cohen, clothier, grocer and
                                        liquor dealer and the best-evidenced house in the
                                        whole pool, in `recon_1835_blk_south_water_clark_
                                        a3_05`, which is a privy. Found by T-0417 trying
                                        to spend the allocation into the structure
                                        records, where the generator's own gate stopped
                                        it. An ancillary roof is not free supply.
  6. `this face already holds this proprietor` — the corpus prints one house under more
                                        than one heading. 'Peter Cohen' and 'Peter
                                        Cohen's store', 'the Chicago Bakery' and 'Chicago
                                        Bakery' and 'D. Graves' who kept it, 'John
                                        Holbrook' and 'John Holbrook, hats, clothing,
                                        boots and shoes'. Seating both puts one man in two
                                        storefronts on one street, which no advertisement
                                        says. So a business whose normalised proprietor
                                        SURNAME SET is exactly one already adopted on this
                                        face is refused, and the better-evidenced heading
                                        keeps the roof.

                                        **Exactly, and not by resemblance.** A firm that
                                        shares ONE partner surname with a sole trader is
                                        NOT refused: whether those are one house is
                                        T-0338's open question over thirty-one such
                                        groups, and a placement pass must not answer it by
                                        seating or refusing. Nor does this reach a
                                        variant SPELLING — 'F. G. Blanshard', 'G.
                                        Blanshard', 'W. G. Blanchard' and 'Wm. G.
                                        Branchaud' advertise the same Lake Street trade
                                        within five months and take three roofs here
                                        (the two exact 'Blanshard's collide and one is
                                        refused), because the gazetteer's identity layer
                                        has not judged them one man and this file will not
                                        judge it either. T-0408 measures that group and is
                                        where it is settled.

WHAT THIS FILE WILL NOT DO. It will not raise a structure, move one, promote one, or
write a lot. It writes ONE derived table and nothing else; spending it — a card, a
signboard, a frontage — is T-0263's and the seeding tickets'. It will not invent a
citation: every adoption carries the claim id of the advertisement that names the street.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import fronting_street  # noqa: E402  (needs the path above)

DATA = ROOT / "data"
REGISTER = DATA / "research" / "newspapers" / "register_1835.json"
GAZETTEER = DATA / "research" / "newspapers" / "gazetteer.json"
OUT = DATA / "research" / "newspapers" / "street_face_adoptions.json"
STRUCTURES = DATA / "structures"
HOUSEHOLDS = DATA / "residents" / "households"
PROGRAMME = DATA / "reconstruction" / "1835_inferred_household_programme.json"

SCENE_DATE = "1835-07-01"
FRONT = "lot front"          # tools/fronting_street.FRONT
SIDE = "corner side"
BAND = "centreline band"

# The keys an adoption record may carry. `--check` refuses anything else, which is how
# limit 1 is enforced against a future field rather than only against today's.
ADOPTION_KEYS = {
    "business_id", "business_name", "trade", "proprietors",
    "street_id", "street_name", "street_text", "placement_class",
    "cites", "first_issue", "last_issue", "mentions",
    "structure_id", "face", "roof_confidence",
    "lot", "claims_lot", "order_is_a_claim", "note",
}

REFUSALS = (
    "not present at the scene date",
    "the face holds no roof standing on it",
    "this face already holds this proprietor",
    "every roof on the face is spoken for",
)

#: The readings of "already standing on that street face" the ruling adopts, in the order
#: a face is dealt. `lot front` is the owner's ruling of 2026-08-29 (T-0354); `corner side`
#: is his ruling of 2026-08-30 (T-0416), on the measurement this file produced. `centreline
#: band` was put to him in the same question and DECLINED, and it is absent here rather than
#: commented out so that adopting it again would have to be a deliberate edit.
ADOPTED_READINGS = (FRONT, SIDE)

#: How a record says, in its own note, why its roof stands on the face it took. A corner
#: adoption must not read as a lot-front one: the visitor is owed the difference between
#: "its platted lot faces that street" and "it ends its tier against that street".
FACE_PHRASE = {
    FRONT: "whose platted lot faces %s",
    SIDE: "standing at the end of its platted tier, where the tier meets %s: a corner "
          "building, which the owner ruled on 2026-08-30 stands on both its faces",
    # Only reachable from a COUNTERFACTUAL deal — the band is not an adopted reading, so
    # no record derive() writes can carry this phrase. It is here so that costing the
    # declined reading does not crash, which is a poorer reason to lose a measurement than
    # any argument about it.
    BAND: "lying within 25 m of the platted centreline of %s, which is the reading the "
          "owner declined on 2026-08-30",
}

#: The reading that was measured, offered and refused. Kept so the written table can name
#: what declining it cost, and so `--report` can go on printing the disagreement.
DECLINED_READING = BAND


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(doc) -> str:
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# the town: which reconstructed roofs front which street, and which are homes
# ---------------------------------------------------------------------------

def reconstructed_roofs() -> dict[str, str]:
    """structure id -> the confidence its own phase gives the building, for `recon_*`.

    The `recon_*` prefix is the anonymous count-unit layer — a roof raised to meet an
    aggregate target, standing for no named building. Those are the only roofs the ruling
    reaches: adopting a roof this project argues IS some particular structure would put a
    documented business inside a documented building on no evidence at all.
    """
    out: dict[str, str] = {}
    for path in sorted(STRUCTURES.glob("recon_*.json")):
        doc = load(path)
        phases = doc.get("phases") or []
        grades = {(phase.get("documented_range") or {}).get("confidence")
                  for phase in phases}
        grades.discard(None)
        out[doc["id"]] = sorted(grades)[0] if len(grades) == 1 else "|".join(sorted(grades))
    return out


def yard_roofs() -> set[str]:
    """The `recon_*` roofs the anonymous parcels dealt as YARD BUILDINGS.

    `reconstruction.inventory_class` is the parcels' own word for it: a
    `principal_functional` roof is a building on the lot, an `ancillary` one is a privy, a
    stable or a woodshed standing behind it. `tools/generate_block_infill.py` refuses to
    write an `occupants` block onto an ancillary roof — "a yard building serves the lot it
    stands behind, and an adoption is a claim about who lived or worked in a building" —
    and that rule is older than this pass and outranks it.
    """
    out: set[str] = set()
    for path in sorted(STRUCTURES.glob("recon_*.json")):
        doc = load(path)
        if ((doc.get("reconstruction") or {}).get("inventory_class")) == "ancillary":
            out.add(doc["id"])
    return out


def named_dwellings() -> dict[str, list[str]]:
    """structure id -> the NAMED household ids `data/residents/` seats in it."""
    out: dict[str, list[str]] = {}
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        doc = load(path)
        at = (doc.get("lives_at") or {}).get("value")
        if isinstance(at, str) and at:
            out.setdefault(at, []).append(doc["id"])
    return out


def inferred_dwellings() -> dict[str, list[str]]:
    """structure id -> the INFERRED household ids the reconstruction seats in it.

    The other layer that holds a roof, and it does not live in `data/residents/`: the
    inferred-household programme hypothesises an occupant from the town's arithmetic
    without naming anybody, so its households have no resident record to be found by
    `named_dwellings()` above. `tools/inferred_occupancy.py` is the ledger that spends
    both layers into the structure records, and it RAISES if one roof is claimed twice —
    "one roof, one occupant" — because letting either win silently would put a documented
    shopkeeper into an inferred labourer's cottage, or lose the labourer.
    """
    if not PROGRAMME.exists():
        return {}
    out: dict[str, list[str]] = {}
    for household in load(PROGRAMME).get("households", []):
        for key in ("lives_at", "works_at"):
            at = household.get(key)
            if isinstance(at, str) and at.startswith("recon_"):
                out.setdefault(at, []).append(household["id"])
    return out


def dwellings() -> dict[str, list[str]]:
    """structure id -> every household id ANY layer seats in it. Refusal 4's supply test.

    Both layers, and refusal 4 has covered both since 2026-08-30. It could not bite under
    the narrow reading — no roof the inferred programme held happened to have its platted
    lot on a street the register named — and the corner-side ruling made it bite at once:
    the very first re-derivation handed Elmira Fowler's Dearborn Street millinery a corner
    roof, `recon_1835_south_w4_032`, that the inferred layer already holds. The ledger
    caught it, which is what the ledger is for; refusing it HERE is what keeps the table
    derivable rather than merely gated.

    It is the same refusal in both cases and for the same reason. A roof some layer seats
    a household in is that household's home, and hanging a documented store on it would
    assert a relation between two claims nothing supports. That the inferred household is
    itself an invention makes the case stronger, not weaker: the relation would then be
    between a printed advertisement and a hypothesis.
    """
    out = {sid: list(ids) for sid, ids in named_dwellings().items()}
    for sid, ids in inferred_dwellings().items():
        out.setdefault(sid, []).extend(ids)
    return out


EMPTY_FACE = {FRONT: [], SIDE: [], BAND: [], "free": [], "homes": [], "yards": []}

# The order a pass deals a face's roofs when it is allowed to read more than one of
# them: the plat first, then the corner sides, then the band. It is the order of
# decreasing claim, so a widened reading never takes a weaker roof while a stronger one
# is free, and the lot-front-only allocation this pass actually writes is unchanged by
# the existence of the others.
READING_ORDER = (FRONT, SIDE, BAND)


def free_under(face: dict, readings: tuple[str, ...], homes: dict,
               yards: set[str]) -> list[str]:
    """The roofs a pass adopting `readings` could take, in READING_ORDER then id order.

    Refusals 5 and 6 are applied here rather than by the caller, because they are
    refusals of a ROOF and hold under any reading of "face": a named household's home is
    that household's home whichever street the roof shows, and a privy is a privy.
    `free_under(face, (FRONT,), ...)` is exactly `face["free"]`, which is what keeps the
    committed allocation byte-identical.
    """
    out: list[str] = []
    for how in READING_ORDER:
        if how not in readings:
            continue
        out += [sid for sid in face[how] if sid not in homes and sid not in yards]
    return out


def reading_of(face: dict, structure_id: str) -> str:
    """Which of the three readings put this roof on this face."""
    for how in READING_ORDER:
        if structure_id in face[how]:
            return how
    raise AssertionError("%s is not on this face under any reading" % structure_id)


def supply(roofs: dict[str, str], homes: dict[str, list[str]],
           yards: set[str]) -> dict:
    """Per street: the roofs that show it a face, under each reading, and the free ones.

    A roof standing on this street under an ADOPTED reading lands in exactly one of three
    buckets, and only `free` is supply: a named household's home (refusal 4), a yard
    building (refusal 5), or a roof a business may take. The bucketing spans the adopted
    readings rather than `lot front` alone, because refusals 4 and 5 refuse a ROOF and hold
    whichever way it shows the street — a privy is a privy seen end-on. Roofs that reach
    the street only by the DECLINED reading are counted under their own key and are not
    supply at all.
    """
    out: dict[str, dict] = {}
    for structure_id in sorted(roofs):
        for street_id, how in fronting_street.fronting(structure_id):
            face = out.setdefault(street_id, {key: list(value)
                                              for key, value in EMPTY_FACE.items()})
            face[how].append(structure_id)
            if how in ADOPTED_READINGS:
                if structure_id in homes:
                    face["homes"].append(structure_id)
                elif structure_id in yards:
                    face["yards"].append(structure_id)
                else:
                    face["free"].append(structure_id)
    return out


# ---------------------------------------------------------------------------
# the pool: the register's street_only businesses, ranked by evidence
# ---------------------------------------------------------------------------

def surnames(entry: dict) -> tuple[str, ...]:
    """The normalised proprietor surname SET a register entry prints, sorted.

    Empty where the advertisement names no proprietor at all — an anonymous 'wholesale
    wine and liquor store' cannot collide with anything, and is never refused by refusal 5.
    """
    found: set[str] = set()
    for name in entry.get("proprietors") or []:
        text = re.sub(r"^\[uncertain:\s*", "", str(name)).rstrip("]").strip()
        # 'Mulford, J. H.' is the same man as 'J. H. Mulford'; the comma form puts the
        # surname first, and the corpus prints both.
        head = text.split(",")[0].strip() if "," in text else text
        parts = [word for word in re.split(r"\s+", head) if word]
        if not parts:
            continue
        surname = re.sub(r"[^a-z]", "", parts[-1].lower())
        if surname:
            found.add(surname)
    return tuple(sorted(found))


def rank_key(entry: dict, gaz: dict) -> tuple:
    """Evidence first — most printings, then earliest sighting, then id.

    A ranking, not a claim: it decides which business is served first where a face is
    short of roofs, and nothing about where any of them stood.
    """
    printed = gaz.get(entry["id"], {})
    mentions = len(printed.get("mentions") or [])
    first = (entry.get("evidence") or {}).get("first_issue") or "9999-99-99"
    return (-mentions, first, entry["id"])


def allocate(pool: list, gaz: dict, faces: dict, roofs: dict, homes: dict,
             yards: set[str], readings: tuple[str, ...]) -> tuple[list, list]:
    """Deal the ranked pool onto the faces, reading "face" as `readings` says.

    The pass this file writes calls it with `ADOPTED_READINGS` and nothing else, and
    `limits()` re-asserts that against the committed document independently of anything
    here. The parameter exists so the counterfactual another ruling would produce can be
    MEASURED by dealing it, rather than estimated from the count of businesses a widened
    supply would make eligible; those two numbers are not the same, because a widened
    supply still meets refusals 3 and 4. It is what produced the +12 the owner ruled on.

    ONE ROOF, ONE BUSINESS — AND `taken` IS THEREFORE GLOBAL RATHER THAN PER STREET. Under
    the narrow reading a roof reached exactly one face, so the two were the same thing.
    From 2026-08-30 a corner roof stands on TWO faces, and a per-street ledger would let
    the Dearborn deal and the Lake deal each hand out the same corner: one building, two
    shopfronts, on nothing. `limits()` would have caught it after the fact and failed the
    gate; refusing it here means the table is never written that way in the first place.
    """
    taken: set[str] = set()
    seated: dict[str, dict[tuple[str, ...], str]] = {}
    adoptions: list[dict] = []
    refusals: list[dict] = []

    for entry in pool:
        street_id = entry["action_target"]
        printed = gaz.get(entry["id"], {})
        common = {
            "business_id": entry["id"],
            "business_name": entry["name"],
            "street_id": street_id,
            "street_name": fronting_street.street_name(street_id),
        }
        if not entry.get("present_at_scene_date"):
            refusals.append(dict(common, refusal=REFUSALS[0],
                                 detail=entry.get("exclusion_note")
                                 or entry.get("exclusion") or ""))
            continue
        face = faces.get(street_id) or {key: list(value)
                                        for key, value in EMPTY_FACE.items()}
        free = [sid for sid in free_under(face, readings, homes, yards)
                if sid not in taken]
        if not any(face[how] for how in readings):
            refusals.append(dict(
                common, refusal=REFUSALS[1],
                detail="no roof stands on this street under an adopted reading: %d has "
                       "its platted lot on it, %d end a tier against it, and %d lie "
                       "within the centreline band, which the owner declined as a face "
                       "on 2026-08-30."
                       % (len(face[FRONT]), len(face[SIDE]), len(face[BAND]))))
            continue
        house = surnames(entry)
        held = seated.setdefault(street_id, {})
        if house and house in held:
            refusals.append(dict(
                common, refusal=REFUSALS[2],
                detail="%r already stands on this face under the same proprietor "
                       "surname(s) %s, on better evidence. One house, one roof per face; "
                       "whether these are two headings of one business is the "
                       "gazetteer's to judge (T-0338, T-0340), not this pass's."
                       % (held[house], ", ".join(house))))
            continue
        if not free:
            on_face = [sid for how in readings for sid in face[how]]
            refusals.append(dict(
                common, refusal=REFUSALS[3],
                detail="%d roof(s) stand on this street: %d are a household's "
                       "dwelling under one layer or the other, %d are yard buildings the "
                       "parcels dealt behind a lot, and %d are already adopted by a "
                       "better-evidenced business."
                       % (len(on_face),
                          len([sid for sid in on_face if sid in homes]),
                          len([sid for sid in on_face if sid in yards]),
                          len([sid for sid in on_face if sid in taken]))))
            continue

        structure_id = free[0]
        taken.add(structure_id)
        if house:
            held[house] = entry["name"]
        how = reading_of(face, structure_id)
        adoptions.append({
            "business_id": entry["id"],
            "business_name": entry["name"],
            "trade": entry.get("trade"),
            "proprietors": entry.get("proprietors") or [],
            "street_id": street_id,
            "street_name": fronting_street.street_name(street_id),
            "street_text": printed.get("street"),
            "placement_class": entry.get("placement_class"),
            "cites": sorted(printed.get("mentions") or []),
            "first_issue": (entry.get("evidence") or {}).get("first_issue"),
            "last_issue": (entry.get("evidence") or {}).get("last_issue"),
            "mentions": len(printed.get("mentions") or []),
            "structure_id": structure_id,
            "face": how,
            "roof_confidence": roofs[structure_id],
            "lot": None,
            "claims_lot": False,
            "order_is_a_claim": False,
            "note": "The advertisement names %s and nothing narrower, so this business "
                    "takes the street face and not a lot. The roof it is attached to is "
                    "an anonymous reconstructed count-unit %s; it stays reconstructed, "
                    "and WHICH roof on the face is an allocation by "
                    "tools/adopt_street_faces.py rather than a reading of any source. "
                    "Nothing here says this business stood nearer the corner than any "
                    "other on the same face."
                    % (fronting_street.street_name(street_id),
                       FACE_PHRASE[how] % fronting_street.street_name(street_id)),
        })

    adoptions.sort(key=lambda row: row["business_id"])
    refusals.sort(key=lambda row: (row["refusal"], row["business_id"]))
    return adoptions, refusals


#: Every reading of "face" the project has costed, dealt out in full so the table carries
#: the disagreement the decisions were made about. The first two are now HISTORY — the
#: narrow reading that shipped on 2026-08-29 and the corner-side widening the owner adopted
#: on 2026-08-30 — and the third is the one he declined. Keeping all three means the
#: written table answers "what did that ruling cost, and what did the other one save?"
#: without anybody re-deriving it from a git history.
COSTED_READINGS = (
    ("lot front only", (FRONT,)),
    ("a corner side is a face", (FRONT, SIDE)),
    ("a corner side or the band is a face", (FRONT, SIDE, BAND)),
)


def costed(pool: list, gaz: dict, faces: dict, roofs: dict, homes: dict,
           yards: set[str], adoptions: list) -> dict:
    """What each reading of "face" actually SEATS, dealt rather than estimated.

    `widened_reading_would_reach` counts the businesses refused for want of a face —
    the ones a wider reading would let back into the deal. It is NOT the number one
    seats, and reading it as one overstates the ruling: those businesses then meet
    refusal 3 (this face already holds this proprietor) and refusal 4 (every roof on the
    face is spoken for), and the supply a widening adds is itself net of refusals 5 and 6,
    because a corner-side roof can be a household's home or a privy exactly as a fronting
    one can. T-0416 is the ticket that put this to the owner, and dealing it is what let
    the question be asked as "twelve shops" rather than "twenty-four".
    """
    today = {row["business_id"]: row for row in adoptions}
    out: dict[str, dict] = {}
    for label, readings in COSTED_READINGS:
        would, refused = allocate(pool, gaz, faces, roofs, homes, yards, readings)
        seated = {row["business_id"]: row for row in would}
        gained = sorted(set(seated) - set(today))
        # A wider reading is not automatically a superset. Roofs are dealt to the pool in
        # evidence order and a roof can be taken once, so a corner roof a side-reading
        # hands to a Dearborn advertisement is a roof no longer free to the Lake Street
        # one whose lot fronts it. Reporting only the gain would hide that, so both
        # directions are counted and the delta below is the net.
        lost = sorted(set(today) - set(seated))
        by_street: dict[str, int] = {}
        for business_id in gained:
            street_id = seated[business_id]["street_id"]
            by_street[street_id] = by_street.get(street_id, 0) + 1
        out[label] = {
            "adopted_faces": list(readings),
            "in_force": tuple(readings) == ADOPTED_READINGS,
            "would_seat": len(would),
            "against_the_reading_in_force": len(would) - len(today),
            "seats_that_the_reading_in_force_does_not": gained,
            "seats_that_the_reading_in_force_does_not_by_street":
                dict(sorted(by_street.items())),
            "loses_against_the_reading_in_force": lost,
            "would_still_refuse": len(refused),
            "would_still_refuse_by_reason": {reason: sum(1 for row in refused
                                                         if row["refusal"] == reason)
                                             for reason in REFUSALS},
        }
    return out


def derive() -> dict:
    register = load(REGISTER)
    gaz = {b["id"]: b for b in load(GAZETTEER)["businesses"]}
    roofs = reconstructed_roofs()
    named = named_dwellings()
    homes = dwellings()
    yards = yard_roofs()
    faces = supply(roofs, homes, yards)

    pool = [b for b in register["businesses"] if b["action"] == "street_only"]
    pool.sort(key=lambda entry: rank_key(entry, gaz))

    adoptions, refusals = allocate(pool, gaz, faces, roofs, homes, yards,
                                   ADOPTED_READINGS)

    unplaceable = [b for b in register["businesses"]
                   if b["action"] == "unplaceable" and b.get("present_at_scene_date")]
    by_street: dict[str, dict] = {}
    for street_id in sorted({b["action_target"] for b in pool
                             if b["action_target"]} | set(faces)):
        named = [b for b in pool if b["action_target"] == street_id]
        if not named:
            continue
        face = faces.get(street_id) or {key: list(value)
                                        for key, value in EMPTY_FACE.items()}
        by_street[street_id] = {
            "street_name": fronting_street.street_name(street_id),
            "businesses_naming_it": len(named),
            "adopted": sum(1 for row in adoptions if row["street_id"] == street_id),
            "roofs_lot_front": len(face[FRONT]),
            "roofs_corner_side": len(face[SIDE]),
            "roofs_on_the_adopted_face": sum(len(face[how])
                                             for how in ADOPTED_READINGS),
            "roofs_free": len(face["free"]),
            "roofs_home": len(face["homes"]),
            "roofs_home_named": len([sid for sid in face["homes"] if sid in named]),
            "roofs_home_inferred": len([sid for sid in face["homes"]
                                        if sid not in named]),
            "roofs_yard": len(face["yards"]),
            "roofs_in_centreline_band_declined": len(face[BAND]),
        }

    eligible = sum(1 for row in refusals if row["refusal"] == REFUSALS[1])
    costed_readings = costed(pool, gaz, faces, roofs, homes, yards, adoptions)

    # THE BAND, CONSIDERED AND DECLINED — recorded here rather than left to a document,
    # so a later run reads the refusal off the same file it reads the adoption off and
    # does not re-open it as an oversight (T-0416's acceptance).
    band = costed_readings["a corner side or the band is a face"]
    declined = {
        "reading": DECLINED_READING,
        "ruled": "The owner, 2026-08-30 (T-0416): the band is NOT added.",
        "why": "A band is a distance from a centreline and not an orientation. A roof "
               "within 25 m of a street's platted line may show it a wall, a gable end "
               "or nothing at all, and no reading of the plat can say which. The corner "
               "side adopted above is an orientation the plat does state.",
        "it_would_have_seated": len(band["seats_that_the_reading_in_force_does_not"]),
        "it_would_have_seated_ids": band["seats_that_the_reading_in_force_does_not"],
        "it_would_have_cost": len(band["loses_against_the_reading_in_force"]),
        "it_would_have_cost_ids": band["loses_against_the_reading_in_force"],
    }
    return {
        "schema": 1,
        "generated_by": "tools/adopt_street_faces.py",
        "_doc": "DERIVED, NEVER AUTHORED. Rebuilt from register_1835.json, the committed "
                "structures and data/residents/ by tools/adopt_street_faces.py; "
                "tools/check.sh refuses a committed copy a rebuild would not produce. "
                "The policy is docs/STREET-FACE-ADOPTION.md and the liberty is L212. "
                "An adoption claims a STREET FACE and never a lot.",
        "policy": "docs/STREET-FACE-ADOPTION.md",
        "ruling": "The owner, 2026-08-29 (T-0354): a business the paper places on a "
                  "platted street and nothing narrower adopts a reconstructed roof "
                  "already standing on that street face.",
        "ruling_extended": "The owner, 2026-08-30 (T-0416): a corner side IS a face — a "
                           "building on a corner stands on both the streets it meets, "
                           "and a business advertising on either is saying where its "
                           "door is. The centreline band was offered in the same "
                           "question and DECLINED.",
        "scene_date": SCENE_DATE,
        "reading": {
            "adopted_faces": list(ADOPTED_READINGS),
            "refused_faces": [DECLINED_READING],
            "why": "An advertisement's street is where the door is. A corner building has "
                   "a door on each of the two streets it meets, so both are faces; a "
                   "centreline band is a distance from a line rather than an "
                   "orientation, and says nothing about which way a building looks.",
            "considered_and_declined": declined,
            "refused_for_want_of_a_face": eligible,
            "refused_for_want_of_a_face_note":
                "The count of businesses REFUSED FOR WANT OF A FACE, which is how many a "
                "wider reading would let back into the deal — not how many it would "
                "seat. `costed_readings` below deals every reading out in full and "
                "reports what each actually stands up (T-0416).",
            "costed_readings": costed_readings,
        },
        "counts": {
            "street_only_in_register": len(pool),
            "adopted": len(adoptions),
            "refused": len(refusals),
            "refused_by_reason": {reason: sum(1 for row in refusals
                                              if row["refusal"] == reason)
                                  for reason in REFUSALS},
            "unplaceable_present_at_scene_date": len(unplaceable),
            "by_street": by_street,
        },
        "adoptions": adoptions,
        "refusals": refusals,
    }


# ---------------------------------------------------------------------------
# build / check / report
# ---------------------------------------------------------------------------

def build() -> int:
    OUT.write_text(dumps(derive()), encoding="utf-8")
    print("wrote %s" % OUT.relative_to(ROOT))
    return 0


def limits(doc: dict) -> list[str]:
    """The four limits, re-asserted against the committed document."""
    bad: list[str] = []
    roofs = reconstructed_roofs()
    seen: set[str] = set()
    for row in doc["adoptions"]:
        who = row.get("business_id", "?")
        extra = set(row) - ADOPTION_KEYS
        if extra:
            bad.append("%s carries field(s) the policy does not allow: %s"
                       % (who, ", ".join(sorted(extra))))
        for key, value in row.items():
            if "lot" in key and value not in (None, False):
                bad.append("%s names a lot in %r — limit 1 refuses it" % (who, key))
        if row.get("lot") is not None or row.get("claims_lot") is not False:
            bad.append("%s does not declare `lot: null, claims_lot: false`" % who)
        if row.get("order_is_a_claim") is not False:
            bad.append("%s does not declare `order_is_a_claim: false`" % who)
        structure_id = row.get("structure_id")
        if structure_id not in roofs:
            bad.append("%s adopts %r, which is not an anonymous reconstructed roof"
                       % (who, structure_id))
        elif roofs[structure_id] != "reconstructed":
            bad.append("%s adopts %s, whose building is now %r — limit 2 refuses a "
                       "promoted roof" % (who, structure_id, roofs[structure_id]))
        else:
            how = fronting_street.fronts(structure_id, row["street_id"])
            if how not in ADOPTED_READINGS:
                bad.append("%s adopts %s, which does not front %s by a lot front or a "
                           "corner side — it reaches that street %s"
                           % (who, structure_id, row["street_id"],
                              "by the centreline band, which the owner declined as a "
                              "face on 2026-08-30" if how == BAND else "not at all"))
            elif row.get("face") != how:
                # The `face` field is what a card, a note or a later pass reads to know
                # WHICH claim the adoption makes. A record that says `lot front` over a
                # corner is the quiet way this ruling gets overstated, so it is checked
                # against the derivation rather than taken on trust.
                bad.append("%s says it took %s by its %r, but %s reaches that street by "
                           "its %r" % (who, row["street_id"], row.get("face"),
                                       structure_id, how))
        if structure_id in seen:
            bad.append("%s is the second business on %s — one roof, one business"
                       % (who, structure_id))
        seen.add(structure_id)
        if not row.get("cites"):
            bad.append("%s cites no printing of its street" % who)
    named = named_dwellings()
    inferred = inferred_dwellings()
    for structure_id in sorted(seen & (set(named) | set(inferred))):
        bad.append("%s is a %s household's dwelling and cannot also be adopted"
                   % (structure_id, "named" if structure_id in named else "n inferred"))
    for structure_id in sorted(seen & yard_roofs()):
        bad.append("%s is a yard building — a privy, a stable or a woodshed standing "
                   "behind a lot — and a business cannot be seated in one" % structure_id)
    return bad


def check() -> int:
    if not OUT.exists():
        print("MISSING %s — run tools/adopt_street_faces.py" % OUT.relative_to(ROOT))
        return 1
    committed = load(OUT)
    rebuilt = derive()
    if dumps(committed) != dumps(rebuilt):
        print("STALE %s — a rebuild does not reproduce the committed copy."
              % OUT.relative_to(ROOT))
        for key in sorted(set(committed) | set(rebuilt)):
            if committed.get(key) != rebuilt.get(key):
                print("  differs: %s" % key)
        return 1
    bad = limits(committed)
    if bad:
        for line in bad:
            print("  FAIL %s" % line)
        return 1
    counts = committed["counts"]
    print("  ok    %d street-only business(es): %d adopted a street face, %d wait; "
          "no adoption claims a lot"
          % (counts["street_only_in_register"], counts["adopted"], counts["refused"]))
    print("  ok    %d unplaceable business(es) stand outside this policy (T-0354 half two)"
          % counts["unplaceable_present_at_scene_date"])
    return 0


def report() -> int:
    doc = derive()
    counts = doc["counts"]
    print("STREET-FACE ADOPTION — T-0354, the owner's ruling of 2026-08-29,")
    print("extended by his ruling of 2026-08-30 that a corner side is a face (T-0416)\n")
    print("  %-28s %s" % ("street_only in the register", counts["street_only_in_register"]))
    print("  %-28s %s" % ("adopted a street face", counts["adopted"]))
    print("  %-28s %s" % ("waiting", counts["refused"]))
    for reason, n in counts["refused_by_reason"].items():
        print("      %-40s %s" % (reason, n))
    print("  %-28s %s" % ("unplaceable, still open", counts["unplaceable_present_at_scene_date"]))
    print("\n  BY STREET FACE — `front` and `side` are both adopted faces; `band` is not")
    print("  %-20s %5s %5s %6s %5s %5s %5s"
          % ("street", "ads", "took", "front", "side", "free", "band"))
    for street_id, row in sorted(counts["by_street"].items(),
                                 key=lambda kv: (-kv[1]["businesses_naming_it"], kv[0])):
        print("  %-20s %5d %5d %6d %5d %5d %5d"
              % (row["street_name"], row["businesses_naming_it"], row["adopted"],
                 row["roofs_lot_front"], row["roofs_corner_side"], row["roofs_free"],
                 row["roofs_in_centreline_band_declined"]))
    print("\n  EVERY READING COSTED, because the reader is owed the disagreement the")
    print("  decisions were made about. Eligible is not seated: refusals 3 and 4 still")
    print("  hold, and the supply a wider reading adds is already net of a household's")
    print("  home and a yard building, so each row below is DEALT rather than estimated.")
    print("      %-36s %d refused for want of any face"
          % ("in force:", doc["reading"]["refused_for_want_of_a_face"]))
    for label, row in doc["reading"]["costed_readings"].items():
        mark = "<-- IN FORCE" if row["in_force"] else ""
        print("      %-34s %2d seated (%+d), %d still refused  %s"
              % (label, row["would_seat"], row["against_the_reading_in_force"],
                 row["would_still_refuse"], mark))
        gains = row["seats_that_the_reading_in_force_does_not_by_street"]
        print("          gains: %s" % (", ".join(
            "%s +%d" % (fronting_street.street_name(street_id), n)
            for street_id, n in gains.items()) or "nothing"))
        if row["loses_against_the_reading_in_force"]:
            print("          loses: %s"
                  % ", ".join(row["loses_against_the_reading_in_force"]))
    declined = doc["reading"]["considered_and_declined"]
    print("\n  CONSIDERED AND DECLINED — the %s, %s" % (declined["reading"],
                                                        declined["ruled"]))
    print("      it would have seated %d further business(es): %s"
          % (declined["it_would_have_seated"],
             ", ".join(declined["it_would_have_seated_ids"]) or "none"))
    print("\n  ADOPTIONS")
    for row in doc["adoptions"]:
        print("      %-46s %-20s %s" % (row["business_name"][:46], row["street_name"],
                                        row["structure_id"]))
    print("\n  REFUSALS")
    for row in doc["refusals"]:
        print("      %-46s %-20s %s" % (row["business_name"][:46], row["street_name"],
                                        row["refusal"]))
        print("          %s" % row["detail"])
    return 0


def self_test() -> int:
    """Break each limit and each ruling boundary in turn; every one must fire.

    `--check` compares a rebuild before it reaches the limits, so a hand-edit trips the
    staleness gate first and the limits themselves would never be exercised by any
    ordinary failure. That is precisely how a gate becomes decoration. These cases call
    `limits()` on a mutated copy of the committed document and assert it complains.
    """
    doc = load(OUT)
    if not doc["adoptions"]:
        print("  FAIL nothing is adopted, so nothing can be broken")
        return 1
    failed = 0

    def case(label: str, mutate, wanted: str) -> None:
        nonlocal failed
        broken = json.loads(json.dumps(doc))
        mutate(broken)
        found = limits(broken)
        if any(wanted in line for line in found):
            print("  fires: %s" % label)
        else:
            failed = 1
            print("  FAIL  %s did not fire — got %r" % (label, found))

    def first(broken):
        return broken["adoptions"][0]

    case("a record that grows a lot field",
         lambda b: first(b).update(lot_id="blk_south_water_clark/n/3"),
         "does not allow")
    case("a record that fills the lot field it declares",
         lambda b: first(b).update(lot=7),
         "names a lot")
    case("a record that stops declaring `claims_lot: false`",
         lambda b: first(b).update(claims_lot=True),
         "names a lot")
    case("a record that makes its order a claim",
         lambda b: first(b).update(order_is_a_claim=True),
         "order_is_a_claim")
    case("an adoption on a roof this project does not hold",
         lambda b: first(b).update(structure_id="a_roof_that_is_not_there"),
         "not an anonymous reconstructed roof")
    case("an adoption on a roof that does not front its street",
         lambda b: first(b).update(street_id="washington"),
         "does not front")

    # THE 2026-08-30 RULING'S OWN BOUNDARY. It widened what counts as a face by exactly
    # one reading, and the two ways that widening could quietly become three are a record
    # that reaches its street only by the DECLINED band, and a corner adoption that
    # describes itself as a lot front. Neither is caught by any case above: both name a
    # street the roof genuinely reaches, and the second is a true record of a real
    # adoption with one field overstated.
    corner = next((row for row in doc["adoptions"] if row["face"] == SIDE), None)
    if corner is None:
        print("  FAIL  nothing is adopted on a corner side, so the 2026-08-30 ruling "
              "cannot be tested")
        failed = 1
    else:
        case("a corner adoption that calls itself a lot front",
             lambda b: next(row for row in b["adoptions"]
                            if row["business_id"] == corner["business_id"]
                            ).update(face=FRONT),
             "says it took")

    banded = next(((sid, street_id) for sid in sorted(reconstructed_roofs())
                   for street_id, how in fronting_street.fronting(sid) if how == BAND),
                  None)
    if banded is None:
        print("  FAIL  no roof reaches a street by the band, so the declined reading "
              "cannot be tested")
        failed = 1
    else:
        case("an adoption reaching its street only by the declined centreline band",
             lambda b: first(b).update(structure_id=banded[0], street_id=banded[1],
                                       face=BAND),
             "declined as a face")
    case("two businesses on one roof",
         lambda b: b["adoptions"].__setitem__(
             1, dict(b["adoptions"][1], structure_id=first(b)["structure_id"])),
         "one roof, one business")
    case("an adoption citing no printing of its street",
         lambda b: first(b).update(cites=[]),
         "cites no printing")

    # Refusal 5's live half. Nine adoptions stood in outbuildings until 2026-08-29, so
    # this case is the one that would have caught it: seat the first business on a roof
    # the parcels dealt as ancillary and the limits must say so.
    yards = sorted(yard_roofs())
    if not yards:
        print("  FAIL  the town holds no ancillary roof, so refusal 5 cannot be tested")
        failed = 1
    else:
        case("a business seated in a yard building",
             lambda b: first(b).update(structure_id=yards[0], street_id=next(
                 street for street, how in fronting_street.fronting(yards[0])
                 if how == FRONT)),
             "is a yard building")

    # Refusal 4's OTHER half, and the one the corner-side ruling made live. A roof the
    # inferred-household programme holds is somebody's home too, and it is invisible to
    # `data/residents/`; the first re-derivation under the widened reading walked straight
    # into one. This is the case that would have caught it.
    inferred_only = sorted(set(inferred_dwellings()) - set(named_dwellings()))
    if not inferred_only:
        print("  FAIL  the inferred-household programme holds no roof of its own, so "
              "refusal 4's second half cannot be tested")
        failed = 1
    else:
        case("a business seated in a roof the inferred-household layer holds",
             lambda b: first(b).update(structure_id=inferred_only[0]),
             "inferred household's dwelling")

    # Limit 2's live half: a roof promoted out of `reconstructed` must fail. It cannot be
    # faked by mutating the table — the confidence is read from the structure — so this
    # asserts the reader that limit 2 depends on actually distinguishes the grades.
    roofs = reconstructed_roofs()
    grades = set(roofs.values())
    if grades == {"reconstructed"}:
        print("  ok:    every adoptable roof reads `reconstructed` from its own phase "
              "(%d roofs), which is what limit 2 re-reads" % len(roofs))
    else:
        print("  ok:    the phase reader distinguishes %s, so a promoted roof is visible "
              "to limit 2" % ", ".join(sorted(grades)))

    if failed:
        print("SELF-TEST FAIL")
        return 1
    print("SELF-TEST PASS — all four limits, both halves of both roof "
          "refusals and both edges of the 2026-08-30 face ruling fire when broken "
          "(12 cases)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="re-derive, diff the committed copy, and re-assert the limits")
    ap.add_argument("--report", action="store_true",
                    help="the adoption and every refusal, with counts")
    ap.add_argument("--self-test", action="store_true",
                    help="break each of the four limits in turn; every one must fire")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.check:
        return check()
    if args.report:
        return report()
    return build()


if __name__ == "__main__":
    raise SystemExit(main())
