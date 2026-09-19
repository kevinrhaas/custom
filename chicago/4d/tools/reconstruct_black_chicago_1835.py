#!/usr/bin/env python3
"""T-1377, stage `free_black` — the free Black town of 1835, to the low end of its bracket.

    python3 tools/reconstruct_black_chicago_1835.py --build      draw them, write the cards
    python3 tools/reconstruct_black_chicago_1835.py --check      re-derive and refuse drift
    python3 tools/reconstruct_black_chicago_1835.py --report     who was drawn, and against what
    python3 tools/reconstruct_black_chicago_1835.py --self-test  the rules, each refusing its own case

WHAT THIS STAGE IS. The owner, 2026-09-17: "it is also very important that we keep and
capture and identify the black owned businesses and residents and family households."
Until now this reconstruction held not one free Black resident. The only trace it carried
was a sentence in a white lawyer's card — John Dean Caton, August 1833, defending "six or
seven free coloured men" before the Court of County Commissioners and obtaining
certificates of freedom for them, his fee a dollar from each. Six or seven men, named by
nobody, two years before the scene, in a town this project has otherwise read down to the
name of the man who shod the horses.

THE BRACKET, AND ITS TWO ENDS.

  FLOOR — 6 persons. Caton's six. The lower of "six or seven", because this project takes
  the lower of a source's own pair. They are ATTESTED as a count and unnamed as people:
  a dated proceeding of a court of record, in a card already in the layer.

  CEILING — 28 persons. The Sixth Census counts 53 free coloured persons at Chicago on
  1 June 1840 (data/research/census_1840/composition_1840.json, from the full-count
  extract; the bands are printed there and this file re-reads them). Scaled back to the
  town of 1 July 1835 by the town model's own population point of 2,536 against the 1840
  city, that share is 28 persons at the lower of the two available 1840 denominators and
  30 at the higher. This stage takes 28. The scaling is the invented step and it is named:
  a population that grew from about 2,500 to about 4,500 in five years did not grow
  uniformly across its communities, and nothing in this corpus says how the free Black
  share moved. The ceiling is a ceiling, not an estimate of anybody.

  WHAT LIES BETWEEN — this stage mints 28, in six households, and 28 IS THE CEILING. That
  is not a figure chosen to fill the bracket: the deal takes one household for each of the
  floor's six men, deals the composition stock below to them in the sheets' own order, and
  stops the moment the ceiling would be passed. Six households of 6, 4, 2, 6, 6 and 4 come
  to 28 exactly, and the arithmetic is a coincidence of the stock rather than a target. It
  is stated here because a mint that lands on its own ceiling should be read as what it is:
  the model has no room left for a free Black Chicagoan this cohort has not counted, and a
  reading that finds one retires a drawn household rather than joining it. The floor is met
  by the draw rather than forced onto it — the dealt composition seats six adult men, which
  is what the certificates counted.

THE COMPOSITION STOCK — CHICAGO'S OWN BLACK HOUSEHOLDS, FIVE YEARS ON. Sixty-three sheets
of the 1840 Cook County enumeration are read into data/research/census_1840/pages/. Seven
of their households carry a mark in the free coloured columns; four of those carry NO free
white person at all, which is to say they were Black-headed households, and their band
vectors are the only measured structure of a Black household in this place that this corpus
holds. This stage deals those four vectors, in the order the sheets print them, cycled, to
six households. Two of the four are headed by a woman, and the cohort inherits that.

  A vector is a household's SHAPE, never its people. Nothing about George White, Oliver
  Henson, John Johnson or the woman the sheet writes as "Eliza As[?]ie" is carried into a
  drawn household: not their names, not their ages as individuals, not the industry their
  household was marked in. They lived in 1840 and this scene is 1835; a source that names a
  person may never be spent on somebody drawn.

THE NAMES, AND WHAT IS REFUSED. The heads are named; nobody else is. The four Black-headed
households of 1840 show ordinary Anglo-American naming — White, Henson, Johnson; George,
Oliver, John, Eliza — the same stock as their white neighbours, and that is the whole of
what this corpus attests about how free Black Chicagoans were named. So the pool extends
that stock rather than inventing a distinct naming, and it excludes three sets of names:
every surname the four attested households bear (a drawn head must not read as the 1840
family's kin), every surname the town's own attested residents bear (nor as a documented
white family's kin), and every full name anywhere in the layer. Inside a household, nobody
is named at all: the 1840 sheet names the head and counts the rest, so a name for a woman
or a child here would invent the person AND their relation to the head in one stroke. They
carry a designation, their sex and their band, and the ticket that would name them.

WHAT THIS STAGE DOES NOT CLAIM. No kin tie: the schedule of 1840 records no relationships
and none is written here, so every member below the head is `household_member` and the
families of this cohort are owed to T-1170/T-1171 like everybody else's. No residence:
T-1199 seats reconstructed households. No arrival: T-1169 owns it, and the circle the trade
households name applies here too. Every person carries `review_required`, because the
cohort tickets are reviewable by the communities they reconstruct before this scene is
released, and every value carries the reading that would retire it.

THE TRADES. The one occupational fact this corpus holds about a Black-headed Chicago
household is the industry column of the 1840 continuation sheet paired to printed page 219,
which marks the Henson household in MANUFACTURES AND TRADES — not in service. It is not
carried into any drawn household; it is why the trade deal below may not be all-service.
The deal is even over the trades this layer's own vocabulary carries for the employments
T-1177 names — labourer and teamster for a man, laundress and domestic for a woman — and
`barber`, `cook` and `whitewasher` are REFUSED rather than smuggled in under a near term:
this layer's occupation vocabulary has no word for any of them, and inventing one here
would put a trade into the town's census of trades that nothing ordered.

THE ONE FIRM. A drawn household that carries more than one adult man is a house where men
lodged, and the largest such household's head keeps it. One, and not one per vector that
qualifies: T-1187 owns how many boarding houses the town had against the 42-roof
programme, and a cohort may not order more of them than its own evidence carries.

EVERY VALUE IS REPRODUCIBLE. Nothing is random: each value comes from `blake2s(seed)` over
a seed string printed on the record beside it. Re-running `--build` on the same inputs
writes the same bytes, and `--check` is what proves it.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESIDENTS = DATA / "residents"
MINTED = RESIDENTS / "black_chicago"
PAGES = DATA / "research" / "census_1840" / "pages"
COMPOSITION = DATA / "research" / "census_1840" / "composition_1840.json"
CATON = RESIDENTS / "households" / "hh_caton_john_dean.json"
TOWN = DATA / "reconstruction" / "1835_town_model.json"
POOLS = DATA / "reconstruction" / "1835_invented_name_pools.json"
LEDGER = DATA / "reconstruction" / "1835_black_chicago.json"
INDEX = RESIDENTS / "index.json"

TICKET = "T-1377"
PARENT = "T-1177"
STAGE = "free_black"
PROGRAMME = "chicago_1835_resident_reconstruction"

# The 1840 schedule's free coloured columns, in the printed order, and the two other
# vocabularies the page readings use for the same cells.
BANDS = [
    ("male", "under 10", "27", "cm_u10"),
    ("male", "10 under 24", "28", "cm_10_23"),
    ("male", "24 under 36", "29", "cm_24_35"),
    ("male", "36 under 55", "30", "cm_36_54"),
    ("male", "55 under 100", "31", "cm_55_99"),
    ("male", "100 and upwards", "32", "cm_100_up"),
    ("female", "under 10", "33", "cf_u10"),
    ("female", "10 under 24", "34", "cf_10_23"),
    ("female", "24 under 36", "35", "cf_24_35"),
    ("female", "36 under 55", "36", "cf_36_54"),
    ("female", "55 under 100", "37", "cf_55_99"),
    ("female", "100 and upwards", "38", "cf_100_up"),
]
WHITE_KEYS = {str(n) for n in range(1, 27)}
ADULT_BANDS = {"24 under 36", "36 under 55", "55 under 100", "100 and upwards"}
# 10-under-24 straddles majority and is NOT counted an adult here: half of it is children.

TRADES_MALE = ["labourer", "teamster"]
TRADES_FEMALE = ["laundress", "domestic"]
REFUSED_TRADES = {
    "barber": "no term in data/residents/index.json's occupation vocabulary; `barber_surgeon` is a different trade and is not it",
    "cook": "no term in the vocabulary, and `domestic` is a household's servant rather than a cook by trade",
    "whitewasher": "no term in the vocabulary, and no committed source puts the trade in this town at all",
    "drayman": "no term; `teamster` is the vocabulary's word for the work and is what the deal uses",
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, payload):
    Path(path).write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n",
                          encoding="utf-8")


def draw(seed: str) -> int:
    return int.from_bytes(hashlib.blake2s(seed.encode("utf-8"), digest_size=8).digest(), "big")


def cell(cells, numeric, alt):
    for key in (numeric, alt):
        value = cells.get(key)
        if isinstance(value, (int, float)) and value:
            return int(value)
    return 0


def all_1840_head_names():
    """Every head of household name the read sheets carry, as written."""
    names = []
    for path in sorted(PAGES.glob("*.json")):
        page = load(path)
        for record in page.get("records") or []:
            name = record.get("normalized") or record.get("as_read")
            confidence = record.get("name_confidence") or page.get("name_confidence")
            if name and "[?]" not in name and confidence != "low":
                names.append(name)
    return names


def read_1840_free_coloured_households():
    """Every household in the read sheets that carries a free coloured person."""
    rows = []
    for path in sorted(PAGES.glob("*.json")):
        page = load(path)
        for record in page.get("records") or []:
            cells = record.get("cells") or {}
            if not cells:
                continue
            vector = [(sex, band, cell(cells, num, alt)) for sex, band, num, alt in BANDS]
            persons = sum(n for _, _, n in vector)
            if not persons:
                continue
            white = sum(v for k, v in cells.items()
                        if k in WHITE_KEYS and isinstance(v, (int, float)))
            rows.append({
                "familysearch_id": page["familysearch_id"],
                "printed_page": page.get("printed_page"),
                "line": record["line"],
                "head_as_read": record.get("normalized") or record.get("as_read"),
                "free_coloured_persons": persons,
                "free_white_persons": int(white),
                "black_headed": white == 0,
                "vector": [{"sex": s, "band": b, "persons": n} for s, b, n in vector if n],
            })
    rows.sort(key=lambda r: (r["printed_page"] or 0, r["line"]))
    return rows


def caton_sentence():
    """The August 1833 certificates, quoted out of the card that carries them."""
    blob = json.dumps(load(CATON), ensure_ascii=False)
    match = re.search(r"In August 1833 he defended[^\.]+\.", blob)
    if not match:
        raise SystemExit("the Caton card no longer carries the 1833 certificates sentence")
    return match.group(0)


def bracket(rows, composition, town):
    """Floor from the certificates, ceiling from 1840 scaled back to the scene."""
    fc = composition["age_bands"]["free_coloured"]
    counted_1840 = composition["totals"]["free_coloured_persons"]
    assert sum(b["persons"] for b in fc) == counted_1840
    enumerated = composition["totals"]["persons"]
    citypop = (composition["totals"].get("citypop_variable") or [None])[0]
    population = next(f for f in town["sections"][0]["figures"]
                      if f["figure"] == "population_on_1_july_1835")["point"]
    scalings = []
    for label, denominator in (("the extract's enumerated persons", enumerated),
                               ("the census's own city population", citypop)):
        if not denominator:
            continue
        scalings.append({
            "denominator": label,
            "persons_1840": denominator,
            "free_coloured_share": round(counted_1840 / denominator, 5),
            "scaled_to_1835": round(counted_1840 / denominator * population, 1),
        })
    ceiling = int(min(s["scaled_to_1835"] for s in scalings) + 0.5)
    return {
        "floor_persons": 6,
        "floor_is": ("The six of Caton's 'six or seven', August 1833 — the lower of the "
                     "source's own pair, as this project takes every such pair."),
        "ceiling_persons": ceiling,
        "ceiling_is": ("The 53 free coloured persons the Sixth Census counts at Chicago on "
                       "1 June 1840, scaled back to the town model's population point for "
                       "1 July 1835 (%d) at the LOWER of the two 1840 denominators. The "
                       "scaling is this file's one invented step." % population),
        "population_on_1_july_1835": population,
        "free_coloured_persons_1840": counted_1840,
        "scalings": scalings,
        "bands_1840": fc,
    }


def attested_surnames():
    """Every surname the resident layer already carries, so no drawn head reads as kin."""
    index = load(INDEX)
    names = set()
    for entry in index.get("households", []):
        path = RESIDENTS / entry.get("file", "")
        if not path.exists():
            continue
        for person in load(path).get("persons", []) or []:
            name = (person.get("name") or "").strip()
            if name:
                names.add(name)
    surnames = {n.split()[-1] for n in names if n.split()}
    return names, surnames


def build_pool(rows, pools):
    """The free_black pool: the attested seed, and the stock it licenses."""
    seed_rows = [r for r in rows if r["black_headed"]]
    seed_surnames, seed_given = [], []
    for row in seed_rows:
        parts = [p for p in re.split(r"\s+", row["head_as_read"]) if p]
        if len(parts) >= 2 and "[?]" not in parts[-1]:
            seed_surnames.append(parts[-1])
        if parts and "[?]" not in parts[0]:
            seed_given.append(parts[0])
    return {
        "id": "free_black",
        "label": "Free Black Chicago",
        "seeded_from": [
            {"head_as_read": r["head_as_read"], "familysearch_id": r["familysearch_id"],
             "printed_page": r["printed_page"], "line": r["line"],
             "free_coloured_persons": r["free_coloured_persons"]}
            for r in seed_rows],
        "seed_surnames": sorted(set(seed_surnames)),
        "seed_given_names": sorted(set(seed_given)),
        "what_the_seed_shows": (
            "Four Black-headed households at Chicago in 1840 bearing ordinary "
            "Anglo-American names — the same naming stock as their white neighbours. That "
            "is the whole of what this corpus attests about how free Black Chicagoans were "
            "named, and it is what licenses the extension below."),
        "extension_rule": (
            "SURNAMES from the 1840 Cook County sheets themselves — the naming of this place "
            "in this decade, written by its own enumerator — MINUS every surname the 1835 "
            "resident layer already carries and MINUS the four Black-headed households' own. "
            "FORENAMES from the ordinary Anglo-American given names the pools file carries, "
            "by sex, which is what the seed's four heads show. No drawn full name may equal "
            "a name anywhere in the layer and no two heads share a surname. The subtractions "
            "are the point: a drawn head must read as neither the 1840 family's kin nor a "
            "documented white family's."),
        "not_a_distinct_naming": (
            "No separate 'Black' name list is invented here and none is cited, because "
            "inventing one would be a claim about this community's naming that no source in "
            "this corpus makes, and the seed says the opposite."),
        "sources": ["census_1840_chicago_familysearch_images"],
    }


def surname_stock(rows_all, layer_surnames, seed_surnames):
    """The surnames Chicago's own enumerator wrote in 1840, less the ones this town holds.

    A drawn head needs a surname, and the honest stock for one is the naming of this place
    in this decade rather than a general sense of what sounds old. The 1840 Cook County
    sheets read into data/research/census_1840/pages/ carry hundreds of heads of household;
    the stock is their surnames, MINUS every surname the 1835 resident layer already carries
    (so no drawn head reads as a documented family's kin), MINUS the surnames of the four
    Black-headed households the pool is seeded from (so none reads as their kin either), and
    minus every name the reading could not resolve.
    """
    stock = set()
    for row in rows_all:
        parts = [p for p in re.split(r"\s+", row) if p]
        if len(parts) < 2:
            continue
        surname = parts[-1]
        if not re.fullmatch(r"[A-Z][A-Za-z'\-]{2,}", surname):
            continue
        stock.add(surname)
    return sorted(stock - set(layer_surnames) - set(seed_surnames))


def pick_names(pool, pools, layer_names, layer_surnames, sexes, stock):
    base = next(c for c in pools["communities"] if c["id"] == "yankee")
    given = {"male": list(base["given_male"]), "female": list(base["given_female"])}
    chosen = []
    used_surnames, used_full = set(), set(layer_names)
    for i, sex in enumerate(sexes):
        slot = "%s:head:%03d" % (STAGE, i + 1)
        surname = None
        for attempt in range(256):
            candidate = stock[draw(slot + ":surname:%d" % attempt) % len(stock)]
            if candidate in used_surnames:
                continue
            surname = candidate
            break
        if surname is None:
            raise SystemExit("the surname stock is exhausted at head %d" % (i + 1))
        forename = None
        for attempt in range(256):
            candidate = given[sex][draw(slot + ":forename:%d" % attempt) % len(given[sex])]
            if "%s %s" % (candidate, surname) in used_full:
                continue
            forename = candidate
            break
        if forename is None:
            raise SystemExit("the forename stock is exhausted at head %d" % (i + 1))
        used_surnames.add(surname)
        used_full.add("%s %s" % (forename, surname))
        chosen.append({"slot": slot, "forename": forename, "surname": surname, "sex": sex,
                       "seed_surname": slot + ":surname", "seed_forename": slot + ":forename"})
    return chosen


BAND_SPAN = {
    "under 10": ("0-9", 0, 9),
    "10 under 24": ("10-23", 10, 23),
    "24 under 36": ("24-35", 24, 35),
    "36 under 55": ("36-54", 36, 54),
    "55 under 100": ("55-99", 55, 99),
    "100 and upwards": ("100+", 100, 120),
}
BAND_ORDER = [b for _, b, _, _ in BAND_SPAN.items()] if False else list(BAND_SPAN)


def persons_of(vector):
    """A band vector as a list of people, eldest first within each sex."""
    out = []
    for row in vector:
        for _ in range(row["persons"]):
            out.append({"sex": row["sex"], "band": row["band"]})
    out.sort(key=lambda p: (-BAND_SPAN[p["band"]][1], p["sex"]))
    return out


def head_index(people):
    adults = [i for i, p in enumerate(people) if p["band"] in ADULT_BANDS]
    men = [i for i in adults if people[i]["sex"] == "male"]
    return (men or adults or [0])[0]


def claim(value, tier, kind, ident, note, seed, retires, extra=None):
    block = {"value": value, "confidence": tier, "tier": tier,
             "basis": {"kind": kind, "id": ident, "note": note},
             "seed": seed,
             "replaceable_by": {"kind": "person", "match": retires}}
    if extra:
        block.update(extra)
    return block


def deal_trade(slot, sex, keeper):
    if keeper:
        return ("boarding_house_keeper",
                "THE ONE FIRM. This household is dealt more than one adult man, which is a "
                "house where men lodged rather than a family, and its head keeps it. One "
                "such house is minted and no more: T-1187 owns how many boarding houses "
                "the town had against the 42-roof programme.")
    table = TRADES_MALE if sex == "male" else TRADES_FEMALE
    trade = table[draw(slot + ":trade") % len(table)]
    return (trade,
            "An EVEN DEAL over the employments T-1177 names that this layer's occupation "
            "vocabulary actually carries. No source ranks them for this town, so an even "
            "deal is the only apportionment that adds no ranking the record does not carry. "
            "The 1840 industry column marks the one Black-headed Chicago household this "
            "corpus can reach in MANUFACTURES AND TRADES rather than in service, which is "
            "why the men's table is labour and carriage and not domestic work.")


def household_record(ordinal, name, vector_row, keeper):
    people = persons_of(vector_row["vector"])
    head_at = head_index(people)
    slot = "%s:household:%03d" % (STAGE, ordinal)
    head_id = "fb_%s_%s" % (name["surname"].lower(), name["forename"].lower())
    hh_id = "hh_" + head_id
    head_person = people[head_at]
    trade, trade_note = deal_trade(slot, head_person["sex"], keeper)
    vector_cite = ("printed page %s, line %s, FamilySearch image %s"
                   % (vector_row["printed_page"], vector_row["line"],
                      vector_row["familysearch_id"]))
    stands_on = (
        "Caton's six certificates of freedom, August 1833, are the cohort's floor, and this "
        "is one of the six households the bracket's ceiling leaves room for. The SHAPE is "
        "the band vector of a Black-headed Chicago household of 1840 (%s), dealt here as a "
        "structure and never as its people." % vector_cite)
    records = []
    for i, person in enumerate(people):
        is_head = i == head_at
        band_value, low, high = BAND_SPAN[person["band"]]
        pid = head_id if is_head else "%s_m%02d" % (head_id, i + 1)
        display = ("%s %s" % (name["forename"], name["surname"]) if is_head else
                   "A %s of this household, %s (reconstructed, unnamed)"
                   % ({"male": "man", "female": "woman"}[person["sex"]]
                      if person["band"] not in ("under 10", "10 under 24") else
                      {"male": "boy", "female": "girl"}[person["sex"]], band_value))
        record = {
            "id": pid,
            "name": display,
            "relationship": "head" if is_head else "household_member",
            "grade": "reconstructed",
            "sex": person["sex"],
            "age_band": claim(
                band_value, "reconstructed", "model", "census_1840_free_coloured_bands",
                "The 1840 schedule's own band, carried from the composition stock's vector "
                "(%s). A band, never a year: this project writes no age it cannot read."
                % vector_cite,
                slot + ":person:%02d:band" % (i + 1),
                "a source that states this person's age or their birth year",
                {"low": low, "high": high}),
            "occupation": claim(
                trade if is_head else "none_recorded", "reconstructed", "model",
                "1835_black_chicago", trade_note if is_head else
                "NOT DEALT. The 1840 schedule marks an industry against a HOUSEHOLD and "
                "names only its head, so a trade for anybody else here would be invented "
                "whole. T-1189 staffs the businesses and T-1174 owns the women's "
                "employments.",
                slot + ":person:%02d:trade" % (i + 1),
                "a source naming a free Black resident of this town at a trade"),
            "name_basis": claim(
                display, "reconstructed", "model", "1835_invented_name_pools",
                "Drawn from the free_black pool, whose seed is the four Black-headed "
                "households of the 1840 Cook County sheets and whose extension excludes "
                "every surname that seed and this town's attested residents bear."
                if is_head else
                "NOT NAMED, AND THE REASON IS THE SOURCE'S OWN SHAPE. The 1840 schedule "
                "names the head and COUNTS everybody else. A name here would invent the "
                "person and their relation to the head in one stroke, so this record "
                "carries a designation, a sex and a band, and nothing else.",
                slot + ":person:%02d:name" % (i + 1),
                "a source naming a free Black resident of this town"),
            "basis": {
                "kind": "model", "id": "1835_black_chicago",
                "note": stands_on},
            "seed": slot + ":person:%02d" % (i + 1),
            "replaceable_by": {
                "kind": "person",
                "match": "a source naming a free Black resident of Chicago in 1835, who "
                         "would stand in this slot instead"},
            "reconstruction": {
                "stage": STAGE,
                "programme": PROGRAMME,
                "community": "free_black",
                "review_required": True,
                "review_owed_to": (
                    "A reading by Black Chicago historians or community organisations "
                    "before this scene is marked released, as T-1177 asks of every "
                    "under-documented cohort it reconstructs."),
            },
            "resident_subtype": ("reconstructed_free_black_head" if is_head
                                 else "reconstructed_free_black_member"),
            "note": (
                "RECONSTRUCTED, NOT FOUND. No source names this person. What is claimed is "
                "what the bracket carries: that free Black Chicagoans lived in this town on "
                "1 July 1835 — six men of them certificated free before the county court in "
                "August 1833 — and that their households were shaped like the Black-headed "
                "households Chicago's own enumerator counted five years later. Every value "
                "is reproducible from the seeds printed beside it. No figure is drawn (L1)."),
        }
        records.append(record)
    return {
        "id": hh_id,
        "name": "The %s household — free Black Chicago, at the floor of its bracket"
                % name["surname"],
        "division": "unplaced",
        "head": head_id,
        "source_pass": "reconstructed_free_black_household",
        "free_black_household": {
            "ticket": TICKET,
            "parent_ticket": PARENT,
            "stage": STAGE,
            "slot": slot,
            "composition_vector": {
                "familysearch_id": vector_row["familysearch_id"],
                "printed_page": vector_row["printed_page"],
                "line": vector_row["line"],
                "head_as_read_in_1840": vector_row["head_as_read"],
                "free_coloured_persons": vector_row["free_coloured_persons"],
                "bands": vector_row["vector"],
                "what_is_carried": "The SHAPE only — how many people, of which sex, in "
                                   "which band. No name, no age of any individual, no "
                                   "industry mark and no identity crosses from 1840 into "
                                   "this household.",
            },
            "stands_on": stands_on,
            "withdrawn_if": "a reading that names Chicago's free Black residents of 1835, "
                            "or a re-cut of the bracket that no longer leaves room for this "
                            "household; the retirement runs through --build, never by hand",
        },
        "kin_owed": {
            "note": "NO KIN TIE IS CLAIMED. The schedule of 1840 records no relationships "
                    "at all, so everybody below the head is `household_member` and this "
                    "stage writes no wife, no son and no daughter. The families of this "
                    "cohort are owed to T-1170 and T-1171 exactly as every other "
                    "household's are.",
            "seated_by": "T-1170 (named families), T-1171 (modelled families), T-1179 "
                         "(converge)",
        },
        "arrival": {
            "value": None, "confidence": "reconstructed", "tier": "unknown",
            "note": "NOT DRAWN HERE. T-1169 owns the arrival fill, and the circle the trade "
                    "households name holds here too: the arrival model is computed over the "
                    "compiled scene and the scene carries these cards. One bound is on the "
                    "record already — six men were at Chicago in August 1833, two years "
                    "before the scene — and T-1169 is where it is spent.",
            "seated_by": "T-1169 (the arrival fill), T-1179 (converge)",
        },
        "lives_at": {
            "value": None, "confidence": "reconstructed", "tier": "unknown",
            "note": "Not seated. T-1199 seats the reconstructed households on the lot grid "
                    "by the placement policy, and nothing in this corpus says where "
                    "Chicago's free Black residents lived in 1835. The division is "
                    "`unplaced` and stays unplaced until it does.",
        },
        "works_at": {
            "value": None, "confidence": "reconstructed", "tier": "unknown",
            "note": "Not seated. T-1189 staffs the businesses; the one firm this stage "
                    "mints carries its keeper by id.",
        },
        "present_on_scene_date": {
            "value": "present", "confidence": "reconstructed", "tier": "reconstructed",
            "basis": {
                "kind": "rule", "id": "free_black_bracket_1835",
                "note": "Ordered by the bracket, not argued person by person: six free "
                        "coloured men were certificated free at Chicago in August 1833 and "
                        "the town's free Black population of 1840 scales back to 28 on the "
                        "scene date. This household is one of the six the bracket carries.",
            },
            "replaceable_by": {
                "kind": "person",
                "match": "a re-cut bracket that no longer carries this household",
            },
        },
        "persons": records,
        "touches_removal": False,
        "review_required": True,
        "research_note": (
            "WRITTEN BY tools/reconstruct_black_chicago_1835.py (T-1377, of T-1177), the "
            "`free_black` stage of the 1835 resident reconstruction programme. This file is "
            "NOT research and is not a mint output: data/residents/households/ is "
            "re-derived by the mint writers and data/residents/index.json is derived from "
            "that directory, so a reconstruction lives here instead and is overlaid onto "
            "the scene by tools/compile_scene.py. docs/RESEARCH/black_chicago_1835.md is "
            "the page and docs/LIBERTIES.md carries the invention."),
    }


def firm_record(house, name):
    """The one boarding house, as an authored `rcb_` business record."""
    keeper = next(p for p in house["persons"] if p["relationship"] == "head")
    return {
        "id": "rcb_%s_boarding_house" % name["surname"].lower(),
        "register_id": None,
        "name": "%s's boarding house" % name["surname"],
        "provenance": "reconstructed",
        "type": ["other"],
        "trade": None,
        "occupation": "boarding_house_keeper",
        "goods": [],
        "firm_styles": [],
        "proprietors": [{
            "name": keeper["name"],
            "person_id": keeper["id"],
            "role": "proprietor",
            "tier": "reconstructed",
            "basis": ("The head of the one drawn household of this cohort that carries more "
                      "than one adult man. A house of lodging men is the reading its "
                      "composition vector allows and a family is not, so its head keeps it. "
                      "Nobody is named by any source: the keeper is a reconstructed person "
                      "of the free_black stage and this record is graded with them."),
        }],
        "partners": [],
        "staff": [],
        "locations": [{
            "kind": "unplaceable",
            "structure_id": None,
            "street_id": None,
            "face": None,
            "primary": True,
            "tier": "reconstructed",
            "basis": "Nothing in this corpus says where Chicago's free Black residents "
                     "lived or kept house in 1835.",
            "limit_reason": "No source places this house. T-1199 seats the reconstructed "
                            "households and T-1187 owns the boarding-house programme; a "
                            "coordinate written here would be invented twice over.",
        }],
        "dates": {
            "opened": None,
            "closed": None,
            "precision": "unbounded",
            "tier": "reconstructed",
            "basis": "Undated. The cohort's own floor is dated — six free coloured men "
                     "certificated at Chicago in August 1833 — but nothing dates a house.",
        },
        "present_at_scene_date": True,
        "exclusion": None,
        "exclusion_note": None,
        # The business schema's own enum for this field is not the resident layer's
        # vocabulary — it carries `black` where the resident layer carries `free_black` —
        # and reconciling the two is T-1378's, which owns the field and the filter. This
        # record uses the word the schema will accept and the keeper's own card carries
        # `free_black`, so the join is exact whichever side a reader comes from.
        "proprietor_community": "black",
        "customers": [],
        "sources": [],
        "claim_ids": [],
        "liberties": {"survival_required": False, "backdating_required": False},
        "review_required": True,
        "replaceable_by": "A source naming a boarding house kept by a free Black Chicagoan "
                          "in 1835, or a re-cut of the lodging programme (T-1187) that "
                          "orders this house differently.",
    }


def assemble():
    rows = read_1840_free_coloured_households()
    composition = load(COMPOSITION)
    town = load(TOWN)
    bounds = bracket(rows, composition, town)
    pools = load(POOLS)
    layer_names, layer_surnames = attested_surnames()
    pool = build_pool(rows, pools)
    stock = [r for r in rows if r["black_headed"]]
    if len(stock) < 2:
        raise SystemExit("the composition stock has collapsed: %d vectors" % len(stock))

    # Six households, because the floor counts six men and the ceiling leaves room for
    # them: the vectors are dealt in the sheets' own printed order and cycled.
    households_wanted = bounds["floor_persons"]
    deal = [stock[i % len(stock)] for i in range(households_wanted)]
    while deal and sum(r["free_coloured_persons"] for r in deal) > bounds["ceiling_persons"]:
        deal.pop()
    sexes = []
    for row in deal:
        people = persons_of(row["vector"])
        sexes.append(people[head_index(people)]["sex"])
    name_stock = surname_stock(all_1840_head_names(), layer_surnames, pool["seed_surnames"])
    names = pick_names(pool, pools, layer_names, layer_surnames, sexes, name_stock)

    # The one firm: the largest dealt household carrying more than one adult man, and the
    # earliest of them where they tie.
    def adult_men(row):
        return sum(b["persons"] for b in row["vector"]
                   if b["sex"] == "male" and b["band"] in ADULT_BANDS)
    lodging = [i for i, row in enumerate(deal) if adult_men(row) > 1]
    keeper_at = max(lodging, key=lambda i: (deal[i]["free_coloured_persons"], -i)) \
        if lodging else None

    houses = [household_record(i + 1, names[i], row, i == keeper_at)
              for i, row in enumerate(deal)]
    firm = firm_record(houses[keeper_at], names[keeper_at]) if keeper_at is not None else None

    minted_persons = sum(len(h["persons"]) for h in houses)
    men_seated = sum(1 for h in houses for p in h["persons"]
                     if p["sex"] == "male" and p["age_band"]["low"] >= 24)
    pool = dict(pool, surname_stock=name_stock,
                surname_stock_is=(
                    "Every surname the 1840 Cook County sheets read here carry at a name "
                    "confidence above `low`, less every surname the 1835 resident layer "
                    "already holds and less the four Black-headed households' own — %d names." % len(name_stock)),
                given_name_stock_is=(
                    "The ordinary Anglo-American forenames of "
                    "data/reconstruction/1835_invented_name_pools.json, by sex, which is "
                    "what the seed's own four heads show."))
    ledger = {
        "id": "1835_black_chicago",
        "ticket": TICKET,
        "parent_ticket": PARENT,
        "stage": STAGE,
        "generated_by": "tools/reconstruct_black_chicago_1835.py --build",
        "_doc": __doc__.strip(),
        "the_attested_traces": [
            {"trace": "the certificates of freedom, August 1833",
             "says": caton_sentence(),
             "source": "data/residents/households/hh_caton_john_dean.json",
             "what_it_carries": "A dated count of six or seven free coloured men at Chicago "
                                "before a court of record, two years before the scene. It "
                                "names none of them and gives no household, no trade and no "
                                "place of residence."},
            {"trace": "the free coloured households of the 1840 Cook County sheets",
             "says": "%d households in the sheets read here carry a free coloured person, "
                     "%d persons in all; %d of those households carry no free white person "
                     "and are Black-headed."
                     % (len(rows), sum(r["free_coloured_persons"] for r in rows),
                        len([r for r in rows if r["black_headed"]])),
             "source": "data/research/census_1840/pages/",
             "rows": rows,
             "what_it_carries": "Five years after the scene: names of heads, band vectors, "
                                "and nothing about 1835. It is the composition stock and the "
                                "name pool's seed, and it is never evidence of presence."},
            {"trace": "the industry column, printed page 219",
             "says": "The continuation sheet paired to printed page 219 marks the Henson "
                     "household — Black-headed, line 25 — in MANUFACTURES AND TRADES.",
             "source": "data/research/census_1840/pages/33S7-9YYJ-24.json",
             "what_it_carries": "The one occupational fact this corpus holds about a "
                                "Black-headed Chicago household. It is not carried into any "
                                "drawn household; it is why the trade deal may not be "
                                "all-service. The pairing is T-0642's; the left sheet's own "
                                "cells sum to 2 against the continuation's TOTAL of 3 for "
                                "that line, a residual recorded on the page file and not "
                                "resolved here.",
             "reachable_for": "1 of the 4 Black-headed households — the other three sit on "
                              "left sheets whose continuations are unpaired."},
            {"trace": "the count of 1840",
             "says": "53 free coloured persons at Chicago on 1 June 1840, in the bands "
                     "printed in the bracket below.",
             "source": "data/research/census_1840/composition_1840.json",
             "what_it_carries": "The ceiling's numerator. A count of 1840 and of nothing "
                                "else."},
        ],
        "the_bracket": bounds,
        "the_pool": pool,
        "the_composition_stock": stock,
        "the_deal": [
            {"household": h["id"], "head": h["head"], "persons": len(h["persons"]),
             "vector_from": h["free_black_household"]["composition_vector"]["familysearch_id"],
             "printed_page": h["free_black_household"]["composition_vector"]["printed_page"],
             "line": h["free_black_household"]["composition_vector"]["line"],
             "trade": next(p["occupation"]["value"] for p in h["persons"]
                           if p["relationship"] == "head")}
            for h in houses],
        "the_refusals": [
            {"refused": "a name for anybody but a head",
             "why": "The 1840 schedule names the head and counts the rest. A name here would "
                    "invent the person and their relation to the head at once."},
            {"refused": "a kin tie of any kind",
             "why": "The schedule records no relationships. Every member is "
                    "`household_member` and the families are owed to T-1170/T-1171."},
            {"refused": "the trades barber, cook, whitewasher and drayman",
             "why": REFUSED_TRADES},
            {"refused": "a second boarding house",
             "why": "T-1187 owns how many boarding houses the town had against the 42-roof "
                    "programme. This cohort mints one and orders no more."},
            {"refused": "any identity, age or industry mark carried from 1840 into 1835",
             "why": "A source that names a person may never be spent on somebody drawn. The "
                    "vectors carry shape and nothing else."},
            {"refused": "a residence, a division and an arrival year",
             "why": "Nothing in this corpus says where Chicago's free Black residents lived "
                    "in 1835. T-1199 seats them, T-1169 dates them, and `unplaced` is the "
                    "honest division until then."},
        ],
        "totals": {
            "households_minted": len(houses),
            "persons_minted": minted_persons,
            "adult_men_seated": men_seated,
            "floor_persons": bounds["floor_persons"],
            "ceiling_persons": bounds["ceiling_persons"],
            "inside_the_bracket": bounds["floor_persons"] <= minted_persons
                                  <= bounds["ceiling_persons"],
            "floor_met_by_the_draw": men_seated >= bounds["floor_persons"],
            "firms_minted": 1 if firm else 0,
        },
        "minted": [{"file": "black_chicago/%s.json" % h["id"], "household": h["id"],
                    "head": h["head"], "persons": len(h["persons"]), "stage": STAGE,
                    "community": "free_black", "review_required": True}
                   for h in houses],
        "firm": {"file": "authored/%s.json" % firm["id"], "id": firm["id"],
                 "keeper": firm["proprietors"][0]["person_id"]} if firm else None,
    }
    return ledger, houses, firm


def write(ledger, houses, firm):
    MINTED.mkdir(parents=True, exist_ok=True)
    for stale in MINTED.glob("hh_fb_*.json"):
        stale.unlink()
    for house in houses:
        dump(MINTED / ("%s.json" % house["id"]), house)
    (MINTED / "README.md").write_text(README, encoding="utf-8")
    dump(LEDGER, ledger)
    if firm:
        dump(DATA / "businesses" / "authored" / ("%s.json" % firm["id"]), firm)


README = """# `data/residents/black_chicago/`

The free Black households of 1835, written by `tools/reconstruct_black_chicago_1835.py`
(T-1377, of T-1177) and re-derived whole on every `--build`. Do not hand-edit one: the
gate re-runs the generator and refuses drift.

Six households, at the floor of a bracket whose ends are a dated count and a later
census — `data/reconstruction/1835_black_chicago.json` carries both, and
`docs/RESEARCH/black_chicago_1835.md` is the page. Every person is `reconstructed`,
carries `community: free_black` and `review_required`, and names the reading that would
retire them. Only heads are named; the rest carry a designation, because the source this
cohort's shape comes from names heads and counts everybody else.
"""


def cmd_build():
    ledger, houses, firm = assemble()
    write(ledger, houses, firm)
    print("built %d households, %d persons, %d firm(s) — bracket %d..%d"
          % (ledger["totals"]["households_minted"], ledger["totals"]["persons_minted"],
             ledger["totals"]["firms_minted"], ledger["totals"]["floor_persons"],
             ledger["totals"]["ceiling_persons"]))
    return 0


def cmd_check():
    if not LEDGER.exists():
        print("MISSING %s — run --build" % LEDGER)
        return 1
    ledger, houses, firm = assemble()
    failures = []
    if load(LEDGER) != ledger:
        failures.append("%s has drifted from its generator" % LEDGER.name)
    for house in houses:
        path = MINTED / ("%s.json" % house["id"])
        if not path.exists():
            failures.append("missing %s" % path.name)
        elif load(path) != house:
            failures.append("%s has drifted from its generator" % path.name)
    on_disk = {p.name for p in MINTED.glob("hh_fb_*.json")}
    extra = on_disk - {"%s.json" % h["id"] for h in houses}
    if extra:
        failures.append("orphaned card(s): %s" % ", ".join(sorted(extra)))
    if firm:
        path = DATA / "businesses" / "authored" / ("%s.json" % firm["id"])
        if not path.exists():
            failures.append("missing %s" % path.name)
        elif load(path) != firm:
            failures.append("%s has drifted from its generator" % path.name)
    totals = ledger["totals"]
    if not totals["inside_the_bracket"]:
        failures.append("the mint of %d is outside the bracket %d..%d"
                        % (totals["persons_minted"], totals["floor_persons"],
                           totals["ceiling_persons"]))
    if not totals["floor_met_by_the_draw"]:
        failures.append("the draw seats %d adult men against a floor of %d"
                        % (totals["adult_men_seated"], totals["floor_persons"]))
    for failure in failures:
        print("FAIL  %s" % failure)
    if failures:
        return 1
    print("ok  %d households, %d persons, %d adult men against a floor of %d, inside a "
          "ceiling of %d; every card re-derives"
          % (totals["households_minted"], totals["persons_minted"],
             totals["adult_men_seated"], totals["floor_persons"],
             totals["ceiling_persons"]))
    return 0


def cmd_report():
    ledger, houses, firm = assemble()
    bounds = ledger["the_bracket"]
    print("THE BRACKET  floor %d (%s)" % (bounds["floor_persons"], "Caton, August 1833"))
    for scaling in bounds["scalings"]:
        print("             %-38s %d/%d = %.4f  →  %.1f persons in 1835"
              % (scaling["denominator"], bounds["free_coloured_persons_1840"],
                 scaling["persons_1840"], scaling["free_coloured_share"],
                 scaling["scaled_to_1835"]))
    print("             ceiling %d" % bounds["ceiling_persons"])
    print()
    print("THE STOCK    %d Black-headed households in the sheets read" %
          len(ledger["the_composition_stock"]))
    for row in ledger["the_composition_stock"]:
        print("             p%-4s l%-3s %-20s %d persons"
              % (row["printed_page"], row["line"], row["head_as_read"],
                 row["free_coloured_persons"]))
    print()
    print("THE DEAL")
    for row in ledger["the_deal"]:
        print("             %-28s %d persons  %-20s from p%s l%s"
              % (row["head"], row["persons"], row["trade"], row["printed_page"],
                 row["line"]))
    print()
    print("THE FIRM     %s" % (firm["id"] if firm else "none"))
    print("TOTALS       %s" % json.dumps(ledger["totals"]))
    return 0


def cmd_self_test():
    failures = []

    def ok(label, condition):
        print("   self-test | %s   %s" % ("ok  " if condition else "FAIL", label))
        if not condition:
            failures.append(label)

    ledger, houses, firm = assemble()
    names = [p["name"] for h in houses for p in h["persons"]]
    heads = [p for h in houses for p in h["persons"] if p["relationship"] == "head"]
    layer_names, layer_surnames = attested_surnames()

    ok("no drawn head bears a name the layer already carries",
       not {h["name"] for h in heads} & layer_names)
    ok("no drawn head bears a surname the layer already carries",
       not {h["name"].split()[-1] for h in heads} & layer_surnames)
    ok("no drawn head bears a surname of the 1840 households the pool is seeded from",
       not {h["name"].split()[-1] for h in heads} & set(ledger["the_pool"]["seed_surnames"]))
    ok("no two drawn heads share a surname",
       len({h["name"].split()[-1] for h in heads}) == len(heads))
    ok("nobody below a head is named",
       all("(reconstructed, unnamed)" in p["name"]
           for h in houses for p in h["persons"] if p["relationship"] != "head"))
    ok("every person is graded reconstructed",
       all(p["grade"] == "reconstructed" for h in houses for p in h["persons"]))
    ok("every person carries community free_black and review_required",
       all(p["reconstruction"]["community"] == "free_black"
           and p["reconstruction"]["review_required"]
           for h in houses for p in h["persons"]))
    ok("every person carries a seed and a retirement rule",
       all(p["seed"] and p["replaceable_by"]["match"]
           for h in houses for p in h["persons"]))
    ok("no household claims a kin tie",
       all(p["relationship"] in ("head", "household_member")
           for h in houses for p in h["persons"]))
    ok("no household is placed", all(h["lives_at"]["value"] is None for h in houses))
    ok("the mint sits inside its own bracket", ledger["totals"]["inside_the_bracket"])
    ok("the draw seats the floor's six men without forcing them",
       ledger["totals"]["floor_met_by_the_draw"])
    ok("the trade deal is not all service",
       any(p["occupation"]["value"] in TRADES_MALE + ["boarding_house_keeper"]
           for p in heads))
    ok("no refused trade reaches a card",
       not {p["occupation"]["value"] for p in heads} & set(REFUSED_TRADES))
    ok("exactly one firm is minted", ledger["totals"]["firms_minted"] == 1)
    ok("the firm's keeper is a person this stage mints",
       firm is None or firm["proprietors"][0]["person_id"] in {p["id"] for p in heads})
    ok("the firm is unplaced and reviewable",
       firm is None or (firm["locations"][0]["kind"] == "unplaceable"
                        and firm["review_required"]))
    ok("every id is unique", len(names) == len({p["id"] for h in houses
                                                for p in h["persons"]}))
    ok("the build is reproducible", assemble()[0] == ledger)

    print("   self-test | %d failure(s)" % len(failures))
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--self-test", action="store_true", dest="self_test")
    args = parser.parse_args()
    if args.build:
        return cmd_build()
    if args.check:
        return cmd_check()
    if args.report:
        return cmd_report()
    if args.self_test:
        return cmd_self_test()
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
