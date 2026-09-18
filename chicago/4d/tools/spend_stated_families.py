#!/usr/bin/env python3
"""T-1170: the family members the committed sources NAME, onto the heads that have them.

    python3 tools/spend_stated_families.py              the reading, on stdout
    python3 tools/spend_stated_families.py --build      write the layer and the report
    python3 tools/spend_stated_families.py --check      re-derive, and hold every statement to a ruling
    python3 tools/spend_stated_families.py --self-test  the assertions of --check, broken on purpose

WHAT THIS IS FOR.

`tools/survey_stated_kin.py` (T-0734) counts the kinship the corpus states and lands it
where BOTH ends are people the town already holds. Its own count says what that leaves:
of 263 statements read, 30 have both ends in town and 12 name a relative of a resident
who is nobody in this dataset. Those twelve are not the world outside the town talking —
each one is a source naming the wife, the son or the daughter OF A HEAD THIS LAYER
CARRIES, and the household card has never recorded them. That is the seam this pass
works, and it is T-1170's first half: the members a source NAMES.

A second reading is needed to see all of it. The survey's prose pattern is
`<relation> of <Name>` — 'brother of Samuel', 'son of Jean Baptiste Beaubien'. The
period does not usually print a wife that way. It prints a marriage: 'he was married to
Miss Emeline Mahbutt', 'married Welthyan Loomis 30 October 1808', 'married Catherine
Daugherty at Naperville on April 6, 1835'. A wife named by the verb is invisible to the
survey and visible to a reader, so this pass reads the marriage verb as well, over the
same corpus — the prose the cards already carry, quoted from sources that have already
been adjudicated.

WHAT IT DOES NOT DO. It does not reconstruct. A member a source COUNTS but does not name
— an 1840 census band, an 'and family' notice — is the OTHER half of T-1170 and belongs
to the reconstruction programme (`tools/reconstruct_residents_1835.py`), which is the
one writer of a `reconstructed` person. This pass calls
`refuse_reconstructed_grade.refuse()` on everything it is about to write, in every mode,
exactly as the four mints do: it may emit `attested` or `inferred` and nothing else.

A STATEMENT IS A READING; A WRITE IS A RULING. The reading below is DERIVED and moves
when the cards move. What happens to each statement is AUTHORED, one at a time, in
`data/residents/stated_family_rulings.json`, by somebody who has read the source — the
same split `kin_survey.json` / `kin_rulings.json` keeps, and for the same reason: a
derivation that carried its own verdicts would rewrite them every time the corpus grew.
`--check` refuses while one statement stands unanswered, so a card edit that surfaces a
new marriage cannot quietly widen the town.

THE SIX VERDICTS.

  write                  the source names this person as the relative of an 1835 head,
                         and nothing dates them out of the scene. Written onto the
                         head's card, graded `inferred`, carrying the source, the
                         relation, the quoted reading and what the source does NOT say.
  already_held           the town holds this person already, under this name or another.
                         Nothing to write; a tie between two households is kin_rulings'.
  later_only             the source dates the relationship AFTER 1835-07-01. A wife of
                         20 August 1835 is not a wife on 1 July, and this dataset does
                         not silently promote her.
  not_present            named, and something the sources say puts them outside the
                         household on the scene date — a first wife the source itself
                         supersedes, a relative recorded somewhere else.
  no_seat                named and real, and this layer holds no household that can carry
                         them: `relationship` states a place inside ONE household, and the
                         only card the source reaches belongs to somebody else. Reported
                         rather than forced, because the seat is the next run's finding.
  insufficient_identity  the reading does not reach a person: a fragment, an initial, a
                         people rather than a name, or a head whose own identity this
                         layer declines to assert.

WHAT A WRITTEN PERSON CARRIES. `stated_family` names the statement that produced them,
so the write is re-derivable and a person this pass wrote can never be confused with one
a mint did. `--check` holds the layer to it both ways: every `write` ruling is on exactly
one card, and every `stated_family` person answers to a live statement and a live ruling.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refuse_reconstructed_grade as refusal  # noqa: E402
import survey_stated_kin as survey  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RESIDENTS = ROOT / "data" / "residents"
HOUSEHOLDS = RESIDENTS / "households"
INDEX = RESIDENTS / "index.json"
RULINGS = RESIDENTS / "stated_family_rulings.json"
REPORT = ROOT / "docs" / "RESEARCH" / "stated-families-2026-09.md"

WRITER = "spend_stated_families.py"
TICKET = "T-1170"
PASS_KEY = "stated_families"
SCENE_DATE = "1835-07-01"

VERDICTS = ("write", "already_held", "later_only", "not_present", "no_seat",
            "insufficient_identity")

# `married [first|second|again] [to] [Miss|Mrs] <Name>` in prose a card already carries.
# The name is at most four capitalised tokens; more than that is a sentence. The verb is
# the whole reading — this pass does not infer a marriage from a shared surname, an
# honorific or a household's shape.
MARRIAGE = re.compile(
    r"\b(?:was\s+)?married\s+(?:first\s+|second(?:ly)?\s+|again\s+)?(?:to\s+)?"
    r"(?:(?:Miss|Mrs\.?|Mme\.?)\s+)?"
    r"((?:[A-Z][\w'’\-]+)(?:\s+[A-Z][\w'’\-]+){0,3})"
)
# Prose the cards use to DISCUSS the period's habits rather than to state a marriage.
# Each is a phrase this project wrote about its own method, and a reading taken off one
# would be a reading of the dataset's commentary on itself.
NOT_A_STATEMENT = re.compile(
    r"MARRIED WOMAN'S ENTRY|MARRIED THEM|married on the day this dataset|"
    r"a married woman|married man with children|married and left|married name",
    re.IGNORECASE,
)


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", text.lower())).strip("_")


def load_cards() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(HOUSEHOLDS.glob("hh_*.json"))}


def strings(node, path: str = "", sources=None):
    """Every string in a card, with its path and the nearest enclosing `sources`."""
    if isinstance(node, dict):
        nearest = node.get("sources") if isinstance(node.get("sources"), list) else sources
        for key, value in node.items():
            yield from strings(value, f"{path}.{key}", nearest)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from strings(value, f"{path}[{i}]", sources)
    elif isinstance(node, str):
        yield path, node, sources


def read_marriages(cards: dict[str, dict]) -> list[dict]:
    """The marriages the cards' own prose states, one row per (household, name read)."""
    rows, seen = [], set()
    for hid, card in cards.items():
        for path, text, sources in strings(card):
            for match in MARRIAGE.finditer(text):
                window = text[max(0, match.start() - 90):match.end() + 60]
                if NOT_A_STATEMENT.search(window):
                    continue
                name = " ".join(match.group(1).split())
                key = (hid, slug(name))
                if key in seen:
                    continue
                seen.add(key)
                rows.append({
                    "id": f"marriage:{hid}:{slug(name)}",
                    "reading": "marriage_verb",
                    "household": hid,
                    "subject": card["head"],
                    "relation": "spouse",
                    "other_as_read": name,
                    "read_from": path,
                    "quote": " ".join(
                        text[max(0, match.start() - 180):match.end() + 180].split()),
                    "sources": sorted(sources or []),
                })
    return sorted(rows, key=lambda r: r["id"])


def read_unlanded_kin(cards: dict[str, dict]) -> list[dict]:
    """The survey's own leftovers: a relative of a resident who is nobody in this town."""
    town = survey.Town(cards)
    statements = survey.read_church() + survey.read_cards(cards) + survey.read_authored()
    rows = []
    for row in survey.classify(statements, town):
        if row["outcome"] != "other_not_in_town" or not row.get("subject"):
            continue
        household = row["subject"][0]["household"]
        rows.append({
            "id": f"kin:{row['id']}",
            "reading": "stated_kin",
            "household": household,
            "subject": row["subject"][0]["person"],
            "relation": row["relation"],
            "other_as_read": row["other_as_read"],
            "read_from": row["locator"],
            "quote": " ".join(str(row.get("as_read") or "").split()),
            "sources": sorted((cards[household].get("persons") or [{}])[0].get("sources") or []),
        })
    return sorted(rows, key=lambda r: r["id"])


def corpus(cards: dict[str, dict]) -> dict[str, dict]:
    """The cards WITHOUT this pass's own writing — the only thing it is allowed to read.

    A person written here carries a note quoting the source, and a pass that read that
    note back would be reading its own output as evidence: the second run would see one
    more printing of the same marriage, the third one more again. The corpus is the tree
    as it stood before this pass touched it, so the reading is a function of the sources
    and not of how many times the build has run.
    """
    view = {}
    for hid, card in cards.items():
        card = dict(card)
        card["persons"] = [p for p in card.get("persons") or []
                           if (p.get("stated_family") or {}).get("pass") != PASS_KEY]
        view[hid] = card
    return view


def statements(cards: dict[str, dict]) -> list[dict]:
    view = corpus(cards)
    return read_marriages(view) + read_unlanded_kin(view)


def load_rulings() -> dict:
    return json.loads(RULINGS.read_text(encoding="utf-8"))


def person_of(ruling: dict, statement: dict) -> dict:
    """The person a `write` ruling puts on the card, assembled here and not authored raw.

    The ruling names WHO and WHY; the shape — the id slot, the grade, the marker that
    makes the write re-derivable — is this pass's and is the same for every one of them.
    """
    write = ruling["write"]
    person = {
        "id": write["id"],
        "name": write["name"],
        "relationship": write["relationship"],
        "grade": "inferred",
    }
    if write.get("sex"):
        person["sex"] = write["sex"]
    person["occupation"] = {
        "value": "none_recorded",
        "confidence": "reconstructed",
        "note": "No source records an occupation for this person. This is the ABSENCE of "
                "a record rather than a claim that they did no work - the sources of 1835 "
                "name the occupations of household heads and almost never those of wives, "
                "children or the people counted with them.",
    }
    person["sources"] = sorted(write.get("sources") or statement["sources"])
    person["note"] = write["note"]
    person["stated_family"] = {
        "pass": PASS_KEY,
        "ticket": TICKET,
        "statement": statement["id"],
        "relation": statement["relation"],
        "as_read": statement["other_as_read"],
        "read_from": statement["read_from"],
    }
    return person


def build(cards: dict[str, dict], rows: list[dict], rulings: dict) -> dict[str, dict]:
    """The cards as this pass would write them. Pure: nothing touches disk here."""
    written = {}
    by_id = {row["id"]: row for row in rows}
    for sid, ruling in sorted(rulings["rulings"].items()):
        if ruling.get("verdict") != "write" or sid not in by_id:
            continue
        statement = by_id[sid]
        card = json.loads(json.dumps(cards[statement["household"]]))
        card = written.get(statement["household"], card)
        person = person_of(ruling, statement)
        card["persons"] = [p for p in card["persons"]
                           if (p.get("stated_family") or {}).get("statement") != sid]
        card["persons"].append(person)
        written[statement["household"]] = card
    refusal.refuse(written, WRITER)
    return written


def reindex(index: dict, cards: dict[str, dict]) -> dict:
    """The manifest's counts, re-derived from the cards this pass leaves behind."""
    index = json.loads(json.dumps(index))
    persons = 0
    grades = {"attested": 0, "inferred": 0, "reconstructed": 0}
    for entry in index["households"]:
        card = cards[entry["id"]]
        entry["persons"] = len(card["persons"])
        local: dict[str, int] = {}
        for person in card["persons"]:
            local[person["grade"]] = local.get(person["grade"], 0) + 1
        entry["grades"] = {g: local[g] for g in ("attested", "inferred", "reconstructed")
                           if g in local}
        persons += len(card["persons"])
        for grade, n in local.items():
            grades[grade] += n
    index["counts"]["persons"] = persons
    index["counts"]["by_grade"] = grades
    return index


def report_text(rows: list[dict], rulings: dict) -> str:
    """The reader's copy. DERIVED — `--check` says so when it and the tree disagree."""
    table = rulings["rulings"]
    counts = {v: sum(1 for r in rows if table.get(r["id"], {}).get("verdict") == v)
              for v in VERDICTS}
    written = [r for r in rows if table.get(r["id"], {}).get("verdict") == "write"]
    lines = [
        "# The family members the sources NAME — read, ruled and written",
        "",
        f"GENERATED by `tools/spend_stated_families.py --build` ({TICKET}). Hand-edits lose:",
        "`--check` re-derives this file from the cards and the rulings and fails when they",
        "disagree. The verdicts are AUTHORED in `data/residents/stated_family_rulings.json`.",
        "",
        "## What was read",
        "",
        f"- {sum(1 for r in rows if r['reading'] == 'marriage_verb')} marriage statements, "
        "read off the marriage verb in prose the cards already carry.",
        f"- {sum(1 for r in rows if r['reading'] == 'stated_kin')} relatives named by "
        "`tools/survey_stated_kin.py` whose other end is nobody this town holds.",
        f"- {len(rows)} statements in all, every one of them answered below.",
        "",
        "## The verdicts",
        "",
        "| verdict | statements |",
        "|---|---|",
    ]
    for verdict in VERDICTS:
        lines.append(f"| `{verdict}` | {counts[verdict]} |")
    lines += [
        "",
        f"## The {len(written)} people this pass wrote",
        "",
        "| person | relation | household | source says | grade |",
        "|---|---|---|---|---|",
    ]
    for row in written:
        write = table[row["id"]].get("write") or {}
        lines.append(f"| {write.get('name', '?')} | {write.get('relationship', '?')} | "
                     f"`{row['household']}` | {row['other_as_read']} | inferred |")
    lines += ["", "## Every statement, with its ruling", ""]
    for row in rows:
        ruling = table.get(row["id"], {})
        lines += [
            f"### `{row['id']}`",
            "",
            f"- **read as** {row['other_as_read']} — {row['relation']} of "
            f"`{row['subject']}` in `{row['household']}`",
            f"- **from** `{row['read_from']}`",
            f"- **verdict** `{ruling.get('verdict', 'UNRULED')}` — {ruling.get('why', '')}",
            "",
            f"> {row['quote']}",
            "",
        ]
    return "\n".join(lines) + "\n"


def check(cards: dict[str, dict] | None = None, rulings: dict | None = None,
          index: dict | None = None, report: str | None = None) -> list[str]:
    """Every problem this pass can see, as sentences. Empty means green."""
    cards = load_cards() if cards is None else cards
    rulings = load_rulings() if rulings is None else rulings
    index = json.loads(INDEX.read_text(encoding="utf-8")) if index is None else index
    report = REPORT.read_text(encoding="utf-8") if report is None else report
    problems: list[str] = []

    rows = statements(cards)
    table = rulings.get("rulings") or {}
    by_id = {row["id"]: row for row in rows}

    # 1. EVERY STATEMENT IS ANSWERED. A card edit that surfaces a new marriage is a new
    #    question, and this pass does not let it pass unasked.
    for row in rows:
        ruling = table.get(row["id"])
        if not ruling:
            problems.append(
                f"{row['id']}: the corpus states this and no ruling answers it — "
                f"'{row['other_as_read']}', {row['relation']} of {row['subject']}. Rule it in "
                f"{RULINGS.relative_to(ROOT)}")
        elif ruling.get("verdict") not in VERDICTS:
            problems.append(f"{row['id']}: verdict {ruling.get('verdict')!r} is not one of "
                            f"{list(VERDICTS)}")
        elif not str(ruling.get("why") or "").strip():
            problems.append(f"{row['id']}: a ruling states its reason — a verdict with no "
                            f"reason is an assertion, not a reading")

    # 2. NO RULING OUTLIVES ITS STATEMENT. A verdict about prose the cards no longer
    #    carry would be an answer to a question nobody is asking.
    for sid in sorted(table):
        if sid not in by_id:
            problems.append(f"{sid}: a ruling with no statement — the corpus no longer says "
                            f"this. Withdraw it rather than leaving it standing.")

    # 3. THE LAYER MATCHES THE RULINGS, BOTH WAYS.
    on_card = {}
    for hid, card in cards.items():
        for person in card.get("persons") or []:
            marker = person.get("stated_family")
            if isinstance(marker, dict) and marker.get("pass") == PASS_KEY:
                on_card.setdefault(marker.get("statement"), []).append((hid, person))
    for sid, ruling in sorted(table.items()):
        seats = on_card.get(sid) or []
        if ruling.get("verdict") == "write":
            if len(seats) != 1:
                problems.append(f"{sid}: ruled `write` and stands on {len(seats)} card(s) — "
                                f"run --build")
            elif sid in by_id and seats[0][0] != by_id[sid]["household"]:
                problems.append(f"{sid}: written onto {seats[0][0]}, not onto "
                                f"{by_id[sid]['household']}")
        elif seats:
            problems.append(f"{sid}: ruled `{ruling.get('verdict')}` and yet a person written "
                            f"by this pass stands on {seats[0][0]} — a refusal that left "
                            f"somebody in the town is worse than no refusal")
    for sid, seats in sorted(on_card.items()):
        if sid not in table:
            for hid, person in seats:
                problems.append(f"{hid}/{person.get('id')}: written by this pass under "
                                f"statement {sid!r}, which no ruling claims")

    # 4. A RESEARCH WRITER MAY NOT MINT A RECONSTRUCTED RESIDENT — asserted in --check
    #    and not only when writing, so the boundary cannot rot between builds.
    try:
        refusal.refuse(cards, WRITER)
    except refusal.ReconstructedGradeRefused as exc:
        problems.append(str(exc))

    # 5. THE MANIFEST AND THE REPORT BOTH FOLLOW FROM THE CARDS.
    if reindex(index, cards) != index:
        problems.append(f"{INDEX.relative_to(ROOT)} disagrees with the cards — "
                        f"run {WRITER} --build")
    if report_text(rows, rulings) != report:
        problems.append(f"{REPORT.relative_to(ROOT)} is stale — run {WRITER} --build")
    return problems


def write(paths: dict[str, dict]) -> None:
    for name, doc in sorted(paths.items()):
        (HOUSEHOLDS / f"{name}.json").write_text(
            json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_build() -> int:
    cards = load_cards()
    rulings = load_rulings()
    rows = statements(cards)
    unruled = [r["id"] for r in rows if r["id"] not in (rulings.get("rulings") or {})]
    if unruled:
        print(f"REFUSED: {len(unruled)} statement(s) carry no ruling, and this pass does not "
              f"decide what a source means:", file=sys.stderr)
        for sid in unruled:
            print(f"  {sid}", file=sys.stderr)
        return 1
    written = build(cards, rows, rulings)
    write(written)
    # RE-READ AFTER WRITING. `corpus()` keeps this pass's own persons out of the reading,
    # so the second reading should equal the first — and this is where that is asserted
    # rather than assumed. A statement the write raised anyway is a question, and it is
    # asked here rather than discovered by --check.
    cards = load_cards()
    rows = statements(cards)
    fresh = [r["id"] for r in rows if r["id"] not in rulings["rulings"]]
    if fresh:
        print(f"WROTE, AND THE WRITE RAISED {len(fresh)} NEW STATEMENT(S) — rule them and "
              f"build again:", file=sys.stderr)
        for sid in fresh:
            print(f"  {sid}", file=sys.stderr)
        return 1
    INDEX.write_text(json.dumps(reindex(json.loads(INDEX.read_text(encoding="utf-8")), cards),
                                indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(report_text(rows, rulings), encoding="utf-8")
    people = sum(1 for r in rows if rulings["rulings"][r["id"]]["verdict"] == "write")
    print(f"{len(rows)} statement(s) read, {people} person(s) written onto "
          f"{len(written)} card(s).")
    print(f"  {REPORT.relative_to(ROOT)}")
    return 0


def cmd_check() -> int:
    problems = check()
    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    rows = statements(load_cards())
    rulings = load_rulings()
    people = sum(1 for r in rows if rulings["rulings"][r["id"]]["verdict"] == "write")
    print(f"ok  {len(rows)} stated family statement(s), every one ruled; {people} person(s) "
          f"written and accounted for on both sides")
    return 0


def cmd_report() -> int:
    rows = statements(load_cards())
    rulings = load_rulings()
    for row in rows:
        ruling = (rulings.get("rulings") or {}).get(row["id"], {})
        print(f"{ruling.get('verdict', 'UNRULED'):<22} {row['id']}")
        print(f"    {row['relation']:<10} {row['other_as_read']}  ({row['read_from']})")
    return 0


def self_test() -> int:
    """Each assertion of --check, broken on purpose, on a tree held in memory."""
    cards = load_cards()
    rulings = load_rulings()
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    report = REPORT.read_text(encoding="utf-8")
    failures = 0

    def case(name: str, expect: str, **kw) -> None:
        nonlocal failures
        problems = check(**{"cards": cards, "rulings": rulings, "index": index,
                            "report": report, **kw})
        hit = any(expect in p for p in problems)
        print(f"   self-test | {'ok  ' if hit else 'FAIL'} {name}")
        if not hit:
            failures += 1
            for p in problems:
                print(f"   self-test |      saw: {p}")

    # the live tree is green, or none of the cases below mean anything
    live = check(cards=cards, rulings=rulings, index=index, report=report)
    print(f"   self-test | {'ok  ' if not live else 'FAIL'} the committed tree is green")
    if live:
        failures += 1
        for p in live:
            print(f"   self-test |      {p}")

    dropped = json.loads(json.dumps(rulings))
    gone = sorted(dropped["rulings"])[0]
    del dropped["rulings"][gone]
    case("a statement nobody ruled on", "no ruling answers it", rulings=dropped)

    invented = json.loads(json.dumps(rulings))
    invented["rulings"]["marriage:hh_nobody:nobody"] = {"verdict": "write", "why": "x"}
    case("a ruling with no statement", "a ruling with no statement", rulings=invented)

    silent = json.loads(json.dumps(rulings))
    silent["rulings"][gone] = dict(silent["rulings"].get(gone, {}), verdict="write", why="")
    case("a verdict with no reason", "a verdict with no reason", rulings=silent)

    pulled = json.loads(json.dumps(cards))
    written = next((sid for sid, r in rulings["rulings"].items()
                    if r.get("verdict") == "write"), None)
    if written:
        for card in pulled.values():
            card["persons"] = [p for p in card["persons"]
                               if (p.get("stated_family") or {}).get("statement") != written]
        case("a ruled write that is not on the card", "stands on 0 card(s)", cards=pulled)

    moved = json.loads(json.dumps(cards))
    orphan = dict(next(p for c in cards.values() for p in c["persons"]
                       if (p.get("stated_family") or {}).get("pass") == PASS_KEY)) \
        if written else None
    if orphan:
        orphan = json.loads(json.dumps(orphan))
        orphan["id"] = f"{orphan['id']}_orphan"
        orphan["stated_family"] = dict(orphan["stated_family"], statement="marriage:nobody")
        next(iter(moved.values()))["persons"].append(orphan)
        case("a person this pass wrote that no ruling claims", "which no ruling claims",
             cards=moved)

    drifted = json.loads(json.dumps(index))
    drifted["counts"]["persons"] = -1
    case("a manifest that disagrees with the cards", "disagrees with the cards",
         index=drifted)

    case("a stale report", "is stale", report="")

    reconstructed = json.loads(json.dumps(cards))
    next(iter(reconstructed.values()))["persons"][0]["grade"] = "reconstructed"
    case("a reconstructed grade under a research writer", WRITER, cards=reconstructed)

    print(f"   self-test | {failures} failure(s)")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.build:
        return cmd_build()
    if args.check:
        return cmd_check()
    if args.self_test:
        return self_test()
    return cmd_report()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
