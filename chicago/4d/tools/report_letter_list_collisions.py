#!/usr/bin/env python3
"""Every surname collision the corrected letter-list reading uncovered, derived twice.

WHY THIS EXISTS (T-0660). The post office printed a name in either order and, until
T-0638, `mint_letter_list_residents.surname()` read the LAST token as the family name
in both. `Mills Joel C.` was therefore minted under the surname `c` and `Joel C. Mills`
would have been minted under `mills`, and the pass's refusals 7 and 8 — one household
per surname in the town, one per surname in this pass — never saw the two printings as
landing on one family name. T-0638 corrected the reading and deliberately did not act
on what it revealed, because acting RETIRES RECORDS.

WHAT THIS TOOL IS. The instrument T-0660's first acceptance clause asks for: the pairs
DERIVED rather than hand-assembled, by running the pass's own `mint()` twice over the
same committed tree — once with the pre-T-0638 reading of a printed name, once with the
corrected one — and reporting every candidate the corrected reading refuses that the old
one accepted, with the two printings side by side and the record that holds the surname
instead.

WHAT IT DELIBERATELY DOES NOT DO. It retires nothing and writes nothing into
`data/residents/`. Which of a colliding pair survives is not a question a tool may
answer here: the pairs are not all duplicates. `Joel C. Mills` and `Philo C. Mills` are
two different men who may not both hold `mills`, and the pass's `rank()` — which sorts
single-return names by the NEWEST return — would keep `B. Osborn` over `Wm. Osborn`, an
initial over a written given name. Retiring a record removes a person from the town, so
the rule that picks the survivor is the owner's ruling, and this report is what makes it
a decidable one.

THE SECOND FINDING, and the reason this report exists as a file rather than a paragraph
in a PR: the committed letter-list cohort is a long way out of step with what its own
tool now derives, and only a small part of that is this fault. `check.sh` runs the
pass's `--gate` and not its `--check`, so the drift has never been red. The report
counts it, and splits it by cause.

    python3 tools/report_letter_list_collisions.py            # print the report
    python3 tools/report_letter_list_collisions.py --write    # write the committed copy
    python3 tools/report_letter_list_collisions.py --check    # committed copy still true?
    python3 tools/report_letter_list_collisions.py --self-test
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mint_letter_list_residents as m  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/RESEARCH/letter-list-surname-collisions.md"


# ---------------------------------------------------------------------------
# the two readings
# ---------------------------------------------------------------------------

def pre_t0638_surname(name: str) -> str:
    """The family name as the pass read it BEFORE T-0638: the last printed token.

    Kept here rather than in the pass, because the pass has one reading and this
    report needs two. It is the exact body of `surname()` as of 9d962929, with the
    apostrophe handling of the current one so that fault B (T-0638's other half)
    does not leak into a diff that is about fault A.
    """
    parts = m.words(name)
    if not parts:
        return ""
    if "," in name:
        head = m.words(name.partition(",")[0])
        picked = head[-1] if head else parts[0]
    else:
        picked = parts[-1]
    return picked.lower().strip("'").replace("'", "")


def mint_with(reading, docs: dict, index: dict):
    """`mint()` run under a given reading of a printed name.

    Every one of the pass's own rules is used unchanged — the pool, the ranking and
    all nine refusals — because a second implementation of them would be measuring
    something other than the pass.
    """
    original = m.surname
    m.surname = reading
    try:
        return m.mint(docs, index)
    finally:
        m.surname = original


# ---------------------------------------------------------------------------
# what a record carries, which is what survivorship turns on
# ---------------------------------------------------------------------------

def committed_letter_list(docs: dict) -> dict:
    """Committed letter-list households, keyed by the display name on the card."""
    out = {}
    for path, doc in docs.items():
        if m.minted_by(path, doc, "letter_list", m.PREFIX):
            for person in doc.get("persons") or []:
                out[person["name"]] = (path.stem, doc, person)
    return out


def attachment(doc: dict, person: dict) -> list[str]:
    """The downstream things a record carries that a retirement would strand."""
    carried = []
    research = person.get("resident_research")
    if research:
        carried.append(f"research row {research.get('ticket', '?')}"
                       f" ({research.get('outcome', '?')})")
    directories = doc.get("directories") or {}
    for source in directories.get("sources") or []:
        carried.append(f"directory {source}")
    for key in ("census_1840", "bridge_1840", "crosswalk"):
        if doc.get(key) or person.get(key):
            carried.append(key)
    return carried


# ---------------------------------------------------------------------------
# the derivation
# ---------------------------------------------------------------------------

def derive() -> dict:
    docs = {p: m.load(p) for p in sorted(m.HOUSEHOLDS.glob("*.json"))}
    index = m.load(m.INDEX)

    new_accepted, new_refused = mint_with(m.surname, docs, index)
    old_accepted, _old_refused = mint_with(pre_t0638_surname, docs, index)

    new_by_id = {cand["id"]: cand for cand, _ in new_accepted}
    old_by_id = {cand["id"]: cand for cand, _ in old_accepted}
    # T-0660's ruling (c) changed where the answer is read from, and not what it is.
    # A mint-time refusal no longer drops a standing record, so the difference between
    # the readings is no longer a difference in who is ACCEPTED — it is a difference in
    # who the pass now SAYS a collision on. Same candidates, same order, same rows.
    new_collided = {cand["id"]: cand["surname_collision"]
                    for cand, _ in new_accepted if cand.get("surname_collision")}
    old_collided = {cand["id"] for cand, _ in old_accepted
                    if cand.get("surname_collision")}
    returns = {cand["id"]: len(m.returns_of(gaz["mentions"]))
               for cand, gaz in new_accepted}
    printings = {cand["id"]: len(gaz["mentions"]) for cand, gaz in new_accepted}
    for cand, gaz in old_accepted:
        returns.setdefault(cand["id"], len(m.returns_of(gaz["mentions"])))
        printings.setdefault(cand["id"], len(gaz["mentions"]))

    committed = committed_letter_list(docs)

    pairs = []
    for cid in sorted(set(new_collided) - old_collided):
        printed = new_by_id[cid]["name"]
        shown = m.display(printed)
        stem, doc, person = committed.get(shown, (None, None, None))
        held = new_collided[cid]["holds_the_surname"]
        pairs.append({
            "printed": printed,
            "display": shown,
            "old_surname": pre_t0638_surname(printed),
            "new_surname": m.surname(printed),
            "reason": new_collided[cid]["refusal"],
            "committed": stem,
            "returns": returns.get(cid, 0),
            "printings": printings.get(cid, 0),
            "carries": attachment(doc, person) if doc else [],
            "holder": "; ".join(held[:3]) + (" …" if len(held) > 3 else "") or "—",
        })

    admitted = []
    for cid in sorted(set(new_by_id) - set(old_by_id)):
        printed = new_by_id[cid]["name"]
        admitted.append({
            "printed": printed,
            "display": m.display(printed),
            "old_surname": pre_t0638_surname(printed),
            "new_surname": m.surname(printed),
            "returns": returns.get(cid, 0),
            "printings": printings.get(cid, 0),
        })

    # the committed cohort against its own derivation, split by cause
    shown_ids: set[str] = set()
    derived_ids = set()
    for cand, _gaz in new_accepted:
        hid = m.household_id(cand["name"], m.PREFIX, "letter_list", docs, shown_ids)
        shown_ids.add(hid)
        derived_ids.add(hid)
    committed_ids = {path.stem for path, doc in docs.items()
                     if m.minted_by(path, doc, "letter_list", m.PREFIX)}
    derived_names = {m.display(cand["name"]) for cand, _ in new_accepted}
    refused_by_name = {m.display(name): reason
                       for _cid, name, _n, reason in new_refused}
    this_fault = {p["display"] for p in pairs}
    causes: dict[str, int] = {}
    for hid in sorted(committed_ids - derived_ids):
        name = docs[m.HOUSEHOLDS / f"{hid}.json"]["persons"][0]["name"]
        if name in derived_names:
            key = "the record stands under a different id (a rename, not a retirement)"
        elif name in this_fault:
            key = "THIS FAULT — the corrected reading collides it with another record"
        elif name in refused_by_name:
            key = ("the town gained this surname from another pass after the mint "
                   f"({m.reason_key(refused_by_name[name])})")
        else:
            key = "no longer in the pool the register offers"
        causes[key] = causes.get(key, 0) + 1

    return {
        "pool": len(new_accepted) + len(new_refused),
        "new_accepted": len(new_accepted),
        "old_accepted": len(old_accepted),
        "new_collided": len(new_collided),
        "old_collided": len(old_collided),
        "committed": len(committed_ids),
        "derived": len(derived_ids),
        "pairs": pairs,
        "admitted": admitted,
        "causes": causes,
        "residual": residual_comma_fault(docs, index),
    }


def residual_comma_fault(docs: dict, index: dict) -> list[dict]:
    """Printings the CORRECTED reading still takes a given name off as the surname.

    `surname_is_first_token()` fires when the token the plain rule lands on is an
    initial and some earlier token is a full word. With a comma in the printing that
    test can pick the token before the comma when the family name is the one after
    it: `Augustus H, Conant` reads `augustus`. Reported, not fixed — a change to
    `surname()` re-derives the whole cohort, which is the very thing T-0660 exists to
    put to the owner first.
    """
    own = frozenset(doc["head"] for doc in docs.values()
                    if doc.get("source_pass") == "letter_list")
    out = []
    for cand in m.letter_list_pool(m.load(m.REGISTER), own):
        name = cand["name"]
        if "," not in name or not m.surname_is_first_token(name):
            continue
        head = m.words(name.partition(",")[0])
        tail = m.words(name.partition(",")[2])
        if not tail or not m.full_word(tail[0]):
            continue          # nothing after the comma that could be a family name
        if m.surname(name) == tail[0].lower().strip("'").replace("'", ""):
            continue          # already reading the token after the comma
        if m.UNCERTAIN.search(name):
            continue          # garbled, and refusal 2 drops it before this matters
        out.append({"printed": name, "reads": m.surname(name),
                    "after_the_comma": tail[0], "head": " ".join(head)})
    return out


# ---------------------------------------------------------------------------
# the report
# ---------------------------------------------------------------------------

def lines(d: dict) -> list[str]:
    out = [
        "# The surname collisions the corrected letter-list reading uncovered",
        "",
        "DERIVED, NOT WRITTEN. Every number and every row below is produced by",
        "`tools/report_letter_list_collisions.py`, which runs",
        "`mint_letter_list_residents.mint()` twice over the committed tree — once under the",
        "pre-T-0638 reading of a printed name, once under the corrected one — and reports the",
        "difference. `--check` re-derives it and fails if this file has drifted from what the",
        "tree now says, so it cannot quietly go stale.",
        "",
        "T-0843 MOVED ONE ROW OUT OF THIS REPORT AND THE REASON IS WORTH READING. The pass",
        "now consults the cross-domain identity master before it writes a card, so",
        "`Norton N. R.` is refused under BOTH readings — the master resolves the initials",
        "onto the committed Nelson R. Norton whichever token the old rule took for a",
        "surname. It was never a difference between the two readings; the surname test was",
        "simply too blunt to see it under one of them. The count below fell by one",
        "accordingly, and nothing was retired to make that happen.",
        "",
        "THE OWNER RULED, 2026-09-18: option (c). Refusals 7 and 8 are MINT-TIME rules and",
        "do not un-mint a record that already stands. NOTHING IS RETIRED. The pass keeps every",
        "standing record a mint-time refusal lands on and SAYS the collision on its card — a",
        "`surname_collision` block naming the other holder — so a reader sees both records and",
        "why both are here. `rank()` is unchanged, the cohort is not re-derived, and the",
        "population does not move. This report is therefore no longer a list of proposed",
        "retirements; it is the derivation behind the blocks, and the rows below are the same",
        "rows they were, read now off what the pass says rather than off who it drops.",
        "",
        "## The two readings, over the same pool",
        "",
        f"* the pool the register offers this pass: **{d['pool']}** candidates",
        f"* accepted under the pre-T-0638 reading: **{d['old_accepted']}**",
        f"* accepted under the corrected reading: **{d['new_accepted']}**",
        f"* standing records a mint-time refusal lands on, corrected reading: "
        f"**{d['new_collided']}**; pre-T-0638 reading: **{d['old_collided']}**",
        f"* THE COLLISIONS THIS FAULT UNCOVERED — said under the corrected reading and "
        f"not under the old one: **{len(d['pairs'])}**",
        f"* candidates the correction ADMITS that the old reading refused: "
        f"**{len(d['admitted'])}**",
        "",
        "## The collisions — what the paper printed, and who holds the surname instead",
        "",
        "`old` and `new` are the family name each reading takes off the printing. `holds it`",
        "is the record the refusal defers to, and under the ruling it defers by SAYING so and",
        "not by standing down. `carries` is what a retirement would have stranded, and is kept",
        "in the table because it is the measure of what option (c) declined to throw away.",
        "",
        "| printed | as a card shows it | old | new | the refusal it says | holds it | returns | carries |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for p in d["pairs"]:
        out.append(
            f"| `{p['printed']}` | {p['display']} | `{p['old_surname']}` | "
            f"`{p['new_surname']}` | {p['reason']} | {p['holder']} | {p['returns']} | "
            f"{', '.join(p['carries']) or '—'} |")
    out += [
        "",
        "## Why no tool picks a survivor, and why the ruling asked none to",
        "",
        "These were the three reasons the loop could not answer the survivorship question,",
        "and they are why the owner answered it with (c) — keep both, say the collision.",
        "",
        "* **They are not all duplicates.** `Joel C. Mills` and `Philo C. Mills` are two",
        "  different men. Refusal 8 is a rule about how much one pass may assert on a family",
        "  name, not a statement that two records are one person — so retiring on it would",
        "  have removed a person rather than merging two.",
        "* **`rank()` is blind to how good a record is.** It orders single-return names by",
        "  the NEWEST return, so the survivor would have been whichever letter was printed",
        "  later — not the one with the fuller name, the research row or the directory match.",
        "  The ruling leaves `rank()` alone precisely because it no longer has to pick.",
        "* **The loser would have been the better-attested record.** The `carries` column",
        "  above is the measure of that, and it is not empty.",
        "",
        "## The committed cohort against its own derivation",
        "",
        f"The tree holds **{d['committed']}** letter-list households. The pass, run today",
        f"against that same tree, derives **{d['derived']}**. `check.sh` runs this pass's",
        "`--gate` and not its `--check`, so the gap has never been red. Under the ruling the",
        "mint-time causes are gone from this table by construction — a standing record is no",
        "longer out of step with its own pass for colliding on a family name. What is left is",
        "split by cause:",
        "",
        "| households | cause |",
        "|---|---|",
    ]
    for cause, n in sorted(d["causes"].items(), key=lambda kv: -kv[1]):
        out.append(f"| {n} | {cause} |")
    out += [
        "",
        "**This is the finding that resized T-0660, and the ruling then dissolved it.** The",
        "ticket was filed believing the retirements were the collisions. Most of them were",
        "not: they were records whose surname the town acquired from a LATER pass, long after",
        "this cohort was minted — T-0691's 76, filed as a separate ruling about a separate",
        "rule. Option (c) answers both with one sentence, because neither kind of collision",
        "un-mints anything now. What survives of T-0691 is wiring its `--check` into",
        "`check.sh`, which is a gate question and not a retirement question.",
        "",
        "## The candidates the correction admits",
        "",
        "The other half of the same diff, and none of them is committed today.",
        "",
        "| printed | as a card would show it | old | new | returns |",
        "|---|---|---|---|---|",
    ]
    for a in d["admitted"]:
        out.append(f"| `{a['printed']}` | {a['display']} | `{a['old_surname']}` | "
                   f"`{a['new_surname']}` | {a['returns']} |")
    out += [
        "",
        "## A residual fault in the corrected reading",
        "",
        "Reported here rather than fixed, because a change to `surname()` re-derives the",
        "whole cohort, and the ruling of 2026-09-18 explicitly declined to pay for that: it",
        "is option (b)'s cost, and (b) is not what was chosen.",
        "",
    ]
    if d["residual"]:
        out += ["| printed | reads the surname as | after the comma |", "|---|---|---|"]
        for r in d["residual"]:
            out.append(f"| `{r['printed']}` | `{r['reads']}` | `{r['after_the_comma']}` |")
        out += [
            "",
            "A comma says the family name is the group BEFORE it. When that group ends on an",
            "initial, `surname_is_first_token()` fires and takes the first full word of the",
            "whole printing — the given name — instead of the full word after the comma.",
        ]
    else:
        out.append("None in the pool as it stands.")
    out += [
        "",
        "---",
        "",
        "Generated by `tools/report_letter_list_collisions.py --write`. Do not hand-edit:",
        "`--check` compares this file against a fresh derivation.",
    ]
    return out


def render() -> str:
    return "\n".join(lines(derive())) + "\n"


# ---------------------------------------------------------------------------
# the blocks the ruling asks for, on the cards this fault collided
# ---------------------------------------------------------------------------

def blocks() -> dict:
    """The `surname_collision` block for each of this fault's standing cards.

    DERIVED FROM THE PASS, NOT WRITTEN HERE. `mint_letter_list_residents.record()`
    composes the block, so the card and the refusal that produced it cannot drift
    apart, and this tool only says WHICH cards T-0660 owns: the ones the corrected
    reading collides and the pre-T-0638 reading did not. The other collisions the
    pass now says — the ones the town's LATER passes caused, which were T-0691's
    subject — are written when the cohort is next re-derived; they are not this
    ticket's rows and are not hand-picked into it.

    Returns {path: block}, and nothing else on the card is touched: a full re-derive
    of this cohort is a different unit of work (T-1222 holds its 798-file drift) and
    landing it through here would bury eight blocks in it.
    """
    docs = {q: m.load(q) for q in sorted(m.HOUSEHOLDS.glob("*.json"))}
    index = m.load(m.INDEX)
    new_accepted, _ = mint_with(m.surname, docs, index)
    old_accepted, _ = mint_with(pre_t0638_surname, docs, index)
    old_collided = {cand["id"] for cand, _ in old_accepted
                    if cand.get("surname_collision")}

    out, seen = {}, set()
    for cand, gaz in new_accepted:
        doc = m.record(cand, gaz, docs, seen)
        seen.add(doc["id"])
        if not cand.get("surname_collision") or cand["id"] in old_collided:
            continue
        path = m.HOUSEHOLDS / f"{doc['id']}.json"
        if path not in docs:
            continue          # not standing, so the ruling has nothing to protect
        out[path] = doc["surname_collision"]
    return out


def carded(write: bool) -> int:
    """Write (or check) the block on each card, changing nothing else on it."""
    drifted = []
    for path, block in sorted(blocks().items()):
        doc = m.load(path)
        if doc.get("surname_collision") == block:
            continue
        if not write:
            drifted.append(path)
            continue
        doc["surname_collision"] = block
        path.write_text(m.dumps(doc, 1), encoding="utf-8")
        print(f"   said the collision on {path.stem}")
    if drifted:
        for path in drifted:
            print(f"   DRIFT: {path.relative_to(ROOT)} does not say its collision")
        return 1
    print("   OK: every card this fault collides says so" if not write else
          "   done")
    return 0


def self_test() -> int:
    """The report is only worth anything if the two readings really are two."""
    failures = []
    if pre_t0638_surname("Mills Joel C.") != "c":
        failures.append("the pre-T-0638 reading no longer takes the trailing initial")
    if m.surname("Mills Joel C.") != "mills":
        failures.append("the corrected reading no longer takes the leading surname")
    if pre_t0638_surname("Joel C. Mills") != m.surname("Joel C. Mills"):
        failures.append("the two readings disagree on a printing they must agree on")
    d = derive()
    if not d["pairs"]:
        failures.append("no collision derived at all — the diff cannot be empty while "
                        "the corrected reading still collides these printings")
    if d["old_accepted"] > d["new_accepted"]:
        failures.append("the corrected reading accepts FEWER records than the old one: "
                        "T-0660's ruling (c) says a mint-time refusal retires nobody")
    if any(p["new_surname"] == p["old_surname"] and "already minted" not in p["reason"]
           for p in d["pairs"]):
        failures.append("a collision is reported whose surname did not move and whose "
                        "refusal is not a within-pass one")
    for line in failures:
        print(f"   FAIL: {line}")
    if failures:
        return 1
    print(f"   OK: {len(d['pairs'])} collision(s), {len(d['admitted'])} admission(s), "
          f"both readings behave")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write the committed report")
    ap.add_argument("--check", action="store_true",
                    help="re-derive and fail if the committed report has drifted")
    ap.add_argument("--write-records", action="store_true",
                    help="write the surname_collision block onto the standing cards")
    ap.add_argument("--check-records", action="store_true",
                    help="fail if a card this fault collides does not say so")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.write_records or args.check_records:
        return carded(args.write_records)
    text = render()
    if args.write:
        REPORT.write_text(text, encoding="utf-8")
        print(f"   wrote {REPORT.relative_to(ROOT)}")
        return 0
    if args.check:
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != text:
            print(f"   DRIFT: {REPORT.relative_to(ROOT)} is not what the tree derives")
            return 1
        print(f"   OK: {REPORT.relative_to(ROOT)} matches a fresh derivation")
        return 0
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
