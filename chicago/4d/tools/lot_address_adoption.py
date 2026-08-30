#!/usr/bin/env python3
"""The addresses that name a LOT AND A BLOCK, resolved onto the roofs standing on them.

    python3 tools/lot_address_adoption.py --check      re-resolve every row, refuse drift
    python3 tools/lot_address_adoption.py --report     the resolution, and what it rests on
    python3 tools/lot_address_adoption.py --self-test  every refusal, fired on purpose

WHAT THIS IS FOR (T-0423).

`data/research/newspapers/register_1835.json` places most of the corpus's businesses on a
STREET and nothing narrower, and `tools/adopt_street_faces.py` is the owner's ruling about
those: the business adopts a reconstructed roof already standing on that street face, and
its first limit is that it claims a face and NEVER a lot.

Exactly one statement in the whole corpus is narrower than a street. G. Spring's For-Sale
notice ran six times in the *Chicago Democrat* between 1834-06-18 and 1834-11-19 and names
a lot, a block, a street and a neighbour — *"LOT No. 7, in block No. 16, one lot east of
Haddock's Tavern, on Lake street … There is on said lot a large Dwelling-House and fine
well"*. Until T-0358 committed the Thompson plat's block numbers it resolved to nothing.
Now it resolves to one lot, and one anonymous reconstructed roof stands on that lot.

So there is no allocation to make here and nothing to choose — which is the difference
from the street-face table, and the reason this is a separate file rather than a widening
of that one. A street face asks *which of these roofs*; a lot address asks only *does this
project hold the numbering well enough to say this roof*.

HOW A ROW IS VERIFIED, AND WHY IT IS VERIFIED RATHER THAN TRUSTED.

The resolution is a chain of committed things — the block's number, the block's lot
numbering, the lot's polygon, and which committed footprint stands on that polygon — and
every link of it can move under a row that was authored once and never looked at again. A
re-derived plat, a moved roof or a second building dealt onto the lot would each leave the
authored `structure_id` pointing at a house that is no longer there, and the card would go
on naming it. So `--check` re-runs the whole chain on every commit and refuses the row
rather than the tree, and `tools/check.sh` runs it.

THE FOUR LIMITS are stated in the table's own `limits` field, in the words a reader of the
data needs, and each one is an assertion here:

  1. the roof stays `reconstructed` — only `documented_range` is regraded, and only to
     `inferred`, because that attribute is the claim that a building stood on this ground;
  2. the identification inherits the WEAKEST grade in the chain that resolves it — the
     block number is `inferred` and the lot lines are `conjectural`, so `inferred` is the
     ceiling and this refuses a row that grades itself above it;
  3. one lot, one roof, and that roof inside the anonymous `recon_*` layer;
  4. the roof is not dealt twice — it keeps its id, its family, its sequence, its count
     toward the 665-roof programme and whatever occupant the occupancy ledger seated in
     it. This module writes no `occupants` block and refuses a row that tries to.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from plat_occupancy import lot_holders  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "data" / "research" / "newspapers" / "lot_address_adoptions.json"
GRID = ROOT / "data" / "traces" / "vectors" / "thompson_lots.json"
DATUM = ROOT / "data" / "datum.json"
NUMBERING = ROOT / "data" / "traces" / "thompson_block_numbering.json"

#: The grade a lot address may not rise above, and the reason it may not (limit 2). The
#: block number is counted rather than read and the lot lines are drawn from no sheet, so
#: `documented` is unreachable here however good the notice is.
CEILING = "inferred"

#: A claim id opens with the paper's name; the structure schema wants the SOURCE RECORD.
#: Kept identical to tools/inferred_occupancy.py's mapping rather than imported, because
#: that module's copy is the ledger's and this one is the plat's, and a shared constant
#: would make one of them silently follow the other's corpus.
CORPUS_SOURCE = (
    ("chicago_american_", "chicago_american_1835"),
    ("chicago_democrat_", "chicago_democrat_1833_1835"),
)


class AddressError(RuntimeError):
    """A lot address does not resolve, or a row claims more than the chain carries."""


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def table(doc: dict | None = None) -> dict:
    if doc is not None:
        return doc
    return load(TABLE) if TABLE.exists() else {"adoptions": []}


def _sources(cites: list[str]) -> list[str]:
    out = set()
    for cite in cites:
        for prefix, source_id in CORPUS_SOURCE:
            if cite.startswith(prefix):
                out.add(source_id)
                break
        else:
            raise AddressError("the address cites %r, which names no corpus source" % cite)
    return sorted(out)


def _block(grid: dict, number: int) -> dict:
    """The committed block carrying this plat number, or a refusal naming the number."""
    hits = [b for b in grid["blocks"]
            if (b.get("plat_block_number") or {}).get("number") == number]
    if len(hits) != 1:
        raise AddressError("block No. %d is carried by %d committed blocks; the numbering "
                           "in data/traces/thompson_block_numbering.json must name exactly "
                           "one" % (number, len(hits)))
    return hits[0]


def _lot_index(block: dict, number: int) -> int:
    hits = [i for i, lot in enumerate(block["lots"])
            if lot.get("plat_lot_number") == number]
    if len(hits) != 1:
        raise AddressError("lot No. %d is emitted %d times on %s" %
                           (number, len(hits), block["id"]))
    return hits[0]


def resolve(doc: dict | None = None) -> list[dict]:
    """Every row, re-resolved through the committed plat and the committed footprints.

    Returns the rows with what the chain actually says appended — the block the number
    lands on, the lot index, the roof standing on it — so `--report` prints the
    derivation rather than the authored answer.
    """
    doc = table(doc)
    grid, datum = load(GRID), load(DATUM)
    held = lot_holders(grid, datum)
    out: list[dict] = []
    seen: set[str] = set()

    for row in doc.get("adoptions", []):
        who = row.get("address_id", "?")
        if "occupants" in row:
            raise AddressError("%s writes an `occupants` block — a lot address says what a "
                               "building WAS, never who was in it (limit 4)" % who)
        if row.get("confidence") != CEILING:
            raise AddressError("%s grades itself %r; a lot address resolved through an "
                               "inferred block number and conjectural lot lines is %r and "
                               "may not rise above it (limit 2)"
                               % (who, row.get("confidence"), CEILING))
        cites = row.get("cites") or []
        if not cites:
            raise AddressError("%s cites no printing of its address" % who)
        legible = row.get("cites_legible") or []
        if not set(legible) <= set(cites):
            raise AddressError("%s calls a printing legible that it does not cite" % who)

        block = _block(grid, row["plat_block_number"])
        if block["id"] != row.get("block_id"):
            raise AddressError("%s says block No. %d is %s; the committed numbering puts it "
                               "on %s" % (who, row["plat_block_number"], row.get("block_id"),
                                          block["id"]))
        index = _lot_index(block, row["plat_lot_number"])
        standing = held.get(block["id"], {}).get(index, [])
        if len(standing) != 1:
            raise AddressError("%s resolves to lot %d of %s, which %s (limit 3)"
                               % (who, row["plat_lot_number"], block["id"],
                                  "holds no roof" if not standing
                                  else "holds %d roofs: %s" % (len(standing),
                                                               ", ".join(sorted(standing)))))
        sid = standing[0]
        if not sid.startswith("recon_"):
            raise AddressError("%s resolves onto %s, which is outside the anonymous "
                               "reconstructed layer — reconciling two documented claims is "
                               "a different question (limit 3)" % (who, sid))
        if sid != row.get("structure_id"):
            raise AddressError("%s names %s and the plat resolves to %s. The chain has "
                               "moved under the row: re-read it before re-pointing it"
                               % (who, row.get("structure_id"), sid))
        if sid in seen:
            raise AddressError("%s is the second address on %s — one roof, one address"
                               % (who, sid))
        seen.add(sid)
        out.append({**row, "resolved_block_id": block["id"], "resolved_lot_index": index,
                    "resolved_structure_id": sid, "sources": _sources(cites)})
    return out


def overrides(doc: dict | None = None) -> dict[str, dict]:
    """structure_id -> what a generated record carries because of its address.

    The generator owns the record and this owns the address, exactly as
    `tools/inferred_occupancy.py` owns the occupants of an adopted roof: hand-editing a
    generated record would fail the drift check that makes the block parcels trustworthy,
    and authoring the same words in two places would let them disagree.

    Six keys, and no seventh. `name` and `aka` are what the card is titled; the
    `documented_range` REPLACES the anonymous count-unit's own — that record says in as
    many words that "no evidence establishes that this particular building existed", which
    stops being true the moment the address resolves — and `research_note` is the sentence
    the dossier line owes a reader. Nothing here touches the position, the footprint, the
    form, the family, the sequence or the occupants.
    """
    out: dict[str, dict] = {}
    for row in resolve(doc):
        printings = "%d printing%s, %s to %s" % (
            row["printings"], "" if row["printings"] == 1 else "s",
            row["first_issue"], row["last_issue"])
        cited = ", ".join(row["cites"])
        out[row["resolved_structure_id"]] = {
            "name": row["name"],
            "aka": list(row.get("aka") or []),
            "documented_range": {
                "from": "1835-01-01", "to": "1835-12-31",
                "confidence": row["confidence"],
                "sources": row["sources"],
                "note": (
                    "A BUILDING ON THIS LOT IS DOCUMENTED; THIS BUILDING IS NOT. "
                    + row["advertised_by"] + "'s notice — \"" + row["printed_address"]
                    + " … There is on said lot " + row["printed_building"]
                    + "\" — ran " + printings + " (" + cited + "). "
                    + row["legibility_note"] + " THE ADDRESS RESOLVES THROUGH THE PLAT: "
                    "block No. " + str(row["plat_block_number"]) + " is "
                    + row["resolved_block_id"] + " (`inferred`, counted along the tier from "
                    "a numeral read off Wright's 1834 sheet — data/traces/"
                    "thompson_block_numbering.json), and lot No. "
                    + str(row["plat_lot_number"]) + " is the third lot east of the Dearborn "
                    "corner under a lot scheme graded `conjectural` because no sheet drew "
                    "the lines it numbers. This roof is the one standing on that lot. "
                    "THE GRADE IS THE WEAKEST LINK IN THAT CHAIN and not the notice's own; "
                    "docs/RESEARCH/thompson_block_numbering.md §§ 6-7 is the reading, and "
                    "§ 6 is the three independent statements that agree on this block. "
                    + row["scene_date_note"]),
            },
            # The two sentences the anonymous parcel writes about the PLACE that stop
            # being true when an address resolves onto it. Neither regrades anything:
            # the position is still the typology's and still `reconstructed`, and what
            # is not derivable is still not derivable — it is the REASON that changes,
            # from "no lot in this block is numbered" to "the lot is numbered and the
            # notice still does not say where on it the house stood".
            "symbolic_location": (
                "Lot " + str(row["plat_lot_number"]) + " of block "
                + str(row["plat_block_number"]) + " — the north side of Lake Street, the "
                "third lot east of Dearborn, in the South Division block bounded by South "
                "Water, State, Lake and Dearborn"),
            "position_derivation_reason": (
                "The lot is numbered and the address resolves onto it, but no source "
                "states where on the lot the house stood, how big it was or which way it "
                "faced. The position inside the lot is the 665-roof programme's typology, "
                "exactly as it was before the address was read."),
            "research_note": (
                "THE ADDRESS IS DOCUMENTED AND THE FABRIC UNDER IT IS NOT. This roof was "
                "raised by the 665-roof programme as an anonymous count-unit and is "
                "unchanged by the adoption — its existence as drawn, its position inside "
                "the lot, its footprint, its family and its form are all still invented, "
                "and it still counts once toward the programme. What changed is that the "
                "lot it stands on is named by a period notice, so the card says whose "
                "house this ground carried instead of naming nobody. " + row["fabric_note"]
                + " THE WELL: " + row["well"]["why_not"]),
        }
    return out


def report() -> int:
    rows = resolve()
    print("LOT ADDRESSES — %d row(s), each resolved through the committed plat" % len(rows))
    for row in rows:
        print("\n  %s" % row["address_id"])
        print("    printed      %s" % row["printed_address"])
        print("    resolves to  block %d = %s, lot %d = index %d"
              % (row["plat_block_number"], row["resolved_block_id"],
                 row["plat_lot_number"], row["resolved_lot_index"]))
        print("    the roof     %s" % row["resolved_structure_id"])
        print("    grade        %s (ceiling %s)" % (row["confidence"], CEILING))
        print("    cites        %d printing(s), %d legible end to end"
              % (len(row["cites"]), len(row["cites_legible"])))
        print("    well drawn   %s" % ("yes" if row["well"]["drawn"] else "no — see the row"))
    return 0


def self_test() -> int:
    """Every refusal, fired on a copy in memory. A gate nobody has watched fail is decor."""
    import copy
    doc = table()
    if not doc.get("adoptions"):
        print("  FAIL  the table is empty, so nothing can be broken")
        return 1
    failed = 0

    def case(label: str, mutate) -> None:
        nonlocal failed
        broken = copy.deepcopy(doc)
        mutate(broken)
        try:
            resolve(broken)
        except AddressError as exc:
            print("  fires: %s — %s" % (label, str(exc)[:78]))
            return
        failed = 1
        print("  FAIL  %s did not fire" % label)

    case("a row graded above the chain that resolves it",
         lambda b: b["adoptions"][0].update(confidence="documented"))
    case("a row that seats an occupant",
         lambda b: b["adoptions"][0].update(occupants={"value": "somebody"}))
    case("a row citing no printing",
         lambda b: b["adoptions"][0].update(cites=[]))
    case("a row calling a printing legible that it does not cite",
         lambda b: b["adoptions"][0].update(cites_legible=["chicago_democrat_1899_01_01#c1"]))
    case("a claim id that names no corpus source",
         lambda b: b["adoptions"][0].update(cites=["the_tribune_1871#c1"],
                                            cites_legible=[]))
    case("a row whose block id disagrees with the committed numbering",
         lambda b: b["adoptions"][0].update(block_id="blk_lake_clark"))
    case("a block number the committed numbering does not carry",
         lambda b: b["adoptions"][0].update(plat_block_number=99))
    case("a lot number the block does not emit",
         lambda b: b["adoptions"][0].update(plat_lot_number=99))
    case("a row pointing at a roof the plat does not put on the lot",
         lambda b: b["adoptions"][0].update(structure_id="green_tree_tavern"))
    case("two addresses on one roof",
         lambda b: b["adoptions"].append(copy.deepcopy(b["adoptions"][0])))

    if failed:
        print("SELF-TEST FAIL")
        return 1
    print("SELF-TEST PASS — the lot-address layer refuses every way a row could lie "
          "(10 cases)")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    if "--report" in sys.argv:
        return report()
    rows = resolve()
    print("lot addresses: %d row(s) resolve through the committed plat onto %d roof(s)"
          % (len(rows), len({r["resolved_structure_id"] for r in rows})))
    for row in rows:
        print("  %s -> %s (block %d lot %d)"
              % (row["address_id"], row["resolved_structure_id"],
                 row["plat_block_number"], row["plat_lot_number"]))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AddressError as exc:
        print("LOT ADDRESS REFUSED — %s" % exc)
        raise SystemExit(1)
