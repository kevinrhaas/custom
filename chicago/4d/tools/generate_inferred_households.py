#!/usr/bin/env python3
"""Expand the inferred-household programme: people, adoptions, and new buildings.

    python3 tools/generate_inferred_households.py            write
    python3 tools/generate_inferred_households.py --check    re-derive and diff

Phase two of docs/ROADMAP.md K1. Phase one wrote the town's DOCUMENTED and DERIVED
people and deliberately wrote no inferred ones; this expands
`data/reconstruction/1835_inferred_household_programme.json` into

  * `data/residents/households/hh_inf_*.json` — one file per inferred household,
    every person graded `inferred`, none of them named;
  * `data/residents/index.json` — the manifest's household rows and counts, and
    the five documented households whose buildings this parcel finally builds;
  * `data/structures/*.json` — the new records: the seven documented buildings
    phase one found with no record, and the inferred workplaces and dwellings the
    occupation census requires.

The adopted anonymous roofs are NOT written here. They belong to the two
anonymous-infill generators, which read `tools/inferred_occupancy.py` for the
occupancy block so their own byte-for-byte drift check keeps working.

WHAT THIS FILE WILL NOT DO. It will not invent a name: every inferred person
carries a designation and says in its note that it is a hypothesis. It will not
grade an invention `inferred` to make a gate pass: a position nobody recorded is
`conjectural` here exactly as it is on every other record in the dataset, and it
owes docs/LIBERTIES.md a `Covers:` token like any other invention.
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRUCTURES = DATA / "structures"
HOUSEHOLDS = DATA / "residents" / "households"
INDEX = DATA / "residents" / "index.json"
PROGRAMME = DATA / "reconstruction" / "1835_inferred_household_programme.json"
INVENTORY = DATA / "reconstruction" / "1835_building_inventory.json"
RESERVED = (DATA / "reconstruction" / "1835_phase2_west_wolf_point_approaches.json",
            DATA / "reconstruction" / "1835_phase2_south_core_and_mixed_recipe.json")
SPEC = "owner_chicago_1835_reconstruction_spec_2026"
ANDREAS = "andreas_1884_v1"
SCENE_DATE = "1835-07-01"
PREFIX = "hh_inf_"

sys.path.insert(0, str(ROOT / "generators"))
sys.path.insert(0, str(ROOT / "tools"))

from inferred_occupancy import label  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(doc, indent: int) -> str:
    return json.dumps(doc, indent=indent, ensure_ascii=False) + "\n"


# --------------------------------------------------------------------------
# people
# --------------------------------------------------------------------------

def arrival_block() -> dict:
    return {
        "value": SCENE_DATE,
        "confidence": "inferred",
        "note": ("NOT AN ARRIVAL, A BOUND. Nothing dates a hypothesised household, and a year "
                 "would be a claim nobody made. `not_later_than` the scene date states the only "
                 "thing the inference carries: the town's need is measured on 1 July 1835, so "
                 "the household is posited as being here by then and at no stated time before "
                 "it."),
        "precision": "not_later_than",
    }


def null_block(note: str) -> dict:
    return {"value": None, "confidence": "conjectural", "note": note}


def link_block(sid, note: str) -> dict:
    if sid is None:
        return null_block(note)
    return {"value": sid, "confidence": "inferred", "sources": [SPEC], "note": note}


def person(hh: dict, census: dict, idx: int | None = None, extra: dict | None = None) -> dict:
    occ = (extra or hh)["occupation"]
    trade = label(occ)
    base = hh["id"].removeprefix("hh_")
    if extra is None:
        article = "An" if trade[0] in "aeiou" else "A"
        pid, rel, name = base, "head", f"{article} {trade} (inferred resident, unnamed)"
        why = (f"THE {ordinal_word(hh['ordinal']).upper()} OF {hh['of']} {trade.upper()} "
               f"HOUSEHOLDS THIS LAYER INFERS. " + census[occ]["argument"])
    else:
        pid = f"{base}_{extra['relationship'][:1]}{idx}"
        rel = extra["relationship"]
        article = "An" if rel[0] in "aeiou" else "A"
        name = f"{article} {rel} {trade} (inferred resident, unnamed)"
        why = (f"A {rel} in the same shop. The trade's own argument: "
               + census[occ]["argument"])
    p = {
        "id": pid,
        "name": name,
        "relationship": rel,
        "grade": "inferred",
        "occupation": {
            "value": occ,
            "confidence": "inferred",
            "sources": [ANDREAS, SPEC],
            "note": census[occ]["argument"],
        },
        "note": ("HYPOTHESISED, AND NOT A PERSON. No source names this resident and none is "
                 "claimed to: the record asserts that a town of 3,265 people in 398 dwellings "
                 "held at least this many households of this trade, and asserts nothing whatever "
                 "about any individual. The name field carries a designation because inventing a "
                 "surname would make this record indistinguishable at a glance from the "
                 "documented layer beside it. No figure is drawn (docs/LIBERTIES.md L1). " + why),
    }
    if occ in ("laundress", "domestic"):
        p["sex"] = "female"
        p["note"] += (" SEX IS STATED HERE AND NOWHERE ELSE IN THIS LAYER: the argument for the "
                      "trade is explicitly an argument about women's work, so recording the "
                      "person as male would contradict the reasoning that produced her.")
    return p


ORDINALS = ("zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
            "eighth", "ninth", "tenth", "eleventh", "twelfth")


def ordinal_word(n: int) -> str:
    return ORDINALS[n] if n < len(ORDINALS) else f"{n}th"


def household_record(hh: dict, census: dict, buildings: dict) -> dict:
    occ = hh["occupation"]
    trade = label(occ)
    persons = [person(hh, census)]
    for i, extra in enumerate(hh.get("extras") or [], start=1):
        persons.append(person(hh, census, i, extra))

    def where(sid: str) -> str:
        if sid is None:
            return ""
        if sid.startswith("recon_"):
            return ("an anonymous inferred roof already standing on the plat, adopted rather "
                    "than duplicated: its existence, position and footprint stay conjectural and "
                    "the adoption adds only the occupant argument")
        if sid in buildings:
            return ("a structure record this parcel raises for the purpose, because no roof of "
                    "the right family stood free in this district")
        return "a documented building in this dataset"

    lives = hh.get("lives_at")
    works = hh.get("works_at")
    lives_note = (f"THE HOUSEHOLD IS HOUSED, WHICH IS THE POINT OF THE LAYER. {lives} is "
                  f"{where(lives)}. Which roof of the right family and district a hypothesised "
                  f"household occupies is not evidence about that roof; the household needed a "
                  f"dwelling and the programme assigned it one.") if lives else \
        "No dwelling is claimed for this household."
    if works == lives and works:
        works_note = (f"THE SAME BUILDING. {works} is a shop or house that this layer reads as "
                      f"both workplace and dwelling - the schedule's store-residence and "
                      f"boarding-house families are exactly that, and a frontier tradesman "
                      f"living over his own premises is the type rather than the exception.")
    elif works:
        works_note = (f"{works} is {where(works)}. The workplace is assigned from the "
                      f"reconstruction schedule's workshop and store families for this trade.")
    else:
        works_note = (f"NO SEPARATE WORKPLACE. A {trade} in this town worked in other people's "
                      f"buildings, in the street, or in the dwelling itself, and inventing a "
                      f"shop for the sake of a link would be inventing a building.")

    return {
        "id": hh["id"],
        "name": f"An inferred {trade}'s household ({hh['division']} division)",
        "division": hh["division"],
        "head": persons[0]["id"],
        "arrival": arrival_block(),
        "party_size_on_arrival": null_block(
            "Not claimed. The layer infers households, not families: the person entries here are "
            "the ones the trade argument requires and nothing counts wives or children, because "
            "counting them would multiply a hypothesis by an invention."),
        "origin": null_block(
            "Not claimed. Where a hypothesised resident came from is unknowable by construction, "
            "and the documented layer's origins (Vermont, Washington, Ann Arbor) are evidence "
            "about those men and not a distribution to sample from."),
        "reason_for_coming": null_block(
            "Not claimed for the person. The reason the HOUSEHOLD is in the dataset is the trade "
            "argument in research_note, which is a statement about the town and not about a "
            "motive."),
        "lives_at": link_block(lives, lives_note),
        "works_at": link_block(works, works_note),
        "present_on_scene_date": {
            "value": "present",
            "confidence": "inferred",
            "note": ("Presence on the scene date IS the hypothesis: this household exists in the "
                     "dataset because the town of 1 July 1835 demonstrably needed households of "
                     "this trade. It is not a finding about anybody's whereabouts."),
        },
        "persons": persons,
        "touches_removal": False,
        "review_required": False,
        "research_note": (
            f"INFERRED HOUSEHOLD - {ordinal_word(hh['ordinal'])} of {hh['of']} {trade} households "
            f"in this layer, in the {hh['division']} division. " + census[occ]["argument"] +
            " METHOD: the count comes from the occupation census in "
            "data/reconstruction/1835_inferred_household_programme.json, which calibrates every "
            "trade against three things this project already holds - the 1835 town census "
            "(3,265 people, 398 dwellings), Andreas's roster of the fall of 1833 (about fifty "
            "named people, most with a trade, in a settlement of some 350), and the "
            "reconstruction specification's roof schedule, whose workshop and store family "
            "targets are treated as the ceiling on a trade rather than as its measure. Every "
            "count is stated NET of the documented layer: this dataset infers a tradesman only "
            "where it cannot name one."),
    }


# --------------------------------------------------------------------------
# buildings
# --------------------------------------------------------------------------
FT = 0.3048


def footprint_origin(ce: float, cn: float, w: float, d: float, bearing: float):
    th = math.radians(bearing)
    cos, sin = math.cos(th), math.sin(th)
    return (ce - w * .5 * cos - d * .5 * sin, cn + w * .5 * sin - d * .5 * cos)


def inferred_form(archetype: str, family: str, spec_note: str, width_m: float = 9.0) -> dict:
    def a(v):
        return {"value": v, "confidence": "inferred", "sources": [SPEC], "note": spec_note}

    if archetype == "log_dwelling":
        return {"stories": a(1), "wall_height_m": a(2.5), "roof_type": a("gable"),
                "roof_pitch_deg": a(35.0), "construction": a("log"), "loft": a(True),
                "chimneys": a(1)}
    if archetype == "frame_dwelling":
        two = family in ("D7", "H2", "H3")
        return {"stories": a(2 if two else 1), "wall_height_m": a(5.05 if two else 2.78),
                "roof_type": a("gable"), "roof_pitch_deg": a(38.0),
                "construction": a("braced_frame"),
                "plan": a("centre_passage" if two else ("single_pen" if family == "D3"
                                                        else "hall_parlour")),
                "bays": a(5 if two else 3), "chimneys": a(1), "paint": a("unpainted")}
    if archetype == "frame_storefront":
        # A glazed shopfront needs 3.25 m of bay plus a return at each end. Below about
        # 6 m of frontage the archetype cannot build one and neither could a carpenter:
        # a shop that narrow had a door and a window, which is what the record then says.
        wide = width_m >= 6.0
        narrow_note = (spec_note + " THE SHOPFRONT IS OFF because this frontage cannot carry "
                       "one: the archetype's glazed front needs 3.25 m of bay plus a return at "
                       "each end, and a shop of this width had a door and a window instead.")
        return {"stories": a(1), "wall_height_m": a(3.25), "roof_type": a("gable"),
                "roof_pitch_deg": a(33.0), "gable_front": a(True),
                "construction": a("braced_frame"), "cladding": a("clapboard"),
                "paint": a("unpainted"), "loft": a(family in ("C2", "C3")), "chimneys": a(1),
                "shopfront": ({"value": False, "confidence": "inferred", "sources": [SPEC],
                               "note": narrow_note} if not wide else a(True)),
                "goods_door": a(wide), "goods_door_side": a("end")}
    door = "wagon" if family in ("W1", "W2", "W3", "W5", "F1", "A2") else (
        "stable" if family == "A1" else "man")
    roof = "shed" if family in ("D2", "A3", "A4", "A5") else "gable"
    wall = 3.42 if door == "wagon" else (2.75 if door == "stable" else 2.05)
    return {"wall_height_m": a(wall), "roof_type": a(roof),
            "roof_pitch_deg": a(18.0 if roof == "shed" else 32.0),
            "construction": a("plank" if family.startswith("D") else "light_frame"),
            "door": a(door), "door_side": a("front"),
            "loft": a(family in ("W2", "W5", "A1", "A2")),
            "board_gap_m": a(0.012), "paint": a("unpainted")}


def attested(value, confidence, sources, note) -> dict:
    block = {"value": value, "confidence": confidence}
    if sources:
        block["sources"] = list(sources)
    block["note"] = note
    return block


def structure_record(b: dict, datum: dict, prose: dict, hh_by_building: dict) -> dict:
    bid = b["id"]
    ce, cn = b["center_local_enu_m"]
    wft, dft = b["footprint_ft"]
    w, d = round(wft * FT, 3), round(dft * FT, 3)
    e0, n0 = footprint_origin(ce, cn, w, d, float(b["rotation_deg"]))
    documented = b["kind"] == "documented"
    p = prose.get(bid, {})
    occupants_hh = hh_by_building.get(bid, [])

    if documented:
        exist_conf, exist_src, exist_note = p["existence"]
        pos_conf, pos_src, pos_note = p["position"]
        foot_note = p["footprint"]
        func_conf, func_src, func_note = "documented", [ANDREAS], p["research"]
        name = p["name"]
        function_value = p["function"]
        occ_conf, occ_src, occ_note = p["occupants"]
        research = p["research"]
        form_over = p.get("form") or {}
        phase_id = "documented_1835"
        change = ("The building as this dataset can state it on the scene date. Where the "
                  "sources give a size, a plan or a fabric, the record carries it; where they do "
                  "not, the note says so attribute by attribute.")
    else:
        role = b["role"]
        role_lc = role[0].lower() + role[1:]
        trade = label(b["occupation"])
        name = "Inferred " + b["function"].replace("_", " ") + " (" + trade + ")"
        function_value = b["function"]
        exist_conf, exist_src = "conjectural", None
        exist_note = ("NO EVIDENCE ESTABLISHES THAT THIS PARTICULAR BUILDING EXISTED. It is the "
                      "roof an inferred household requires - " + role_lc + " The argument for the "
                      "trade's presence in the town is in the household record and in the "
                      "occupation census at "
                      "data/reconstruction/1835_inferred_household_programme.json; the argument "
                      "for THIS BUILDING is only that the household needs somewhere to be.")
        pos_conf, pos_src = "conjectural", None
        pos_note = ("INTERPRETIVE PLACEMENT, NOT A RECOVERED LOT. " + role + " The band follows "
                    "ROADMAP K1's placement rule - businesses toward the river and the built "
                    "streets, residences further out - using the same frontage bands the "
                    "reconstruction recipes already work in, which come from the 80 ft platted "
                    "street module in data/traces/street_control.json. The centre was tested "
                    "against every structure footprint in the dataset, against the reserved "
                    "slots of the two uninstantiated phase-2 recipes, and against the committed "
                    "heightfield for coverage, dry ground and step tolerance; it is free ground "
                    "and nothing more. The dataset's 20 m working georeference uncertainty "
                    "applies on top of an already invented position.")
        foot_note = (f"A {wft:g} x {dft:g} ft rectangle from the {b['family']} family band in the "
                     f"reconstruction specification. NO DIMENSION IS DOCUMENTED for this "
                     f"building, which does not exist in any source; the band is type-level "
                     f"evidence about what buildings of this class measured and is not evidence "
                     f"about this one.")
        func_conf, func_src, func_note = "inferred", [ANDREAS, SPEC], role
        occ_conf, occ_src = "inferred", [ANDREAS, SPEC]
        occ_note = ("The inferred household this building exists for: "
                    + ", ".join(occupants_hh) + " in data/residents/households/. No name is "
                    "claimed and no figure is drawn.")
        research = ("INFERRED BUILDING, RAISED FOR AN INFERRED HOUSEHOLD (docs/ROADMAP.md K1, "
                    "phase two). " + role + " It is NOT one of the anonymous count-units of the "
                    "665-roof programme: those are placed by aggregate mix and carry no occupant, "
                    "while this one exists because the occupation census says the town held a "
                    "household of this trade and no anonymous roof of the right family stood free "
                    "in this district. It consumes one slot of its district's programme target "
                    "rather than adding to it - see the accounting block in "
                    "data/reconstruction/1835_inferred_household_programme.json.")
        form_over = {}
        phase_id = "inferred_1835"
        change = ("Raised by the inferred-household programme. A better-evidenced named building "
                  "substitutes for this roof rather than standing beside it.")

    spec_note = (f"Type-level choice within the {b['family']} band in the reconstruction "
                 f"specification; it is not evidence for this building.")
    form = inferred_form(b["archetype"], b["family"], spec_note, w)
    for key, value in (form_over or {}).items():
        form[key] = attested(value, "inferred", [ANDREAS] if documented else [SPEC],
                             p.get("form_note") or spec_note)

    phase = {
        "id": phase_id,
        "documented_range": {
            "from": p.get("from", "1835-01-01") if documented else "1835-01-01",
            "to": "1835-12-31",
            "confidence": exist_conf,
            **({"sources": list(exist_src)} if exist_src else {}),
            "note": exist_note,
        },
        "position": {
            "utm_e": round(float(datum["origin_utm_e"]) + e0, 3),
            "utm_n": round(float(datum["origin_utm_n"]) + n0, 3),
            "rotation_deg": float(b["rotation_deg"]),
            "symbolic_location": b.get("symbolic_location") or p.get("symbolic_location")
            or f"{b['district'].capitalize()} Division, local ENU E {ce:g} N {cn:g}",
            "confidence": pos_conf,
            **({"sources": list(pos_src)} if pos_src else {}),
            "note": pos_note,
            "derivation": {
                "method": "not_derivable",
                "reason": ("No source gives this building a lot. The placement is a frontage-band "
                           "assignment tested for clearance and buildable ground, which is a "
                           "production control and not a derivation from any line in the "
                           "dataset."),
            },
        },
        "footprint": {
            "polygon": [[0, 0], [w, 0], [w, d], [0, d]],
            "confidence": "conjectural",
            "note": foot_note,
        },
        "form": form,
        "change_note": change,
    }
    if p.get("ground_contact"):
        state, note = p["ground_contact"]
        phase["ground_contact"] = {"state": state, "note": note}

    record = {
        "id": bid,
        "name": name,
        "archetype": b["archetype"],
        "phases": [phase],
        "function": attested(function_value, func_conf, func_src, func_note),
        "occupants": attested(
            p["occupants_value"] if documented else "An inferred household; no name is claimed",
            occ_conf, occ_src, occ_note),
        "research_note": research,
        "review_required": False,
    }
    return record


# --------------------------------------------------------------------------
# geometry gates
# --------------------------------------------------------------------------

def world_polygon(pos: dict, poly: list, origin: tuple) -> list:
    th = math.radians(float(pos.get("rotation_deg") or 0))
    cos, sin = math.cos(th), math.sin(th)
    e0 = float(pos["utm_e"]) - origin[0]
    n0 = float(pos["utm_n"]) - origin[1]
    return [(e0 + u * cos + v * sin, n0 - u * sin + v * cos) for u, v in poly]


def rect_polygon(ce, cn, wft, dft, bearing) -> list:
    w, d = wft * FT, dft * FT
    th = math.radians(bearing)
    cos, sin = math.cos(th), math.sin(th)
    return [(ce + u * cos + v * sin, cn - u * sin + v * cos)
            for u, v in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]


def overlaps(a: list, b: list, pad: float = 0.0) -> bool:
    """Convex SAT with a separation pad; touching or near-touching counts as a hit."""
    for poly in (a, b):
        for i, p in enumerate(poly):
            q = poly[(i + 1) % len(poly)]
            ax, ay = -(q[1] - p[1]), q[0] - p[0]
            length = math.hypot(ax, ay) or 1.0
            ax, ay = ax / length, ay / length
            pa = [x * ax + y * ay for x, y in a]
            pb = [x * ax + y * ay for x, y in b]
            if max(pa) <= min(pb) + pad or max(pb) <= min(pa) + pad:
                return False
    return True


def reserved_slots() -> list[tuple[str, list]]:
    out = []
    west = load(RESERVED[0])
    for slot in west.get("placements", []):
        ce, cn = slot["center_local_enu_m"]
        wft, dft = slot["footprint_ft"]
        out.append((f"west recipe {slot['id']}", rect_polygon(ce, cn, wft, dft,
                                                              slot.get("rotation_deg", 0))))
    south = load(RESERVED[1])
    for cluster in south.get("clusters", []):
        for slot in cluster.get("placements", []):
            sid, e, n, _fam, wft, dft, bearing, _cls = slot
            out.append((f"south phase-2 recipe {sid}", rect_polygon(e, n, wft, dft, bearing)))
    return out


def validate(records: list[dict], households: list[dict], programme: dict, datum: dict) -> None:
    origin = (float(datum["origin_utm_e"]), float(datum["origin_utm_n"]))

    # every form must resolve through an implemented archetype
    for record in records:
        module = importlib.import_module(f"archetypes.{record['archetype']}_params")
        module.from_phase(record["phases"][0])

    # nothing may be stacked on anything: existing records, reserved slots, each other
    mine = [(r["id"], world_polygon(r["phases"][0]["position"],
                                    r["phases"][0]["footprint"]["polygon"], origin))
            for r in records]
    new_ids = {r["id"] for r in records}
    existing = []
    for path in sorted(STRUCTURES.glob("*.json")):
        doc = load(path)
        if doc.get("id") in new_ids:
            continue
        for phase in doc.get("phases", []):
            pos = phase.get("position") or {}
            poly = (phase.get("footprint") or {}).get("polygon")
            if pos.get("utm_e") is None or not poly:
                continue
            existing.append((doc["id"], world_polygon(pos, poly, origin)))
    for name, poly in existing + reserved_slots():
        for sid, other in mine:
            if overlaps(poly, other, -3.0):
                raise SystemExit(f"{sid} is within 3 m of {name}")
    for i, (sid, poly) in enumerate(mine):
        for other_sid, other in mine[:i]:
            if overlaps(poly, other, -3.0):
                raise SystemExit(f"{sid} is within 3 m of {other_sid}")

    # buildable ground, on the same committed surface the walker uses
    from heightfield import Heightfield  # noqa: PLC0415
    field = Heightfield.load(DATA / "terrain" / "epochs" / "e1834_harbor_cut")
    if field is None:
        raise SystemExit("cannot validate placements: the committed heightfield is missing")
    declared = {r["id"] for r in records if r["phases"][0].get("ground_contact")}
    for sid, poly in mine:
        pts = []
        for i, a in enumerate(poly):
            b = poly[(i + 1) % len(poly)]
            steps = max(2, int(math.dist(a, b)))
            pts += [(a[0] + (b[0] - a[0]) * k / steps, a[1] + (b[1] - a[1]) * k / steps)
                    for k in range(steps)]
        covered = all(field.covers(e, n) for e, n in pts)
        if sid in declared:
            if covered:
                raise SystemExit(f"{sid} declares ground_contact and stands on modelled ground")
            continue
        if not covered:
            raise SystemExit(f"{sid} falls outside the modelled terrain and declares nothing")
        heights = [field.height(e, n) for e, n in pts]
        if min(heights) < -.10:
            raise SystemExit(f"{sid} stands on the water side of the terrain")
        if max(heights) - min(heights) > .30:
            raise SystemExit(f"{sid} spans {max(heights) - min(heights):.2f} m of relief")

    # the census and the households have to agree, in both directions
    census = {c["occupation"]: c for c in programme["occupation_census"]}
    counted: dict[str, int] = {}
    for h in households:
        counted[h["occupation"]] = counted.get(h["occupation"], 0) + 1
    for occ, c in census.items():
        if counted.get(occ, 0) != c["inferred_households"]:
            raise SystemExit(f"census says {c['inferred_households']} {occ} household(s), "
                             f"the recipe deals {counted.get(occ, 0)}")
    for occ in counted:
        if occ not in census:
            raise SystemExit(f"household trade '{occ}' has no entry in the occupation census")

    # one roof, one household living in it; and no household is homeless. A WORKPLACE
    # MAY BE SHARED - a sawpit is worked by two men by definition, and a shop with a
    # journeyman in it is the reason the journeyman is in the record - so only the
    # dwelling link is exclusive.
    homes: dict[str, str] = {}
    for h in households:
        sid = h.get("lives_at")
        if not sid:
            raise SystemExit(f"{h['id']} has no dwelling; the layer exists to house households")
        if sid in homes:
            raise SystemExit(f"{sid} is the dwelling of both {homes[sid]} and {h['id']}")
        homes[sid] = h["id"]

    # the 665-roof programme is a ceiling, not a budget to overspend
    inventory = load(INVENTORY)
    by_district: dict[str, int] = {}
    for path in sorted(STRUCTURES.glob("recon_*.json")):
        doc = load(path)
        by_district[doc["reconstruction"]["district"]] = \
            by_district.get(doc["reconstruction"]["district"], 0) + 1
    for b in programme["buildings"]:
        by_district[b["district"]] = by_district.get(b["district"], 0) + 1
    for district, count in sorted(by_district.items()):
        target = inventory["districts"][district]["target"]
        if count > target:
            raise SystemExit(f"{district}: {count} inferred roofs against a programme target of "
                             f"{target}")


# --------------------------------------------------------------------------
# expansion
# --------------------------------------------------------------------------

def build_all() -> tuple[dict[Path, str], list[dict], list[dict]]:
    programme = load(PROGRAMME)
    datum = load(DATA / "datum.json")
    census = {c["occupation"]: c for c in programme["occupation_census"]}
    buildings = {b["id"]: b for b in programme["buildings"]}
    prose = programme["building_prose"]

    hh_by_building: dict[str, list[str]] = {}
    for h in programme["households"]:
        for key in ("lives_at", "works_at"):
            sid = h.get(key)
            if sid in buildings:
                hh_by_building.setdefault(sid, [])
                if h["id"] not in hh_by_building[sid]:
                    hh_by_building[sid].append(h["id"])
    for link in programme["documented_household_links"]:
        for key in ("lives_at", "works_at"):
            sid = link.get(key)
            if sid in buildings:
                hh_by_building.setdefault(sid, [])
                if link["household"] not in hh_by_building[sid]:
                    hh_by_building[sid].append(link["household"])

    records = [structure_record(b, datum, prose, hh_by_building)
               for b in programme["buildings"]]
    households = [household_record(h, census, buildings) for h in programme["households"]]
    validate(records, programme["households"], programme, datum)

    files: dict[Path, str] = {}
    for record in records:
        files[STRUCTURES / f"{record['id']}.json"] = dumps(record, 2)
    for h in households:
        files[HOUSEHOLDS / f"{h['id']}.json"] = dumps(h, 1)

    # the documented households whose buildings this parcel finally builds
    documented_updates = []
    for link in programme["documented_household_links"]:
        path = HOUSEHOLDS / f"{link['household']}.json"
        doc = load(path)
        for key in ("lives_at", "works_at"):
            if link.get(key):
                doc[key] = {
                    "value": link[key],
                    "confidence": "documented",
                    "sources": [ANDREAS],
                    "note": link["note"] + " Linked by the inferred-household programme's "
                                           "building parcel (docs/ROADMAP.md K1, phase two); the "
                                           "building record carries the evidence.",
                }
        files[path] = dumps(doc, 1)
        documented_updates.append(doc)

    # the manifest
    index = load(INDEX)
    vocab = index["vocabulary"]
    if "labourer" not in vocab["occupations"]:
        vocab["occupations"] = sorted(set(vocab["occupations"]) | {"labourer"})
    keep = [e for e in index["households"] if not e["id"].startswith(PREFIX)]
    by_id = {d["id"]: d for d in households + documented_updates}
    for entry in keep:
        doc = by_id.get(entry["id"])
        if doc:
            entry["lives_at"] = (doc["lives_at"] or {}).get("value")
            entry["works_at"] = (doc["works_at"] or {}).get("value")
    rows = keep + [{
        "id": h["id"],
        "file": f"households/{h['id']}.json",
        "head": h["head"],
        "division": h["division"],
        "persons": len(h["persons"]),
        "grades": {"inferred": len(h["persons"])},
        "lives_at": (h["lives_at"] or {}).get("value"),
        "works_at": (h["works_at"] or {}).get("value"),
        "present_on_scene_date": h["present_on_scene_date"]["value"],
        "review_required": h["review_required"],
    } for h in households]
    rows.sort(key=lambda e: e["id"])
    index["households"] = rows

    totals = {"documented": 0, "derived": 0, "inferred": 0}
    for entry in rows:
        for grade, n in entry["grades"].items():
            totals[grade] = totals.get(grade, 0) + n
    index["counts"] = {"households": len(rows),
                       "persons": sum(e["persons"] for e in rows),
                       "by_grade": totals}
    files[INDEX] = dumps(index, 1)
    return files, records, households


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="report missing, changed, or extra outputs")
    args = parser.parse_args()
    files, records, households = build_all()

    drift = []
    for path, text in sorted(files.items()):
        if args.check:
            if not path.exists():
                drift.append(f"{path.relative_to(ROOT)} is missing")
            elif path.read_text(encoding="utf-8") != text:
                drift.append(f"{path.relative_to(ROOT)} has drifted from the household programme")
        else:
            path.write_text(text, encoding="utf-8")

    expected = {p.name for p in files}
    extras = sorted(p.name for p in HOUSEHOLDS.glob(f"{PREFIX}*.json") if p.name not in expected)
    drift.extend(f"data/residents/households/{name} is outside the household programme"
                 for name in extras)
    if drift:
        print("INFERRED HOUSEHOLD PROGRAMME DRIFT")
        for item in drift:
            print(f"  - {item}")
        return 1
    mode = "verified" if args.check else "generated"
    persons = sum(len(h["persons"]) for h in households)
    adopted = len({sid for h in load(PROGRAMME)["households"]
                   for sid in (h.get("lives_at"), h.get("works_at"))
                   if sid and sid.startswith("recon_")})
    print(f"{mode} {len(households)} inferred households ({persons} persons), "
          f"{len(records)} structure records, {adopted} anonymous roofs adopted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
