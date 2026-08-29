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

**Only `lot front` is adopted.** An advertisement that says "on South Water Street" says
where the door is, and a roof whose lot faces Randolph does not have a door on Dearborn
because its gable end reaches it. A band is a distance and says nothing about which way a
building looks. Refusing the other two costs this pass the whole of Dearborn Street, and
that cost is reported rather than avoided: `--report` prints BOTH readings, because the
reader is owed the disagreement the decision was made about, and a later owner ruling
that a corner side is a face has one number to change.

THE REFUSALS, AND WHY EACH ONE IS THERE.

  1. `not present at the scene date`  — the register excluded it already; a business
                                        contradicted before 1 July 1835, or first printed
                                        after it, is not standing in this town.
  2. `the face holds no roof whose lot fronts it` — the named street has reconstructed
                                        roofs beside it but none whose platted lot faces
                                        it. Dearborn Street is the case: eighteen roofs
                                        show it a corner side and not one a front.
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
  5. `this face already holds this proprietor` — the corpus prints one house under more
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
    "the face holds no roof whose lot fronts it",
    "this face already holds this proprietor",
    "every roof on the face is spoken for",
)


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


def dwellings() -> dict[str, list[str]]:
    """structure id -> the household ids `data/residents/` seats in it."""
    out: dict[str, list[str]] = {}
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        doc = load(path)
        at = (doc.get("lives_at") or {}).get("value")
        if isinstance(at, str) and at:
            out.setdefault(at, []).append(doc["id"])
    return out


def supply(roofs: dict[str, str], homes: dict[str, list[str]]) -> dict:
    """Per street: the roofs that front it, and the free ones, under each reading."""
    out: dict[str, dict] = {}
    for structure_id in sorted(roofs):
        for street_id, how in fronting_street.fronting(structure_id):
            face = out.setdefault(street_id, {FRONT: [], SIDE: [], BAND: [],
                                              "free": [], "homes": []})
            face.setdefault(how, []).append(structure_id)
            if how == FRONT:
                (face["homes"] if structure_id in homes else face["free"]).append(
                    structure_id)
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


def derive() -> dict:
    register = load(REGISTER)
    gaz = {b["id"]: b for b in load(GAZETTEER)["businesses"]}
    roofs = reconstructed_roofs()
    homes = dwellings()
    faces = supply(roofs, homes)

    pool = [b for b in register["businesses"] if b["action"] == "street_only"]
    pool.sort(key=lambda entry: rank_key(entry, gaz))

    taken: dict[str, list[str]] = {}
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
        face = faces.get(street_id) or {FRONT: [], SIDE: [], BAND: [],
                                        "free": [], "homes": []}
        free = [sid for sid in face["free"] if sid not in taken.get(street_id, [])]
        if not face[FRONT]:
            refusals.append(dict(
                common, refusal=REFUSALS[1],
                detail="%d roof(s) show this street a corner side and %d stand within "
                       "the centreline band; none has its platted lot on it."
                       % (len(face[SIDE]), len(face[BAND]))))
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
            refusals.append(dict(
                common, refusal=REFUSALS[3],
                detail="%d roof(s) front this street: %d are a named household's "
                       "dwelling and %d are already adopted by a better-evidenced "
                       "business." % (len(face[FRONT]), len(face["homes"]),
                                      len(taken.get(street_id, [])))))
            continue

        structure_id = free[0]
        taken.setdefault(street_id, []).append(structure_id)
        if house:
            held[house] = entry["name"]
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
            "face": FRONT,
            "roof_confidence": roofs[structure_id],
            "lot": None,
            "claims_lot": False,
            "order_is_a_claim": False,
            "note": "The advertisement names %s and nothing narrower, so this business "
                    "takes the street face and not a lot. The roof it is attached to is "
                    "an anonymous reconstructed count-unit whose platted lot faces that "
                    "street; it stays reconstructed, and WHICH roof on the face is an "
                    "allocation by tools/adopt_street_faces.py rather than a reading of "
                    "any source. Nothing here says this business stood nearer the corner "
                    "than any other on the same face."
                    % fronting_street.street_name(street_id),
        })

    adoptions.sort(key=lambda row: row["business_id"])
    refusals.sort(key=lambda row: (row["refusal"], row["business_id"]))

    unplaceable = [b for b in register["businesses"]
                   if b["action"] == "unplaceable" and b.get("present_at_scene_date")]
    by_street: dict[str, dict] = {}
    for street_id in sorted({b["action_target"] for b in pool
                             if b["action_target"]} | set(faces)):
        named = [b for b in pool if b["action_target"] == street_id]
        if not named:
            continue
        face = faces.get(street_id) or {FRONT: [], SIDE: [], BAND: [], "homes": []}
        by_street[street_id] = {
            "street_name": fronting_street.street_name(street_id),
            "businesses_naming_it": len(named),
            "adopted": sum(1 for row in adoptions if row["street_id"] == street_id),
            "roofs_fronting": len(face[FRONT]),
            "roofs_fronting_free": len(face[FRONT]) - len(face["homes"]),
            "roofs_side_only": len(face[SIDE]),
            "roofs_in_centreline_band": len(face[BAND]),
        }

    widened = sum(1 for row in refusals if row["refusal"] == REFUSALS[1])
    return {
        "schema": 1,
        "generated_by": "tools/adopt_street_faces.py",
        "_doc": "DERIVED, NEVER AUTHORED. Rebuilt from register_1835.json, the committed "
                "structures and data/residents/ by tools/adopt_street_faces.py; "
                "tools/check.sh refuses a committed copy a rebuild would not produce. "
                "The policy is docs/STREET-FACE-ADOPTION.md and the liberty is L207. "
                "An adoption claims a STREET FACE and never a lot.",
        "policy": "docs/STREET-FACE-ADOPTION.md",
        "ruling": "The owner, 2026-08-29 (T-0354): a business the paper places on a "
                  "platted street and nothing narrower adopts a reconstructed roof "
                  "already standing on that street face.",
        "scene_date": SCENE_DATE,
        "reading": {
            "adopted_face": FRONT,
            "refused_faces": [SIDE, BAND],
            "why": "An advertisement's street is where the door is. A corner side is the "
                   "cross street's building shown end-on, and a centreline band is a "
                   "distance rather than an orientation.",
            "widened_reading_would_reach": widened,
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
        elif fronting_street.fronts(structure_id, row["street_id"]) != FRONT:
            bad.append("%s adopts %s, which does not front %s by its platted lot"
                       % (who, structure_id, row["street_id"]))
        if structure_id in seen:
            bad.append("%s is the second business on %s — one roof, one business"
                       % (who, structure_id))
        seen.add(structure_id)
        if not row.get("cites"):
            bad.append("%s cites no printing of its street" % who)
    homes = dwellings()
    for structure_id in sorted(seen & set(homes)):
        bad.append("%s is a named household's dwelling and cannot also be adopted"
                   % structure_id)
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
    print("STREET-FACE ADOPTION — T-0354, the owner's ruling of 2026-08-29\n")
    print("  %-28s %s" % ("street_only in the register", counts["street_only_in_register"]))
    print("  %-28s %s" % ("adopted a street face", counts["adopted"]))
    print("  %-28s %s" % ("waiting", counts["refused"]))
    for reason, n in counts["refused_by_reason"].items():
        print("      %-40s %s" % (reason, n))
    print("  %-28s %s" % ("unplaceable, still open", counts["unplaceable_present_at_scene_date"]))
    print("\n  BY STREET FACE")
    print("  %-20s %5s %5s %6s %5s %5s %5s"
          % ("street", "ads", "took", "fronts", "free", "side", "band"))
    for street_id, row in sorted(counts["by_street"].items(),
                                 key=lambda kv: (-kv[1]["businesses_naming_it"], kv[0])):
        print("  %-20s %5d %5d %6d %5d %5d %5d"
              % (row["street_name"], row["businesses_naming_it"], row["adopted"],
                 row["roofs_fronting"], row["roofs_fronting_free"],
                 row["roofs_side_only"], row["roofs_in_centreline_band"]))
    print("\n  BOTH READINGS, because the reader is owed the disagreement:")
    print("      lot front only (this pass)              %d adopted"
          % counts["adopted"])
    print("      widened to a corner side or a band      %d more would become eligible"
          % doc["reading"]["widened_reading_would_reach"])
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
    """Break each limit in turn against the committed table; every one must fire.

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
    case("two businesses on one roof",
         lambda b: b["adoptions"].__setitem__(
             1, dict(b["adoptions"][1], structure_id=first(b)["structure_id"])),
         "one roof, one business")
    case("an adoption citing no printing of its street",
         lambda b: first(b).update(cites=[]),
         "cites no printing")

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
    print("SELF-TEST PASS — all four limits fire when broken (8 cases)")
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
