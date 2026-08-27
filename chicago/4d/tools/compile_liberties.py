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

One field is read as data rather than as prose: `**Covers:**` lists the inventions
an entry admits to, as `structure_id[.phase_id].aspect` tokens, and `validate.py`
matches those claims against the records in both directions. The aspect may be a
drawn one (`footprint`, `position`) or any attribute of the building's form
(`form.roof_type`) — anything a record states without evidence.

The ground admits to its inventions in a namespace of its own,
`terrain.<epoch>.<claim>`, because the terrain is not a structure and squeezing
it into the structures' grammar would misname it in the one file whose whole job
is calling things what they are. Epoch is part of the token rather than dropped:
`docs/EPOCHS.md` versions terrain per epoch, so a later year gets its own
shoreline and its own inventions, and an admission about the 1834 bank must not
silently discharge whatever an 1830 one makes up.

Deliberately NOT a markdown renderer. It reads the one shape this document has —
`### L<n> — <title>` followed by `**Label:** text` fields — and carries the field
text through verbatim, markdown and all, for the renderer to display. Anything it
cannot parse it reports rather than dropping.

WHICH SECTION AN ENTRY IS IN TAKES TWO STATEMENTS THAT AGREE (T-0054). `resolved`
is not a label like the others: `validate.py` exempts that section from the check
that a claimed invention is still an invention, which is what lets an append-only
document survive its own data being corrected. So it is the one section a mistake
in cannot be caught by anything downstream — the exemption's whole job is to stop
asking.

It was reached by accident 23 times. `## Resolved` was the LAST section of the
document, and this project's rule is that a liberty is APPENDED, so an entry
written at the end of the file landed inside the exemption and compiled
`section: "resolved"` while the fence it was written for stood in the town. The
markdown and the compiled JSON agreed exactly — this file read the fault the same
way both times — which is the same blind spot T-0207 found with conflict markers:
a consistency check cannot see a fault that both sides reproduce faithfully.

The document was reshaped so that appending lands in the per-subject register, and
that is the fix. This is the guard: an entry's own text says whether it was
settled, in the `**Resolved:**` line the section's preamble has always asked for,
and its position says the same thing independently. The exemption is granted only
where the two agree. Either half alone is reported, and the compiled section is
the one that is still checked — a misfiled entry is a standing liberty until
somebody writes down what settled it.
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
#
# The trailing letter is part of the id and not decoration: `L31` and `L31a` are
# two entries, nine such sub-entries stand in the document today, and a numbering
# check that folds them onto their parent cries wolf nine times on an unmodified
# file — which is worse than no check, because a gate that is always red gets
# switched off (T-0186).
HEADING = re.compile(r"^###\s+(L\d+[a-z]?)\s*[—-]\s*(.+?)\s*$", re.M)

# A line that MEANT to be an entry heading, matched loosely so the strict grammar
# above can be told apart from a near miss.
#
# The strict shape is not a filter, it is a CLIFF. A heading it rejects is not
# reported and not dropped — the body underneath it folds into the previous
# entry's fields, and the liberty leaves the register without a word. Measured
# 2026-08-27 (T-0186) by appending `### L198 – title` with an EN dash, which the
# `[—-]` class does not carry: 197 liberties compiled, `--check` exited 0, the
# whole of check.sh stayed green, and L198 was simply not there while its
# Decision and Recorded hung off the end of L197.
#
# That is the same silence this ticket was filed for, one step earlier than the
# duplicate number. A ledger whose whole job is to say which parts we made up
# cannot lose an entry quietly: an invention with no admission is the one fault
# that outranks everything else here.
NEAR_HEADING = re.compile(r"^\s{0,3}#{2,6}\s*L\s*\d+")
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
#
# Two shapes of aspect, and the difference is deliberate. The record's fixed
# blocks — `footprint`, `position`, `documented_range`, `ground_contact`, and the
# structure-level `function` and `occupants` — are a closed list, because their
# names are part of the schema. Everything under `form` is open, because that is where a building's
# character is written and the vocabulary grows with the archetypes; a form claim
# therefore carries its `form.` prefix, which is also what keeps the last segment
# from having to be guessed at.
COVER_ASPECTS = ("footprint", "position", "documented_range", "function", "occupants",
                 "ground_contact")
FORM_ASPECT = r"form(?:\.[a-z0-9_]+)+"
COVER_TOKEN = re.compile(
    r"^([a-z0-9_]+\*?|\*)(?:\.([a-z0-9_]+?|\*))?\.("
    + "|".join(COVER_ASPECTS) + r"|" + FORM_ASPECT + r"|form\.\*)$")

# A CLASS token: `recon_*.*.form.*`.
#
# Added because grading the invented buildings honestly turned ~2,900 values into
# admitted inventions overnight, and the alternative was 2,900 hand-written
# tokens. That is not a stricter document, it is an unreadable one — and this
# register exists to be read. A visitor's question is "which parts of this did
# you make up", and "every dimension of every building the reconstruction
# programme raised, because none of them is recorded anywhere" answers it better
# than two thousand lines they will never scroll through.
#
# The wildcard is deliberately narrow. It may stand for a structure id, a phase
# id, or the attribute after `form.` — never for the aspect vocabulary itself,
# so no entry can write `*.*.*` and silently discharge the whole gate. An
# admission still has to say WHAT KIND of thing it is admitting to inventing.
WILDCARD = "*"

# "**Covers:** `terrain.e1834_harbor_cut.bank`" — the ground's own namespace.
#
# The terrain invents as freely as a record does — a bank profile nobody drew, a
# channel section whose note says it carries no evidence at all — and until this
# existed the coverage gate read `data/structures/` and could not see any of it,
# so those admissions were owed by a person rather than demanded by a check.
#
# `terrain` is a reserved first segment rather than a structure id, and the claim
# is the id `compile_scene.ground_claims` gives the block — one segment for a
# whole block (`bank`, `micro_relief`) and two for a member of a list of them
# (`swales.west_prairie_swale_a`). The epoch sits between the two because
# `docs/EPOCHS.md` versions the ground: a second scene gets a second terrain with
# its own inventions, and one admission must not discharge both.
TERRAIN_NS = "terrain"
TERRAIN_TOKEN = re.compile(r"^terrain\.([a-z0-9_]+)\.(.+)$")

SECTION_KEY = {
    "standing liberties": "standing",
    "per-subject liberties": "per_subject",
    "resolved": "resolved",
}

# The order the Evidence panel reads in, which is not the order the document is
# written in. The markdown is a ledger and grows by appending; the panel is read
# by a visitor, and what we are still making up belongs above what we no longer
# are. Emitting in this order also means the file can be reshaped — as it was to
# get Resolved out of the append path — without the panel's order moving.
SECTION_ORDER = ("standing", "per_subject", "resolved", "other")

# The section that cannot be entered by accident, and the field that has to say so.
RESOLVED = "resolved"
SETTLED_FIELD = "resolved"

# Where a misfiled entry lands instead. It is the section that is still CHECKED:
# an entry nobody has said is settled keeps its obligations, and the register it
# keeps them in is the per-subject one, which is 167 of the 170 unsettled entries.
UNSETTLED_DEFAULT = "per_subject"


def _clean(text: str) -> str:
    """Collapse the markdown's hard-wrapped lines into one paragraph."""
    return re.sub(r"\s*\n\s*", " ", text).strip().rstrip()


def claim_sort_key(c: dict) -> tuple:
    """A total order over both domains, so the derived file is deterministic."""
    if c.get("domain") == TERRAIN_NS:
        return (TERRAIN_NS, c["epoch"], "", c["claim"])
    return ("structure", c["structure"], c["phase"] or "", c["aspect"])


def claim_token(c: dict) -> str:
    """A claim back in the text the document wrote it as.

    One function, so an error message quoting a token and the markdown that has
    to be edited to satisfy it cannot come to disagree about the grammar.
    """
    if c.get("domain") == TERRAIN_NS:
        return f"{TERRAIN_NS}.{c['epoch']}.{c['claim']}"
    return ".".join(t for t in (c["structure"], c["phase"], c["aspect"]) if t)


def parse_covers(text: str, lid: str, problems: list[str]) -> list[dict]:
    """`Covers:` tokens -> the claims this entry makes, in one of two domains.

    For a structure the token is `structure_id[.phase_id].aspect`. The aspect is
    the trailing segment (or `form.` plus one, for the open half of the
    vocabulary), so a two-segment token and a three-segment one are told apart
    without guessing: `walker_meeting_house.position` covers whichever phases drew
    a position from nothing, `walker_meeting_house.log_1831.position` covers
    exactly one, and `sauganash_hotel.log_1829.form.roof_type` names the one
    attribute in the one phase.

    For the ground it is `terrain.<epoch>.<claim>`, and the domain is carried on
    the claim rather than guessed at from its shape by whoever reads it later.
    Two vocabularies meeting in one field is exactly where a reader starts
    inferring which one they are looking at, and this project has already paid
    once for a name read as being about the wrong thing.
    """
    claims: list[dict] = []
    for raw in re.split(r"[,;]", text):
        token = raw.strip().strip(".").strip("`").strip()
        if not token:
            continue
        if token.split(".")[0] == TERRAIN_NS:
            m = TERRAIN_TOKEN.match(token)
            if not m:
                problems.append(f"{lid}: Covers entry '{token}' is not "
                                f"terrain.<epoch>.<claim>, which is the shape an "
                                f"admission about the ground takes")
                continue
            claims.append({"domain": TERRAIN_NS, "epoch": m.group(1), "claim": m.group(2)})
            continue
        m = COVER_TOKEN.match(token)
        if not m:
            problems.append(f"{lid}: Covers entry '{token}' is not "
                            f"structure_id[.phase_id].<{'|'.join(COVER_ASPECTS)}"
                            f"|form.attribute> or terrain.<epoch>.<claim>")
            continue
        claims.append({"domain": "structure", "structure": m.group(1),
                       "phase": m.group(2), "aspect": m.group(3)})
    if not claims:
        problems.append(f"{lid}: a Covers field that claims nothing — drop the field "
                        f"or name what it discharges")
    return sorted(claims, key=claim_sort_key)


def settled_section(lid: str, positional: str, states_settled: bool,
                    problems: list[str]) -> str:
    """The section an entry is in, from its position AND its own words.

    They are two independent statements of one fact, and `resolved` is granted
    only where they agree, because `resolved` is the section `validate.py`
    exempts from the over-claim check. A section that switches a check off is
    the one section a mistake in has nothing downstream to catch it.

    Neither half is silently believed:

      * Under `## Resolved`, saying nothing about what settled it — the T-0054
        fault, and the reason the document was reshaped. It compiles as a
        standing liberty, keeps its obligations, and is named here.
      * Carrying a `**Resolved:**` line somewhere else — the mirror image, and
        the likelier one now that appending lands in the per-subject register.
        It compiles where it sits, because a line of prose may not switch off a
        check on its own; the entry is moved, or it is not resolved.
    """
    if positional == RESOLVED and not states_settled:
        problems.append(
            f"{lid}: sits under '## Resolved' but no '**Resolved:**' line says what "
            f"settled it — an entry appended at the end of the file used to land "
            f"here and be exempted from the check that its claim is still an "
            f"invention (T-0054). Compiled as '{UNSETTLED_DEFAULT}'. Move it into the "
            f"per-subject register, or write down what settled it")
        return UNSETTLED_DEFAULT
    if positional != RESOLVED and states_settled:
        problems.append(
            f"{lid}: carries a '**Resolved:**' line but sits under the "
            f"'{positional}' section — say what settled it AND move the entry into "
            f"'## Resolved'. Compiled as '{positional}': one line of prose does not "
            f"exempt an entry from the check that its claim is still an invention")
    return positional


def unparsed_headings(markdown: str) -> list[tuple[int, str]]:
    """Lines that look like an entry heading and are not one, with line numbers.

    The one thing this document cannot survive is losing an entry silently, and
    a heading the grammar rejects does exactly that — see NEAR_HEADING. So the
    near miss is caught here rather than downstream, where there is nothing left
    to catch: the compiled JSON, the liberties gate and the Evidence panel all
    agree perfectly about a register the entry was never in.

    Line numbers, because the whole point is that the reader cannot see it. A
    bare "a heading did not parse" in an 8,800-line file is a search, and an en
    dash and an em dash are the same three pixels apart.
    """
    parsed = {markdown.count("\n", 0, m.start()) for m in HEADING.finditer(markdown)}
    return [(i + 1, line) for i, line in enumerate(markdown.splitlines())
            if NEAR_HEADING.match(line) and i not in parsed]


def duplicate_ids(entries: list[dict]) -> list[str]:
    """Numbers taken twice, reported with both titles.

    Two branches that each append `### L177` merge CLEAN when their appends land
    in different parts of the file, and git says nothing because neither touched
    the other's lines (T-0186, 2026-08-24: it happened twice in one afternoon).
    A conflict is safe because it stops you; a clean merge of two appends to a
    numbered ledger is not, and this is what stands in for the conflict.

    Both titles, because the number alone does not tell you which of the two
    entries is the newcomer to renumber — and the renumber has to carry its
    references, since liberty numbers are cited from records, tickets, STATUS.md
    and the research docs.
    """
    seen: dict[str, str] = {}
    problems: list[str] = []
    for e in entries:
        first = seen.get(e["id"])
        if first is not None:
            problems.append(
                f"{e['id']}: taken twice — '{first}' and '{e['title']}'. Two "
                f"appends to a numbered ledger merged clean; renumber the newer "
                f"entry and carry its citations. A lettered sub-entry ({e['id']}a) "
                f"is a different id and is not this")
        else:
            seen[e["id"]] = e["title"]
    return problems


def parse(markdown: str, known: dict[str, str]) -> tuple[list[dict], list[str]]:
    problems: list[str] = []
    for lineno, line in unparsed_headings(markdown):
        problems.append(
            f"line {lineno}: '{line.strip()[:70]}' looks like an entry heading and "
            f"does not parse as one, so its body folds into the entry above it and "
            f"the liberty leaves the register. The shape is "
            f"'### L<n>[a] — Title', with an em dash or a plain hyphen")

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
            "section": settled_section(m.group(1), section_at(m.start()),
                                       SETTLED_FIELD in by_label, problems),
            "subjects": subjects,
            "covers": covers,
            "recorded": recorded.group(1) if recorded else None,
            "revised": revised.group(1) if revised else None,
            "fields": fields,
        })

    if not entries:
        problems.append("no '### L<n> — title' entries found at all")
    problems.extend(duplicate_ids(entries))
    for e in entries:
        if e["recorded"] is None:
            problems.append(f"{e['id']}: no Recorded date")

    # Grouped for the reader, stable within each group, so the panel's order is
    # a decision here rather than a side effect of where a section sits in a
    # 7,800-line markdown file. Nothing else in the derived file is reordered.
    entries.sort(key=lambda e: SECTION_ORDER.index(e["section"])
                 if e["section"] in SECTION_ORDER else len(SECTION_ORDER))

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


SPECIMEN = """# Liberties taken

## Standing liberties

### L1 — A whole-scene decision
**Decision:** something the scene does everywhere.
**Recorded:** 2026-08-09.

---

## Resolved

Kept verbatim, with a **Resolved:** line saying what settled them.

### L2 — Settled, and it says so
**Decision:** something we invented.
**Recorded:** 2026-08-10.
**Resolved:** 2026-08-11, the evidence arrived.

### L3 — Appended at the end of the file, which used to be here
**Decision:** something we are still inventing.
**Recorded:** 2026-08-12.

---

## Per-subject liberties

### L4 — One building
**Decision:** something about one building.
**Recorded:** 2026-08-13.

### L5 — Says it was settled, and was never moved
**Decision:** something we invented.
**Recorded:** 2026-08-14.
**Resolved:** 2026-08-15, the evidence arrived.
"""


# The numbering faults, in miniature. Separate from SPECIMEN because that one is
# about which SECTION an entry is in and this one is about its NUMBER, and a
# specimen carrying both faults at once cannot show either cleanly.
#
# It holds the shape the committed document actually has — a parent with lettered
# sub-entries under it — beside the collision those sub-entries are forever being
# mistaken for. Both readings have to be asserted together or the check drifts
# into one of its two failure modes: silent on a real duplicate, or red nine
# times on a file nobody touched.
NUMBERING_SPECIMEN = """# Liberties taken

## Per-subject liberties

### L31 — A parent entry
**Decision:** something we invented.
**Recorded:** 2026-08-09.

### L31a — A lettered sub-entry, which is a different entry and not a duplicate
**Decision:** something narrower.
**Recorded:** 2026-08-10.

### L31b — A second sub-entry of the same parent
**Decision:** something else narrower.
**Recorded:** 2026-08-11.

### L32 — One branch's entry
**Decision:** something one branch invented.
**Recorded:** 2026-08-12.

### L32 — The other branch's entry, carried in by a merge that raised no conflict
**Decision:** something the other branch invented.
**Recorded:** 2026-08-13.
"""

# A heading that misses the grammar by one character. The en dash is the real
# instance — it is three pixels from the em dash the shape requires, and it is
# what a paste from anywhere else in the world brings with it.
SHAPE_SPECIMEN = """# Liberties taken

## Per-subject liberties

### L40 — An entry that parses
**Decision:** something we invented.
**Recorded:** 2026-08-09.

### L41 \u2013 An en dash, which the heading shape does not accept
**Decision:** something we invented and admit to.
**Recorded:** 2026-08-10.
"""


def self_test() -> bool:
    """Every assertion fires when broken.

    The specimen is the document in miniature, faults and all: an entry that is
    settled and says so, one that landed under Resolved by being appended (the
    T-0054 fault), and one that says it was settled without being moved (the
    mirror image). A synthetic document is the only way to hold both faults,
    because the committed one is repaired — and the repaired document is
    asserted too, at the end, so this cannot pass on the specimen alone.
    """
    ok = True

    def check(label, got, want=True):
        nonlocal ok
        if got != want:
            ok = False
        print(f"  {'ok  ' if got == want else 'FAIL'}  {label}")

    entries, problems = parse(SPECIMEN, {})
    at = {e["id"]: e["section"] for e in entries}
    blamed = {lid for lid in at for p in problems if p.startswith(lid + ":")}

    check("a standing entry compiles standing", at.get("L1") == "standing")
    check("a resolved entry that says what settled it compiles resolved",
          at.get("L2") == "resolved")
    check("…and is not blamed for anything", "L2" not in blamed)
    check("an entry under Resolved saying nothing is NOT compiled resolved",
          at.get("L3") == UNSETTLED_DEFAULT)
    check("…and the gate names it", "L3" in blamed)
    check("a per-subject entry compiles per_subject", at.get("L4") == "per_subject")
    check("…and is not blamed for anything", "L4" not in blamed)
    check("a Resolved line outside the section does NOT exempt the entry",
          at.get("L5") == "per_subject")
    check("…and the gate names that too", "L5" in blamed)
    check("the reader's order is standing, then per-subject, then resolved — "
          "and inside a group, the order the document was written in",
          [e["id"] for e in entries] == ["L1", "L3", "L4", "L5", "L2"])

    # The NUMBER of an entry, which is the other half. Same discipline as the
    # section assertions above: the fault in a specimen, then the live document
    # beside it, because a check can only be trusted once it has been seen to
    # fire and seen to stay quiet.
    num, num_problems = parse(NUMBERING_SPECIMEN, {})
    dupes = [p for p in num_problems if "taken twice" in p]
    check("a number taken by two entries is reported",
          len(dupes) == 1 and dupes[0].startswith("L32:"))
    check("…and the report names BOTH titles, so the newcomer can be told apart",
          bool(dupes) and "One branch's entry" in dupes[0]
          and "the other branch's entry" in dupes[0].lower())
    check("a lettered sub-entry is NOT a duplicate of its parent",
          [e["id"] for e in num] == ["L31", "L31a", "L31b", "L32", "L32"])
    check("…and nothing is reported for the sub-entries",
          not [p for p in num_problems if p.startswith(("L31:", "L31a:", "L31b:"))])

    # The heading that misses the grammar and takes its entry with it.
    shape, shape_problems = parse(SHAPE_SPECIMEN, {})
    near = [p for p in shape_problems if "looks like an entry heading" in p]
    want_line = SHAPE_SPECIMEN.splitlines().index(
        [l for l in SHAPE_SPECIMEN.splitlines() if "en dash" in l][0]) + 1
    check(f"a heading the grammar rejects is reported rather than swallowed "
          f"(line {want_line})",
          len(near) == 1 and f"line {want_line}:" in near[0])
    check("…and the entry it would have swallowed is named by line, not left "
          "to be searched for", bool(near) and "L41" in near[0])
    check("…and it is the ONLY entry parsed, which is why the silence mattered",
          [e["id"] for e in shape] == ["L40"])

    # And the document that ships. The fault this exists for is exactly a
    # section nobody meant to be in, so the specimen proving the assertion
    # fires is worth nothing without the live reading beside it.
    live, live_problems = parse(SOURCE.read_text(), {})
    settled = [e["id"] for e in live if e["section"] == RESOLVED]
    misfiled = [p for p in live_problems if "## Resolved" in p or "**Resolved:**" in p]
    check(f"the committed document misfiles nothing ({len(settled)} settled, "
          f"{len(live) - len(settled)} still standing)", not misfiled)

    # The nine sub-entries are the reason the lettered-id assertion above is not
    # academic: a check that folded them onto their parents would report nine
    # duplicates on an unmodified file, and the gate would be switched off within
    # the day rather than fixed.
    subs = [e["id"] for e in live if re.fullmatch(r"L\d+[a-z]", e["id"])]
    check(f"the committed document carries no duplicate number, across "
          f"{len(live)} entries including {len(subs)} lettered sub-entries "
          f"({', '.join(subs)})", not duplicate_ids(live))
    check(f"…and every one of its {len(live)} headings parses",
          not unparsed_headings(SOURCE.read_text()))
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and compare against the committed file")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the section assertions fire when broken")
    args = ap.parse_args()

    if args.self_test:
        print("\n\033[1m== …and its own assertions still fire when broken\033[0m")
        good = self_test()
        print("\nSELF-TEST " + ("PASS" if good else "FAIL"))
        return 0 if good else 1

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
        # The summary line has to agree with the exit code. It used to print
        # "OK: … matches its markdown" and then exit 1 on the problems listed
        # directly above it, which reads as green in a 600-line gate log — the
        # one place a duplicate number was ever going to be noticed (T-0186).
        # Matching is not passing: the derived file agreeing with a faulty
        # register is the exact shape of fault this project has now paid for
        # three times (T-0054, T-0207, and this one).
        if problems:
            print(f"   data/liberties.json matches its markdown, and the markdown "
                  f"has {len(problems)} problem(s) listed above — a faithful copy "
                  f"of a faulty register is still a fail")
            return 1
        print(f"OK: {doc['count']} liberties, data/liberties.json matches its markdown")
        return 0

    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)} — {doc['count']} liberties"
          + (f" — {len(problems)} problem(s) above" if problems else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
