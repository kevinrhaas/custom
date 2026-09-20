#!/usr/bin/env python3
"""THE 1835 RECONSTRUCTION ORDER BOOK: known minus model, resolved into work.

T-1166, which closes the 1835 TOWN ANALYSIS band. Every model above states a
TARGET (T-1293, folding T-1161..T-1165); the profile states what is KNOWN
(T-1160); the roster states which REAL NAMES are still on offer (T-1159). The
order book is the subtraction — and, because a subtraction nobody can spend is
just another number, it is the subtraction resolved into buckets, each with the
ticket that owns filling it and a counter that ticket writes back.

    tools/build_order_book_1835.py --build       write the book and its report
    tools/build_order_book_1835.py --check       re-derive both and refuse drift
    tools/build_order_book_1835.py --self-test   the guards, fired on fixtures

WHAT THIS TOOL IS.  An ADJUDICATION over files this repository already holds and
already gates, exactly as the town model is. It reads no page of any source,
opens no network, names nobody, ages nobody, houses nobody, and creates no
person, household, business or building. Every quantity it prints is a function
of a committed derived file, and the file is named beside the quantity.

WHAT A BUCKET IS.  A cell of the town, keyed by the axes the models bound:
persons by sex x age band x division x household type x trade, households by
type x division, businesses by class, structures by archetype group x division.
Each carries `target` (the model), `known_attested` / `known_inferred` (the
layer), `to_reconstruct` (the difference), the `owning_ticket` that must fill
it, and `filled` — the counter a filler increments through its own `--build`.

THE FOUR RULES THIS BOOK ADDS, AND WHY EACH IS STATED RATHER THAN HIDDEN.

1. A POINT FROM A RANGE.  The town model answers in ranges on purpose, and a
   quota cannot be a range: a filler asked for "between 469 and 816 households"
   builds nothing. Where the model gives a `point` the book takes it; where it
   gives only `low` and `high` the book takes the MIDPOINT, rounds half up, and
   carries the range beside it so the reader can see the width of what was
   collapsed. The midpoint is a planning figure and never a claim about 1835.

2. THE UNRESOLVED KNOWN.  A named person the layer cannot place in a cell is
   still a person standing in the town, and a book that ignored them would order
   their replacement a second time. So the known who cannot be resolved onto an
   axis are subtracted PRO RATA across the cells of that axis, which is the only
   distribution that keeps the totals honest without asserting where anybody was.

3. PRESENCE IS THE TEST FOR "KNOWN".  A household record whose presence on
   1 July 1835 is `uncertain` is not a household this town holds; it is a
   candidate T-1172 may re-admit, and it is already counted on the roster as
   class R1. Counting it as known AND offering it on the roster would order one
   person twice, so only `present` records count as known here.

4. THE FORT IS NOT APPORTIONED.  The garrison of 1 July 1835 is a return to be
   read (T-1176), not a share of a town model, so the fort division's person and
   household targets are `null` and its bucket says which ticket bounds them.
   Whatever T-1176 returns is subtracted from the civilian quota at the next
   `--build`, which is why that ticket is named in the bucket rather than guessed at.

THE COUNTERS ARE CARRIED, NOT RE-DERIVED.  `filled` and the `fills` ledger are
written by the reconstruction tools, not by this one, so `--check` re-derives
every bucket from the inputs, carries the committed counters across unchanged,
and then REFUSES an overfilled bucket or a fill naming no ticket. That is what
makes the book a quota rather than a report: a filler that bypasses it is red.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "data" / "reconstruction" / "1835_reconstruction_order_book.json"
REPORT = ROOT / "docs" / "RESEARCH" / "1835_reconstruction_order_book.md"

MODEL = ROOT / "data" / "reconstruction" / "1835_town_model.json"
PROFILE = ROOT / "data" / "reconstruction" / "1835_population_profile.json"
ROSTER = ROOT / "data" / "reconstruction" / "1835_borderline_roster.json"
PROGRAMME = ROOT / "data" / "reconstruction" / "1835_665_roof_programme.json"
INVENTORY = ROOT / "data" / "reconstruction" / "1835_building_inventory.json"
CROSSWALK = ROOT / "data" / "research" / "books" / "trade_census_1835_crosswalk.json"
COMPOSITION = ROOT / "data" / "research" / "census_1840" / "composition_1840.json"
RESIDENTS = ROOT / "data" / "residents" / "index.json"
REGISTER = ROOT / "data" / "research" / "newspapers" / "register_1835.json"

SCENE_DATE = "1835-07-01"

# The divisions the town model and the building programme both speak in. `fort`
# is carried but never apportioned — see rule 4 in the docstring.
CIVIL_DIVISIONS = ("south", "west", "north")
DIVISIONS = CIVIL_DIVISIONS + ("fort",)

# The age bands the book orders in. The 1840 schedule prints thirteen bands a sex
# and the extract uses ten; these six are those ten folded at the edges the
# reconstruction tickets actually act on — a child, a youth, and four adult
# decades, the last open. `low` is inclusive, `high` exclusive, `None` open.
AGE_BANDS = (
    ("under_10", 0, 10, "a child: the age pyramid's floor and the schedule's first two columns"),
    ("10_19", 10, 20, "a youth: at school, apprenticed, or at work in the household"),
    ("20_29", 20, 30, "the port's largest cohort by a wide margin"),
    ("30_39", 30, 40, "the second cohort: most heads of household sit here"),
    ("40_49", 40, 50, "established heads"),
    ("50_plus", 50, None, "the oldest cohort the schedule counts in any number"),
)
ADULT_FROM = 20

# The household types a person can be seated in. `transient` is the summer of
# 1835's own cohort and the model does not bound it: T-1178 does.
HOUSEHOLD_TYPES = (
    ("family", "a household of kin — a head, a spouse where there was one, children, servants and apprentices"),
    ("lodging", "a bed in a boarding house, an inn, a hotel, aboard a vessel or over a shop"),
    ("garrison", "the fort establishment: the companies, the staff and the soldiers' families"),
    ("transient", "in the town on 1 July 1835 and not of it: the land-sale crowd, the immigrants waiting for lots, the works gang"),
)

# Which ticket fills a person bucket. Read top-down; the first rule that matches
# owns the cell. Written here rather than in prose so the book can be audited
# against the queue.
PERSON_TICKET_RULES = (
    ("fort division", lambda a: a["division"] == "fort", "T-1176"),
    ("the transient cohort", lambda a: a["household_type"] == "transient", "T-1178"),
    ("a bed rather than a household", lambda a: a["household_type"] == "lodging", "T-1175"),
    # T-1347 repointed this off its split parent. T-1173 was the epic; it split into
    # T-1346 (read the 1839 trade table) and T-1347 (draw the heads), and a bucket whose
    # owning ticket is a SPLIT parent names nobody who can act on it (T-1237).
    ("an adult at a trade", lambda a: a["trade"] == "trade", "T-1347"),
    ("a woman or a person under twenty", lambda a: a["sex"] == "female" or a["age_band"] in ("under_10", "10_19"), "T-1174"),
    ("otherwise: a family drawn from the household model", lambda a: True, "T-1171"),
)

# The roster's classes, and the ticket each class is offered to. A roster class is
# a LICENCE to use a real read name; it is not a quota, and it is reported against
# its ticket rather than smeared across cells that cannot hold it.
ROSTER_TICKETS = {
    "R1_in_window_uncertain": "T-1172",
    "R2_in_window_single_source": "T-1172",
    "R3_1834_return_or_muster": "T-1172",
    "R4_surname_only_census": "T-1170",
    "R5_later_only_backprojectable": "T-1172",
    "R6_native_metis_black": "T-1177",
}

# Household types against the roof groups that hold them, and the ticket that
# reconstructs the household (not the roof — that is the structure band).
HOUSEHOLD_BUCKETS = (
    ("family_dwelling", "ordinary_dwellings", "T-1171"),
    ("store_residence", "stores_mixed_use", "T-1171"),
    ("boarding_house", "larger_boarding_houses", "T-1175"),
    ("inn_tavern", "inns_taverns", "T-1175"),
    ("institutional", "institutional_public", "T-1188"),
    ("garrison", "fort_principal", "T-1176"),
)

# Which build ticket owns a structure group in a division. The queue's 5C band is
# cut by district and street, so this maps the programme's own group x district
# matrix onto the ten build tickets.
STRUCTURE_TICKETS = {
    ("south", "ordinary_dwellings"): "T-1203",
    ("south", "stores_mixed_use"): "T-1201",
    ("south", "larger_boarding_houses"): "T-1209",
    ("south", "inns_taverns"): "T-1201",
    ("south", "workshops"): "T-1201",
    ("south", "warehouses_freight"): "T-1200",
    ("south", "institutional_public"): "T-1202",
    ("south", "barns_stables"): "T-1212",
    ("south", "small_outbuildings"): "T-1212",
    ("west", "ordinary_dwellings"): "T-1208",
    ("west", "stores_mixed_use"): "T-1207",
    ("west", "larger_boarding_houses"): "T-1209",
    ("west", "inns_taverns"): "T-1207",
    ("west", "workshops"): "T-1207",
    ("west", "warehouses_freight"): "T-1207",
    ("west", "institutional_public"): "T-1208",
    ("west", "barns_stables"): "T-1212",
    ("west", "small_outbuildings"): "T-1212",
    ("north", "ordinary_dwellings"): "T-1206",
    ("north", "stores_mixed_use"): "T-1205",
    ("north", "larger_boarding_houses"): "T-1209",
    ("north", "inns_taverns"): "T-1205",
    ("north", "workshops"): "T-1205",
    ("north", "warehouses_freight"): "T-1205",
    ("north", "institutional_public"): "T-1205",
    ("north", "barns_stables"): "T-1212",
    ("north", "small_outbuildings"): "T-1212",
    ("fort", "fort_principal"): "T-1204",
    ("fort", "stores_mixed_use"): "T-1204",
    ("fort", "workshops"): "T-1204",
    ("fort", "barns_stables"): "T-1204",
    ("fort", "small_outbuildings"): "T-1204",
}

# Which business ticket owns a December 1835 trade-census class.
BUSINESS_TICKETS = {
    "store": "T-1184",
    "book_store": "T-1184",
    "druggist": "T-1184",
    "silversmith_jeweller": "T-1185",
    "tin_and_copper_manufactory": "T-1185",
    "printing_office": "T-1188",
    "brewery": "T-1185",
    "steam_saw_mill": "T-1187",
    "iron_foundry": "T-1185",
    "storage_and_forwarding": "T-1187",
    "tavern": "T-1187",
    "lottery_office": "T-1182",
    "bank": "T-1182",
    "church": "T-1188",
    "school": "T-1188",
    # T-1186 was split on 2026-09-20 when the unit ruling below turned out to be a
    # demonstration of its own; T-1418 is the piece that owns these two rows and T-1419
    # the services, which the census enumerates nowhere and which therefore own no bucket.
    "lawyer": "T-1418",
    "physician": "T-1418",
    "lyceum_and_reading_room": "T-1182",
    "other": "T-1182",
    "not_stated": "T-1182",
}

# The ground each division waits on before its structure buckets can be built.
GROUND_TICKETS = {
    "south": ["T-1194"],
    "west": ["T-1192", "T-1193", "T-1194"],
    "north": ["T-1191", "T-1193", "T-1194"],
    "fort": [],
}


class Fault(Exception):
    """A refusal. Never a warning: an order book with a hole in it is not a quota."""


# ---------------------------------------------------------------- arithmetic --

def point_of(fig: dict) -> tuple[int, str]:
    """The quota a figure hands the book, and the sentence that says how."""
    low, high, pt = fig.get("low"), fig.get("high"), fig.get("point")
    if low is None or high is None:
        raise Fault(f"the figure {fig.get('figure')!r} carries no range at all")
    if high < low:
        raise Fault(f"the figure {fig.get('figure')!r} is inverted: {low}..{high}")
    if pt is not None:
        return int(round(pt)), f"the model's own point within {low:,}-{high:,}"
    mid = int((low + high) / 2 + 0.5)
    return mid, f"the midpoint of the model's {low:,}-{high:,}, rounded half up"


def largest_remainder(total: int, weights: dict[str, float]) -> dict[str, int]:
    """Apportion `total` across `weights` so the parts sum to it exactly.

    Deterministic by construction: the remainder order breaks ties on the key,
    so two builds on the same inputs are byte-identical.
    """
    if total < 0:
        raise Fault(f"an apportionment of a negative total: {total}")
    mass = sum(weights.values())
    if mass <= 0:
        raise Fault("an apportionment across weights that sum to zero")
    exact = {k: total * (w / mass) for k, w in weights.items()}
    out = {k: int(v) for k, v in exact.items()}
    short = total - sum(out.values())
    order = sorted(weights, key=lambda k: (-(exact[k] - out[k]), k))
    for k in order[:short]:
        out[k] += 1
    if sum(out.values()) != total:
        raise Fault(f"an apportionment that does not close: {sum(out.values())} of {total}")
    return out


def subtract_pro_rata(targets: dict[str, int], unresolved: int) -> dict[str, int]:
    """Spread `unresolved` known people across cells in proportion to their target.

    Rule 2 of the docstring. A person the layer cannot place is still standing in
    the town; the book must not order a replacement for them.
    """
    if unresolved <= 0:
        return {k: 0 for k in targets}
    live = {k: v for k, v in targets.items() if v > 0}
    if not live:
        raise Fault("the unresolved known have nowhere to go: every target is zero")
    return {**{k: 0 for k in targets}, **largest_remainder(min(unresolved, sum(live.values())), live)}


# --------------------------------------------------------------------- inputs --

def load(root: Path = ROOT) -> dict:
    paths = {
        "model": root / "data" / "reconstruction" / "1835_town_model.json",
        "profile": root / "data" / "reconstruction" / "1835_population_profile.json",
        "roster": root / "data" / "reconstruction" / "1835_borderline_roster.json",
        "programme": root / "data" / "reconstruction" / "1835_665_roof_programme.json",
        "inventory": root / "data" / "reconstruction" / "1835_building_inventory.json",
        "crosswalk": root / "data" / "research" / "books" / "trade_census_1835_crosswalk.json",
        "trade_spend": root / "data" / "research" / "books" / "trade_census_1835_spend.json",
        "composition": root / "data" / "research" / "census_1840" / "composition_1840.json",
        "residents": root / "data" / "residents" / "index.json",
        "register": root / "data" / "research" / "newspapers" / "register_1835.json",
        "presence_rulings": root / "data" / "reconstruction" / "1835_presence_rulings.json",
    }
    out = {}
    for key, path in paths.items():
        if not path.exists():
            raise Fault(f"the order book's input {path.name} is missing — it cannot be built without it")
        out[key] = json.loads(path.read_text(encoding="utf-8"))
    return out


def figure(model: dict, section_key: str, name: str) -> dict:
    for s in model.get("sections", []):
        if s.get("key") != section_key:
            continue
        for f in s.get("figures", []):
            if f.get("figure") == name:
                return f
    raise Fault(f"the town model carries no figure {section_key}.{name}")


# ------------------------------------------------------------ the shape of it --

def sex_shares(model: dict) -> dict[str, float]:
    """Male / female shares from the model's sex ratio, which is the 1840 adult one."""
    ratio = figure(model, "population", "males_per_100_females")
    pt, _ = ratio.get("point"), None
    if pt is None:
        raise Fault("the sex ratio carries no point and the book cannot halve a ratio")
    male = float(pt) / (100.0 + float(pt))
    return {"male": male, "female": 1.0 - male}


def age_shares(composition: dict) -> dict[str, dict[str, float]]:
    """The 1840 free-white pyramid, folded to the book's bands, WITHIN each sex.

    Within-sex rather than overall, because the sex split is the model's (1835's
    adult ratio) and the 1840 overall ratio is a different town four years on.
    """
    rows = composition.get("age_bands", {}).get("free_white", [])
    if not rows:
        raise Fault("the 1840 composition carries no free-white age bands")
    out: dict[str, dict[str, float]] = {"male": {}, "female": {}}
    totals = {"male": 0, "female": 0}
    for sex in ("male", "female"):
        counts = {name: 0 for name, _, _, _ in AGE_BANDS}
        for row in rows:
            if row.get("sex") != sex:
                continue
            edge = int(row["low_edge"])
            for name, low, high, _ in AGE_BANDS:
                if edge >= low and (high is None or edge < high):
                    counts[name] += int(row["persons"])
                    break
            else:
                raise Fault(f"the 1840 band at age {edge} falls in none of the book's bands")
        total = sum(counts.values())
        if total <= 0:
            raise Fault(f"the 1840 pyramid counts no {sex}s at all")
        totals[sex] = total
        out[sex] = {k: v / total for k, v in counts.items()}
    return out


def division_shares(inventory: dict) -> dict[str, float]:
    """Where the civilian town was, taken from the roof programme's own district targets."""
    districts = inventory.get("districts", {})
    weights = {}
    for d in CIVIL_DIVISIONS:
        target = districts.get(d, {}).get("target")
        if not target:
            raise Fault(f"the building inventory sets no roof target for the {d} division")
        weights[d] = float(target)
    mass = sum(weights.values())
    return {k: v / mass for k, v in weights.items()}


def known_layer(residents: dict) -> dict:
    """The known people and households, read off the committed resident index.

    Rule 3: only a household whose presence on the scene date is `present` counts
    as known. The `uncertain` ones are the roster's R1 class and are offered, not
    counted — counting them in both places would order one person twice.

    AND A RECONSTRUCTED PERSON IS NOT KNOWN. `known` is what the SOURCES give the town;
    a reconstructed person is the order being filled, and `filled` is their counter.
    Counting them here as well would retire their own quota a second time — a bucket
    that drew its last person would read `filled: n` against `to_reconstruct: 0` and the
    overfill gate would fire on a stage that obeyed it exactly. T-1171 was the first
    stage to write a person and the first to meet this; it read zero before that.
    """
    households = residents.get("households", [])
    if not households:
        raise Fault("the resident index carries no households")
    out = {
        "households_total": len(households),
        "households_present": 0,
        "households_uncertain": 0,
        "households_reconstructed": 0,
        "persons_total": 0,
        "persons_present": 0,
        "persons_present_attested": 0,
        "persons_present_inferred": 0,
        "persons_present_by_division": {d: 0 for d in DIVISIONS},
        "households_present_by_division": {d: 0 for d in DIVISIONS},
        "persons_present_unplaced": 0,
        "households_present_unplaced": 0,
        "households_with_a_lives_at": 0,
        "households_with_a_works_at": 0,
    }
    for hh in households:
        persons = int(hh.get("persons") or 0)
        out["persons_total"] += persons
        presence = hh.get("present_on_scene_date")
        if presence == "uncertain":
            out["households_uncertain"] += 1
            continue
        if presence != "present":
            continue
        grades = hh.get("grades") or {}
        named = persons - int(grades.get("reconstructed") or 0)
        # AND A RECONSTRUCTED HOUSEHOLD IS NOT KNOWN EITHER (T-1174). The paragraph above
        # says why for a person; a household nobody is named in is the same thing one level
        # up. `women_and_children` is the first stage to write a household rather than to
        # draw into one, and while these counted as known its own quota fell by one for
        # every house it made — so the second build of the same stage derived 65 houses
        # where the first derived 124, and `--check` could never have held it. A wholly
        # reconstructed house is the order being filled; `filled` is its counter.
        if persons and named == 0:
            out["households_reconstructed"] += 1
            continue
        out["households_present"] += 1
        out["persons_present"] += named
        out["persons_present_attested"] += int(grades.get("attested") or 0)
        out["persons_present_inferred"] += int(grades.get("inferred") or 0)
        division = hh.get("division")
        if division in out["persons_present_by_division"]:
            out["persons_present_by_division"][division] += named
            out["households_present_by_division"][division] += 1
        else:
            out["persons_present_unplaced"] += named
            out["households_present_unplaced"] += 1
        if hh.get("lives_at"):
            out["households_with_a_lives_at"] += 1
        if hh.get("works_at"):
            out["households_with_a_works_at"] += 1
    return out


# -------------------------------------------------------------------- buckets --

def person_buckets(model: dict, composition: dict, inventory: dict, known: dict) -> dict:
    pop_fig = figure(model, "population", "population_on_1_july_1835")
    town, town_basis = point_of(pop_fig)
    lodging_fig = figure(model, "lodging_and_institutions", "share_of_the_town_in_lodging")
    lodging_low, lodging_high = float(lodging_fig["low"]), float(lodging_fig["high"])
    lodging_share = (lodging_low + lodging_high) / 2.0
    employed_fig = figure(model, "occupations", "employed_persons")
    employed, employed_basis = point_of(employed_fig)

    sexes = sex_shares(model)
    ages = age_shares(composition)
    divisions = division_shares(inventory)

    # The civilian town, apportioned. Targets first, on the model's own marginals:
    # sex x age within sex x division x household type. The fort is not in here
    # (rule 4) and neither is the transient cohort (T-1178 bounds it).
    weights: dict[str, float] = {}
    axes: dict[str, dict] = {}
    for sex, sex_share in sexes.items():
        for band, _, _, _ in AGE_BANDS:
            for division, div_share in divisions.items():
                for htype in ("family", "lodging"):
                    share = sex_share * ages[sex][band] * div_share
                    share *= lodging_share if htype == "lodging" else (1.0 - lodging_share)
                    key = f"{sex}/{band}/{division}/{htype}"
                    weights[key] = share
                    axes[key] = {"sex": sex, "age_band": band, "division": division,
                                 "household_type": htype, "trade": "none"}
    targets = largest_remainder(town, weights)

    # Then the employed, drawn out of the adult cells only. A trade is a column of
    # the 1840 schedule that counts persons in families and cannot be split by sex,
    # so the book splits it by nothing but the population already in each cell.
    adult = {k: targets[k] for k in targets
             if next(b for b in AGE_BANDS if b[0] == axes[k]["age_band"])[1] >= ADULT_FROM}
    if sum(adult.values()) < employed:
        raise Fault(f"the model wants {employed:,} employed persons and the town model's own "
                    f"adults number {sum(adult.values()):,}")
    employed_by_cell = largest_remainder(employed, {k: float(v) for k, v in adult.items() if v > 0})

    # The known, subtracted. What the layer resolves onto a division is subtracted
    # there; what it cannot is spread pro rata (rule 2).
    resolved = {d: known["persons_present_by_division"][d] for d in CIVIL_DIVISIONS}
    unresolved = known["persons_present_unplaced"]
    known_by_cell = {k: 0 for k in targets}
    for division in CIVIL_DIVISIONS:
        cells = {k: float(targets[k]) for k in targets if axes[k]["division"] == division}
        for k, v in subtract_pro_rata({k: targets[k] for k in cells}, resolved[division]).items():
            known_by_cell[k] += v
    for k, v in subtract_pro_rata(targets, unresolved).items():
        known_by_cell[k] += v

    attested_share = (known["persons_present_attested"] / known["persons_present"]) if known["persons_present"] else 0.0
    buckets = []
    for key in sorted(targets):
        a = axes[key]
        cell_employed = employed_by_cell.get(key, 0)
        for trade in ("trade", "none"):
            target = cell_employed if trade == "trade" else targets[key] - cell_employed
            if target <= 0 and trade == "trade":
                continue
            share_of_cell = (target / targets[key]) if targets[key] else 0.0
            k_total = int(round(known_by_cell[key] * share_of_cell))
            k_att = int(round(k_total * attested_share))
            axes_out = {**a, "trade": trade}
            owner, why = person_owner(axes_out)
            buckets.append({
                "key": f"persons/{key}/{trade}",
                "axes": axes_out,
                "target": target,
                "known_attested": k_att,
                "known_inferred": k_total - k_att,
                "to_reconstruct": max(0, target - k_total),
                "filled": 0,
                "owning_ticket": owner,
                "basis": why,
            })

    buckets.append({
        "key": "persons/garrison/fort",
        "axes": {"sex": "any", "age_band": "any", "division": "fort",
                 "household_type": "garrison", "trade": "any"},
        "target": None,
        "known_attested": known["persons_present_by_division"]["fort"],
        "known_inferred": 0,
        "to_reconstruct": None,
        "filled": 0,
        "owning_ticket": "T-1176",
        "basis": "NOT APPORTIONED. The garrison of 1 July 1835 is a return to be read — the "
                 "companies of the 5th Infantry to their strength, the staff and the soldiers' "
                 "families — and T-1176 bounds it from the sources. Whatever it returns is "
                 "subtracted from the civilian quota at the next --build.",
    })
    buckets.append({
        "key": "persons/transient/town",
        "axes": {"sex": "any", "age_band": "any", "division": "any",
                 "household_type": "transient", "trade": "any"},
        "target": None,
        "known_attested": 0,
        "known_inferred": 0,
        "to_reconstruct": None,
        "filled": 0,
        "owning_ticket": "T-1178",
        "basis": "NOT APPORTIONED. The town model bounds the town's RESIDENTS; the land-sale "
                 "crowd, the immigrants awaiting lots, the harbour gang and the crews ashore "
                 "are in the town on 1 July 1835 and not of it. T-1178 bounds the cohort and "
                 "says where it slept.",
    })

    return {
        "town_target": town,
        "town_target_basis": town_basis,
        "town_target_range": [pop_fig["low"], pop_fig["high"]],
        "employed_target": employed,
        "employed_basis": employed_basis,
        "lodging_share": round(lodging_share, 4),
        "lodging_share_range": [lodging_low, lodging_high],
        "buckets": buckets,
    }


def person_owner(axes: dict) -> tuple[str, str]:
    for why, test, ticket in PERSON_TICKET_RULES:
        if test(axes):
            return ticket, why
    raise Fault(f"no ticket owns the person bucket {axes}")


def household_buckets(model: dict, inventory: dict, known: dict) -> dict:
    hh_fig = figure(model, "households_and_families", "households_on_1_july_1835")
    total, basis = point_of(hh_fig)
    matrix = inventory.get("district_group_matrix", {})
    if not matrix:
        raise Fault("the building inventory carries no district/group matrix")

    weights: dict[str, float] = {}
    for htype, group, _ in HOUSEHOLD_BUCKETS:
        row = matrix.get(group)
        if row is None:
            raise Fault(f"the inventory's matrix has no row for {group}")
        for division in CIVIL_DIVISIONS:
            roofs = float(row.get(division) or 0)
            if roofs > 0:
                weights[f"{htype}/{division}"] = roofs
    targets = largest_remainder(total, weights)

    resolved = {d: known["households_present_by_division"][d] for d in CIVIL_DIVISIONS}
    known_by_cell = {k: 0 for k in targets}
    for division in CIVIL_DIVISIONS:
        cells = {k: targets[k] for k in targets if k.endswith("/" + division)}
        for k, v in subtract_pro_rata(cells, resolved[division]).items():
            known_by_cell[k] += v
    for k, v in subtract_pro_rata(targets, known["households_present_unplaced"]).items():
        known_by_cell[k] += v

    owners = {h: t for h, _, t in HOUSEHOLD_BUCKETS}
    buckets = []
    for key in sorted(targets):
        htype, division = key.split("/")
        buckets.append({
            "key": f"households/{key}",
            "axes": {"household_type": htype, "division": division},
            "target": targets[key],
            "known": known_by_cell[key],
            "to_reconstruct": max(0, targets[key] - known_by_cell[key]),
            "filled": 0,
            "owning_ticket": owners[htype],
            "basis": f"the model's {total:,} households apportioned on the inventory's own "
                     f"{htype} roof count in the {division} division",
        })
    buckets.append({
        "key": "households/garrison/fort",
        "axes": {"household_type": "garrison", "division": "fort"},
        "target": None,
        "known": known["households_present_by_division"]["fort"],
        "to_reconstruct": None,
        "filled": 0,
        "owning_ticket": "T-1176",
        "basis": "NOT APPORTIONED — the fort's establishment is read, not modelled (rule 4).",
    })
    return {
        "households_target": total,
        "households_target_basis": basis,
        "households_target_range": [hh_fig["low"], hh_fig["high"]],
        "known_present": known["households_present"],
        "known_uncertain_offered_to_T-1172": known["households_uncertain"],
        "buckets": buckets,
    }



# THE TWO CENSUS LINES THAT COUNT MEN, AND THE BRACKET THE SCENE DATE PUTS THEM IN.
#
# Every other enumerated line of the December 1835 State census counts PREMISES — four
# druggists, eight taverns, two breweries — and the register counts premises too, so the
# two sit in one unit and `target - known` is a quota. Two lines do not: "twenty-two
# lawyers" and "fourteen physicians" count PEOPLE, and T-1007's spend
# (`trade_census_1835_spend.json`) is the adjudication that says so and does the join —
# eighteen lawyer records are thirteen men, five of them second printings of one office,
# and three physician records are eight men once the resident cards carrying Egan, Harmon,
# Goodhue, Kimberly and Temple are read alongside them. Set the census's men against the
# register's NOTICES and the book orders four lawyers the town already has and eleven
# physicians it is nothing like short of.
#
# AND THE COUNT IS NOT OF THE SCENE. The census was returned between 1 September and
# December 1835 over a town of 3,297; the scene is 1 July 1835, and the town model brackets
# that day's population between 2,353 and 3,265. A class of men who serve a population
# scales with it, so the number practising on the scene date is bracketed by the same two
# ratios, and the book orders to the LOW END of that bracket and never above it: a
# reconstruction that filled to the December figure would put into the July town the
# practitioners who arrived in the three months after it.
#
# The bracket is stated on the bucket rather than folded into a number, and the low end is
# floored rather than rounded, because a fraction of a physician is a physician this town
# is not known to have had.
PERSON_UNIT_SPEND = "data/research/books/trade_census_1835_spend.json"


def person_unit_brackets(spend: dict, model: dict) -> dict:
    """`{class: bracket}` for the census lines T-1007's spend rules are counted in MEN."""
    july = figure(model, "population", "population_on_1_july_1835")
    census_pop = figure(model, "population", "recorded_state_count_september_to_december_1835")
    denominator = int(census_pop.get("low") or 0)
    if denominator <= 0:
        raise Fault("the town model carries no State-census population to scale the trade "
                    "lines by, and a bracket cannot be drawn without one")
    low_pop, high_pop = int(july["low"]), int(july["high"])
    if low_pop > high_pop:
        raise Fault("the town model's population bracket for the scene date is inverted")
    out = {}
    for row in spend.get("classes", []):
        if row.get("unit") != "person":
            continue
        name = row["class"]
        count = int(row["census_count"])
        held = row.get("held_in_the_counted_unit")
        if held is None:
            raise Fault(f"the spend rules {name!r} in men and does not say how many the town "
                        f"holds in that unit; the book will not guess it")
        out[name] = {
            "unit": "person",
            "unit_basis": row.get("unit_basis"),
            "census_count": count,
            "held_in_the_counted_unit": int(held),
            "register_records": int(row.get("register_records") or 0),
            "low": (count * low_pop) // denominator,
            "high": (count * high_pop) // denominator,
            "scaled_by": {
                "state_census_population": denominator,
                "scene_date_population_low": low_pop,
                "scene_date_population_high": high_pop,
                "figure": "population_on_1_july_1835",
            },
            "method": (f"The census counts {count} in a town of {denominator}; the town model "
                       f"brackets 1 July 1835 between {low_pop} and {high_pop} people. A "
                       f"profession scales with the population it serves, so the scene date "
                       f"holds between {(count * low_pop) // denominator} and "
                       f"{(count * high_pop) // denominator} of them. The book orders to the "
                       f"low end, floored."),
            "source": PERSON_UNIT_SPEND,
            "ticket": "T-1418",
        }
    return out


def business_buckets(crosswalk: dict, register: dict, spend: dict,
                     model: dict) -> dict:
    classes = crosswalk.get("classes", [])
    if not classes:
        raise Fault("the trade-census crosswalk carries no classes")
    documented_zero = set(crosswalk.get("classes_the_town_holds_nothing_for", []))
    brackets = person_unit_brackets(spend, model)
    buckets = []
    for row in sorted(classes, key=lambda r: r["class"]):
        name = row["class"]
        # A class the December census never put a figure against — `other` and
        # `not_stated` — is not a quota: the book orders against printed counts or
        # not at all. `compared: false` is carried rather than skipped, because a
        # class the crosswalk declined to compare (the churches) still has a census
        # figure and still has a ticket that must answer for it.
        if row.get("census_count") is None:
            continue
        census_count = int(row["census_count"])
        known = int(row["town_records_at_scene_date"])
        ticket = BUSINESS_TICKETS.get(name)
        if ticket is None:
            raise Fault(f"no ticket owns the business class {name!r}")
        zero = name in documented_zero
        # A CLASS THE CENSUS COUNTS IN MEN IS ORDERED IN MEN, and to the scene date's
        # bracket rather than to the December return. Both halves of the row move
        # together — the target to the bracket's low end and `known` to the men the
        # spend holds — because a quota with one unit on each side of the subtraction
        # is not a quota. Every other class keeps the premises reading it always had.
        bracket = None if zero else brackets.get(name)
        if bracket is None:
            target = 0 if zero else census_count
            basis = ("a DOCUMENTED ZERO of the December 1835 State census — the town held none, "
                     "and none is reconstructed" if zero else
                     f"the December 1835 State census prints {census_count}; the register holds "
                     f"{known} at the scene date")
        else:
            target = bracket["low"]
            known = bracket["held_in_the_counted_unit"]
            basis = (f"the December 1835 State census prints {census_count} — a line that counts "
                     f"MEN and not premises (T-1007). The town holds {known} of them at the scene "
                     f"date against {bracket['register_records']} register records, and the "
                     f"scene date's population brackets the class between {bracket['low']} and "
                     f"{bracket['high']}. The book orders to the low end, {target}")
        buckets.append({
            "key": f"businesses/{name}",
            "axes": {"class": name, "division": "unassigned"},
            "census_line": row.get("census_line"),
            "census_count": 0 if zero else census_count,
            "unit": "person" if bracket else "establishment",
            "scene_bracket": bracket,
            "target": 0 if zero else target,
            "known": known,
            "to_reconstruct": 0 if zero else max(0, target - known),
            "filled": 0,
            "owning_ticket": ticket,
            "documented_zero": zero,
            "staff_implied": None,
            "staff_owning_ticket": "T-1183",
            "compared_by_the_crosswalk": bool(row.get("compared")),
            "crosswalk_note": row.get("note"),
            "basis": basis,
        })
    totals = crosswalk.get("totals", {})
    return {
        "register_total": int(totals.get("businesses_in_register") or 0),
        "at_scene_date": int(totals.get("at_scene_date") or 0),
        "census_enumerated_total": int(totals.get("census_enumerated_total") or 0),
        "register_businesses_read": len(register.get("businesses", [])),
        "division_note": "EVERY BUSINESS BUCKET IS `unassigned` BY DIVISION TODAY, and that is a "
                         "reading rather than a hole: the register carries a street where the "
                         "paper printed one and no division at all, and assigning premises to a "
                         "division is T-1182's audit and T-1198's seating. The key carries the "
                         "axis so those tickets fill it rather than re-cut the book.",
        "staffing_note": "The STAFF each business implies is T-1183's model and is not guessed at "
                         "here; T-1189 staffs them from it.",
        "buckets": buckets,
    }


def structure_buckets(inventory: dict, programme: dict, occupancy: dict) -> dict:
    matrix = inventory.get("district_group_matrix", {})
    remaining = programme.get("remaining", {}).get("by_district_group", {})
    standing_total = programme.get("standing", {}).get("structure_records")
    buckets = []
    for group in sorted(matrix):
        row = matrix[group]
        for division in DIVISIONS:
            target = int(row.get(division) or 0)
            if target <= 0:
                continue
            to_build = int((remaining.get(division) or {}).get(group) or 0)
            standing = target - to_build
            ticket = STRUCTURE_TICKETS.get((division, group))
            if ticket is None:
                raise Fault(f"no build ticket owns {group} in the {division} division")
            buckets.append({
                "key": f"structures/{group}/{division}",
                "axes": {"group": group, "division": division},
                "target": target,
                "standing": standing,
                "to_build": to_build,
                "to_retire_or_redeal": max(0, -standing) if standing < 0 else 0,
                "filled": 0,
                "owning_ticket": ticket,
                "ground_waits_on": GROUND_TICKETS[division],
                "basis": f"the inventory's district/group matrix sets {target}; the 668-roof "
                         f"programme leaves {to_build} of them to build",
            })
    return {
        "roof_target": int(inventory.get("targets", {}).get("roof_total") or 0),
        "standing_records": standing_total,
        "standing_with_an_occupant": occupancy["with_occupants"],
        "standing_without_an_occupant": occupancy["without_occupants"],
        "to_build_total": int(programme.get("remaining", {}).get("roofs") or 0),
        "redeal_note": "A roof standing where the order book has nobody to put in it is a "
                       "SUBSTITUTION for T-1197, never a demolition: "
                       f"{occupancy['without_occupants']} of the {standing_total} standing records "
                       "carry no occupants block today, and T-1197 re-audits them against this book.",
        "buckets": buckets,
    }


def occupancy_of(root: Path = ROOT) -> dict:
    """Standing structure records, and how many carry an `occupants` block."""
    directory = root / "data" / "structures"
    if not directory.is_dir():
        raise Fault("data/structures is missing — the book cannot count standing roofs")
    with_occ = without = 0
    for path in sorted(directory.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or "id" not in doc:
            continue
        if doc.get("occupants"):
            with_occ += 1
        else:
            without += 1
    if with_occ + without == 0:
        raise Fault("data/structures holds no structure records at all")
    return {"records": with_occ + without, "with_occupants": with_occ, "without_occupants": without}


def ground_buckets(programme: dict) -> dict:
    buckets = []
    for row in programme.get("schedule", []):
        if row.get("state") != "gated":
            continue
        division = row.get("district")
        buckets.append({
            "key": f"ground/{row['id']}",
            "axes": {"division": division},
            "roofs_gated": int(row.get("headroom") or row.get("capacity_roofs") or 0),
            "waiting_on": row.get("waiting_on"),
            "owning_tickets": GROUND_TICKETS.get(division, []),
            "filled": 0,
        })
    coverage = programme.get("coverage", {})
    return {
        "roofs_on_committed_ground": int(coverage.get("schedulable_on_committed_ground") or 0),
        "roofs_gated_on_coverage": int(coverage.get("gated_on_coverage") or 0),
        "statement": coverage.get("statement"),
        "buckets": buckets,
    }


def programme_deltas(model: dict, inventory: dict, programme: dict,
                     persons: dict, households: dict) -> list[dict]:
    """Where a model target and the 668-roof programme disagree.

    The book carries THE MODEL — that is what the band above it is for — and
    lists the difference here so T-1196 can re-cut the schedule against it rather
    than discover the disagreement halfway through a district.
    """
    matrix = inventory.get("district_group_matrix", {})
    dwellings = figure(model, "households_and_families", "dwellings_the_programme_schedules")
    per_dwelling = figure(model, "households_and_families", "people_per_dwelling_november_1835")
    ordinary = int(matrix.get("ordinary_dwellings", {}).get("total") or 0)
    boarding_model = figure(model, "lodging_and_institutions", "larger_boarding_houses")
    boarding_programme = int(matrix.get("larger_boarding_houses", {}).get("total") or 0)
    institutional = figure(model, "lodging_and_institutions", "institutional_and_public_roofs")
    institutional_programme = int(matrix.get("institutional_public", {}).get("total") or 0)
    inns = figure(model, "lodging_and_institutions", "inns_and_taverns")
    inns_programme = int(matrix.get("inns_taverns", {}).get("total") or 0)
    out = [
        {"id": "households_against_dwellings", "owning_ticket": "T-1196",
         "model": households["households_target"], "programme": ordinary,
         "delta": households["households_target"] - ordinary,
         "statement": f"The household model wants {households['households_target']:,} households "
                      f"and the programme schedules {ordinary:,} ordinary dwellings "
                      f"({dwellings['low']}-{dwellings['high']} in the model's own reading). More "
                      "than one household to a roof is the resolution the census's own "
                      f"{per_dwelling['low']} people per dwelling implies; T-1196 re-cuts the "
                      "schedule to say how many."},
        {"id": "boarding_houses", "owning_ticket": "T-1196",
         "model": boarding_model["low"], "programme": boarding_programme,
         "delta": int(boarding_model["low"]) - boarding_programme,
         "statement": "The lodging model and the programme agree on the larger boarding houses."
                      if int(boarding_model["low"]) == boarding_programme else
                      "The lodging model and the programme disagree on the larger boarding houses."},
        {"id": "inns_and_taverns", "owning_ticket": "T-1196",
         "model": inns["high"], "programme": inns_programme,
         "delta": int(inns["high"]) - inns_programme,
         "statement": f"The model reads {inns['low']}-{inns['high']} inns and taverns; the "
                      f"programme schedules {inns_programme}."},
        {"id": "institutional_and_public", "owning_ticket": "T-1196",
         "model": institutional["high"], "programme": institutional_programme,
         "delta": int(institutional["high"]) - institutional_programme,
         "statement": f"The model reads {institutional['low']}-{institutional['high']} "
                      f"institutional and public roofs; the programme schedules "
                      f"{institutional_programme}."},
        {"id": "people_per_roof", "owning_ticket": "T-1196",
         "model": persons["town_target"],
         "programme": int(inventory.get("targets", {}).get("roof_total") or 0),
         "delta": 0,
         "statement": f"{persons['town_target']:,} people under "
                      f"{int(inventory.get('targets', {}).get('roof_total') or 0):,} roofs is the "
                      "ratio the completed town must meet; the census's own reading for November "
                      f"1835 is {per_dwelling['low']} people per dwelling over 398 dwellings."},
    ]
    return out


def invariants(known: dict, persons: dict, households: dict, structures: dict) -> list[dict]:
    return [
        {"id": "every_person_housed", "owning_ticket": "T-1215",
         "statement": "Every person in the layer — attested, inferred or reconstructed — is a "
                      "member of a household or a lodging place that is seated on a roof.",
         "measured_now": f"{known['households_with_a_lives_at']} of "
                         f"{known['households_present']} present households name a lives_at."},
        {"id": "every_working_person_has_a_workplace", "owning_ticket": "T-1189",
         "statement": "Every person carrying a trade, profession or employment has a workplace, "
                      "or a stated `no fixed workplace`.",
         "measured_now": f"{known['households_with_a_works_at']} of "
                         f"{known['households_present']} present households name a works_at."},
        {"id": "every_business_has_staff", "owning_ticket": "T-1189",
         "statement": "Every business — attested, inferred or reconstructed — carries the staff "
                      "T-1183's model implies for its kind.",
         "measured_now": "not yet measurable: the authored business layer is T-1180."},
        {"id": "every_structure_occupied_or_its_use_stated", "owning_ticket": "T-1197",
         "statement": "Every standing roof carries an occupant or a stated use.",
         "measured_now": f"{structures['standing_without_an_occupant']} of "
                         f"{structures['standing_records']} standing records carry no occupants block."},
        {"id": "dwellings_ratio_within_its_bracket", "owning_ticket": "T-1215",
         "statement": "The town census's people-per-dwelling ratio is met within the model's bracket.",
         "measured_now": f"the book orders {persons['town_target']:,} people into "
                         f"{households['households_target']:,} households."},
        {"id": "no_bucket_overfilled", "owning_ticket": "T-1166",
         "statement": "No bucket's `filled` exceeds its `to_reconstruct`; a filler that bypasses "
                      "the book is red in check.sh.",
         "measured_now": "enforced by --check on every gate run."},
    ]


# ----------------------------------------------------------------- the build --

def build(data: dict, fills: list | None = None, occupancy: dict | None = None) -> dict:
    fills = list(fills or [])
    for fill in fills:
        if not isinstance(fill, dict) or not fill.get("ticket") or not fill.get("bucket"):
            raise Fault("a fill in the ledger names no ticket or no bucket")
    known = known_layer(data["residents"])
    occ = occupancy if occupancy is not None else occupancy_of()
    persons = person_buckets(data["model"], data["composition"], data["inventory"], known)
    households = household_buckets(data["model"], data["inventory"], known)
    businesses = business_buckets(data["crosswalk"], data["register"], data["trade_spend"],
                                  data["model"])
    structures = structure_buckets(data["inventory"], data["programme"], occ)
    ground = ground_buckets(data["programme"])

    # SUMMED, NOT KEYED. This was a dict comprehension over `fills` until T-1174, so two
    # stages filling the SAME bucket kept only the last of them: `modelled_families` put
    # 300 wives and children into the family buckets and `women_and_children` put 556 more
    # into the same 24 of them, and the book printed 556 as though the first 300 had never
    # happened. Worse, the `no_bucket_overfilled` invariant below was reading that same
    # number, so the one gate that is supposed to refuse an overfilled bucket could not
    # have seen an overfill made by two tickets between them.
    counted = Counter()
    for fill in fills:
        counted[fill["bucket"]] += int(fill.get("records") or 0)
    families = []
    for key, title, lead, payload in (
        ("persons", "Persons", "Who the town still has to be given, by sex, age, division, "
         "household and trade.", persons),
        ("households", "Households", "The households the model wants, by kind and division.", households),
        ("businesses", "Businesses", "The December 1835 State census set against the register the "
         "town already holds.", businesses),
        ("structures", "Structures", "The roofs the 668-roof programme still owes, by archetype "
         "group and division.", structures),
        ("ground", "Ground first", "The streets, terrain and lots a structure bucket waits on.", ground),
    ):
        buckets = payload.pop("buckets")
        for b in buckets:
            b["filled"] = counted.get(b["key"], 0)
            todo = b.get("to_reconstruct", b.get("to_build"))
            if todo is not None and b["filled"] > todo:
                raise Fault(f"the bucket {b['key']} is overfilled: {b['filled']} of {todo}")
        families.append({"key": key, "title": title, "lead": lead,
                         "summary": payload, "buckets": buckets})

    roster = data["roster"].get("counts", {}).get("by_class", {})
    offered = {k: v for k, v in sorted(roster.items()) if k in ROSTER_TICKETS}

    doc = {
        "$schema_note": "DERIVED — regenerate with tools/build_order_book_1835.py --build; "
                        "tools/check.sh re-derives it. Do not hand-edit. The `fills` ledger and "
                        "each bucket's `filled` are written by the reconstruction tools.",
        "id": "chicago_july_1835_reconstruction_order_book",
        "ticket": "T-1166",
        "target_date": SCENE_DATE,
        "generated_by": "tools/build_order_book_1835.py --build",
        "not_a_reading": "an adjudication over committed derived files — no page of any source "
                         "was opened, nobody is named, nobody is aged, nobody is housed",
        "inputs": [
            "data/reconstruction/1835_town_model.json",
            "data/reconstruction/1835_population_profile.json",
            "data/reconstruction/1835_borderline_roster.json",
            "data/reconstruction/1835_665_roof_programme.json",
            "data/reconstruction/1835_building_inventory.json",
            "data/research/books/trade_census_1835_crosswalk.json",
            "data/research/books/trade_census_1835_spend.json",
            "data/research/census_1840/composition_1840.json",
            "data/residents/index.json",
            "data/research/newspapers/register_1835.json",
            "data/structures/*.json",
        ],
        "method": {
            "point_from_range": "Where the town model gives a point the book takes it; where it "
                                "gives only a range the book takes the MIDPOINT, rounded half up, "
                                "and carries the range beside it. A quota cannot be a range.",
            "unresolved_known": "A named person or household the layer cannot place on an axis is "
                                "subtracted PRO RATA across that axis's cells, so the book never "
                                "orders a replacement for somebody already standing in the town.",
            "presence_is_the_test": "Only a household recorded `present` on the scene date counts "
                                    "as known. An `uncertain` one is the roster's R1 class and is "
                                    "offered to T-1172 — counting it in both places orders one "
                                    "person twice.",
            "the_fort_is_read_not_apportioned": "The garrison and its households carry a null "
                                                "target; T-1176 reads the return and the civilian "
                                                "quota is re-cut at the next --build.",
            "rounding": "Largest remainder throughout, ties broken on the bucket key, so two "
                        "builds on one set of inputs are byte-identical.",
            "real_names_first": "The roster (T-1159) offers every name the corpus printed and "
                                "withheld. It is a licence on WHICH name a filler uses and never "
                                "a quota, so it is counted against its ticket rather than smeared "
                                "across cells that cannot hold it.",
        },
        "known_layer": known,
        # THE POPULATION THE RULINGS PUT IN THE TOWN (T-1386), stated beside `known_layer`
        # and deliberately NOT summed into it. `known_layer` counts what the resident
        # INDEX records `present`, and the index is a summary of the household directory
        # and nothing else (T-0715); the 827 people the research left `uncertain` are ruled
        # into the town by a ruling layer outside those cards, so the two are different
        # reads and the book says both rather than averaging them.
        #
        # WHY THE QUOTAS ARE NOT RE-CUT HERE. Every bucket's `to_reconstruct` is
        # `target - known`, and 983 reconstructed people have already been drawn against
        # the quotas `known` gives today. Adding 826 named people to `known` shrinks those
        # quotas under work already done, which the `no_bucket_overfilled` invariant would
        # refuse — correctly, because the answer is to retire or re-family the surplus and
        # that is T-1196's re-cut of the programme and T-1197's re-audit of the anonymous
        # roofs, not a side effect of a presence ruling. T-1179 converges the layer over
        # both. What this block owes the book is the FIGURE and the delta, so the next
        # stage re-cuts from a number rather than rediscovering it.
        "population_ruled_in": {
            "ticket": "T-1386",
            "source": "data/reconstruction/1835_presence_rulings.json",
            "persons_ruled_present": int(
                (data["presence_rulings"].get("counts") or {}).get("persons_ruled") or 0),
            "households_ruled_present": int(
                (data["presence_rulings"].get("counts") or {}).get("households_ruled") or 0),
            "by_presence_tier": (data["presence_rulings"].get("counts") or {}
                                 ).get("persons_by_tier") or {},
            "by_residence_grade": (data["presence_rulings"].get("counts") or {}
                                   ).get("persons_by_residence_grade") or {},
            "persons_known_today": known["persons_present"],
            "persons_known_if_the_rulings_are_summed_in": known["persons_present"] + sum(
                int(n or 0) for grade, n in
                ((data["presence_rulings"].get("counts") or {}).get(
                    "persons_by_residence_grade") or {}).items()
                if grade in ("attested", "inferred")),
            "what_re_cuts_the_quotas": ["T-1196", "T-1197", "T-1179"],
        },
        "roster_offered": {
            "total": int(data["roster"].get("counts", {}).get("offered") or 0),
            "by_class": offered,
            "tickets": {k: ROSTER_TICKETS[k] for k in sorted(offered)},
        },
        "totals": {
            "persons_target": persons["town_target"],
            "persons_known": known["persons_present"],
            "persons_to_reconstruct": sum(b["to_reconstruct"] or 0 for b in families[0]["buckets"]),
            "households_target": households["households_target"],
            "households_known": known["households_present"],
            "households_to_reconstruct": sum(b["to_reconstruct"] or 0 for b in families[1]["buckets"]),
            "businesses_target": sum(b["target"] for b in families[2]["buckets"]),
            "businesses_known": sum(b["known"] for b in families[2]["buckets"]),
            "businesses_to_reconstruct": sum(b["to_reconstruct"] for b in families[2]["buckets"]),
            "roofs_target": structures["roof_target"],
            "roofs_standing": structures["standing_records"],
            "roofs_to_build": structures["to_build_total"],
        },
        "bucket_families": families,
        "programme_deltas": programme_deltas(data["model"], data["inventory"],
                                             data["programme"], persons, households),
        "invariants": invariants(known, persons, households, structures),
        "fills": fills,
    }
    if len(doc["bucket_families"]) != 5:
        raise Fault("the order book is five bucket families; fewer is a book with a hole in it")
    return doc


# ---------------------------------------------------------------- the report --

def report_text(doc: dict) -> str:
    t = doc["totals"]
    out = [
        "# The 1835 reconstruction order book",
        "",
        "> DERIVED from `data/reconstruction/1835_reconstruction_order_book.json`. Regenerate with",
        "> `tools/build_order_book_1835.py --build`; `tools/check.sh` re-derives both. Do not hand-edit.",
        "",
        f"**T-1166.** Known minus model, per bucket, with the ticket that owns filling it. "
        f"The town converges to **{t['persons_target']:,} people** in "
        f"**{t['households_target']:,} households**, working "
        f"**{t['businesses_target']:,} enumerated businesses**, under "
        f"**{t['roofs_target']:,} roofs**.",
        "",
        "| | target | known | to reconstruct |",
        "|---|---:|---:|---:|",
        f"| Persons | {t['persons_target']:,} | {t['persons_known']:,} | {t['persons_to_reconstruct']:,} |",
        f"| Households | {t['households_target']:,} | {t['households_known']:,} | {t['households_to_reconstruct']:,} |",
        f"| Businesses (enumerated classes) | {t['businesses_target']:,} | {t['businesses_known']:,} | {t['businesses_to_reconstruct']:,} |",
        f"| Roofs | {t['roofs_target']:,} | {t['roofs_standing']:,} | {t['roofs_to_build']:,} |",
        "",
        "## The rules this book adds",
        "",
    ]
    for key, text in doc["method"].items():
        out.append(f"- **{key.replace('_', ' ')}** — {text}")
    out += ["", "## Real names before invented ones", "",
            f"The roster offers {doc['roster_offered']['total']:,} names the corpus printed and this "
            "project withheld. Each class is a licence, not a quota:", "",
            "| class | offered | ticket |", "|---|---:|---|"]
    for cls, n in doc["roster_offered"]["by_class"].items():
        out.append(f"| `{cls}` | {n:,} | {doc['roster_offered']['tickets'][cls]} |")

    for family in doc["bucket_families"]:
        out += ["", f"## {family['title']}", "", family["lead"], ""]
        summary = family["summary"]
        for k, v in summary.items():
            if isinstance(v, (int, float)):
                out.append(f"- `{k}`: {v:,}")
            elif isinstance(v, str):
                out.append(f"- `{k}`: {v}")
            elif isinstance(v, list):
                out.append(f"- `{k}`: {', '.join(str(x) for x in v)}")
        out += ["", "| bucket | target | known | to do | filled | ticket |", "|---|---:|---:|---:|---:|---|"]
        for b in family["buckets"]:
            target = b.get("target", b.get("roofs_gated"))
            known = b.get("known", (b.get("known_attested", 0) + b.get("known_inferred", 0))
                          if "known_attested" in b else b.get("standing"))
            todo = b.get("to_reconstruct", b.get("to_build"))
            owner = b.get("owning_ticket") or ", ".join(b.get("owning_tickets", []))
            fmt = lambda v: "—" if v is None else f"{v:,}"
            out.append(f"| `{b['key']}` | {fmt(target)} | {fmt(known)} | {fmt(todo)} "
                       f"| {b['filled']:,} | {owner} |")

    out += ["", "## Where the model and the roof programme disagree", "",
            "The book carries THE MODEL. Every difference is listed here for T-1196, which "
            "re-cuts the 668-roof schedule against it.", "",
            "| | model | programme | delta |", "|---|---:|---:|---:|"]
    for d in doc["programme_deltas"]:
        out.append(f"| **{d['id']}** — {d['statement']} | {d['model']:,} | {d['programme']:,} "
                   f"| {d['delta']:+,} |")

    out += ["", "## The invariants the convergence tickets assert", ""]
    for inv in doc["invariants"]:
        out.append(f"- **{inv['id']}** ({inv['owning_ticket']}) — {inv['statement']} "
                   f"*Now:* {inv['measured_now']}")
    out.append("")
    return "\n".join(out)


# ------------------------------------------------------------------ commands --

def _fills_on_disk() -> list:
    if not BOOK.exists():
        return []
    try:
        return json.loads(BOOK.read_text(encoding="utf-8")).get("fills", [])
    except json.JSONDecodeError as exc:
        raise Fault(f"the committed order book is not JSON: {exc}") from exc


def cmd_build() -> int:
    doc = build(load(), _fills_on_disk())
    BOOK.parent.mkdir(parents=True, exist_ok=True)
    BOOK.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report_text(doc), encoding="utf-8")
    n = sum(len(f["buckets"]) for f in doc["bucket_families"])
    print(f"OK: 1835 reconstruction order book — {n} buckets in "
          f"{len(doc['bucket_families'])} families; {doc['totals']['persons_to_reconstruct']:,} "
          f"persons, {doc['totals']['households_to_reconstruct']:,} households, "
          f"{doc['totals']['businesses_to_reconstruct']:,} businesses and "
          f"{doc['totals']['roofs_to_build']:,} roofs to reconstruct")
    return 0


def cmd_check() -> int:
    faults = []
    if not BOOK.exists():
        print("FAIL: the 1835 reconstruction order book is missing — run --build", file=sys.stderr)
        return 1
    expected = build(load(), _fills_on_disk())
    if json.loads(BOOK.read_text(encoding="utf-8")) != expected:
        faults.append("the 1835 reconstruction order book is stale — run --build")
    if not REPORT.exists():
        faults.append("the order book's report is missing — run --build")
    elif REPORT.read_text(encoding="utf-8") != report_text(expected):
        faults.append("the order book's report is stale — run --build")
    if faults:
        for f in faults:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1
    t = expected["totals"]
    print(f"OK: 1835 reconstruction order book — {t['persons_to_reconstruct']:,} persons, "
          f"{t['households_to_reconstruct']:,} households, "
          f"{t['businesses_to_reconstruct']:,} businesses, {t['roofs_to_build']:,} roofs to go")
    return 0


def cmd_self_test() -> int:
    data = load()
    occ = occupancy_of()
    fired = 0

    def fires(why, fn):
        nonlocal fired
        try:
            fn()
        except Fault:
            fired += 1
            print(f"   fires: {why}")
            return
        raise AssertionError(f"did not fire: {why}")

    # AN APPORTIONMENT CLOSES OR IT IS NOT ONE.
    assert sum(largest_remainder(100, {"a": 1, "b": 1, "c": 1}).values()) == 100
    assert largest_remainder(10, {"a": 1, "b": 1}) == {"a": 5, "b": 5}
    # …and it is DETERMINISTIC: the same weights give the same answer, tie or no tie.
    assert largest_remainder(7, {"a": 1, "b": 1, "c": 1}) == largest_remainder(7, {"c": 1, "b": 1, "a": 1})
    fires("an apportionment across weights that sum to zero",
          lambda: largest_remainder(5, {"a": 0}))
    fires("an apportionment of a negative total", lambda: largest_remainder(-1, {"a": 1}))

    # A POINT FROM A RANGE, and an inverted range is a fault rather than a negative quota.
    assert point_of({"figure": "x", "low": 10, "high": 20, "point": None})[0] == 15
    assert point_of({"figure": "x", "low": 10, "high": 20, "point": 12})[0] == 12
    fires("an inverted range", lambda: point_of({"figure": "x", "low": 20, "high": 10}))
    fires("a figure with no range at all", lambda: point_of({"figure": "x"}))

    # A MISSING INPUT IS A FAULT, not a book quietly built without it.
    fires("an input file the book cannot read", lambda: load(Path("/nonexistent-root-for-the-self-test")))

    # THE UNRESOLVED KNOWN ARE SUBTRACTED, NEVER DROPPED.
    spread = subtract_pro_rata({"a": 10, "b": 30}, 20)
    assert sum(spread.values()) == 20, spread
    assert spread["b"] > spread["a"], spread
    assert sum(subtract_pro_rata({"a": 3, "b": 1}, 0).values()) == 0

    # AN OVERFILLED BUCKET IS RED. This is the whole point of the counters: a filler
    # that writes more records than its quota cannot merge.
    doc = build(data, [], occ)
    first = doc["bucket_families"][0]["buckets"][0]
    fires("a bucket filled past its quota",
          lambda: build(data, [{"ticket": "T-1347", "bucket": first["key"],
                                "records": (first["to_reconstruct"] or 0) + 1}], occ))
    fires("a fill that names no ticket",
          lambda: build(data, [{"bucket": first["key"], "records": 1}], occ))

    # TWO TICKETS FILLING ONE BUCKET ARE ADDED, NOT OVERWRITTEN (T-1174). Both
    # `modelled_families` and `women_and_children` fill the family buckets, and while this
    # was a dict comprehension the second ticket's row simply replaced the first's — so a
    # bucket could be filled to twice its quota and the overfill gate above would never
    # have fired, because it was reading the same replaced number.
    halves = [{"ticket": "T-1171", "bucket": first["key"], "records": 1},
              {"ticket": "T-1174", "bucket": first["key"], "records": 2}]
    assert build(data, halves, occ)["bucket_families"][0]["buckets"][0]["filled"] == 3
    fires("two tickets overfilling one bucket between them",
          lambda: build(data, [{"ticket": "T-1171", "bucket": first["key"],
                                "records": first["to_reconstruct"] or 0},
                               {"ticket": "T-1174", "bucket": first["key"],
                                "records": 1}], occ))

    # EVERY BUCKET NAMES A TICKET, and every ticket named is in the reconstruction bands.
    for family in doc["bucket_families"]:
        for b in family["buckets"]:
            owners = [b["owning_ticket"]] if b.get("owning_ticket") else b.get("owning_tickets", [])
            for owner in owners:
                assert owner.startswith("T-1"), (b["key"], owner)

    # THE PERSON TOTALS CLOSE ON THE MODEL'S OWN NUMBER.
    persons = doc["bucket_families"][0]["buckets"]
    apportioned = sum(b["target"] for b in persons if b["target"] is not None)
    assert apportioned == doc["totals"]["persons_target"], (apportioned, doc["totals"])

    # NOBODY IS NAMED. The book is cohorts and counts; a record id in it would be a
    # person this adjudication had no licence to place.
    text = json.dumps(doc["bucket_families"])
    for forbidden in ("hh_", "person_", "business_", "recon_1835_"):
        assert forbidden not in text, f"the order book names a {forbidden} record"

    # AND THE CHILD SHARE THE PYRAMID PRODUCES SITS INSIDE THE MODEL'S BRACKET —
    # the one place the 1840 shape could silently disagree with the 1835 model.
    child = sum(b["target"] for b in persons
                if b["target"] is not None and b["axes"]["age_band"] == "under_10")
    share = child / doc["totals"]["persons_target"]
    band = figure(data["model"], "population", "share_under_ten")
    assert band["low"] <= share <= band["high"], (share, band["low"], band["high"])

    # TWO BUILDS ARE BYTE-IDENTICAL.
    assert json.dumps(build(data, [], occ), sort_keys=True) == json.dumps(doc, sort_keys=True)

    print(f"build_order_book_1835 self-tests pass ({fired} guards fired, "
          f"{sum(len(f['buckets']) for f in doc['bucket_families'])} buckets, "
          f"child share {share:.3f} inside {band['low']}-{band['high']}, no record named)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    try:
        if args.build:
            return cmd_build()
        if args.check:
            return cmd_check()
        if args.self_test:
            return cmd_self_test()
    except Fault as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
