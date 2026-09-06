#!/usr/bin/env python3
"""The unread-initial rulings still describe the cards they rule on (T-0721).

`data/research/residents/letter_list_unread_initials.json` names three town cards whose
stored name carries a digit, and rules that the digit is an initial this project cannot
read. `tools/consolidate_resident_evidence.py` acts on that ruling: it drops the ruled
token so the legible part of the name can be clustered. A ruling that stops matching its
card is therefore a licence with nothing under it, and it fails silently — the card goes
back to being refused, or worse, a token that is no longer the illegible one gets dropped.

    python3 tools/check_unread_initial_rulings.py --check

  * every ruling names a household and a person the residents layer still holds;
  * the card's stored name is still the one the ruling read, letter for letter;
  * the ruled token still stands in that name;
  * no ruling has acquired a letter. `reading` is null on every row and this gate is
    what keeps it null: a run that wanted to write `S.` onto `A. 8. Perry` would have
    to say so here, in a file whose whole subject is that the column cannot be read.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULINGS = ROOT / "data" / "research" / "residents" / "letter_list_unread_initials.json"
HOUSEHOLDS = ROOT / "data" / "residents" / "households"


def glyph_key(token: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (token or "").lower())


def check() -> int:
    doc = json.loads(RULINGS.read_text(encoding="utf-8"))
    rulings = doc.get("rulings") or []
    problems: list[str] = []

    counts = doc.get("counts") or {}
    if counts.get("rulings") != len(rulings):
        problems.append(f"counts.rulings says {counts.get('rulings')}, the file holds "
                        f"{len(rulings)}")
    supplied = [r for r in rulings if r.get("reading") is not None]
    if counts.get("unreadable") != sum(r.get("outcome") == "unreadable" for r in rulings):
        problems.append("counts.unreadable does not match the rows")
    if counts.get("readings_supplied") != len(supplied):
        problems.append("counts.readings_supplied does not match the rows")
    for row in supplied:
        problems.append(f"{row.get('person')} names a letter ({row['reading']!r}). The "
                        "page images are outside this repository; a reading has to come "
                        "from the printed column, not from this file")

    for row in rulings:
        person = row.get("person")
        path = HOUSEHOLDS / f"{row.get('household')}.json"
        if not path.exists():
            problems.append(f"{person}: no household card at {path.name}")
            continue
        card = json.loads(path.read_text(encoding="utf-8"))
        held = next((p for p in card.get("persons") or [] if p.get("id") == person), None)
        if held is None:
            problems.append(f"{person}: {path.name} no longer holds this person")
            continue
        name = held.get("name") or ""
        if name != row.get("held_as"):
            problems.append(f"{person}: the card now reads {name!r}, the ruling read "
                            f"{row.get('held_as')!r} — re-rule it or drop the row")
            continue
        token = glyph_key(row.get("token") or "")
        if not token:
            problems.append(f"{person}: the ruling names no token")
        elif token not in [glyph_key(t) for t in re.split(r"[\s.,]+", name)]:
            problems.append(f"{person}: {row.get('token')!r} no longer stands in {name!r}")
        if row.get("outcome") != "unreadable":
            problems.append(f"{person}: outcome {row.get('outcome')!r} — this file rules "
                            "'unreadable' and nothing else")
        if not (row.get("impressions_in_hand") or []):
            problems.append(f"{person}: no impression is cited for the reading refused")

    if problems:
        print("UNREAD-INITIAL RULINGS FAIL", file=sys.stderr)
        for p in problems:
            print(" -", p, file=sys.stderr)
        return 1
    print(f"{len(rulings)} unread-initial ruling(s) still match their cards; "
          "no letter is supplied")
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(check())
