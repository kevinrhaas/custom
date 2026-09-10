#!/usr/bin/env python3
"""The cards a merge folded away, still readable by the id they were frozen under.

WHY THIS EXISTS. `tools/consolidate_town_cards.py` folds a town card onto the person
it turned out to be, and its whole promise is that **a merge loses nothing**: the
record is copied whole to `data/residents/merged/<household>.json` with a
`merged_into` block, and `index.json` grows a `merged` redirect table so that "every
`person_id` any file cites — the crosswalks, identity_master.json, the smoke cohorts,
the placed-resident parcels — still resolves to a person". Every consumer but ONE was
reached by that promise, because the crosswalks are all regenerated from the layer as
it stands. The frozen research cohorts are not: their membership is a hardcoded list
of ids, frozen on the day the cohort was drawn, and `tools/check.sh` fails the moment
one of those ids is not on a household file — "frozen cohort member X is no longer in
the town".

The card HAS not left the town. It stands under another id, and the record the cohort
was drawn on is still on disk, byte for byte as it was frozen. T-0842 is where this
first bit: the letter-list card `vanderbogart_h` is in the pilot cohort and in cohort
15, and it folded onto Dr Henry Van der Bogart.

WHY THE FROZEN RECORD AND NOT THE SURVIVOR. A cohort is a record of WHAT WAS
RESEARCHED, and T-0737's acceptance forbids a regeneration from reshuffling
membership, because landed research tickets cite cohort membership by number. Resolve
`vanderbogart_h` to the survivor instead and the pilot's frozen strata move under it —
a letter-list-only member becomes a civic-minted man, the 25/25 stratification the
cohort asserts stops holding, and the cohort would be claiming to have researched a
person it never drew. Reading the superseded record keeps the cohort EXACTLY what it
was: the same 75 people, the same strata, the same starting snapshots. What the merge
adds is a fact ABOUT that member, `merged_into`, which the reader can follow.

WHAT IT DELIBERATELY DOES NOT DO. It does not put folded people back in the town. Only
a caller that already holds a frozen id asks for them, one id at a time, and a fold is
never a way to be selected INTO a cohort — the selectors' own minting paths read the
households folder and nothing here.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGED = ROOT / "data" / "residents" / "merged"


def folded_households() -> dict:
    """household_id -> the household record as it stood when the merge landed.

    Each carries a `merged_into` block naming the person and household it now stands
    under, so a caller can say so rather than silently pretending nothing happened.
    """
    out = {}
    if not MERGED.is_dir():
        return out
    for path in sorted(MERGED.glob("*.json")):
        stub = json.loads(path.read_text(encoding="utf-8"))
        record = stub.get("superseded_record")
        if not isinstance(record, dict) or not record.get("id"):
            continue
        record = dict(record)
        record["merged_into"] = stub.get("merged_into")
        out[record["id"]] = record
    return out


def folded_people() -> dict:
    """person_id -> (household, person), from the same superseded records."""
    out = {}
    for record in folded_households().values():
        for person in record.get("persons") or []:
            if person.get("id"):
                out[person["id"]] = (record, person)
    return out


if __name__ == "__main__":
    hh, people = folded_households(), folded_people()
    print("%d folded household(s), %d folded person(s)" % (len(hh), len(people)))
    for pid, (record, _) in sorted(people.items()):
        into = (record.get("merged_into") or {}).get("person")
        print("  %-28s -> %s" % (pid, into))
