#!/usr/bin/env python3
"""Stop a person record asserting an absence its own file contradicts.

T-0693, and the owner's words that opened it, 2026-09-04: *"and there is evidence in
there he is a druggist but that is not in his person record"*.

`hh_allen_edward_richards.json` states Edward Richards Allen's trade three times — in the
directory line quoted on his card, in the `directories` block's `occupation_later`, and
again in the person's own note — and then the one field a reader and every downstream tool
actually read, `persons[].occupation.value`, says `none_recorded`. That value is not a
hedge, it is a claim, and it is the only one of the four that is untrue. Ninety-seven
cards said it.

THIS IS NOT BACK-PROJECTION, and it must never become it. A trade printed in 1839 is
evidence about 1839. Nobody here is given a shop in the 1835 scene, no 1835 grade moves,
and the `directories` block — which is correct, dated and properly walled off from the
1835 claims — is not touched. What changes is that the ABSENCE gets a date on it, because
two different states had been sharing one string:

    none_recorded            no trade is recorded for this person ANYWHERE in this
                             project's evidence.
    none_recorded_in_1835    no trade is recorded for this person in the scene window,
                             AND the project holds a dated later trade for them.

A reader could not tell those apart, and neither could a tool. Now both can.

WHAT IS DERIVED. The value is derived from the record: a person carries
`none_recorded_in_1835` exactly when their household's `directories.people[]` holds an
`occupation_later` with a value for them. The note's closing sentence is derived from that
same reading — its source id, its printed trade and its `describes_date` — so `--check`
re-derives it rather than trusting prose. The rest of each note is the prose the minting
pass wrote about that person's own evidence and is preserved: this pass adds a dated
sentence, it does not overwrite an account of why the 1835 record is silent.

    tools/reconcile_occupation_dates.py --report      the population, before and after
    tools/reconcile_occupation_dates.py --build       write the person records
    tools/reconcile_occupation_dates.py --check       the invariant holds (tools/check.sh)
    tools/reconcile_occupation_dates.py --self-test   the assertions still fire when broken
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOUSEHOLDS = ROOT / "data" / "residents" / "households"
INDEX = ROOT / "data" / "residents" / "index.json"

NONE_ANYWHERE = "none_recorded"
NONE_IN_WINDOW = "none_recorded_in_1835"

# Both of these mean "this person has no trade recorded for 1835". Every tool that asks
# that question must ask it of the pair, never of `none_recorded` alone — that is the one
# way this change could quietly break a caller, so the set is named and shared.
NO_TRADE_IN_1835 = (NONE_ANYWHERE, NONE_IN_WINDOW)


def load(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def later_trades(household) -> dict:
    """person_id -> the dated later trade its own file carries for them."""
    out = {}
    people = ((household.get("directories") or {}).get("people")) or []
    for entry in people:
        if not isinstance(entry, dict):
            continue
        later = entry.get("occupation_later")
        pid = entry.get("person_id")
        if not isinstance(later, dict) or not later.get("value") or not pid:
            continue
        out[pid] = later
    return out


def dated_sentence(later) -> str:
    """The closing sentence of the note, derived from the reading itself."""
    sources = later.get("sources") or []
    source = sources[0] if sources else "the directory reading on this card"
    return (
        f"WHAT IS KNOWN, AND WHEN — this is an absence for 1835, not an absence "
        f"altogether: {source} prints \"{later.get('value')}\" against this person and "
        f"describes {later.get('describes_date')}. That reading is held in this "
        f"household's directories block, dated there, and is read back onto no 1835 "
        f"claim; the value reads {NONE_IN_WINDOW} rather than {NONE_ANYWHERE} because "
        f"the project holds a dated trade for this person and holds none for the scene "
        f"window. Nothing about the 1835 record — its grade, its date, its placement — "
        f"moved to say so. T-0693."
    )


def survey(paths=None):
    """Every person record, sorted into the states this tool is responsible for."""
    paths = paths if paths is not None else sorted(HOUSEHOLDS.glob("*.json"))
    rows = []
    for path in paths:
        household = load(path)
        trades = later_trades(household)
        for person in household.get("persons") or []:
            occ = person.get("occupation")
            if not isinstance(occ, dict):
                continue
            rows.append({
                "path": path,
                "household": household.get("id"),
                "person": person.get("id"),
                "name": person.get("name"),
                "value": occ.get("value"),
                "note": occ.get("note") or "",
                "later": trades.get(person.get("id")),
            })
    return rows


def problems(rows) -> list:
    """The invariant, stated once and read by --check and --self-test alike."""
    out = []
    for row in rows:
        where = f"{row['household']}/{row['person']}"
        if row["later"] and row["value"] == NONE_ANYWHERE:
            out.append(f"{where} asserts {NONE_ANYWHERE} while its own file carries a "
                       f"trade for it dated {row['later'].get('describes_date')} — "
                       f"run --build")
        elif not row["later"] and row["value"] == NONE_IN_WINDOW:
            out.append(f"{where} reads {NONE_IN_WINDOW} and its file carries no dated "
                       f"later trade to date the absence against")
        elif row["later"] and row["value"] == NONE_IN_WINDOW:
            want = dated_sentence(row["later"])
            if not row["note"].endswith(want):
                out.append(f"{where} does not close its note with the sentence derived "
                           f"from its own reading — run --build")
    return out


def rewrite(household) -> int:
    """Apply the reconciliation to one household in place. Returns persons changed."""
    trades = later_trades(household)
    changed = 0
    for person in household.get("persons") or []:
        occ = person.get("occupation")
        if not isinstance(occ, dict):
            continue
        later = trades.get(person.get("id"))
        if not later or occ.get("value") != NONE_ANYWHERE:
            continue
        occ["value"] = NONE_IN_WINDOW
        note = (occ.get("note") or "").strip()
        sentence = dated_sentence(later)
        # The minting passes re-derive `occupation` from their own evidence and carry the
        # NOTE over as a tail, so on a rebuild the sentence is already there while the
        # value has gone back to `none_recorded`. Appending unconditionally would print it
        # twice on every rebuild; the value is set either way.
        if not note.endswith(sentence):
            note = f"{note} {sentence}".strip() if note else sentence
        occ["note"] = note
        changed += 1
    return changed


def cmd_build() -> int:
    cards = persons = 0
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        household = load(path)
        changed = rewrite(household)
        if not changed:
            continue
        # `indent=1, ensure_ascii=False` and a trailing newline: the households are
        # written that way and a reformat would bury 97 real edits in a whole-file diff.
        path.write_text(json.dumps(household, indent=1, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        cards += 1
        persons += changed
    print(f"  rewrote {persons} person record(s) across {cards} household file(s): "
          f"{NONE_ANYWHERE} -> {NONE_IN_WINDOW}, each with the date its trade is known for")
    if not cards:
        print("  nothing to do — every dated absence is already dated")
    return 0


def cmd_report() -> int:
    rows = survey()
    total = len(rows)
    with_later = [r for r in rows if r["later"]]
    undated = [r for r in with_later if r["value"] == NONE_ANYWHERE]
    dated = [r for r in with_later if r["value"] == NONE_IN_WINDOW]
    trade = [r for r in with_later if r["value"] not in NO_TRADE_IN_1835]
    print(f"\n  person records in the residents layer         {total:>5}")
    print(f"  …carrying a dated later trade of their own    {len(with_later):>5}")
    print(f"      of those, a trade recorded for 1835 too   {len(trade):>5}")
    print(f"      of those, the absence dated to 1835       {len(dated):>5}")
    print(f"      of those, an UNDATED absence (the defect) {len(undated):>5}")
    print(f"  …reading {NONE_ANYWHERE} with no later trade  "
          f"{sum(1 for r in rows if not r['later'] and r['value'] == NONE_ANYWHERE):>5}")
    listing = sorted(undated or dated, key=lambda r: r["person"] or "")
    if listing:
        head = "STILL UNDATED" if undated else "DATED BY THIS PASS"
        print(f"\n  {head} — every card, so the sweep is checkable by hand:\n")
        for row in listing:
            later = row["later"]
            print(f"    {row['person']:<38} {later.get('describes_date')}  "
                  f"{later.get('value')}")
    print()
    return 0


def cmd_check() -> int:
    found = problems(survey())
    vocab = (load(INDEX).get("vocabulary") or {}).get("occupations") or []
    if NONE_IN_WINDOW not in vocab:
        found.append(f"vocabulary.occupations does not declare {NONE_IN_WINDOW}; "
                     f"data/residents/index.json is what validate.py reads")
    for line in found[:20]:
        print(f"  FAIL {line}")
    if len(found) > 20:
        print(f"  FAIL …and {len(found) - 20} more")
    if found:
        return 1
    rows = survey()
    dated = sum(1 for r in rows if r["value"] == NONE_IN_WINDOW)
    print(f"  ok    {dated} dated absence(s) carry their date, their trade and its year; "
          f"no record asserts an absence its own file contradicts")
    return 0


def cmd_self_test() -> int:
    """The assertions must fire when the data is broken, or --check proves nothing."""
    ok = True

    def case(name, rows, want):
        nonlocal ok
        got = len(problems(rows)) > 0
        mark = "ok   " if got == want else "FAIL "
        if got != want:
            ok = False
        print(f"  {mark} {name}")

    later = {"value": "druggist, Leroy M. Boyce", "describes_date": 1839,
             "sources": ["fergus_chicago_directory_1839"]}

    def row(value, note="", carries=True):
        return [{"path": None, "household": "hh_x", "person": "x", "name": "X",
                 "value": value, "note": note, "later": later if carries else None}]

    case("a dated trade beside an undated absence is caught",
         row(NONE_ANYWHERE), True)
    case("the dated absence, with its derived sentence, passes",
         row(NONE_IN_WINDOW, "Some prose. " + dated_sentence(later)), False)
    case("a dated absence whose note lost the sentence is caught",
         row(NONE_IN_WINDOW, "Some prose."), True)
    case("a dated absence on a card with no later trade is caught",
         row(NONE_IN_WINDOW, "Some prose. " + dated_sentence(later), carries=False), True)
    case("an absence on a card with no later trade is left alone",
         row(NONE_ANYWHERE, "Some prose.", carries=False), False)
    case("a person with a real 1835 trade is none of this tool's business",
         row("druggist", "Some prose."), False)

    # …and the rewrite must be idempotent, or --build churns the layer every run.
    household = {"id": "hh_x",
                 "directories": {"people": [{"person_id": "x", "occupation_later": later}]},
                 "persons": [{"id": "x", "occupation": {"value": NONE_ANYWHERE,
                                                        "note": "Some prose."}}]}
    first = rewrite(household)
    second = rewrite(household)
    if first != 1 or second != 0:
        print("  FAIL  --build is not idempotent")
        ok = False
    else:
        print("  ok    --build writes once and is a no-op the second time")

    # The rebuild shape: a mint has re-derived the value back to `none_recorded` while
    # carrying this pass's sentence over on the note. The sentence must not be doubled.
    rebuilt = {"id": "hh_x",
               "directories": {"people": [{"person_id": "x", "occupation_later": later}]},
               "persons": [{"id": "x", "occupation": {
                   "value": NONE_ANYWHERE,
                   "note": "Some prose. " + dated_sentence(later)}}]}
    rewrite(rebuilt)
    note = rebuilt["persons"][0]["occupation"]["note"]
    if note.count("WHAT IS KNOWN, AND WHEN") != 1:
        print("  FAIL  a rebuild doubles the dated sentence on the note")
        ok = False
    else:
        print("  ok    a mint's rebuild re-dates the value without doubling the sentence")

    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.build:
        return cmd_build()
    if args.check:
        return cmd_check()
    if args.report:
        return cmd_report()
    if args.self_test:
        return cmd_self_test()
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
