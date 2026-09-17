#!/usr/bin/env python3
"""Hold dated shoreline states apart and preserve source disagreement as a band.

This is a contract check, not a terrain generator.  It proves four things:

* 1812, 1835 and the 1880s resolve through their terrain epochs to three
  different shoreline-state ids;
* planned states do not borrow the active 1835 geometry while waiting for their
  own tickets;
* every active geometry reference resolves to the named feature and source; and
* the 1834/1849 comparison is the full polygon re-derived from the two committed
  readings, with no adopted midpoint hiding their disagreement.
"""
from __future__ import annotations

import argparse
import copy
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TERRAIN = ROOT / "data" / "terrain"
STATES_PATH = TERRAIN / "shoreline_states.json"
BANDS_PATH = TERRAIN / "shoreline_disagreement_bands.geojson"
EPOCHS_PATH = TERRAIN / "epochs.json"
DATUM_PATH = ROOT / "data" / "datum.json"
OVERLAP_PATH = TERRAIN / "epochs" / "e1834_harbor_cut" / "lake_shore_below_twelfth.geojson"

CONSTRAINTS_PATH = TERRAIN / "1880s_scene_date_constraints.json"


def scene_date_1880s() -> date:
    """The 1880s address date, READ rather than typed (T-1249).

    This constant used to be the literal ``date(1885, 7, 1)``.  T-1152 needed
    some day inside the decade to prove that the 1880s address resolved through
    its own epoch to its own shoreline state, and nothing documented the day it
    picked — it was scaffolding for a different assertion.  It was also three
    and a half years before the Glessner House was finished, so the one scene
    the 1880s epoch exists to carry could not have stood on it.  The date now
    comes out of the committed readings that derive it, and
    tools/check_1880s_scene_date.py re-derives those readings on every commit.
    """
    doc = json.loads(CONSTRAINTS_PATH.read_text(encoding="utf-8"))
    return date.fromisoformat(doc["adopted"]["date"])


ADDRESS_DATES = {
    "1812": date(1812, 8, 15),
    "1835": date(1835, 7, 1),
    "1880s": scene_date_1880s(),
}
EXPECTED_IDS = {
    "1812": "shore_1812_pre_cut",
    "1835": "shore_1835_harbor_cut",
    "1880s": "shore_1880s_ic_edge",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso(value: str) -> date:
    return date.fromisoformat(value)


def epoch_for(epochs: list[dict], target: date) -> dict | None:
    matches = [e for e in epochs
               if parse_iso(e["from"]) <= target <= parse_iso(e["to"])]
    return matches[0] if len(matches) == 1 else None


def feature_at(relative: str, feature_id: str) -> dict | None:
    path = (TERRAIN / relative).resolve()
    if TERRAIN.resolve() not in path.parents or not path.exists():
        return None
    doc = load(path)
    return next((f for f in doc.get("features", []) if f.get("id") == feature_id), None)


def expected_band(overlap: dict, datum: dict) -> tuple[list[list[float]], list[float]]:
    measured = overlap["measured"]["overlap"]
    ns = measured["stations_n_m"]
    wright = measured["wright_1834_e_m"]
    rees = measured["rees_1849_e_m"]
    oe, on = datum["origin_utm_e"], datum["origin_utm_n"]
    west_to_south = [[round(oe + e, 1), round(on + n, 1)]
                     for n, e in zip(ns, wright)]
    east_to_north = [[round(oe + e, 1), round(on + n, 1)]
                     for n, e in reversed(list(zip(ns, rees)))]
    ring = west_to_south + east_to_north + [west_to_south[0]]
    spreads = [round(w - r, 1) for w, r in zip(wright, rees)]
    return ring, spreads


def validate(states_doc: dict, bands_doc: dict, epochs_doc: dict,
             datum: dict, overlap: dict) -> list[str]:
    bad: list[str] = []
    states_list = states_doc.get("states", [])
    state_ids = [s.get("id") for s in states_list]
    if len(state_ids) != len(set(state_ids)):
        bad.append("shoreline state ids are not unique")
    states = {s.get("id"): s for s in states_list}
    epochs = epochs_doc.get("epochs", [])

    addressed: dict[str, str] = {}
    for label, target in ADDRESS_DATES.items():
        epoch = epoch_for(epochs, target)
        if epoch is None:
            bad.append(f"{label} does not resolve to exactly one terrain epoch")
            continue
        sid = epoch.get("shoreline_state")
        addressed[label] = sid
        if sid != EXPECTED_IDS[label]:
            bad.append(f"{label} resolves through {epoch.get('id')} to {sid!r}, "
                       f"expected {EXPECTED_IDS[label]!r}")
        state = states.get(sid)
        if state is None:
            bad.append(f"{epoch.get('id')} names missing shoreline state {sid!r}")
        elif state.get("epoch_id") != epoch.get("id"):
            bad.append(f"{sid} points at epoch {state.get('epoch_id')!r}, not "
                       f"{epoch.get('id')!r}")

    if len(set(addressed.values())) != len(ADDRESS_DATES):
        bad.append("1812, 1835 and the 1880s do not have separate shoreline-state ids")

    active = states.get(EXPECTED_IDS["1835"], {})
    if active.get("status") != "active" or not active.get("geometry"):
        bad.append("the 1835 shoreline state is not active geometry")
    for label in ("1812", "1880s"):
        planned = states.get(EXPECTED_IDS[label], {})
        if planned.get("status") != "planned":
            bad.append(f"the {label} shoreline state is not explicitly planned")
        if planned.get("geometry") is not None:
            bad.append(f"the planned {label} state borrows geometry before its ticket supplies it")

    source_ids = {p.stem for p in (ROOT / "data" / "sources").glob("*.json")}
    geometry = active.get("geometry") or {}
    for ref in geometry.get("dated_lines", []):
        if ref.get("source_id") not in source_ids:
            bad.append(f"dated line cites unresolved source {ref.get('source_id')!r}")
        if feature_at(ref.get("path", ""), ref.get("feature_id", "")) is None:
            bad.append(f"dated line does not resolve: {ref.get('path')}#"
                       f"{ref.get('feature_id')}")
    band_refs = geometry.get("disagreement_bands", [])
    if band_refs != [{"path": "shoreline_disagreement_bands.geojson",
                      "feature_id": "wright_1834_rees_1849_overlap"}]:
        bad.append("the 1835 state does not name exactly the committed disagreement band")

    features = bands_doc.get("features", [])
    band = next((f for f in features
                 if f.get("id") == "wright_1834_rees_1849_overlap"), None)
    if band is None:
        bad.append("the Wright/Rees shoreline disagreement band is missing")
        return bad
    props = band.get("properties", {})
    if props.get("kind") != "shoreline_source_disagreement_band":
        bad.append("the comparison feature is not declared as a shoreline disagreement band")
    if props.get("resolution") != "unresolved" or props.get("adopted_line") is not None:
        bad.append("the disagreement was resolved to a line instead of left as a band")
    if props.get("state_id") != EXPECTED_IDS["1835"]:
        bad.append("the disagreement band is not attached to the 1835 shoreline state")
    if set(props.get("sources", [])) != {"wright_1834", "rees_rucker_1849"}:
        bad.append("the disagreement band does not cite both boundary sources")
    for ref in props.get("boundary_readings", []):
        if ref.get("source_id") not in source_ids:
            bad.append(f"band boundary cites unresolved source {ref.get('source_id')!r}")
        if feature_at(ref.get("path", ""), ref.get("feature_id", "")) is None:
            bad.append(f"band boundary does not resolve: {ref.get('path')}#"
                       f"{ref.get('feature_id')}")

    expected_ring, spreads = expected_band(overlap, datum)
    geom = band.get("geometry", {})
    rings = geom.get("coordinates", []) if geom.get("type") == "Polygon" else []
    if rings != [expected_ring]:
        bad.append("the disagreement polygon is not the full re-derived 1834/1849 spread")
    measured = props.get("spread_m", {})
    expected_spread = {
        "min": round(min(spreads), 1),
        "max": round(max(spreads), 1),
        "mean": round(sum(spreads) / len(spreads), 1),
    }
    if measured != expected_spread:
        bad.append(f"band spread is {measured}, expected {expected_spread}")
    expected_ns = overlap["measured"]["overlap"]["stations_n_m"]
    if props.get("stations_local_n_m") != expected_ns:
        bad.append("band stations do not match the committed overlap reading")
    return bad


def documents() -> tuple[dict, dict, dict, dict, dict]:
    return (load(STATES_PATH), load(BANDS_PATH), load(EPOCHS_PATH),
            load(DATUM_PATH), load(OVERLAP_PATH))


def self_test(docs: tuple[dict, dict, dict, dict, dict]) -> int:
    cases = []

    d = copy.deepcopy(docs)
    d[0]["states"][2]["id"] = d[0]["states"][0]["id"]
    cases.append(("duplicate dated state ids fail", bool(validate(*d))))

    d = copy.deepcopy(docs)
    d[0]["states"][0]["geometry"] = d[0]["states"][1]["geometry"]
    cases.append(("a planned state borrowing 1835 geometry fails", bool(validate(*d))))

    d = copy.deepcopy(docs)
    d[1]["features"][0]["properties"]["adopted_line"] = "midpoint"
    cases.append(("collapsing the spread to a line fails", bool(validate(*d))))

    d = copy.deepcopy(docs)
    d[1]["features"][0]["geometry"]["coordinates"][0][0][0] += 1.0
    cases.append(("editing the band away from its readings fails", bool(validate(*d))))

    for label, passed in cases:
        print(("OK " if passed else "FAIL ") + label)
    return 0 if all(passed for _, passed in cases) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    docs = documents()
    if args.self_test:
        return self_test(docs)
    bad = validate(*docs)
    for problem in bad:
        print("FAIL", problem)
    if not bad:
        print("OK 1812, 1835 and 1880s resolve to separate shoreline states; "
              "the 1834/1849 spread remains an unresolved 50.0-134.4 m band")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
