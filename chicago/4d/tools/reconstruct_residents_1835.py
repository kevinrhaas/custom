#!/usr/bin/env python3
"""T-1167: the ONE writer of a `reconstructed` resident, and its programme's gate.

`grade: reconstructed` means a person the sources do not name, drawn from the
population model to fill a count the town demonstrably needs. The owner retired the
previous reconstructed population on 2026-09-02 because nothing said, in one place,
what had been invented or what would replace it, and ruled that it comes back only
under an explicit programme file. That file is
`data/reconstruction/1835_resident_reconstruction_programme.json`; this tool is the
only thing allowed to act on it.

THE BOUNDARY, IN ONE LINE. Every research writer of `data/residents/` calls
`tools/refuse_reconstructed_grade.refuse()` and may emit only `attested` or
`inferred`. This tool does not call it. That asymmetry IS the rule, it is asserted
from both sides — `refuse_reconstructed_grade.py --check` proves the four writers
still carry their call, and `--self-test` below proves this one is held to the
record contract instead — and neither half is a comment.

A STAGE IS A TICKET. Bands 3A-3C each own one stage of one deterministic build, so
the whole reconstructed layer re-derives from the programme rather than accreting.
`--stage <key> --build` runs one; `--check` re-derives every IMPLEMENTED stage and
holds the committed layer to the record contract; `--self-test` runs the mutation
cases. No stage is implemented by T-1167 itself: this ticket writes no person, and
`--build` says so rather than inventing a default.

  python3 tools/reconstruct_residents_1835.py --list
  python3 tools/reconstruct_residents_1835.py --stage attribute_fill_sex_age --build
  python3 tools/reconstruct_residents_1835.py --check
  python3 tools/reconstruct_residents_1835.py --self-test
"""

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_attribute_tiers import BASIS_KINDS, REPLACEABLE_KINDS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROGRAMME = ROOT / "data" / "reconstruction" / "1835_resident_reconstruction_programme.json"
HOUSEHOLDS = ROOT / "data" / "residents" / "households"
RETIRED = ROOT / "data" / "reconstruction" / "1835_inferred_household_programme.json"
NAME_POOLS = ROOT / "data" / "reconstruction" / "1835_invented_name_pools.json"

RECONSTRUCTED = "reconstructed"
# The stage that alone may write a Native or Metis reconstruction (owner, 2026-09-17).
UNDERDOCUMENTED_STAGE = "underdocumented"
# Communities whose reconstruction is confined to that stage and carries the review.
REVIEWED_COMMUNITIES = ("native", "potawatomi", "metis", "métis", "indigenous")
# The id a reconstructed person's own record must wear, so a grep finds every invention.
INVENTED_PERSON_PREFIX = "rc_"
READMISSION_PASS = "reconstructed_readmission"


# --------------------------------------------------------------------------
# the programme
# --------------------------------------------------------------------------

def load_programme() -> dict:
    return json.loads(PROGRAMME.read_text(encoding="utf-8"))


def stages(prog: dict) -> dict:
    return {s["key"]: s for s in prog.get("stages", [])}


def seed_for(household_id: str, bucket: str) -> str:
    """The seed a reader can retype. See the programme's `seed_rule`."""
    return f"{household_id}:{bucket}"


def draw(seed: str) -> int:
    """The integer a seed draws. Deterministic across runs, machines and Pythons."""
    return int.from_bytes(hashlib.blake2s(seed.encode("utf-8"), digest_size=8).digest(), "big")


# --------------------------------------------------------------------------
# the record contract — what a reconstructed person owes
# --------------------------------------------------------------------------

def check_reconstructed_person(where: str, person: dict, stage_keys, error) -> None:
    """Refuse a reconstructed person that cannot show its working.

    `validate.py` holds the same contract over the committed layer; this is the
    writer's own copy so a stage is refused BEFORE it writes rather than after.
    """
    basis = person.get("basis")
    if not isinstance(basis, dict):
        error(where, "a reconstructed person requires a `basis` naming the model row or the "
                     "rule it was drawn from")
    else:
        if basis.get("kind") not in BASIS_KINDS:
            error(where, f"basis.kind {basis.get('kind')!r} is not one of {sorted(BASIS_KINDS)}")
        if not str(basis.get("id") or "").strip():
            error(where, "basis.id must name the model row or the rule")
        if not str(basis.get("note") or "").strip():
            error(where, "basis.note must state why this person follows from that basis")

    kind = (basis or {}).get("kind") if isinstance(basis, dict) else None
    seed = person.get("seed")
    if kind == "model" and not str(seed or "").strip():
        error(where, "a person DRAWN from a model requires the `seed` that redraws them - a "
                     "draw nobody can reproduce is not a reconstruction")
    if kind == "rule" and seed is not None:
        error(where, "a person argued from a rule carries no `seed`; nothing was drawn")

    rep = person.get("replaceable_by")
    if not isinstance(rep, dict):
        error(where, "a reconstructed person requires `replaceable_by` saying what evidence "
                     "would retire them")
    else:
        if rep.get("kind") not in REPLACEABLE_KINDS:
            error(where, f"replaceable_by.kind {rep.get('kind')!r} is not one of "
                         f"{sorted(REPLACEABLE_KINDS)}")
        if not str(rep.get("match") or "").strip():
            error(where, "replaceable_by.match must say which evidence retires this person")

    rc = person.get("reconstruction")
    if not isinstance(rc, dict) or rc.get("stage") not in stage_keys:
        error(where, f"a reconstructed person must name the programme stage that wrote them, "
                     f"one of {sorted(stage_keys)} - a person no stage claims is a person the "
                     f"programme cannot re-derive")
        return

    community = str(rc.get("community") or "").strip().lower()
    if community in REVIEWED_COMMUNITIES:
        if rc.get("stage") != UNDERDOCUMENTED_STAGE:
            error(where, f"a {community} reconstruction may be written ONLY by stage "
                         f"'{UNDERDOCUMENTED_STAGE}' (T-1177), not by '{rc.get('stage')}'")
        if rc.get("review_required") is not True or rc.get("touches_removal") is not True:
            error(where, f"a {community} reconstruction carries review_required and "
                         f"touches_removal, both true - AGENTS.md's Indigenous-history review")


def check_invented_name(where: str, person: dict, taken_names: set, error) -> None:
    """An invented name may never be a real person's name, nor outrank the invention."""
    pid = str(person.get("id") or "")
    if not pid.startswith(INVENTED_PERSON_PREFIX):
        return  # a re-admission under a read name; it is not invented and owes no pool
    name = " ".join(str(person.get("name") or "").split()).lower()
    if name and name in taken_names:
        error(where, f"the invented name {person.get('name')!r} is already borne by an attested "
                     f"or inferred person - a reader who met that name as a finding would meet "
                     f"it again as an invention")
    basis = person.get("name_basis")
    if not isinstance(basis, dict) or basis.get("confidence") != RECONSTRUCTED:
        error(where, "an invented name carries a name_basis graded 'reconstructed' naming the "
                     "pool it came from")


# --------------------------------------------------------------------------
# reading the committed layer
# --------------------------------------------------------------------------

def read_layer():
    """(reconstructed persons as (where, person), names borne by real people)."""
    reconstructed, real_names = [], set()
    for path in sorted(HOUSEHOLDS.glob("hh_*.json")):
        try:
            rec = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path.name}: {exc}")
        for person in rec.get("persons") or []:
            where = f"{path.name}:{person.get('id')}"
            if person.get("grade") == RECONSTRUCTED:
                reconstructed.append((where, person))
            else:
                name = " ".join(str(person.get("name") or "").split()).lower()
                if name:
                    real_names.add(name)
    return reconstructed, real_names


# --------------------------------------------------------------------------
# stage `attribute_fill_arrival` (T-1169) — arrival year, origin and reason
#
# The first stage of this programme that writes anything, and it writes no PERSON:
# it fills three attribute blocks on households that already exist, at the strongest
# tier each household's own evidence allows. Three legs, in order:
#
#   1. THE EVIDENCE LEG. The Old Settlers roll gives an arrival year and a birthplace
#      for the 46 of its 327 rows the crosswalk merged into this layer. Those are
#      spent onto exactly the cards they name, at `inferred` — never `attested`,
#      because the roll is a recollection registered in 1879 and its own
#      `arrival_year_basis` says it dates the claim and does not prove it.
#   2. THE DRAWN LEG. An arrival YEAR for the 1,196 households whose `arrival` holds
#      a `not_later_than` BOUND and no reading, drawn from the known layer's own
#      year distribution truncated at that bound; and an origin region drawn from the
#      roll's birthplace distribution. `basis.kind` is `model` and each carries the
#      seed that redraws it.
#   3. THE ARGUED LEG. A reason for coming, from the household's own recorded trade
#      where it has one and from its arrival season where it does not. `basis.kind`
#      is `rule` and there is no seed, because nothing was drawn — see the programme
#      file's `arrival_fill.the_argued_leg.WHY_IS_NOT_APPORTIONED` for why this stage
#      refuses to build the cohort x trade table T-1169 asked for.
#
# EVERY BLOCK THIS STAGE WRITES CARRIES `written_by_stage`. That marker is the whole
# of how `--check` re-derives: a block the stage owns is recomputed and compared, and
# a block it does not own is one some earlier reading put there and is not touched.
# Without it `--build` would be a one-way write — the second run would see a filled
# `origin` and skip it, and nothing could ever say the committed value still follows
# from the model row it claims.
# --------------------------------------------------------------------------

ARRIVAL_STAGE = "attribute_fill_arrival"
MARKER = "written_by_stage"
OLD_SETTLERS = ROOT / "data" / "research" / "old_settlers" / "people.json"
TOWN_MODEL = ROOT / "data" / "reconstruction" / "1835_town_model.json"
OLD_SETTLER_SOURCE = "calumet_club_early_chicago_1879"
SCENE_YEAR = 1835

# What retires a value this stage writes, one row an attribute. Imported in spirit
# from migrate_attribute_tiers.REPLACEABLE_BY, restated here for the two keys this
# stage writes that that table does not name.
ARRIVAL_REPLACEABLE = {
    "arrival_year": ("person", "a dated source that says which year this household came to "
                               "Chicago"),
    "origin": ("person", "a source that says where this household came from"),
    "reason_for_coming": ("person", "a source that says why this household came, or a "
                                    "committed source that apportions the town's arrivals "
                                    "between the land sales, the canal and the harbour works"),
}


def town_model_table(name: str) -> dict:
    model = json.loads(TOWN_MODEL.read_text(encoding="utf-8"))
    section = next(s for s in model["sections"] if s["key"] == "arrival_and_origin")
    return section["tables"][name]


def pick(seed: str, rows) -> str:
    """One label from `[(label, weight), ...]`, by the seed and nothing else.

    The rows are sorted by label before the walk, so the draw does not depend on the
    order a table happens to be written in — a table re-ordered by a later edit must
    not silently re-draw the whole town.
    """
    rows = sorted(((label, int(w)) for label, w in rows if int(w) > 0), key=lambda r: r[0])
    total = sum(w for _, w in rows)
    if total <= 0:
        raise ValueError(f"nothing to draw from for seed {seed!r}")
    n = draw(seed) % total
    for label, w in rows:
        if n < w:
            return label
        n -= w
    return rows[-1][0]


def old_settler_facts() -> dict:
    """`{household_id: row}` for the roll's rows the crosswalk MERGED into this layer.

    ELEVEN of the thirty-five merged households are named by more than one row, because
    a man who registered at the Calumet Club in 1879 also appears on the 1882 guest and
    death lists — and only the 1879 REGISTRY row carries a date of arrival and a
    birthplace, which is what `arrival_as_read` marks. So the rows are not simply
    overwritten in file order: the fact-bearing row wins, and ties break on the row id
    so the choice is the same on every machine. (No household in this roll has two
    registry rows, and no two registry rows of one household disagree on the year —
    checked, and if that ever changes this picks the earlier and the disagreement
    becomes visible as a re-derivation failure rather than a silent flip.)
    """
    out: dict = {}
    for row in sorted(json.loads(OLD_SETTLERS.read_text(encoding="utf-8"))["people"],
                      key=lambda r: str(r.get("id"))):
        link = row.get("residents_layer") or {}
        if link.get("outcome") != "merged":
            continue
        hid = link.get("household_id")
        if not hid:
            continue
        held = out.get(hid)
        if held is None:
            out[hid] = row
            continue
        # the fact-bearing row wins; between two of them, the earlier arrival
        held_dated = bool(held.get("arrival_as_read"))
        row_dated = bool(row.get("arrival_as_read"))
        if row_dated and not held_dated:
            out[hid] = row
        elif row_dated and held_dated and (row.get("arrival_year") or 9999) < (
                held.get("arrival_year") or 9999):
            out[hid] = row
    return out


def bound_year(arrival: dict):
    """The latest year the household's arrival block allows, or None if it is a reading."""
    if not isinstance(arrival, dict) or arrival.get("precision") != "not_later_than":
        return None
    value = str(arrival.get("value") or "")
    try:
        return int(value[:4])
    except ValueError:
        return None


def read_year(arrival):
    """The year an arrival block READS, or None when it holds only a bound."""
    if not isinstance(arrival, dict) or arrival.get("precision") == "not_later_than":
        return None
    try:
        return int(str(arrival.get("value") or "")[:4])
    except ValueError:
        return None


def head_trade(hh: dict):
    head = hh.get("head")
    for person in hh.get("persons") or []:
        if person.get("id") == head:
            value = (person.get("occupation") or {}).get("value")
            return value if value not in (None, "", "none_recorded") else None
    return None


def surname_community(hh: dict, pools: dict):
    """The ONE non-yankee pool that carries this household's surname, or None.

    The pools are naming stock, not a census of who bore what name, so this is a weak
    signal and it is used only where it is unambiguous: a surname two pools carry says
    nothing, and the yankee pool's communities are the drawn table's own regions.
    """
    surname = hh["id"][len("hh_"):].split("_")[0].lower()
    hits = [c["id"] for c in pools["communities"]
            if surname in {s.lower() for s in c.get("surnames") or []}]
    if len(hits) != 1 or hits[0] == "yankee":
        return None
    return hits[0]


def trade_reason(recipe: dict, trade: str):
    for key, group in recipe["trade_reasons"].items():
        if trade in group["trades"]:
            return key, group["value"]
    return None, None


def cohort_reason(recipe: dict, year: int):
    for row in recipe["cohort_reasons"]:
        if year <= row["through"]:
            return row["value"]
    return recipe["cohort_reasons"][-1]["value"]


def reconstructed_block(key: str, value, note: str, basis: dict, seed=None) -> dict:
    kind, match = ARRIVAL_REPLACEABLE[key]
    block = {
        "value": value,
        "confidence": RECONSTRUCTED,
        "tier": RECONSTRUCTED,
        "note": note,
        "basis": basis,
    }
    if seed is not None:
        block["seed"] = seed
    block["replaceable_by"] = {"kind": kind, "match": match}
    block[MARKER] = ARRIVAL_STAGE
    return block


def plan_household(hh: dict, recipe: dict, years: list, regions: list, pools: dict,
                   settler) -> dict:
    """The blocks this stage would write on ONE household. Pure; `--check` re-runs it."""
    hid = hh["id"]
    planned = {}
    refusal = recipe["the_refusal_every_reason_carries"]

    # --- the arrival year -------------------------------------------------
    bound = bound_year(hh.get("arrival"))
    settler_year = (settler or {}).get("arrival_year")
    already_read = read_year(hh.get("arrival"))
    if settler and isinstance(settler_year, int) and already_read is not None:
        # THE ARRIVAL IS ALREADY READ, so the roll adds a year nobody needs — unless it
        # DISAGREES with the reading, and then the disagreement is the thing worth
        # recording. Seven of the eight merged settlers whose household carries a read
        # arrival corroborate it exactly; writing seven weaker duplicates of an attested
        # value to surface the eighth would bury it. So only the eighth gets a block, at
        # the layer's own year, saying which statement lost and why.
        if settler_year != already_read:
            planned["arrival_year"] = {
                "value": already_read,
                "confidence": "inferred",
                "tier": "inferred",
                "note": (
                    f"TWO STATEMENTS, AND THE CONTEMPORARY ONE WINS. This household's arrival "
                    f"block reads {already_read} from the evidence that put it in this layer; "
                    f"the same man registered "
                    f"“{settler.get('arrival_as_read') or settler_year}” at the Calumet Club on "
                    f"the roll of 1879. The year carried here is the layer's, because a "
                    f"recollection set down forty-four years later does not outrank a record "
                    f"made nearer the time — and the roll's row is kept as it was read in "
                    f"data/research/old_settlers/people.json rather than corrected to agree."),
                MARKER: ARRIVAL_STAGE,
            }
    elif settler and isinstance(settler_year, int) and settler_year <= SCENE_YEAR:
        planned["arrival_year"] = {
            "value": settler_year,
            "confidence": "inferred",
            "tier": "inferred",
            "note": (
                f"THE MAN'S OWN RECOLLECTION, NOT A CONTEMPORARY RECORD. He registered at the "
                f"Calumet Club on the roll of 1879 and gave "
                f"{settler.get('arrival_as_read') or settler_year} as his date of coming to "
                f"Chicago — forty-four years after the fact. The roll's own "
                f"`arrival_year_basis` says it dates the claim and does not prove it, so the "
                f"year is carried at `inferred` and the household's `arrival` block keeps the "
                f"bound the contemporary evidence sets."),
            "sources": [OLD_SETTLER_SOURCE],
            MARKER: ARRIVAL_STAGE,
        }
    elif bound is not None:
        rows = [(str(r["year"]), r["people"]) for r in years if r["year"] <= bound]
        seed = seed_for(hid, "arrival_year")
        drawn = int(pick(seed, rows))
        # A REFUSAL THE CARD KEEPS. Three merged Old Settlers registered an arrival
        # LATER than the scene — Adams 1837, Campbell 1836, Couch 1836 — while the
        # contemporary evidence that put them in this layer bounds them at or before
        # 1 July 1835. The roll loses, because it is a recollection of 1879 and the
        # bound is a record made at the time; but a refusal nobody writes down is one
        # the next reader re-argues, so the block that overrides it says that it did.
        refused = ""
        if isinstance(settler_year, int) and settler_year > SCENE_YEAR:
            refused = (f" THE ROLL'S OWN YEAR IS REFUSED HERE: this man registered "
                       f"“{settler.get('arrival_as_read') or settler_year}” at the Calumet Club "
                       f"in 1879, which is after the scene date, and the contemporary evidence "
                       f"that put this household in the 1835 layer bounds it at "
                       f"{hh['arrival'].get('value')}. A recollection set down forty-four years "
                       f"later does not outrank a record made at the time, and the roll's row is "
                       f"kept in data/research/old_settlers/people.json rather than corrected.")
        planned["arrival_year"] = reconstructed_block(
            "arrival_year", drawn,
            (f"DRAWN, NOT READ. The household's arrival block holds a BOUND — somebody was here "
             f"by {hh['arrival'].get('value')} and no source says when they came — so the year "
             f"is drawn from the arrival years the known layer records, truncated at that bound "
             f"and renormalised. It says what a household of this bound most likely was, and "
             f"nothing whatever about this household.{refused}"),
            {"kind": "model", "id": "arrival",
             "note": (f"data/reconstruction/1835_town_model.json#arrival_and_origin.tables."
                      f"arrival_year_of_the_known_layer, restricted to years at or before "
                      f"{bound}.")},
            seed=seed)

    # --- where they came from ---------------------------------------------
    birthplace = (settler or {}).get("birthplace_as_read")
    community = surname_community(hh, pools)
    if birthplace:
        planned["origin"] = {
            "value": birthplace,
            "confidence": "inferred",
            "tier": "inferred",
            "note": (
                f"A BIRTHPLACE, WHICH IS NOT THE SAME CLAIM. The Calumet Club roll of 1879 gives "
                f"“{birthplace}” as where this man was BORN; this field asks where the household "
                f"came FROM, and a generation that moved west in stages frequently did not come "
                f"from the state it was born in. It is carried as the best statement of origin "
                f"the sources make about this household and not as a last residence."),
            "sources": [OLD_SETTLER_SOURCE],
            MARKER: ARRIVAL_STAGE,
        }
    elif community:
        planned["origin"] = reconstructed_block(
            "origin", recipe["community_origins"][community],
            (f"ARGUED FROM THE NAME, AND A SURNAME IS NOT A NATIONALITY. This household's "
             f"surname is carried by the {community} pool in "
             f"data/reconstruction/1835_invented_name_pools.json and by no other pool, and that "
             f"pool's `evidence` field states what this dataset attests about who bore those "
             f"names in this town. {recipe['community_origins_note']}"),
            {"kind": "rule", "id": "origin_from_surname_community",
             "note": ("The one community pool that carries this surname points at an origin "
                      "more sharply than a draw over a roll of seventy births does.")})
    else:
        seed = seed_for(hid, "origin_region")
        region = pick(seed, [(r["region"], r["people"]) for r in regions])
        planned["origin"] = reconstructed_block(
            "origin", recipe["origin_regions"][region],
            ("DRAWN FROM A SURVIVORSHIP SAMPLE. No source says where this household came from. "
             "The region is drawn from the birthplaces of the seventy Old Settlers who "
             "registered an arrival at or before 1835 — a self-selected roll set down "
             "forty-four years later that over-represents the men who stayed and prospered, as "
             "the town model's own open questions say. It is the only origin distribution this "
             "project holds and this value is drawn from it, not measured."),
            {"kind": "model", "id": "origin",
             "note": ("data/reconstruction/1835_town_model.json#arrival_and_origin.tables."
                      "birthplace_of_the_old_settlers_who_came_by_1835.")},
            seed=seed)

    # --- why they came ----------------------------------------------------
    trade = head_trade(hh)
    group, value = trade_reason(recipe, trade) if trade else (None, None)
    if value:
        planned["reason_for_coming"] = reconstructed_block(
            "reason_for_coming", value,
            (f"ARGUED FROM THIS HOUSEHOLD'S OWN RECORDED TRADE, WHICH IS NOT ITS MOTIVE. The "
             f"head is recorded as {trade.replace('_', ' ')}, and this names the documented "
             f"draw that trade answered in this town in this decade. It does not claim to know "
             f"why these people came. {refusal}"),
            {"kind": "rule", "id": "reason_from_recorded_trade",
             "note": (f"arrival_fill.trade_reasons.{group} — the head's recorded trade is "
                      f"evidence about this household, and the draw it answered is the reason "
                      f"the record will carry until a source states one.")})
    else:
        # The season this household is argued from, strongest statement of it first:
        # the year this stage just wrote, then the arrival block's own reading, then
        # the bound. A household whose arrival IS a reading is argued from that
        # reading and not from the scene year.
        ay = planned.get("arrival_year")
        year = ay["value"] if ay is not None else read_year(hh.get("arrival"))
        if year is None:
            year = bound if bound is not None else SCENE_YEAR
        planned["reason_for_coming"] = reconstructed_block(
            "reason_for_coming", cohort_reason(recipe, int(year)),
            (f"ARGUED FROM THE SEASON AND NOTHING ELSE. No trade is recorded for this household "
             f"and no source says why it came; the only thing the evidence gives is when it was "
             f"here by. This states the draws that were operating in that season and chooses "
             f"among them nowhere. {refusal}"),
            {"kind": "rule", "id": "reason_from_arrival_cohort",
             "note": (f"arrival_fill.cohort_reasons — the household's arrival year "
                      f"({year}) is the only thing about it this value rests on.")})

    return planned


def owned(block) -> bool:
    return isinstance(block, dict) and block.get(MARKER) == ARRIVAL_STAGE


def writable(hh: dict, key: str) -> bool:
    """A key this stage may write: one it already owns, or one nothing has asserted."""
    block = hh.get(key)
    if block is None:
        return True
    if owned(block):
        return True
    return not isinstance(block, dict) or block.get("value") in (None, "")


def arrival_fill_plan(prog: dict):
    """`[(path, record, planned_blocks)]` over the whole layer. Reads; writes nothing."""
    recipe = prog["arrival_fill"]
    years = town_model_table("arrival_year_of_the_known_layer")["rows"]
    regions = town_model_table("birthplace_of_the_old_settlers_who_came_by_1835")["rows"]
    pools = json.loads(NAME_POOLS.read_text(encoding="utf-8"))
    settlers = old_settler_facts()

    out = []
    for path in sorted(HOUSEHOLDS.glob("hh_*.json")):
        hh = json.loads(path.read_text(encoding="utf-8"))
        planned = plan_household(hh, recipe, years, regions, pools, settlers.get(hh["id"]))
        planned = {k: v for k, v in planned.items() if writable(hh, k)}
        # A KEY THE PLAN NO LONGER PRODUCES AND THE RECORD STILL CARRIES. The stage owns
        # it, so it is the stage's to withdraw: without this a rule that stops writing a
        # block leaves every block it ever wrote behind, and `--check` would keep passing
        # a value the programme can no longer derive. That is exactly the failure the
        # 2026-09-02 retirement was about, one attribute down.
        stale = [k for k in recipe["writes"] if k not in planned and owned(hh.get(k))]
        out.append((path, hh, planned, stale))
    return out


def place(hh: dict, planned: dict, stale=()) -> dict:
    """The record with the planned blocks in it, `arrival_year` seated after `arrival`."""
    out = {}
    for key, value in hh.items():
        if key in stale:
            continue
        out[key] = planned.get(key, value)
        if key == "arrival" and "arrival_year" in planned:
            out["arrival_year"] = planned["arrival_year"]
    for key, value in planned.items():
        if key not in out:
            out[key] = value
    return out


def cmd_build_arrival(prog: dict) -> int:
    counts, written, withdrawn = {}, 0, 0
    for path, hh, planned, stale in arrival_fill_plan(prog):
        if not planned and not stale:
            continue
        withdrawn += len(stale)
        for key, block in planned.items():
            counts[f"{key}:{block['tier']}"] = counts.get(f"{key}:{block['tier']}", 0) + 1
        text = json.dumps(place(hh, planned, stale), indent=1, ensure_ascii=False) + "\n"
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")
            written += 1
    print(f"  built  {ARRIVAL_STAGE}: {written} household file(s) rewritten"
          + (f", {withdrawn} stale block(s) withdrawn" if withdrawn else ""))
    for key in sorted(counts):
        print(f"         {key:<34} {counts[key]}")
    return 0


def check_arrival_fill(prog: dict, error) -> None:
    """Re-derive the stage and hold the committed layer to it, block for block."""
    for path, hh, planned, stale in arrival_fill_plan(prog):
        for key in stale:
            error(f"{path.name}:{key}", f"stage '{ARRIVAL_STAGE}' no longer derives this block "
                                        f"and the record still carries it - run --stage "
                                        f"{ARRIVAL_STAGE} --build to withdraw it")
        for key, block in planned.items():
            committed = hh.get(key)
            if not owned(committed):
                error(f"{path.name}:{key}", f"stage '{ARRIVAL_STAGE}' fills this attribute and "
                                            f"the committed record does not carry its mark - run "
                                            f"--stage {ARRIVAL_STAGE} --build")
            elif committed != block:
                error(f"{path.name}:{key}", f"the committed value does not re-derive from the "
                                            f"programme - a draw that cannot be reproduced is "
                                            f"not a reconstruction. Run --stage "
                                            f"{ARRIVAL_STAGE} --build")
# the stages, and the modules that build them
# --------------------------------------------------------------------------
#
# A STAGE IS A TICKET, and a stage large enough to need its own measurement, its own
# model file and its own gate gets its own module rather than another thousand lines
# here. The programme file names the module in `built_by`; this table is the writer's
# own copy, and `--check` holds the two together so a stage cannot be marked implemented
# with nothing behind it.

def _build_attribute_fill_sex_age() -> int:
    import reconstruct_sex_age
    return reconstruct_sex_age.build()


def _check_attribute_fill_sex_age() -> int:
    import reconstruct_sex_age
    return reconstruct_sex_age.check()


# T-1169's arrival fill predates this table and lives in this module rather than one of
# its own -- it writes three attribute blocks and no person, which is not the thousand
# lines the rule above is about. It registers here all the same: the table is what
# `--check` holds the programme file against, so a stage outside it reads as a stage with
# nothing behind it.
def _build_attribute_fill_arrival() -> int:
    return cmd_build_arrival(load_programme())


STAGE_BUILDERS = {"attribute_fill_sex_age": _build_attribute_fill_sex_age,
                  ARRIVAL_STAGE: _build_attribute_fill_arrival}
STAGE_CHECKERS = {"attribute_fill_sex_age": _check_attribute_fill_sex_age}


# --------------------------------------------------------------------------
# modes
# --------------------------------------------------------------------------

def cmd_list(prog: dict) -> int:
    print(f"{prog['id']} - {len(prog['stages'])} stage(s), written by {prog['written_by']}")
    for s in prog["stages"]:
        mark = "built" if s.get("implemented") else "not yet"
        print(f"  {s['key']:<26} {s['ticket']}  [{mark}]  {s['title']}")
    ob = prog["model_inputs"]["order_book"]
    if not (ROOT / ob["file"]).exists():
        print(f"\n  the order book ({ob['ticket']}) has not landed: {ob['file']}")
        print("  no stage may BUILD until it does - a reconstruction with no quota has "
              "nothing to stop at.")
    return 0


def cmd_build(prog: dict, key: str) -> int:
    table = stages(prog)
    if key not in table:
        print(f"FAIL unknown stage '{key}'. Known: {', '.join(sorted(table))}", file=sys.stderr)
        return 2
    stage = table[key]
    ob = prog["model_inputs"]["order_book"]
    if not (ROOT / ob["file"]).exists():
        print(f"REFUSED stage '{key}' ({stage['ticket']}): the order book has not landed "
              f"({ob['file']}, {ob['ticket']}). It is the quota, and a reconstruction with no "
              f"quota has nothing to stop at.", file=sys.stderr)
        return 1
    if not stage.get("implemented"):
        print(f"REFUSED stage '{key}': {stage['ticket']} has not been built yet. T-1167 opened "
              f"the programme and this writer; it deliberately writes no person. Implement the "
              f"stage in {stage['ticket']} and set `implemented` in the programme file.",
              file=sys.stderr)
        return 1
    builder = STAGE_BUILDERS.get(key)
    if builder is None:
        print(f"FAIL stage '{key}' is marked implemented but carries no build - the programme "
              f"file and this writer disagree", file=sys.stderr)
        return 2
    return builder()


def cmd_check(prog: dict) -> int:
    problems: list[str] = []

    def error(where, msg):
        problems.append(f"{where}: {msg}")

    table = stages(prog)

    # the programme is internally answerable
    if prog.get("written_by") != "tools/reconstruct_residents_1835.py":
        error("programme", "written_by does not name this tool")
    rows = prog["model_inputs"]["rows"]
    model = ROOT / prog["model_inputs"]["town_model"]
    if not model.exists():
        error("programme", f"town model {prog['model_inputs']['town_model']} is missing")
    for stage in prog["stages"]:
        for row in stage["draws_from"]:
            if row not in rows:
                error(f"stage {stage['key']}", f"draws from '{row}', which model_inputs.rows "
                                               f"does not define")
    if UNDERDOCUMENTED_STAGE not in table:
        error("programme", f"no '{UNDERDOCUMENTED_STAGE}' stage - the constraint that confines "
                           f"a Native or Metis reconstruction has nothing to name")
    for path in (NAME_POOLS, RETIRED):
        if not path.exists():
            error("programme", f"{path.name} is missing")

    # the retired programme stays retired
    if RETIRED.exists():
        old = json.loads(RETIRED.read_text(encoding="utf-8"))
        if old.get("resident_population_active") is not False:
            error(RETIRED.name, "resident_population_active is not false - the 2026-09-02 "
                                "retirement is what this programme supersedes WITHOUT restoring")

    # every reconstructed person in the committed layer answers to a stage
    reconstructed, real_names = read_layer()
    for where, person in reconstructed:
        check_reconstructed_person(where, person, set(table), error)
        check_invented_name(where, person, real_names, error)

    built = [s["key"] for s in prog["stages"] if s.get("implemented")]
    for key in built:
        if key not in STAGE_BUILDERS:
            error(f"stage {key}", "is marked implemented and this writer has no build for "
                                  "it - the programme file and the writer disagree")
    if ARRIVAL_STAGE in built:
        check_arrival_fill(prog, error)
    if problems:
        for p in problems:
            print(f"  FAIL {p}")
        return 1
    print(f"  ok    the programme answers for {len(prog['stages'])} stage(s); "
          f"{len(built)} implemented")
    print(f"  ok    {len(reconstructed)} reconstructed person(s) in data/residents/, each "
          f"holding the record contract")
    if not built:
        print("  ok    no stage has been built yet (T-1167 opened the programme and wrote "
              "nobody), so there is no draw to re-derive")
    elif [k for k in built if k not in STAGE_CHECKERS]:
        print(f"  ok    {', '.join(k for k in built if k not in STAGE_CHECKERS)} re-derive from the programme, block for block")
    for key in built:
        checker = STAGE_CHECKERS.get(key)
        if checker is None:
            continue
        print(f"  ---   stage '{key}' re-derives its own draw:")
        if checker() != 0:
            return 1
    return 0


def cmd_self_test() -> int:
    """The mutations the contract must refuse, one case per rule it states."""
    stage_keys = {"modelled_families", UNDERDOCUMENTED_STAGE}

    def refusals(person, taken=frozenset()):
        out = []
        check_reconstructed_person("case", person, stage_keys, lambda w, m: out.append(m))
        check_invented_name("case", person, set(taken), lambda w, m: out.append(m))
        return out

    good = {
        "id": "rc_bardwell_lucy", "name": "Lucy Bardwell", "grade": RECONSTRUCTED,
        "name_basis": {"confidence": RECONSTRUCTED, "note": "Drawn from the yankee pool."},
        "basis": {"kind": "model", "id": "household_size",
                  "note": "The head's own size band in the 1840 histogram wants one more."},
        "seed": seed_for("hh_rc_bardwell_lucy", "household_size"),
        "replaceable_by": {"kind": "person", "match": "a source naming this household's wife"},
        "reconstruction": {"stage": "modelled_families", "community": "yankee"},
    }

    cases = []

    def case(name, person, want, taken=frozenset()):
        cases.append((name, person, want, taken))

    case("a well-formed reconstruction passes", good, False)

    no_basis = {k: v for k, v in good.items() if k != "basis"}
    case("a reconstructed person without a basis is refused", no_basis, True)

    no_seed = dict(good); no_seed.pop("seed")
    case("a value drawn from a model without its seed is refused", no_seed, True)

    ruled = dict(good)
    ruled["basis"] = {"kind": "rule", "id": "head_rule", "note": "Argued, not drawn."}
    case("a rule-argued person carrying a seed is refused", ruled, True)

    ruled_ok = dict(ruled); ruled_ok.pop("seed")
    case("...and passes once the decorative seed is gone", ruled_ok, False)

    no_rep = {k: v for k, v in good.items() if k != "replaceable_by"}
    case("a reconstruction with no replacement rule is refused", no_rep, True)

    no_stage = dict(good); no_stage["reconstruction"] = {"community": "yankee"}
    case("a person no stage claims is refused", no_stage, True)

    wrong_stage = dict(good)
    wrong_stage["reconstruction"] = {"stage": "modelled_families", "community": "metis",
                                     "review_required": True, "touches_removal": True}
    case("a Metis reconstruction outside stage 'underdocumented' is refused", wrong_stage, True)

    unreviewed = dict(good)
    unreviewed["reconstruction"] = {"stage": UNDERDOCUMENTED_STAGE, "community": "native"}
    case("a Native reconstruction without its review is refused", unreviewed, True)

    reviewed = dict(good)
    reviewed["reconstruction"] = {"stage": UNDERDOCUMENTED_STAGE, "community": "native",
                                  "review_required": True, "touches_removal": True}
    case("...and passes in its own stage, carrying the review", reviewed, False)

    case("an invented name that an attested person already bears is refused",
         good, True, taken={"lucy bardwell"})

    over_graded = dict(good)
    over_graded["name_basis"] = {"confidence": "inferred", "note": "Drawn from the pool."}
    case("an invented name graded above the invention is refused", over_graded, True)

    readmission = {
        "id": "gale_abram", "name": "Abram Gale", "grade": RECONSTRUCTED,
        "basis": {"kind": "rule", "id": "readmission",
                  "note": "A read name the research withheld, re-admitted at its evidence limit."},
        "replaceable_by": {"kind": "person", "match": "a second independent source at the scene date"},
        "reconstruction": {"stage": "modelled_families", "community": "yankee"},
    }
    case("a re-admitted read name needs no name_basis and no pool", readmission, False,
         taken={"abram gale"})

    failures = 0
    for name, person, want_refused, taken in cases:
        got = refusals(person, taken)
        if bool(got) != want_refused:
            failures += 1
            print(f"  FAIL {name}: expected {'a refusal' if want_refused else 'a pass'}, "
                  f"got {got or 'a pass'}")
        else:
            print(f"  ok    {name}")

    # the seed is a string a reader can retype, and it redraws the same number
    a = seed_for("hh_rc_bardwell_lucy", "household_size")
    if a != "hh_rc_bardwell_lucy:household_size" or draw(a) != draw(a):
        failures += 1
        print("  FAIL the seed rule does not match the programme file")
    elif draw(a) == draw(seed_for("hh_rc_bardwell_lucy", "sex_ratio")):
        failures += 1
        print("  FAIL two buckets of one household draw the same number")
    else:
        print("  ok    the seed is a retypable string and each bucket draws its own number")

    # THE BOUNDARY, read from the syntax rather than from the prose. The docstring
    # above NAMES the refusal in order to explain the asymmetry, so a substring search
    # over the file would find its own explanation and fail. An AST walk sees imports
    # and calls and not the sentence that describes them.
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported = any(
        (isinstance(n, ast.Import) and any("refuse_reconstructed_grade" in a.name for a in n.names))
        or (isinstance(n, ast.ImportFrom) and "refuse_reconstructed_grade" in (n.module or ""))
        for n in ast.walk(tree))
    called = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                 and n.func.id in ("refuse", "refuse_texts")
                 for n in ast.walk(tree))
    if imported or called:
        failures += 1
        print("  FAIL this writer imports or calls the research writers' refusal - it is the "
              "one tool that may mint the grade, and wiring the refusal in would retire the "
              "programme the owner asked for")
    else:
        print("  ok    the one writer of the grade does not call the refusal the four "
              "research writers carry")

    failures += arrival_stage_self_test()
    return 1 if failures else 0


def arrival_stage_self_test() -> int:
    """Stage `attribute_fill_arrival` (T-1169): the rules its blocks must actually obey.

    The record contract above is checked against hand-written persons. These cases are
    checked against blocks the STAGE builds, from the committed programme, so a recipe
    edit that produces a block `validate.py` would refuse is caught here rather than
    2,400 files later.
    """
    from migrate_attribute_tiers import check_tier_block  # local: the writer must not
    # import the research writers' refusal at module scope, and this keeps the file's
    # import list as bare as the boundary test reads it.

    failures = 0

    def ok(name):
        print(f"  ok    {name}")

    def bad(name, why):
        nonlocal failures
        failures += 1
        print(f"  FAIL {name}: {why}")

    prog = load_programme()
    recipe = prog["arrival_fill"]
    years = town_model_table("arrival_year_of_the_known_layer")["rows"]
    regions = town_model_table("birthplace_of_the_old_settlers_who_came_by_1835")["rows"]
    pools = json.loads(NAME_POOLS.read_text(encoding="utf-8"))

    def household(hid, arrival, precision, trade=None):
        person = {"id": "p", "relationship": "head", "name": "A Head"}
        if trade:
            person["occupation"] = {"value": trade, "confidence": "attested"}
        return {"id": hid, "head": "p",
                "arrival": {"value": arrival, "confidence": "inferred", "precision": precision},
                "persons": [person]}

    # --- the truncation is the evidence, and it binds the draw -------------
    bounded_33 = household("hh_kellogg_asa", "1833-09-30", "not_later_than")
    over = []
    for n in range(400):
        hh = household(f"hh_test_{n}", "1833-09-30", "not_later_than")
        block = plan_household(hh, recipe, years, regions, pools, None)["arrival_year"]
        if block["value"] > 1833:
            over.append((hh["id"], block["value"]))
    if over:
        bad("a bound at 1833 cannot draw a later arrival year", f"{len(over)} did, e.g. {over[0]}")
    else:
        ok("a bound at 1833 cannot draw a later arrival year - the truncation binds the draw")

    # --- the draw is the seed and nothing else ----------------------------
    a = plan_household(bounded_33, recipe, years, regions, pools, None)
    b = plan_household(json.loads(json.dumps(bounded_33)), recipe, years, regions, pools, None)
    if a != b:
        bad("one household draws the same values twice", "two plans of one record disagree")
    elif a["arrival_year"]["seed"] != seed_for("hh_kellogg_asa", "arrival_year"):
        bad("the seed is the one the programme states", a["arrival_year"]["seed"])
    else:
        ok("one household draws the same values twice, from the seed the programme states")

    # --- a table re-ordered by a later edit must not re-draw the town ------
    shuffled = list(reversed(years))
    if plan_household(bounded_33, recipe, shuffled, regions, pools, None) != a:
        bad("re-ordering a model table re-draws the town",
            "pick() is reading the table's order and not its labels")
    else:
        ok("re-ordering a model table draws exactly the same values")

    # --- every block the stage writes survives validate.py's tier contract -
    probes = [
        household("hh_abbot_8_g", "1835-06-30", "not_later_than"),
        household("hh_kelly_john", "1834-03-31", "not_later_than", trade="blacksmith"),
        household("hh_beaubien_x", "1832", "year", trade="trader"),
    ]
    complaints = []
    for hh in probes:
        for key, block in plan_household(hh, recipe, years, regions, pools, None).items():
            check_tier_block(hh["id"], key, block,
                             lambda w, m: complaints.append(f"{w}: {m}"))
    if complaints:
        bad("every block the stage writes holds the per-attribute tier contract",
            complaints[0])
    else:
        ok("every block the stage writes holds the per-attribute tier contract")

    # --- the surname signal is used only where it is unambiguous ----------
    irish = plan_household(household("hh_kelly_john", "1835-06-30", "not_later_than"),
                           recipe, years, regions, pools, None)["origin"]
    plain = plan_household(household("hh_zzzz_john", "1835-06-30", "not_later_than"),
                           recipe, years, regions, pools, None)["origin"]
    if irish["value"] != recipe["community_origins"]["irish"]:
        bad("a surname only the Irish pool carries argues an Irish origin", irish["value"])
    elif irish.get("seed") is not None:
        bad("an argued origin carries no seed", "it carries one")
    elif plain["basis"]["kind"] != "model" or not plain.get("seed"):
        bad("a surname no pool carries is DRAWN from the roll", plain["basis"])
    else:
        ok("a surname only one pool carries is argued; every other surname is drawn")

    # --- a value the stage does not own is never overwritten ---------------
    held = household("hh_dole_george_w", "1835-06-30", "not_later_than")
    held["origin"] = {"value": "Windsor, Vermont", "confidence": "attested",
                      "sources": ["andreas_1884_v1"]}
    if writable(held, "origin"):
        bad("an attested origin is not this stage's to rewrite", "the stage would overwrite it")
    elif not writable(household("hh_x_y", "1835-06-30", "not_later_than"), "origin"):
        bad("an absent origin is writable", "the stage refused an empty field")
    else:
        ok("an attested value is never overwritten and an absent one is filled")

    # --- the refusal the three late registrants get ------------------------
    late = plan_household(household("hh_adams_william_h", "1835-06-30", "not_later_than"),
                          recipe, years, regions, pools,
                          {"arrival_year": 1837, "arrival_as_read": "1837, Sept."})
    if "REFUSED" not in late["arrival_year"]["note"]:
        bad("a roll year later than the scene is refused IN WRITING",
            "the block says nothing about the roll")
    else:
        ok("a roll year later than the scene is refused in writing, on the card")

    # --- and the WHY is argued, never drawn --------------------------------
    drawn_reasons = [k for hh in probes
                     for k, blk in plan_household(hh, recipe, years, regions, pools, None).items()
                     if k == "reason_for_coming" and blk["basis"]["kind"] != "rule"]
    if drawn_reasons:
        bad("no reason for coming is ever DRAWN",
            "the town model apportions the town between the draws nowhere, and neither "
            "may this stage")
    else:
        ok("no reason for coming is ever drawn - the model refuses the split and so does this")

    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", help="the programme stage to run")
    ap.add_argument("--list", action="store_true", help="print the stage table")
    ap.add_argument("--build", action="store_true", help="run the stage named by --stage")
    ap.add_argument("--check", action="store_true", help="re-derive and hold the committed layer")
    ap.add_argument("--self-test", action="store_true", help="the mutations the contract refuses")
    args = ap.parse_args()

    if args.self_test:
        return cmd_self_test()
    if not PROGRAMME.exists():
        print(f"FAIL {PROGRAMME.relative_to(ROOT)} is missing - the programme is the only "
              f"authority under which a reconstructed resident may be written", file=sys.stderr)
        return 2
    prog = load_programme()
    if args.list:
        return cmd_list(prog)
    if args.build:
        if not args.stage:
            print("FAIL --build needs --stage", file=sys.stderr)
            return 2
        return cmd_build(prog, args.stage)
    if args.check:
        return cmd_check(prog)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
