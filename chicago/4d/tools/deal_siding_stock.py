#!/usr/bin/env python3
"""Deal a clapboard stock to every NAMED frame building — T-0049, docs/LIBERTIES.md L148.

Until T-0049 every frame building in the town wore one course rhythm: the
archetypes' shared 0.14 m (~5.5 in) constant. That uniformity is an artefact of
the generator, not a finding about the town — no source states the exposed face
of any Chicago building's siding, and a town supplied by separate shipments of
sawn lumber (by scow from St Joseph — docs/research/02-flora.md) did not side
every building from one pile.

So the exposure is RECONSTRUCTED, invented within a bound, and this tool is the
deal. The bound is a set of four period mill sidings, stated as the exposed face
("to the weather"):

    4.5 in -> 0.114 m      5 in -> 0.127 m
    5.5 in -> 0.140 m      6 in -> 0.152 m

The rule, in full — deterministic, so the committed records re-derive:

1. Only NAMED frame records are dealt (archetype frame_dwelling /
   frame_storefront / frame_tavern, id not prefixed recon_/inf_ and not owned
   by the inferred-household programme's buildings list). Derived records —
   the anonymous parcels AND the programme's named buildings — re-derive
   byte-exact from their recipes and cannot be hand-edited; they keep the
   archetypes' 0.14 m default and count here as fixed 0.140 m neighbours, so a
   dealt building standing among them is never dealt the stock they already
   wear. Dealing the recipes their own stocks is follow-up work, filed as its
   own ticket.
2. Only the phase the 1835 scene resolves is dealt, and only when its resolved
   cladding is clapboard — a vertical-board wall has no course to expose.
3. The base stock is keyed to the phase's construction season
   ((year + quarter) % 4): buildings sided from the same season's shipments
   tend toward the same stock, which is the one supply fact the deal can lean
   on. It is a tendency, not evidence about any building — the note on every
   value says so.
4. Then the deal advances a building's stock until no other frame building
   within NEIGHBOUR_M shares it (named ones in id order, anonymous ones fixed
   at 0.140 m). That separation is not a claim about 1835; it is the surface
   variety T-0049 reconstructs, recorded as such.

Run with no arguments to (re)write the records; --check verifies the committed
values still re-derive from this rule and exits 1 on drift.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRUCTURES = ROOT / "data" / "structures"

FRAME_ARCHETYPES = ("frame_dwelling", "frame_storefront", "frame_tavern")
GENERATED_PREFIXES = ("recon_", "inf_")
# The inferred-household programme regenerates its buildings' records byte-exact
# (tools/generate_inferred_households.py --check), named ones included, so the
# deal must not write into them any more than into a recon_ record. Its
# `buildings` list is the ownership roster.
HOUSEHOLD_PROGRAMME = ROOT / "data" / "reconstruction" / "1835_inferred_household_programme.json"
TARGET = dt.date(1835, 7, 1)

# The period stock set, exposed face in metres, keyed by the original inches.
STOCKS = [("4.5 in", 0.114), ("5 in", 0.127), ("5.5 in", 0.140), ("6 in", 0.152)]
DEFAULT_M = 0.140            # the archetypes' own default, what undealt records wear
NEIGHBOUR_M = 60.0           # within this, two frame buildings must not share a stock

NOTE = ("INVENTED WITHIN A STOCK SET, NOT DERIVED. No source states the exposed face "
        "of any Chicago building's siding. The value is one of four period mill "
        "sidings — 4.5, 5, 5.5 or 6 in to the weather; this record wears {inches} — "
        "dealt by tools/deal_siding_stock.py: keyed to the phase's construction "
        "season, because buildings sided from the same season's shipments of St "
        "Joseph sawn lumber tend toward one stock, then advanced so no frame "
        "building within 60 m shares this one's. The separation is the surface "
        "variety T-0049 reconstructs, not a claim about 1835. docs/LIBERTIES.md "
        "L148 owns the invention.")


def resolve_phase(structure: dict) -> dict | None:
    """The scene rule, identical to generators/build.py and tools/validate.py."""
    hits = []
    for ph in structure.get("phases", []):
        r = ph.get("documented_range", {})
        try:
            frm = dt.date.fromisoformat(r["from"])
            to = dt.date.fromisoformat(r["to"])
        except (KeyError, ValueError):
            continue
        if frm <= TARGET <= to:
            hits.append(ph)
    if len(hits) > 1:
        raise SystemExit(f"{structure['id']}: {len(hits)} phases cover {TARGET}")
    return hits[0] if hits else None


def frame_records() -> list[tuple[Path, dict, dict]]:
    out = []
    for path in sorted(STRUCTURES.glob("*.json")):
        st = json.loads(path.read_text(encoding="utf-8"))
        if st.get("archetype") not in FRAME_ARCHETYPES:
            continue
        ph = resolve_phase(st)
        if ph is None:
            continue
        out.append((path, st, ph))
    return out


def cladding_of(ph: dict) -> str:
    a = (ph.get("form") or {}).get("cladding")
    return "clapboard" if a is None else a.get("value", "clapboard")


def position_of(ph: dict) -> tuple[float, float] | None:
    pos = ph.get("position") or {}
    e, n = pos.get("utm_e"), pos.get("utm_n")
    return None if e is None or n is None else (float(e), float(n))


def season_key(ph: dict) -> int:
    # Year plus quarter, not year*4+quarter: any multiple of len(STOCKS) folds to
    # zero under the modulus, which would silently erase one of the two terms.
    d = dt.date.fromisoformat(ph["documented_range"]["from"])
    return (d.year + (d.month - 1) // 3) % len(STOCKS)


def programme_owned() -> frozenset[str]:
    doc = json.loads(HOUSEHOLD_PROGRAMME.read_text(encoding="utf-8"))
    return frozenset(b["id"] for b in doc.get("buildings", []))


def is_derived(st: dict, owned: frozenset[str]) -> bool:
    """True when another tool regenerates this record byte-exact."""
    return st["id"].startswith(GENERATED_PREFIXES) or st["id"] in owned


def deal() -> dict[str, tuple[str, float]]:
    """structure id -> (inches label, exposure m) for every named clapboard record."""
    records = frame_records()
    owned = programme_owned()
    taken: list[tuple[float, float, float]] = []          # (e, n, exposure) already fixed
    for _, st, ph in records:
        if is_derived(st, owned):
            pos = position_of(ph)
            if pos is not None:
                taken.append((*pos, DEFAULT_M))
    dealt: dict[str, tuple[str, float]] = {}
    for _, st, ph in records:
        if is_derived(st, owned):
            continue
        if cladding_of(ph) != "clapboard":
            continue
        pos = position_of(ph)
        near = set()
        if pos is not None:
            near = {m for e, n, m in taken
                    if math.hypot(e - pos[0], n - pos[1]) <= NEIGHBOUR_M}
        idx = season_key(ph)
        for step in range(len(STOCKS)):
            inches, metres = STOCKS[(idx + step) % len(STOCKS)]
            if metres not in near:
                break
        dealt[st["id"]] = (inches, metres)
        if pos is not None:
            taken.append((*pos, metres))
    return dealt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify the committed values still re-derive from the rule")
    args = ap.parse_args()

    dealt = deal()
    owned = programme_owned()
    drift = []
    changed = 0
    for path, st, ph in frame_records():
        want = dealt.get(st["id"])
        got = (ph.get("form") or {}).get("siding_exposure_m")
        if want is None:
            if got is not None and not is_derived(st, owned):
                drift.append(f"{st['id']}: carries siding_exposure_m but the rule "
                             f"deals it none")
            continue
        inches, metres = want
        attr = {"value": metres, "confidence": "reconstructed",
                "note": NOTE.format(inches=inches)}
        if got == attr:
            continue
        if args.check:
            drift.append(f"{st['id']}: siding_exposure_m has drifted from the deal"
                         if got is not None else
                         f"{st['id']}: the rule deals a stock and the record has none")
            continue
        ph.setdefault("form", {})["siding_exposure_m"] = attr
        path.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        changed += 1
    if drift:
        print("SIDING STOCK DRIFT")
        for item in drift:
            print(f"  - {item}")
        return 1
    mode = "verified" if args.check else f"dealt ({changed} record(s) rewritten)"
    print(f"{mode}: {len(dealt)} named frame building(s) carry a stock; "
          f"{len(STOCKS)} stocks in the set")
    return 0


if __name__ == "__main__":
    sys.exit(main())
