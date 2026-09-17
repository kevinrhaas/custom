#!/usr/bin/env python3
"""The location reconciliation rows: one row per home, workplace and business
location claim, resolved as far as its evidence reaches and no further (T-1237).

    tools/location_reconciliation.py --build      write the rows and the report
    tools/location_reconciliation.py --check      re-derive, diff, re-assert the limits
    tools/location_reconciliation.py --self-test  break the assertions and require them to fire
    tools/location_reconciliation.py --report     print the counts

WHAT THIS IS FOR.

T-1147 asked for a reconciliation row for every home, workplace and business-location
claim the project holds: source and claim id, describes date, the resident, household
and business ids, the printed place, the resolved street, anchor and structure, the
confidence, and the disposition. T-1237 is the first piece of that ask, and it owns
clauses 1, 8 and 9 of the parent.

CLAUSE 8 IS WHY THE SHAPE IS WHAT IT IS. The seating ticket T-1198 builds an address
book, and it is to start from these rows rather than from the evidence again. So every
row keeps `resolved_street`, `resolved_face`, `resolved_anchor` and — the field that
makes the row re-usable — `limit_clause`, the one-line statement of what stopped the
resolution going further. A later rung that wants to add a lot to a face row reads the
clause and knows whether the face was the evidence's limit or merely this pass's.

NOTHING HERE IS AUTHORED. Every row is derived from four committed sources:

  1. `data/residents/households/*.json` — `lives_at` and `works_at`, each with its own
     confidence, sources and note. 1,257 households; 20 name a dwelling and 50 a
     workplace, which is the measurement T-1147 opens with.
  2. The same files' `directories` block — `address_later` readings out of the 1839,
     1843 and 1844 volumes, each already ruled on by a committed back-projection pass
     (`back_projection`, `residence_back_projection`). A LATER ADDRESS IS NOT AN 1835
     PLACEMENT, and this pass does not make it one: the row records the address, the
     clause that fired or refused, and the placement the ruling allowed — which for a
     refusal is none at all. That is T-1147 clause 1's "without treating them as 1835
     placements unless the existing back-projection rule explicitly fires", read
     literally: the rule fired somewhere else, and this only reports where.
  3. `data/research/newspapers/register_1835.json` — the businesses the papers put in
     Chicago on the scene date, with the anchor the advertisement reached.
  4. `data/research/newspapers/street_face_adoptions.json` — what the town did with the
     `street_only` businesses under the owner's ruling of 2026-08-29, and the refusals.
  5. `data/research/newspapers/gazetteer.json` — for the CLAIM IDS. The register carries
     a business's action and its issue dates but not the claims behind it; the gazetteer
     carries `mentions`, which is the list of `<issue>#<claim>` pointers the reading
     actually stands on, and `placement.offset_text`, which is the place as the paper
     PRINTED it ("one door east of Dearborn") rather than as the model resolved it.
     Clause 1 asks for the source and claim id on every row, so the rows take both.

THE TWO AXES T-1157 READS (T-1147 clause 9).

  * businesses, by location limit: `structure` (the advertisement reaches a roof),
    `street_only` (it reaches a platted street and nothing narrower), `unplaceable`
    (it reaches no street the model holds).
  * households, by seating class: `structure`, `lot`, `face`, `division`, `none`.

The parent ticket calls these "the four seating classes" and then lists five labels.
Five is what the data supports and five is what is counted here; `division` and `none`
are different facts — a household the sources put in the North Division is not a
household the sources put nowhere — and collapsing them would lose the distinction the
sign-off needs. The report says so rather than quietly picking one reading.

A HOME ROW EXISTS FOR EVERY HOUSEHOLD, INCLUDING THE ONES WITH NO CLAIM. That is
deliberate and it is not symmetric with the workplace rows, which exist only where a
workplace claim does. The seating-class axis is defined over the whole household layer
— `none` is one of its classes and 1,185 households are in it — so a file that dropped
the empty rows could not answer the question clause 9 asks of it. A workplace has no
such axis, so an absent workplace is an absent row.

NO ROW INVENTS A COORDINATE. `resolved_structure` is only ever an id the dataset already
carries, `resolved_street` is only ever derived from committed geometry by
`fronting_street.fronting()`, and `resolved_face` is that module's own vocabulary — "lot
front", "corner side", "centreline band" — or the face the adoption ruling recorded.
Where the evidence reaches none of them the fields are null and the clause says why.
"""
from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

HOUSEHOLDS = ROOT / "data" / "residents" / "households"
REGISTER = ROOT / "data" / "research" / "newspapers" / "register_1835.json"
GAZETTEER = ROOT / "data" / "research" / "newspapers" / "gazetteer.json"
ADOPTIONS = ROOT / "data" / "research" / "newspapers" / "street_face_adoptions.json"
STRUCTURES = ROOT / "data" / "structures"
OUT = ROOT / "data" / "research" / "location_reconciliation.json.gz"
REPORT = ROOT / "docs" / "RESEARCH" / "location-reconciliation-2026-09-17.md"

SCENE_DATE = "1835-07-01"
AS_OF = "2026-09-17"

#: the business location limits, worst evidence last
BUSINESS_LIMITS = ("structure", "street_only", "unplaceable")
#: the household seating classes, best evidence first
SEATING_CLASSES = ("structure", "lot", "face", "division", "none")
#: what a row's disposition may say
DISPOSITIONS = ("resolved", "limited", "refused", "no_claim")

_cache: dict = {}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# the committed geometry, asked rather than restated
# ---------------------------------------------------------------------------

def _fronting():
    """`fronting_street.fronting`, or a refusal that says the answer is unavailable.

    The module reads the plat, the datum and the structure centroids, and that chain
    wants pyproj. A sandbox without it must not silently report every roof as fronting
    nothing — that is a wrong answer wearing the shape of a right one — so the absence
    is carried to the caller and printed, and `--check` refuses to compare against a
    file built without it.
    """
    if "fronting" not in _cache:
        try:
            from fronting_street import fronting, street_name
            _cache["fronting"] = (fronting, street_name)
        except Exception as exc:  # noqa: BLE001 - any import-chain failure reads the same
            _cache["fronting"] = (None, str(exc))
    return _cache["fronting"]


def frontage(structure_id: str | None):
    """(street name, face) for a committed structure, or (None, None)."""
    if not structure_id:
        return None, None
    fronting, street_name = _fronting()
    if fronting is None:
        return None, None
    faces = fronting(structure_id)
    if not faces:
        return None, None
    street_id, how = faces[0]
    return street_name(street_id), how


def gazetteer() -> dict:
    """business id -> the gazetteer entry, for the claim ids the register drops."""
    if "gazetteer" not in _cache:
        _cache["gazetteer"] = {
            entry["id"]: entry for entry in read_json(GAZETTEER)["businesses"]}
    return _cache["gazetteer"]


def structures() -> dict:
    if "structures" not in _cache:
        _cache["structures"] = {
            path.stem: read_json(path) for path in sorted(STRUCTURES.glob("*.json"))
        }
    return _cache["structures"]


def symbolic_location(structure_id: str | None) -> str | None:
    """What the structure record says about where it stands, in the source's words."""
    record = structures().get(structure_id or "")
    if not record:
        return None
    for phase in record.get("phases", []) or []:
        position = phase.get("position") or {}
        if position.get("symbolic_location"):
            return position["symbolic_location"]
    return None


def uncapitalise(text: str | None) -> str | None:
    """A sentence fragment quoted mid-clause should not open with a capital."""
    if not text or text[:1].islower():
        return text
    # Leave an acronym or a proper noun alone; only a normal sentence opener drops.
    return text[0].lower() + text[1:] if not text[:2].isupper() else text


def first_sentence(note: str | None, limit: int = 240) -> str | None:
    """The clause, not the essay — these notes run to paragraphs."""
    if not note:
        return None
    text = " ".join(note.split())
    for stop in (". ", "; "):
        if stop in text[:limit]:
            text = text[: text.index(stop) + 1]
            break
    return text[:limit].strip()


# ---------------------------------------------------------------------------
# the rows
# ---------------------------------------------------------------------------

def household_rows() -> list[dict]:
    rows = []
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        household = read_json(path)
        hid = household["id"]
        head = household.get("head")
        division = household.get("division")
        for kind, field in (("home", "lives_at"), ("workplace", "works_at")):
            claim = household.get(field)
            # BOTH FIELDS ARE ALWAYS PRESENT, and both are a claim OBJECT whose `value`
            # is null where no source reached a building — the same shape
            # `party_size_on_arrival` uses. So an empty claim is `{"value": null, ...}`,
            # not a missing key, and reading the key's presence as a claim would have
            # reported 1,257 workplaces where the layer holds 50.
            if claim is not None and claim.get("value") is None:
                claim = None
            if claim is None and kind == "workplace":
                continue  # no workplace axis to fill, so no empty row — see the header
            rows.append(_household_row(hid, head, division, kind, field, claim))
        rows.extend(_directory_rows(household, hid, head, division))
    return rows


def _household_row(hid, head, division, kind, field, claim) -> dict:
    """One `lives_at`/`works_at` claim, seated as far as the record reaches."""
    structure_id = (claim or {}).get("value")
    known = structure_id in structures() if structure_id else False
    street, face = frontage(structure_id if known else None)
    if structure_id and known:
        seating, disposition = "structure", "resolved"
        clause = ("The record names a committed structure; the roof is the evidence's "
                  "own limit and nothing narrower is claimed.")
    elif structure_id:
        seating, disposition = "none", "limited"
        clause = (f"The record names {structure_id!r}, which no committed structure "
                  "carries, so the claim reaches no ground.")
    elif division and division not in ("unplaced",):
        seating, disposition = "division", "limited"
        clause = (f"No source reaches a building; the division ({division}) is as far "
                  "as the evidence goes.")
    else:
        seating, disposition = "none", "no_claim"
        clause = "No source reaches a building, a face or a division for this household."
    return {
        "row_id": f"{hid}#{field}",
        "claim_kind": kind,
        "claim_id": f"{hid}#{field}",
        "claims": [],
        "sources": list((claim or {}).get("sources") or []),
        "describes_date": SCENE_DATE if claim else None,
        "resident_id": head,
        "household_id": hid,
        "business_id": None,
        "printed_place": symbolic_location(structure_id) if known else None,
        "resolved_street": street,
        "resolved_face": face,
        "resolved_anchor": ({"kind": "structure", "target": structure_id}
                            if known else None),
        "resolved_structure": structure_id if known else None,
        "confidence": (claim or {}).get("confidence"),
        "seating_class": seating,
        "business_limit": None,
        "disposition": disposition,
        "limit_clause": clause,
    }


def _directory_rows(household, hid, head, division) -> list[dict]:
    """The later-volume addresses, each carrying the ruling already made on it.

    `address_later` is the printed place. `back_projection` is the committed pass's
    ruling on carrying a BUSINESS door back to 1835; `residence_back_projection` is the
    same question for a dwelling. Both already say `placed` or `refused` and name the
    clause, so this reports rather than re-adjudicates — which is the whole of T-1147
    clause 1's instruction about later directory addresses.
    """
    block = household.get("directories")
    if not isinstance(block, dict):
        return []
    rows = []
    for person in block.get("people", []) or []:
        pid = person.get("person_id")
        printed = (person.get("address_later") or {}).get("value")
        for field, kind in (("back_projection", "later_workplace_address"),
                            ("residence_back_projection", "later_home_address")):
            ruling = person.get(field)
            if not isinstance(ruling, dict):
                continue
            rows.append(_directory_row(hid, pid, division, field, kind, ruling, printed,
                                       person.get("address_later")))
    return rows


def _directory_row(hid, pid, division, field, kind, ruling, printed, address) -> dict:
    outcome = ruling.get("outcome")
    placement = ruling.get("placement")
    clause_id = ruling.get("clause")
    if outcome == "placed" and placement:
        seating = placement if placement in SEATING_CLASSES else "face"
        disposition = "resolved"
        clause = (f"Back-projection clause {clause_id} fired: the later volume's address "
                  f"is carried back to 1835 as a {placement} and no further.")
    elif outcome == "already_better_placed":
        seating, disposition = "none", "refused"
        clause = (f"Clause {clause_id}: the 1835 record already places this person "
                  "better than the later volume could, so nothing was carried back.")
    else:
        seating, disposition = "none", "refused"
        clause = (f"Back-projection clause {clause_id} REFUSED: "
                  + (uncapitalise(first_sentence(ruling.get("note"), 180))
                     or "the later address is not carried back to 1835."))
    return {
        "row_id": f"{hid}#{pid}#{field}",
        "claim_kind": kind,
        "claim_id": f"{hid}#{pid}#{field}",
        "claims": [],
        "sources": list(ruling.get("sources") or (address or {}).get("sources") or []),
        "describes_date": ruling.get("describes_date"),
        "resident_id": pid,
        "household_id": hid,
        "business_id": None,
        "printed_place": printed,
        "resolved_street": ruling.get("value") if outcome == "placed" else None,
        "resolved_face": placement if outcome == "placed" else None,
        "resolved_anchor": None,
        "resolved_structure": None,
        "confidence": ruling.get("confidence"),
        "seating_class": seating,
        "business_limit": None,
        "disposition": disposition,
        "limit_clause": clause,
    }


def business_rows() -> list[dict]:
    """One row per business the register stands on the scene date.

    The register's four actions collapse onto three location limits, because
    `enrich_existing` and `new_building` are the same fact about EVIDENCE — the
    advertisement reaches a roof — and differ only in what the town must build.
    """
    register = read_json(REGISTER)
    adoptions = read_json(ADOPTIONS)
    adopted = {row["business_id"]: row for row in adoptions.get("adoptions", [])}
    refused = {row["business_id"]: row for row in adoptions.get("refusals", [])}
    rows = []
    for business in register["businesses"]:
        if not business.get("present_at_scene_date") or business.get("exclusion"):
            continue
        rows.append(_business_row(business, adopted, refused))
    return rows


def _business_row(business, adopted, refused) -> dict:
    bid = business["id"]
    action = business.get("action")
    anchor = business.get("anchor") or {}
    evidence = business.get("evidence") or {}
    target = business.get("action_target")
    if action in ("enrich_existing", "new_building"):
        limit, disposition = "structure", "resolved"
        street, face = frontage(target if target in structures() else None)
        resolved_structure = target if target in structures() else None
        clause = ("The advertisement's anchor reaches a roof; the register's action is "
                  f"{action} on {target!r}.")
    elif action == "street_only":
        limit = "street_only"
        deal, refusal = adopted.get(bid), refused.get(bid)
        street = business.get("street") or (deal or {}).get("street_name")
        if deal:
            disposition, face = "limited", deal.get("face")
            resolved_structure = deal.get("structure_id")
            clause = ("The paper names a platted street and nothing narrower. Under the "
                      "street-face adoption ruling of 2026-08-29 the business takes a "
                      "roof already standing on that face and claims no lot.")
        else:
            disposition, face, resolved_structure = "limited", None, None
            why = (refusal or {}).get("refusal") or "no adoption was recorded for this face"
            clause = ("The paper names a platted street and nothing narrower, and the "
                      f"face could not be adopted: {uncapitalise(why)}.")
    else:
        limit, disposition = "unplaceable", "limited"
        street = face = resolved_structure = None
        clause = ("The paper reaches no street the model holds: "
                  + (uncapitalise(first_sentence(anchor.get("note"), 160))
                     or "no anchor is printed."))
    entry = gazetteer().get(bid, {})
    mentions = list(entry.get("mentions") or [])
    printed = ((entry.get("placement") or {}).get("offset_text")
               or business.get("street")
               or first_sentence(anchor.get("note"), 160))
    return {
        "row_id": f"{bid}#location",
        "claim_kind": "business_location",
        "claim_id": bid,
        "claims": mentions,
        "sources": sorted({c.split("#")[0] for c in mentions}),
        "describes_date": evidence.get("last_issue") or evidence.get("first_issue"),
        "resident_id": None,
        "household_id": None,
        "business_id": bid,
        "printed_place": printed,
        "resolved_street": street,
        "resolved_face": face,
        "resolved_anchor": ({"kind": anchor.get("kind"), "target": anchor.get("target")}
                            if anchor.get("kind") != "unresolved" else None),
        "resolved_structure": resolved_structure,
        "confidence": business.get("match_tier"),
        "seating_class": None,
        "business_limit": limit,
        "disposition": disposition,
        "limit_clause": clause,
    }


# ---------------------------------------------------------------------------
# the document
# ---------------------------------------------------------------------------

def build() -> dict:
    rows = household_rows() + business_rows()
    rows.sort(key=lambda row: (row["claim_kind"], row["row_id"]))
    homes = [r for r in rows if r["claim_kind"] == "home"]
    businesses = [r for r in rows if r["claim_kind"] == "business_location"]
    fronting, why = _fronting()
    return {
        "schema": "location_reconciliation/1",
        "generated_by": "tools/location_reconciliation.py",
        "as_of": AS_OF,
        "scene_date": SCENE_DATE,
        "_doc": (
            "T-1237, the first piece of T-1147. One row per home, workplace and "
            "business-location claim, resolved as far as its evidence reaches. Every "
            "row keeps resolved_street, resolved_face, resolved_anchor and the "
            "limit_clause that stopped it, so T-1198's address book starts here. "
            "DERIVED — rebuild with --build, and --check refuses a hand-edit."),
        "compiled_from": {
            "households": str(HOUSEHOLDS.relative_to(ROOT)),
            "register": str(REGISTER.relative_to(ROOT)),
            "street_face_adoptions": str(ADOPTIONS.relative_to(ROOT)),
            "gazetteer": str(GAZETTEER.relative_to(ROOT)),
            "structures": str(STRUCTURES.relative_to(ROOT)),
        },
        "frontage_available": fronting is not None,
        "frontage_unavailable_because": None if fronting is not None else why,
        "counts": {
            "rows": len(rows),
            "by_claim_kind": dict(sorted(Counter(r["claim_kind"] for r in rows).items())),
            "by_disposition": dict(sorted(Counter(r["disposition"] for r in rows).items())),
            "households_by_seating_class": {
                cls: sum(1 for r in homes if r["seating_class"] == cls)
                for cls in SEATING_CLASSES},
            "businesses_by_location_limit": {
                lim: sum(1 for r in businesses if r["business_limit"] == lim)
                for lim in BUSINESS_LIMITS},
            "rows_with_a_resolved_street": sum(1 for r in rows if r["resolved_street"]),
            "rows_with_a_resolved_structure": sum(
                1 for r in rows if r["resolved_structure"]),
        },
        "rows": rows,
    }


def write(doc: dict) -> None:
    raw = (json.dumps(doc, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))


def read_committed():
    try:
        return json.loads(gzip.decompress(OUT.read_bytes()).decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        return None


def report(doc: dict) -> str:
    counts = doc["counts"]
    seating = counts["households_by_seating_class"]
    limits = counts["businesses_by_location_limit"]
    lines = [
        "# The location reconciliation rows",
        "",
        f"Generated by `tools/location_reconciliation.py` on {doc['as_of']}; "
        f"scene date {doc['scene_date']}. **Derived — do not hand-edit.** The rows "
        f"live in `{OUT.relative_to(ROOT)}`; this is the review surface.",
        "",
        "T-1237, the first piece of T-1147. One row per home, workplace and "
        "business-location claim, carrying the street, face and anchor the evidence "
        "reached and the clause that stopped it going further. T-1198's address book "
        "starts from these rows rather than from the evidence again.",
        "",
        f"**{counts['rows']} rows.** "
        f"{counts['rows_with_a_resolved_street']} reach a street, "
        f"{counts['rows_with_a_resolved_structure']} reach a committed structure.",
        "",
        "## Households, by seating class",
        "",
        "The first of the two axes T-1157 reads as the sign-off's location axis.",
        "",
        "| class | households | what the evidence reached |",
        "|---|---:|---|",
        f"| structure | {seating['structure']} | a committed roof |",
        f"| lot | {seating['lot']} | a platted lot and no roof |",
        f"| face | {seating['face']} | a block face and no lot |",
        f"| division | {seating['division']} | a division and no face |",
        f"| none | {seating['none']} | no ground at all |",
        "",
        "T-1147 clause 9 calls these \"the four seating classes\" and then lists five "
        "labels. Five is what the data supports and five is what is counted: a "
        "household the sources put in the North Division is not a household the sources "
        "put nowhere, and collapsing `division` into `none` would lose exactly the "
        "distinction the sign-off needs. The discrepancy is reported, not resolved.",
        "",
        "## Businesses, by location limit",
        "",
        "The register's four actions collapse onto three limits: `enrich_existing` and "
        "`new_building` are the same fact about the EVIDENCE — the advertisement reaches "
        "a roof — and differ only in what the town must build.",
        "",
        "| limit | businesses | what the paper reached |",
        "|---|---:|---|",
        f"| structure | {limits['structure']} | an anchor that resolves to a roof |",
        f"| street_only | {limits['street_only']} | a platted street and nothing narrower |",
        f"| unplaceable | {limits['unplaceable']} | no street the model holds |",
        "",
        "The 61 street-only and 62 unplaceable businesses are the **location limits "
        "T-1147 asks to preserve**, not missing buildings. They may fall only when a "
        "new source or reading names a stronger anchor.",
        "",
        "## Rows by kind and disposition",
        "",
        "| claim kind | rows |",
        "|---|---:|",
    ]
    for kind, n in counts["by_claim_kind"].items():
        lines.append(f"| {kind} | {n} |")
    lines += ["", "| disposition | rows |", "|---|---:|"]
    for disposition, n in counts["by_disposition"].items():
        lines.append(f"| {disposition} | {n} |")
    lines += [
        "",
        "`no_claim` is a row deliberately kept: a home row exists for every household, "
        "including the 1,185 the sources place nowhere, because the seating-class axis "
        "is defined over the whole layer and `none` is one of its classes. A workplace "
        "has no such axis, so an absent workplace is an absent row.",
        "",
        "## Later directory addresses",
        "",
        "A later volume's address is **not** an 1835 placement. Every `address_later` "
        "reading appears here as a row carrying the committed back-projection pass's own "
        "ruling — the clause that fired or refused — and a refusal resolves to nothing. "
        "This pass reports those rulings; it does not make them.",
        "",
    ]
    if not doc["frontage_available"]:
        lines += [
            "> **Frontage unavailable in the run that built this.** "
            f"`{doc['frontage_unavailable_because']}` — so `resolved_street` and "
            "`resolved_face` are null on the structure rows. A gate must not read that "
            "as a pass; `--check` refuses to compare against a file built this way.",
            "",
        ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# the gate
# ---------------------------------------------------------------------------

class Refused(Exception):
    pass


def assertions(doc: dict) -> None:
    """The limits this file exists to hold. Each one is a way the rows could lie."""
    rows = doc["rows"]
    if not rows:
        raise Refused("no rows: the reconciliation is empty")
    ids = [row["row_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise Refused("row_id is not unique")
    known = structures()
    for row in rows:
        if row["disposition"] not in DISPOSITIONS:
            raise Refused(f"{row['row_id']}: unknown disposition {row['disposition']!r}")
        if not row["limit_clause"]:
            raise Refused(f"{row['row_id']}: no limit_clause — clause 8 wants one on "
                          "every row")
        # NO ROW INVENTS A BUILDING. A resolved structure must be one the dataset holds.
        if row["resolved_structure"] and row["resolved_structure"] not in known:
            raise Refused(f"{row['row_id']}: resolved_structure "
                          f"{row['resolved_structure']!r} is not a committed structure")
        # A STREET-ONLY BUSINESS CLAIMS NO LOT, AND AN UNPLACEABLE ONE CLAIMS NO ROOF.
        if row["business_limit"] == "unplaceable" and (
                row["resolved_structure"] or row["resolved_street"]):
            raise Refused(f"{row['row_id']}: unplaceable, yet it resolves to ground")
        # A REFUSED LATER ADDRESS IS NOT A PLACEMENT.
        if row["disposition"] == "refused" and (
                row["resolved_street"] or row["resolved_structure"]):
            raise Refused(f"{row['row_id']}: refused, yet it resolves to ground")
        if row["claim_kind"] == "home" and row["seating_class"] not in SEATING_CLASSES:
            raise Refused(f"{row['row_id']}: {row['seating_class']!r} is not a seating class")
    seating = doc["counts"]["households_by_seating_class"]
    homes = sum(1 for row in rows if row["claim_kind"] == "home")
    if sum(seating.values()) != homes:
        raise Refused("the seating classes do not partition the home rows")
    limits = doc["counts"]["businesses_by_location_limit"]
    businesses = sum(1 for row in rows if row["claim_kind"] == "business_location")
    if sum(limits.values()) != businesses:
        raise Refused("the location limits do not partition the business rows")


def check() -> int:
    committed = read_committed()
    if committed is None:
        print(f"REFUSED: {OUT.relative_to(ROOT)} is missing or unreadable — "
              "run --build")
        return 1
    fresh = build()
    if not fresh["frontage_available"]:
        print("REFUSED: the frontage chain is unavailable in this run "
              f"({fresh['frontage_unavailable_because']}), so a rebuild cannot be "
              "compared against the committed file. A GATE MAY NOT COUNT THIS AS A PASS.")
        return 1
    if fresh["rows"] != committed["rows"]:
        fresh_ids = {row["row_id"]: row for row in fresh["rows"]}
        old_ids = {row["row_id"]: row for row in committed["rows"]}
        added = sorted(set(fresh_ids) - set(old_ids))
        gone = sorted(set(old_ids) - set(fresh_ids))
        changed = sorted(k for k in set(fresh_ids) & set(old_ids)
                         if fresh_ids[k] != old_ids[k])
        print("REFUSED: a rebuild would not produce the committed rows.")
        for label, items in (("added", added), ("gone", gone), ("changed", changed)):
            if items:
                print(f"  {label} ({len(items)}): {', '.join(items[:5])}"
                      + (" ..." if len(items) > 5 else ""))
        return 1
    if fresh["counts"] != committed["counts"]:
        print("REFUSED: the committed counts are not what the rows say.")
        return 1
    try:
        assertions(committed)
    except Refused as exc:
        print(f"REFUSED: {exc}")
        return 1
    if REPORT.read_text(encoding="utf-8") != report(committed):
        print(f"REFUSED: {REPORT.relative_to(ROOT)} is not what the rows say — "
              "run --build")
        return 1
    counts = committed["counts"]
    print(f"{counts['rows']} rows re-derive; "
          f"households {counts['households_by_seating_class']}; "
          f"businesses {counts['businesses_by_location_limit']}")
    return 0


def self_test() -> int:
    """Break each limit and require its assertion to fire."""
    doc = read_committed() or build()
    faults = []

    def fires(name, mutate):
        broken = json.loads(json.dumps(doc))
        mutate(broken)
        try:
            assertions(broken)
        except Refused as exc:
            print(f"  fires: {name} -> {exc}")
            return
        faults.append(name)

    def duplicate(d):
        d["rows"].append(json.loads(json.dumps(d["rows"][0])))

    def invented_structure(d):
        row = next(r for r in d["rows"] if r["claim_kind"] == "home")
        row["resolved_structure"] = "a_building_nobody_holds"

    def unplaceable_gains_ground(d):
        row = next(r for r in d["rows"] if r["business_limit"] == "unplaceable")
        row["resolved_street"] = "Lake Street"

    def refusal_gains_ground(d):
        row = next(r for r in d["rows"] if r["disposition"] == "refused")
        row["resolved_street"] = "Lake Street"

    def clause_dropped(d):
        d["rows"][0]["limit_clause"] = ""

    def classes_stop_partitioning(d):
        d["counts"]["households_by_seating_class"]["none"] += 1

    def limits_stop_partitioning(d):
        d["counts"]["businesses_by_location_limit"]["unplaceable"] += 1

    fires("a duplicated row_id", duplicate)
    fires("a resolved_structure the dataset does not hold", invented_structure)
    fires("an unplaceable business that resolves to ground", unplaceable_gains_ground)
    fires("a refused later address that resolves to ground", refusal_gains_ground)
    fires("a row with no limit_clause", clause_dropped)
    fires("seating classes that do not partition the home rows", classes_stop_partitioning)
    fires("location limits that do not partition the business rows", limits_stop_partitioning)

    if faults:
        print("SELF-TEST FAILED — these assertions did not fire: " + ", ".join(faults))
        return 1
    print("all 7 assertions fire when broken")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()
    if "--check" in argv:
        return check()
    if "--report" in argv:
        print(report(read_committed() or build()), end="")
        return 0
    if "--build" in argv:
        doc = build()
        if not doc["frontage_available"]:
            print("REFUSED: the frontage chain is unavailable "
                  f"({doc['frontage_unavailable_because']}); a build without it would "
                  "record every roof as fronting nothing. Install the readers and retry.")
            return 1
        assertions(doc)
        write(doc)
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(report(doc), encoding="utf-8")
        counts = doc["counts"]
        print(f"wrote {OUT.relative_to(ROOT)} ({counts['rows']} rows) "
              f"and {REPORT.relative_to(ROOT)}")
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
