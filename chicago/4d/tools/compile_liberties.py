#!/usr/bin/env python3
"""Compile docs/LIBERTIES.md into data/liberties.json for the walkthrough.

    python3 tools/compile_liberties.py            write data/liberties.json
    python3 tools/compile_liberties.py --check    re-derive and diff, write nothing

The project's standard is that *a visitor should be able to tell you which parts
we made up*. The per-attribute confidence model does that for attributes, and the
provenance popup shows it. It cannot show the liberties that live ABOVE any single
attribute — scope, omission, simplification, a navigation rule — because those
belong to no attribute and to no structure. Those are written in LIBERTIES.md,
which until now shipped nowhere a visitor could read it.

So the markdown stays the source of truth and stays append-only, and this derives
the machine-readable copy the renderer loads. Same discipline as data/datum.json:
the derived artefact is committed so the site needs no build step, and `check.sh`
re-derives it on every commit, so an edit to the prose that never reaches the JSON
is a gate failure rather than a silent divergence.

One field is read as data rather than as prose: `**Covers:**` lists the drawn
inventions an entry admits to, as `structure_id[.phase_id].aspect` tokens, and
`validate.py` matches those claims against the records in both directions.

Deliberately NOT a markdown renderer. It reads the one shape this document has —
`### L<n> — <title>` followed by `**Label:** text` fields — and carries the field
text through verbatim, markdown and all, for the renderer to display. Anything it
cannot parse it reports rather than dropping.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "LIBERTIES.md"
OUT = ROOT / "data" / "liberties.json"

# "### L4a — Sauganash Hotel: the log wing is inferred from two derivative images"
HEADING = re.compile(r"^###\s+(L\d+[a-z]?)\s*[—-]\s*(.+?)\s*$", re.M)
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.M)
# "**How to resolve:**" — a bolded label ending in a colon. The colon is what
# keeps ordinary emphasis ("**no** gallery", "**[DISPUTED]**") out of the match.
FIELD = re.compile(r"\*\*([A-Z][^*:]{0,60}):\*\*")
DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# "**Covers:** `sauganash_hotel.log_1829.footprint`, `wolf_point_tavern.footprint`"
# — the structured half of an admission. Shape is checked here; whether the token
# resolves to a real phase carrying a real invention is validate.py's business,
# so a renamed record fails the gate as a semantic error rather than by making the
# derived file uncompilable.
COVER_ASPECTS = ("footprint", "position")
COVER_TOKEN = re.compile(
    r"^([a-z0-9_]+?)(?:\.([a-z0-9_]+?))?\.(" + "|".join(COVER_ASPECTS) + r")$")

SECTION_KEY = {
    "standing liberties": "standing",
    "per-subject liberties": "per_subject",
    "resolved": "resolved",
}


def _clean(text: str) -> str:
    """Collapse the markdown's hard-wrapped lines into one paragraph."""
    return re.sub(r"\s*\n\s*", " ", text).strip().rstrip()


def parse_covers(text: str, lid: str, problems: list[str]) -> list[dict]:
    """`structure_id[.phase_id].aspect` tokens -> the claims this entry makes.

    The aspect is the last segment and comes from a closed vocabulary, so a
    two-segment token and a three-segment one are told apart without guessing:
    `walker_meeting_house.position` covers whichever phases drew a position from
    nothing, `walker_meeting_house.log_1831.position` covers exactly one.
    """
    claims: list[dict] = []
    for raw in re.split(r"[,;]", text):
        token = raw.strip().strip(".").strip("`").strip()
        if not token:
            continue
        m = COVER_TOKEN.match(token)
        if not m:
            problems.append(f"{lid}: Covers entry '{token}' is not "
                            f"structure_id[.phase_id].<{'|'.join(COVER_ASPECTS)}>")
            continue
        claims.append({"structure": m.group(1), "phase": m.group(2), "aspect": m.group(3)})
    if not claims:
        problems.append(f"{lid}: a Covers field that claims nothing — drop the field "
                        f"or name what it discharges")
    return sorted(claims, key=lambda c: (c["structure"], c["phase"] or "", c["aspect"]))


def parse(markdown: str, known: dict[str, str]) -> tuple[list[dict], list[str]]:
    problems: list[str] = []

    # Which "## " section each character offset falls under.
    sections = [(m.start(), m.group(1).strip().lower()) for m in SECTION.finditer(markdown)]

    def section_at(pos: int) -> str:
        name = ""
        for start, title in sections:
            if start < pos:
                name = title
            else:
                break
        if name not in SECTION_KEY:
            problems.append(f"entry at offset {pos} sits under an unknown section '{name}'")
        return SECTION_KEY.get(name, "other")

    entries: list[dict] = []
    heads = list(HEADING.finditer(markdown))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(markdown)
        body = markdown[m.end():end]
        # Stop at the next "## " section rule so a trailing section's prose does
        # not get swallowed into the last entry of the previous one.
        nxt = SECTION.search(body)
        if nxt:
            body = body[:nxt.start()]
        body = body.strip().strip("-").strip()

        fields = []
        marks = list(FIELD.finditer(body))
        if not marks:
            problems.append(f"{m.group(1)}: no '**Label:**' fields found")
        preamble = _clean(body[:marks[0].start()]) if marks else _clean(body)
        if preamble:
            problems.append(f"{m.group(1)}: text before the first field is dropped: "
                            f"{preamble[:60]}…")
        for j, f in enumerate(marks):
            stop = marks[j + 1].start() if j + 1 < len(marks) else len(body)
            text = _clean(body[f.end():stop])
            if not text:
                problems.append(f"{m.group(1)}: field '{f.group(1)}' is empty")
            fields.append({"label": f.group(1).strip(), "text": text})

        by_label = {f["label"].split(" (")[0].lower(): f["text"] for f in fields}
        recorded = DATE.search(by_label.get("recorded", ""))
        revised = DATE.search(by_label.get("revised", ""))

        # A liberty names its subject either as a record id in backticks or, in
        # a title, by the building's name. Both are matched, so the entry can be
        # tied back to the structure it constrains.
        blob = m.group(2) + " " + body
        subjects = sorted(sid for sid, name in known.items()
                          if sid in blob or (name and name in blob))

        covers = (parse_covers(by_label["covers"], m.group(1), problems)
                  if "covers" in by_label else [])

        entries.append({
            "id": m.group(1),
            "title": m.group(2).strip(),
            "section": section_at(m.start()),
            "subjects": subjects,
            "covers": covers,
            "recorded": recorded.group(1) if recorded else None,
            "revised": revised.group(1) if revised else None,
            "fields": fields,
        })

    if not entries:
        problems.append("no '### L<n> — title' entries found at all")
    seen: set[str] = set()
    for e in entries:
        if e["id"] in seen:
            problems.append(f"duplicate id {e['id']}")
        seen.add(e["id"])
        if e["recorded"] is None:
            problems.append(f"{e['id']}: no Recorded date")

    return entries, problems


def build() -> tuple[dict, list[str]]:
    known = {}
    for p in sorted((ROOT / "data" / "structures").glob("*.json")):
        known[p.stem] = json.loads(p.read_text()).get("name", "")
    markdown = SOURCE.read_text()
    entries, problems = parse(markdown, known)
    doc = {
        "_doc": "GENERATED from docs/LIBERTIES.md by tools/compile_liberties.py. "
                "Do not hand-edit: tools/check.sh re-derives this file and fails on drift. "
                "Edit the markdown, which is append-only, and re-run the tool.",
        "source": "docs/LIBERTIES.md",
        "standard": "A visitor should be able to tell you which parts we made up.",
        "note": "The confidence model covers attributes. These are the decisions that live "
                "above any single attribute: scope, omission, simplification, and the choices "
                "a visitor would otherwise have to reverse-engineer.",
        "count": len(entries),
        "liberties": entries,
    }
    return doc, problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and compare against the committed file")
    args = ap.parse_args()

    doc, problems = build()
    for p in problems:
        print(f"   {p}")

    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not OUT.exists():
            print(f"   data/liberties.json is missing — run tools/compile_liberties.py")
            return 1
        if OUT.read_text() != text:
            print("   data/liberties.json does not match docs/LIBERTIES.md — "
                  "re-run tools/compile_liberties.py and commit the result")
            return 1
        print(f"OK: {doc['count']} liberties, data/liberties.json matches its markdown")
        return 1 if problems else 0

    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)} — {doc['count']} liberties")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
