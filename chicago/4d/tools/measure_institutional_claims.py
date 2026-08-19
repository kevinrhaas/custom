#!/usr/bin/env python3
"""Chicago's public buildings are few enough to be listed, so nothing anonymous
may be one.

ROADMAP T-I3. A dwelling nobody named is the ordinary case in this project: the
town held some three thousand people whose houses were never enumerated roof by
roof, so an invented dwelling is a count-unit toward a documented aggregate. A
public building nobody named is a different claim — that an institution stood on
this ground and left no record at all — and the enumeration behind
`docs/RESEARCH/civic_public_buildings_1835.md` is what makes that claim
refusable rather than merely discouraged: on 1 July 1835 the town's public
buildings with a roof are THREE, all three are committed named records, and
every remaining public FUNCTION in the town was carried on inside a private
building.

So the three institutional families are enumerable, and this holds them to it.

## What is asserted

**I1 (worship or meeting) and I3 (civic or public-service) are absolute.** Not a
ratchet: an anonymous roof of either family is a regression, and zero is the
enforceable number. `tools/generate_block_infill.py` has refused all three
families by name since L93, but that refusal only ever covered the block
generator — the North, West and phase-one parcels ran before it existed and
nothing has ever asked the committed records the question.

**I2 (school or community-use) is a ratchet at one.** `recon_1835_north_i2_015`
stands in the North Division from a parcel written before any of this, massed as
a generic frame block. L93 records it rather than quietly removing it, because a
liberty this project took is not deleted to make a gate pass. It may shrink — a
named school record substituting for it is exactly the move T-I3 licenses — and
it may not grow.

## What is only reported

The census: which committed records the physical-roof reconciliation types into
each institutional family, and the family targets they are counted against. The
I3 target of six is **not** asserted here and is the open half of T-I3 — three
of its six slots were never a count of anything, and which of the two available
corrections to make is a claim about the town's roof total rather than about its
public buildings. Read the ROADMAP box before quoting the target.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRUCTURES = DATA / "structures"
RECON = DATA / "reconstruction"

INSTITUTIONAL = ("I1", "I2", "I3")

# The families an anonymous roof may never carry, and the reason, stated where a
# failure will print it. Absolute rather than ratcheted: see the module docstring.
ABSOLUTE = {
    "I1": "worship or meeting buildings. Every congregation in the town in July "
          "1835 is a named record with its own dossier, so an anonymous one is "
          "not a count-unit toward the four — it is a fifth congregation.",
    "I3": "civic or public-service buildings. The town's are enumerable and all "
          "of them are committed named records: the log jail, the council house "
          "and the lighthouse. Every other public function in Chicago on the "
          "scene date — the post office, the United States Land Office, the "
          "county offices — was carried on inside a private building, and the "
          "court-house and the engine house were both built after it.",
}

# The one liberty already taken, named rather than pattern-matched. A ratchet
# that counted by family alone would let a SECOND anonymous school in as long as
# the first went out.
LEGACY_I2 = "recon_1835_north_i2_015"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def anonymous_institutional() -> list[dict]:
    """Every generated roof whose programme typed it into an institutional family.

    Both invented layers are asked, because they are two generators and only one
    of them has ever carried the refusal: the anonymous parcels write a
    `reconstruction` block on the record, and the inferred-household layer keeps
    its family in the household programme.
    """
    households = {
        b["id"]: b
        for b in load(RECON / "1835_inferred_household_programme.json")["buildings"]
    }
    found = []
    for path in sorted(STRUCTURES.glob("*.json")):
        record = load(path)
        rid = record["id"]
        block = record.get("reconstruction") or {}
        family, layer = None, None
        if block.get("status") == "inferred_anonymous":
            family, layer = block.get("family"), "anonymous parcel"
        elif rid in households:
            family, layer = households[rid].get("family"), "inferred household"
        if family in INSTITUTIONAL:
            found.append({"id": rid, "family": family, "layer": layer,
                          "district": block.get("district")
                          or households.get(rid, {}).get("district")})
    return found


def named_institutional() -> dict[str, list[str]]:
    """The committed records the roof reconciliation types into each family."""
    census: dict[str, list[str]] = {f: [] for f in INSTITUTIONAL}
    for entry in load(RECON / "1835_existing_roof_reconciliation.json")["records"]:
        family = entry.get("likely_family")
        if family in INSTITUTIONAL:
            census[family].append(entry["structure_id"])
    return {f: sorted(ids) for f, ids in census.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true",
                        help="exit 1 when an anonymous roof carries an institutional family")
    parser.add_argument("--quiet", action="store_true",
                        help="print the assertion and the failures, not the census")
    args = parser.parse_args()

    targets = load(RECON / "1835_building_inventory.json")["family_targets"]
    census = named_institutional()
    found = anonymous_institutional()

    failures: list[str] = []
    for row in sorted(found, key=lambda r: (r["family"], r["id"])):
        family = row["family"]
        if family in ABSOLUTE:
            failures.append(
                f"{row['id']} is an anonymous roof of family {family} in the "
                f"{row['layer']} layer — {ABSOLUTE[family]}")
        elif row["id"] != LEGACY_I2:
            failures.append(
                f"{row['id']} is a SECOND anonymous roof of family I2. The one this "
                f"project carries, {LEGACY_I2}, is a liberty recorded in "
                f"docs/LIBERTIES.md (L93) and not a precedent. A school nobody named "
                f"is a claim that a school stood here and left no record.")

    if not args.quiet:
        for family in INSTITUTIONAL:
            named = census[family]
            print(f"   {family}  target {targets.get(family, '?'):>2}  "
                  f"{len(named)} named record(s) standing: {', '.join(named) or '—'}")

    anon_i2 = [r["id"] for r in found if r["family"] == "I2"]
    if failures:
        print("\n   INSTITUTIONAL CLAIM FAILURES")
        for line in failures:
            print(f"     - {line}")
        return 1 if args.gate else 0

    print(f"   no anonymous roof carries I1 or I3, and I2 holds at "
          f"{len(anon_i2)} ({', '.join(anon_i2) or 'none'}). The town's public "
          f"buildings are named records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
