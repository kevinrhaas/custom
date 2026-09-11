#!/usr/bin/env python3
"""THE ONCE-EACH RULE, IN ONE PLACE — a card says a register ONCE (T-0677, T-0846).

T-0677 grew this gate inside `tools/spend_land_sales.py` after that pass wrote every one
of its thirty-one cards twice and `tools/check.sh` stayed green. It deliberately did not
generalise ahead of the second case. T-0846 is the second, third and fourth case, so the
rule moves here and the passes call it.

WHY THE OTHER TWO GATES CANNOT SEE IT. Every append-style spend pass finds its own work by
a MARKER sentence, and asks two questions about it: is the marker PRESENT on each ruled
card (`gaps`), and does any UNRULED card carry it (`strays`). Neither question can see a
card that carries the marker TWICE, nor one carrying a superseded pass's paragraph about
the same source beside the current one. A pass that gets rewritten leaves the older version
pushed on a branch, and running that against `dev` appends rather than overwrites.

WHICH PASSES NEED IT. Only the ones that APPEND prose to `person["note"]` — the shape

    if MARKER not in note:
        person["note"] = (note + " " + paragraph(row)).strip()

A pass that rebuilds a whole block and compares bytes (`spend_directories.py`,
`spend_old_settlers.py`) or writes a single scalar key (`spend_ladder_rungs.py`) cannot
double a paragraph, and each of those pins that structurally in its own `--self-test`
rather than carrying a gate that could never fire. T-0846 states the distinction.
"""

from __future__ import annotations

import json
from pathlib import Path


def doubles_over(household_id: str, person: dict, marker: str,
                 superseded: tuple = (), source: str = "register") -> list:
    """The rule for ONE already-loaded person — what a self-test drives and the gate reuses.

    `superseded` is the wording of earlier versions of the SAME pass, which say the same
    thing differently and so slip past a marker count. `source` names the thing on the
    card, so the fault line reads as the pass's own sentence.
    """
    note = person.get("note") or ""
    out = []
    n = note.count(marker)
    if n > 1:
        out.append("%s/%s — carries this pass's paragraph %d times; the %s is written "
                   "onto a card once" % (household_id, person.get("id"), n, source))
    for old in superseded:
        if old in note:
            out.append("%s/%s — carries a superseded paragraph about the same source "
                       "beside this one; the %s is written onto a card once"
                       % (household_id, person.get("id"), source))
    return out


def doubles(households: Path, marker: str, superseded: tuple = (),
            source: str = "register") -> list:
    """…and the same rule over every card in `households`."""
    bad = []
    for path in sorted(households.glob("*.json")):
        hh = json.loads(path.read_text(encoding="utf-8"))
        for person in hh.get("persons") or []:
            bad.extend(doubles_over(hh.get("id"), person, marker, superseded, source))
    return bad


def self_test_lines(marker: str, paragraph: str, superseded: tuple = (),
                    source: str = "register") -> list:
    """(label, boolean) pairs a calling pass's `--self-test` can assert directly.

    Both directions, in one place, so the four passes cannot drift apart on what the rule
    means: silent on the card the applier actually writes, RED on each way a card comes to
    say it twice.
    """
    written = {"id": "p_x", "note": "Existing sentence. " + paragraph}
    doubled = {"id": "p_x", "note": written["note"] + " " + paragraph}
    out = [
        ("doubles must stay silent on the card the applier actually writes",
         not doubles_over("hh_x", written, marker, superseded, source)),
        ("doubles must fire on a card carrying this pass's paragraph twice",
         any("2 times" in d
             for d in doubles_over("hh_x", doubled, marker, superseded, source))),
    ]
    for old in superseded:
        rival = {"id": "p_x", "note": written["note"] + " " + old + " …"}
        out.append(("doubles must fire on a superseded paragraph left standing",
                    any("superseded" in d
                        for d in doubles_over("hh_x", rival, marker, superseded, source))))
    return out
