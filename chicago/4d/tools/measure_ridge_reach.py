#!/usr/bin/env python3
"""Are a family's four committed claims satisfiable AT ONCE — and where one roof is
outside its ridge band, which of them is actually disobeyed? (T-0148)

`tools/measure_ridge_band.py` measures a ROOF: the ridge one record's own eave, footprint
and pitch make, against the band its family authors. It banked 104 roofs outside their
band and its own note read the residual as structural — "for several families no pitch
inside the authored pitch band reaches the authored ridge band at the footprint the family
authors". That sentence is true and it is the wrong conclusion, because it holds the eave
fixed at whatever the record happens to carry. The eave is not fixed. It is the second of
two values the crosswalk authors as a BAND and the samplers draw from, and a ridge band is
reachable or not from a (footprint, eave) PAIR.

So this asks the question one level up, of the SPECIFICATION rather than of a record:

  1. THE FAMILY SWEEP, which is the gate. For every family that authors a footprint band,
     an eave band and a ridge band, at every footprint in that band and every roof form
     its roof line names: is there ANY eave inside the eave band and ANY pitch inside the
     pitch band that lands the ridge inside the ridge band? Today the answer is yes at
     every footprint of every family, and the gate holds it there — so if the crosswalk is
     ever edited into a family whose own claims cannot all be met, that shows up here as a
     specification fault rather than four runs later as a roof nobody can build.

     Closed form, no search: `ridge = eave + run x tan(pitch)` rises with both, so the
     reachable eaves are the interval `family_bands.eave_window_for_ridge` computes and the
     question is whether it meets the authored eave band.

  2. THE RECORD REPORT. For each roof in `tools/ridge_band_baseline.json`, which claim is
     disobeyed — stated, because the answer differs by parcel and the repairs have
     different owners:

       eave-outside-band   the record's eave is not in the band its own note cites. A
                           retyped constant from before the samplers existed; the ridge is
                           downstream of it. Owned by T-0172.
       eave-uncoupled      the eave IS in band, and no pitch in the family band reaches the
                           ridge band from it — but another eave in the same band would.
                           The sampler drew the eave free of the ridge band. Repaired for
                           the two parcels that sample by `family_bands.eave_for_ridge`.
       no-pitch-band       the family's roof line names no rise:run at all, so the pitch is
                           the generator's own type default and the specification makes no
                           claim this could be measured against.
       unreachable         no (eave in band, pitch in band) reaches it at this footprint —
                           a genuine conflict between the family's own claims. None today.

    python3 tools/measure_ridge_reach.py            the sweep, the report, and the gate
    python3 tools/measure_ridge_reach.py --quiet    the gate alone
"""
from __future__ import annotations

import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import family_bands  # noqa: E402
import ridge_model  # noqa: E402

FT = 0.3048
BASELINE = ROOT / "tools" / "ridge_band_baseline.json"
# The footprint band is swept on a grid rather than at its corners. The run is a
# min/max over width and depth for every archetype here, so the extremes are corners
# and a corner sweep would answer correctly — the grid is there so that an archetype
# whose run is not monotone in both cannot slip past a future reader's edit.
GRID = 21
EAVE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$")


def eave_band_m(eave_ft: str | None) -> tuple[float, float] | None:
    m = EAVE_RE.match(str(eave_ft or ""))
    return (float(m.group(1)) * FT, float(m.group(2)) * FT) if m else None


def roof_forms(roof: str | None) -> list[str]:
    """The roof forms a family's roof line names, in the vocabulary `ridge_model` uses."""
    text = str(roof or "").lower()
    forms = []
    if "gable" in text or "hip" in text or not text:
        forms.append("gable")
    if "shed" in text:
        forms.append("shed")
    return forms or ["gable"]


def reachable(run_m: float, pitch: tuple[float, float], ridge: tuple[float, float],
              eave: tuple[float, float]) -> bool:
    lo, hi = family_bands.eave_window_for_ridge(run_m, pitch[0], pitch[1], ridge)
    return min(hi, eave[1]) - max(lo, eave[0]) >= -1e-9


def sweep() -> list[dict]:
    """Per family and roof form, the footprints from which the ridge band is unreachable."""
    out = []
    for fid, spec in family_bands.families().items():
        band = spec.get("band_ft")
        ridge = family_bands.ridge_band_m(spec.get("ridge_ft"))
        eave = eave_band_m(spec.get("eave_ft"))
        pitch = family_bands.pitch_band_deg(spec.get("roof"))
        arch = spec.get("archetype")
        if band is None or ridge is None or eave is None:
            continue
        if pitch is None:
            out.append({"family": fid, "form": None, "state": "no-pitch-band",
                        "tested": 0, "unreachable": 0})
            continue
        lo_w, lo_d, hi_w, hi_d = band
        for form in roof_forms(spec.get("roof")):
            tested = bad = 0
            worst = None
            for i in range(GRID):
                w = (lo_w + (hi_w - lo_w) * i / (GRID - 1)) * FT
                for j in range(GRID):
                    d = (lo_d + (hi_d - lo_d) * j / (GRID - 1)) * FT
                    run = ridge_model.ridge_run_m(arch, form, w, d, None)
                    if run is None:
                        continue
                    tested += 1
                    if not reachable(run, pitch, ridge, eave):
                        bad += 1
                        if worst is None:
                            worst = (round(w / FT, 1), round(d / FT, 1))
            if tested:
                out.append({"family": fid, "form": form, "state": "swept",
                            "tested": tested, "unreachable": bad, "worst": worst,
                            "ridge_ft": spec.get("ridge_ft"), "archetype": arch})
    return out


def record_report() -> list[dict]:
    """Each banked offender, and which of the family's claims its roof actually disobeys."""
    if not BASELINE.exists():
        return []
    banked = json.loads(BASELINE.read_text(encoding="utf-8")).get("offenders", {})
    fams = family_bands.families()
    out = []
    for path in sorted((ROOT / "data" / "structures").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc["id"] not in banked:
            continue
        spec = fams.get(doc.get("reconstruction", {}).get("family") or "")
        if spec is None:
            continue
        ridge = family_bands.ridge_band_m(spec.get("ridge_ft"))
        eave_band = eave_band_m(spec.get("eave_ft"))
        pitch = family_bands.pitch_band_deg(spec.get("roof"))
        for phase in doc.get("phases", []):
            poly = (phase.get("footprint") or {}).get("polygon")
            form = {k: v.get("value") for k, v in (phase.get("form") or {}).items()}
            if not poly or "roof_pitch_deg" not in form:
                continue
            width = max(p[0] for p in poly) - min(p[0] for p in poly)
            depth = max(p[1] for p in poly) - min(p[1] for p in poly)
            run = ridge_model.ridge_run_m(doc.get("archetype", ""),
                                          str(form.get("roof_type") or "gable"),
                                          width, depth, form.get("gable_front"))
            if run is None or ridge is None or eave_band is None:
                continue
            eave = float(form.get("wall_height_m") or 0.0)
            in_band = eave_band[0] - 1e-9 <= eave <= eave_band[1] + 1e-9
            if pitch is None:
                state = "no-pitch-band"
            elif not in_band:
                state = "eave-outside-band"
            elif reachable(run, pitch, ridge, eave_band):
                state = "eave-uncoupled"
            else:
                state = "unreachable"
            tool, samples = parcel(doc["id"])
            out.append({"id": doc["id"], "family": spec_family(fams, doc),
                        "state": state, "eave_ft": round(eave / FT, 2),
                        "band": spec.get("eave_ft"), "parcel": tool,
                        "samples": samples})
    return out


def spec_family(fams: dict, doc: dict) -> str:
    return doc.get("reconstruction", {}).get("family") or "?"


# WHICH PARCEL A RECORD CAME OUT OF, because the answer to "which claim gives way" is
# the parcel's and not the family's. Two of the five anonymous parcels draw their eave
# and pitch from the family bands; the other three still carry the constants T-0144 and
# T-0145 took out of the North one, and T-0172 owns moving them.
PARCELS = [
    ("recon_1835_north_", "generate_north_infill.py", True),
    ("recon_1835_blk_", "generate_block_infill.py", True),
    ("recon_1835_south_", "generate_inferred_infill.py", False),
    ("recon_1835_west_", "generate_west_infill.py", False),
    ("inf_", "generate_inferred_households.py", False),
]


def parcel(structure_id: str) -> tuple[str, bool]:
    for prefix, tool, samples in PARCELS:
        if structure_id.startswith(prefix):
            return tool, samples
    return "?", False


def main() -> int:
    quiet = "--quiet" in sys.argv
    rows = sweep()
    swept = [r for r in rows if r["state"] == "swept"]
    unpitched = [r for r in rows if r["state"] == "no-pitch-band"]

    # A family may name more than one roof form — C1 is "front gable or shed". The
    # claims are unsatisfiable only if NO form it names works at a given footprint;
    # a form that cannot reach the band while another can is reported and not failed,
    # because the specification still describes a buildable roof there.
    by_family: dict[str, list[dict]] = {}
    for r in swept:
        by_family.setdefault(r["family"], []).append(r)
    conflicts = [f for f, rs in by_family.items() if all(r["unreachable"] for r in rs)]
    narrowed = [r for r in swept if r["unreachable"] and r["family"] not in conflicts]

    print(f"   {len(swept)} family/roof-form combination(s) swept across the whole authored "
          f"footprint band; {len(conflicts)} family(ies) with no reachable form")
    if unpitched:
        print(f"   {len(unpitched)} family(ies) author no pitch band, so the ridge follows the "
              f"generator's own type default and the specification claims nothing testable: "
              f"{', '.join(sorted(r['family'] for r in unpitched))}")
    for n in narrowed:
        print(f"   NOTE {n['family']} as a {n['form']}: {n['unreachable']} of {n['tested']} "
              f"footprints cannot reach ridge {n['ridge_ft']} ft, so the family's other roof "
              f"form is the only one its own bands describe (first at "
              f"{n['worst'][0]}x{n['worst'][1]} ft)")

    if not quiet:
        report = record_report()
        by_state: dict[str, list[dict]] = {}
        for r in report:
            by_state.setdefault(r["state"], []).append(r)
        if report:
            print(f"\n   the {len(report)} banked roof(s), by the claim each one disobeys:")
        for state in ("unreachable", "eave-outside-band", "eave-uncoupled", "no-pitch-band"):
            rows_ = by_state.get(state) or []
            if not rows_:
                continue
            print(f"     {state:18} {len(rows_):3}  {', '.join(sorted({r['family'] for r in rows_}))}")
        sampled = [r for r in report if r["samples"]]
        print(f"\n   by parcel — the two that draw eave and pitch from the family bands "
              f"carry {len(sampled)} of them:")
        for tool in sorted({r["parcel"] for r in report}):
            rows_ = [r for r in report if r["parcel"] == tool]
            print(f"     {tool:34} {len(rows_):3}  "
                  f"{'samples its bands' if rows_[0]['samples'] else 'retyped constants (T-0172)'}")

    for f in conflicts:
        rs = by_family[f]
        print(f"   FAIL {f} ({rs[0]['archetype']}): no roof form it names reaches ridge "
              f"{rs[0]['ridge_ft']} ft at every footprint in its own band — "
              f"{', '.join(r['form'] for r in rs)}")
    return 1 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
