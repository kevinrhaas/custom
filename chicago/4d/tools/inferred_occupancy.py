#!/usr/bin/env python3
"""The occupancy ledger the anonymous-infill generators read.

`tools/generate_inferred_infill.py` and `tools/generate_north_infill.py` build the
anonymous roofs of the 665-roof programme and re-derive them byte-for-byte on every
commit. Phase two of the inferred-residents programme (docs/ROADMAP.md K1) ADOPTS
some of those roofs: an inferred household takes one as its dwelling or its shop,
and the roof stops being anonymous massing and becomes a building with an argument
behind it.

That has to reach the structure record, or the adoption exists only in
`data/residents/` and a visitor clicking the building is told nothing. But editing
a generated record by hand would fail the very drift check that makes the
anonymous parcels trustworthy. So the link is data: the household programme names
the roof, this module hands the resulting `occupants` block to whichever generator
owns that roof, and both parcels stay re-derivable from their recipes.

An adopted roof's own existence, position and footprint stay exactly as
conjectural as they were. Nothing here is evidence that a building stood on that
spot; it is evidence about who the town must have held, attached to a roof the
programme had already placed.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRAMME = ROOT / "data" / "reconstruction" / "1835_inferred_household_programme.json"

TRADE_LABEL = {
    "barber_surgeon": "barber-surgeon",
    "boarding_house_keeper": "boarding-house keeper",
    "harness_maker": "harness maker",
    "tavern_keeper": "tavern keeper",
}


def label(occupation: str) -> str:
    return TRADE_LABEL.get(occupation, occupation.replace("_", " "))


def _load() -> dict:
    if not PROGRAMME.exists():
        return {}
    return json.loads(PROGRAMME.read_text(encoding="utf-8"))


def occupancy() -> dict[str, dict]:
    """structure_id -> the `occupants` attested block that structure should carry.

    Only anonymous `recon_*` roofs appear here; the programme's own new records
    carry their occupants inline.
    """
    out: dict[str, dict] = {}
    programme = _load()
    for h in programme.get("households", []):
        for key in ("lives_at", "works_at"):
            sid = h.get(key)
            if not sid or not sid.startswith("recon_"):
                continue
            entry = out.setdefault(sid, {"households": [], "roles": []})
            if h["id"] not in entry["households"]:
                entry["households"].append(h["id"])
                entry["roles"].append((h["occupation"], key, h["ordinal"], h["of"]))

    blocks: dict[str, dict] = {}
    for sid, entry in out.items():
        parts = []
        for occ, key, ordinal, of in entry["roles"]:
            what = "dwelling of" if key == "lives_at" else "workplace of"
            parts.append(f"the {what} an inferred {label(occ)}'s household "
                         f"({ordinal} of {of} this layer infers)")
        blocks[sid] = {
            "value": "An inferred household; no name is claimed",
            "confidence": "derived",
            "sources": ["andreas_1884_v1", "owner_chicago_1835_reconstruction_spec_2026"],
            "note": ("ADOPTED BY THE INFERRED-HOUSEHOLD PROGRAMME (docs/ROADMAP.md K1, phase "
                     "two). This anonymous roof is " + " and ".join(parts) + ": "
                     + ", ".join(entry["households"]) + " in data/residents/households/. THE "
                     "ROOF'S OWN EXISTENCE, POSITION AND FOOTPRINT REMAIN CONJECTURAL and are "
                     "unchanged by the adoption; what the adoption adds is an argued occupant "
                     "instead of an anonymous count-unit. The occupant is hypothesised from the "
                     "town's demonstrable needs - the 1835 census of 3,265 people in 398 "
                     "dwellings against the trades Andreas's 1833 roster names - and is not a "
                     "person: no name is claimed and no figure is drawn."),
        }
    return blocks


if __name__ == "__main__":
    for k, v in sorted(occupancy().items()):
        print(k, "->", v["note"][:90], "...")
