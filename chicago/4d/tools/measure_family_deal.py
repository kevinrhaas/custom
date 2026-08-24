#!/usr/bin/env python3
"""Can the block generator build every family it is allowed to deal? (T-0142)

WHY THIS EXISTS. The platted-block generator does not choose its families: the 665-roof
schedule does, and a recipe entry names one. So a family is either buildable at EVERY
size the crosswalk lets it be dealt at, or the schedule is holding a card that kills the
run whenever it comes up — and it comes up rarely enough that the standing records look
fine. That is exactly what happened to H2. `blk_randolph_dearborn`'s second deal asked
for a merchant house, the family's authored eave band runs 18-21 ft, `frame_dwelling`
refuses a two-storey wall over 6.2 m because the one attested ceiling in this dataset is
the Green Tree's seven and a half feet, and the sample landed at 6.234 m. Two H2s were
already standing, both under the limit by luck, so nothing in the repo said the family
was broken.

Standing records cannot answer that question — there are two H1s and two H2s in the
whole parcel. So this deals each family several hundred synthetic instances through the
generator's OWN sampling and form rules, and asks two things of each:

  1. the archetype the family resolves through will BUILD it — `from_phase` is the same
     call the generator makes before it writes a record; and
  2. every value that cites the family's band is INSIDE that band — the same reading
     `tools/measure_band_claims.py` takes of the records that landed, taken here of the
     records that could.

It builds no geometry and needs no Blender: `from_phase` validates, which is the step
that refuses. Roughly a second for the whole table.

    tools/measure_family_deal.py            the report
    tools/measure_family_deal.py --gate     exit 1 on any refusal
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generators"))
sys.path.insert(0, str(ROOT / "tools"))

from family_bands import dimensions_m, families, pitch_band_deg  # noqa: E402
# The SAME edge epsilons the landed-record gate reads its bands with, imported rather
# than retyped: a value is either inside its band or not, and two gates disagreeing
# about the last millimetre would be a third opinion nobody asked for.
from measure_band_claims import EPS_DEG, EPS_FT  # noqa: E402
import generate_block_infill as blk  # noqa: E402

# How many instances of each family. The failure this exists to catch is a band whose
# TAIL is unbuildable, so the sweep has to be dense enough to reach a tail that is a few
# per cent of the band: 400 deals put about a dozen samples in the top three per cent.
DEALS = 400

# The band a value cites, and how to read the value out of the form. `levels` is not
# tested here — the crosswalk authors it as a value for every family the block generator
# deals, so `family_bands.storeys` cannot put it outside anything.
FT_M = 0.3048


def eave_band_m(spec: dict) -> tuple[float, float] | None:
    from family_bands import RANGE_RE
    m = RANGE_RE.match(str(spec.get("eave_ft") or ""))
    return (float(m.group(1)) * FT_M, float(m.group(2)) * FT_M) if m else None


def sweep(family: str, spec: dict) -> dict:
    """Deal one family `DEALS` times and count what will not build."""
    refused: list[str] = []
    outside: list[str] = []
    module = importlib.import_module(f"archetypes.{spec['archetype']}_params")
    for i in range(DEALS):
        key = f"deal_{family}_{i:04d}"
        width, depth = dimensions_m(family, spec["band_ft"], key)
        _finish, paint = blk.finish_for(key)
        form = blk.form_for(family, spec, key, width, depth, paint)
        phase = {
            "id": "inferred_1835",
            "footprint": {"polygon": [[0, 0], [width, 0], [width, depth], [0, depth]],
                          "confidence": "reconstructed"},
            "form": form,
        }
        try:
            module.from_phase(phase)
        except Exception as exc:                                  # noqa: BLE001
            refused.append(f"{key} {width:.2f}x{depth:.2f} m: {exc}")

        def value(attr):
            entry = form.get(attr)
            return entry.get("value") if entry else None

        pitch, eave = value("roof_pitch_deg"), value("wall_height_m")
        band = pitch_band_deg(spec.get("roof"))
        if band and pitch is not None and not (band[0] - EPS_DEG <= pitch
                                               <= band[1] + EPS_DEG):
            outside.append(f"{key}: pitch {pitch} outside {band[0]:.1f}-{band[1]:.1f} deg")
        eband = eave_band_m(spec)
        eps_m = EPS_FT * FT_M
        if eband and eave is not None and not (eband[0] - eps_m <= eave
                                               <= eband[1] + eps_m):
            outside.append(f"{key}: eave {eave} m outside "
                           f"{eband[0]:.2f}-{eband[1]:.2f} m")
    return {"refused": refused, "outside": outside}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--only", help="one family id")
    args = ap.parse_args()

    table = families()
    wanted = [args.only] if args.only else sorted(blk.FUNCTIONS)
    bad = 0
    print(f"   {DEALS} synthetic deals per family, through the block generator's own "
          f"sampling")
    print(f"   {'family':7s} {'archetype':17s} {'refused':>8s} {'off band':>9s}")
    for family in wanted:
        spec = table.get(family)
        if not spec or not spec.get("band_ft"):
            print(f"   {family:7s} no footprint band in the crosswalk — not dealt")
            continue
        result = sweep(family, spec)
        n_ref, n_out = len(result["refused"]), len(result["outside"])
        bad += n_ref + n_out
        flag = "" if not (n_ref or n_out) else "  <-"
        print(f"   {family:7s} {spec['archetype']:17s} {n_ref:8d} {n_out:9d}{flag}")
        for line in result["refused"][:3] + result["outside"][:3]:
            print(f"           {line}")
    print()
    if bad:
        print(f"   {bad} deal(s) the generator cannot make. A family the schedule may "
              f"deal and the\n   generator cannot build is a run that dies on the day "
              f"the card comes up.")
        return 1 if args.gate else 0
    print("   every family the block schedule may deal builds at every size its own "
          "band allows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
