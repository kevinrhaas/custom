"""Blocks a structure record carries that its own generator did not author (T-0609).

Four parcel expanders — `generate_inferred_infill`, `generate_north_infill`,
`generate_west_infill`, `generate_block_infill` — own their records ENTIRELY: each rebuilds
the file from its recipe and compares the bytes, which is what stops a hand-edit to a
generated roof from surviving. That is the right rule and it has one hole in it: a SECOND
derivation may legitimately write a block onto the same file.

`land_owner` is the first. `tools/resolve_land_tracts.py` writes it onto every structure
whose position falls inside a resolved federal tract, and re-derives it on every commit — so
the block is gated exactly as hard as the recipe is, just by a different tool. Without this
the two gates contradict each other: the join says the block must be there, the parcel says
the file must not differ from the recipe, and no state of the tree passes both.

So the parcels compare the record with the overlay blocks SET ASIDE, and each overlay names
the tool that owns it. Anything not on this list is still drift.
"""
from __future__ import annotations

import json

# key -> the tool whose --check re-derives it
OVERLAYS = {"land_owner": "tools/resolve_land_tracts.py"}


def strip_overlays(text: str) -> str:
    """A committed record's text with every overlay block removed, re-serialised.

    Key order is preserved by the round trip, so a file carrying no overlay comes back
    byte-identical and the parcels' comparison is unchanged for every record but the few
    another derivation has written to.
    """
    doc = json.loads(text)
    if not any(k in doc for k in OVERLAYS):
        return text
    for key in OVERLAYS:
        doc.pop(key, None)
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
