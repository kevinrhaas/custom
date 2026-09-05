#!/usr/bin/env python3
"""One person, one town card: the candidates ledger, the rulings, and the merges.

WHY THIS EXISTS, in the owner's words (2026-09-05, reading the households folder):
*"do a review and consolidate of the residents, like James Allen is almost certainly one
record and he is spread across several, don't lose any data, but consolidation is
needed across the residents."* And, a day's argument later, on what the deliverable is:
*"make the ticket merge those records — research without consolidation is useless."*

THE DEFECT. `consolidate_resident_evidence.py` clusters SOURCE APPEARANCES into
identities. It is careful, and its caution is the right default: an initial-only
forename with two rival full forenames of that surname is R3, a refusal, never a coin
toss. But the residents layer is minted FROM those identities, so every refusal the
consolidation makes becomes another town card, and Gurdon Saltonstall Hubbard stands on
six of them — `hubbard_g`, `_g_s`, `_g_t`, `_gordon_s`, `_gurdon`, `_gurdon_s` — while
Lieut. James Allen stands on four and only the card the ladder never reached knows he
was an army officer.

WHAT THIS TOOL DOES. It puts every cluster of town cards that MIGHT be one person in
front of a reader with the evidence for and against each pair, and it holds the gate
that says a cluster nobody has ruled on is a defect. The rulings themselves live in
`data/research/residents/town_card_crosswalk.json` and are written by hand, because
they are adjudications and not derivations: MERGE, DISTINCT, or UNDECIDED, each with
the evidence it rests on.

WHERE THE MERGE ACTUALLY HAPPENS, and this is the point. A ruled MERGE is spent in the
IDENTITY layer, not here: the crosswalk's `merges` are read by
`consolidate_resident_evidence.py` as rule D3, which folds the two identities into one
before the ladder grades it. Three things follow for free, and all three are what the
ticket asks for. The grade is the LADDER's over the union rather than the best of the
folded grades. The union of appearances, sources and evidence blocks is what the mint
writes, because the mint writes from the identity. And the duplicate card stops being
minted at all, because `mint_civic_residents.decide()` already refuses an identity whose
canonical person is a card this pass does not own — which is why fixing the cause needed
no change to any minting pass, only a gate that notices when the cause recurs.

WHAT `--apply` DOES, therefore, is the part the identity layer cannot do: it leaves a
REDIRECT STUB where every folded card stood, so that no `person_id` or `household_id`
any file cites stops resolving, and it carries the folded card's own prose — the
research notes a mint does not write — onto the survivor. Nothing is deleted.

    tools/consolidate_town_cards.py --candidates   write the ledger
    tools/consolidate_town_cards.py --apply        stubs + carried prose, after a mint
    tools/consolidate_town_cards.py --check        the ledger re-derives; the stubs resolve
    tools/consolidate_town_cards.py --gate         every cluster carries a ruling
    tools/consolidate_town_cards.py --report       the tables, to stdout
    tools/consolidate_town_cards.py --self-test    the assertions still fire when broken
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import consolidate_resident_evidence as cre        # noqa: E402

RESIDENTS = ROOT / "data" / "residents"
HOUSEHOLDS = RESIDENTS / "households"
INDEX = RESIDENTS / "index.json"
RESEARCH = ROOT / "data" / "research" / "residents"
CANDIDATES = RESEARCH / "town_card_candidates.json"
CROSSWALK = RESEARCH / "town_card_crosswalk.json"
REDIRECTS = RESIDENTS / "redirects.json"
MASTER = RESEARCH / "identity_master.json"
GENERATED_BY = "tools/consolidate_town_cards.py --candidates"

# A TITLE IS NOT A FORENAME, and `consolidate_resident_evidence.HONORIFICS` does not
# hold every one the corpus prints — `Lieut` is missing from it, which is why the
# identity layer reads "Lieut Allen" as a man whose forename is *Lieut* and holds him
# apart from James Allen by R4. That list is load-bearing for 6,742 identities and is
# not this ticket's to move; the candidates pass carries its own, wider list so it can
# SEE the cluster the identity layer cannot, and the ruling is what spends it.
TITLES = cre.HONORIFICS | {"lieut", "lieutenant", "captain", "colonel", "major",
                           "general", "doctor", "reverend", "father", "judge",
                           "deacon", "elder", "sergeant", "corporal", "ensign",
                           "prof", "professor", "gov", "governor", "maj", "revd"}


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def dumps(doc, indent=1) -> str:
    return json.dumps(doc, indent=indent, ensure_ascii=False) + "\n"


def parse(name: str):
    """(surname, [forename tokens], [title tokens]) — the titles kept, not dropped.

    A title is EVIDENCE: 'Lieut. James Allen' and 'James Allen' agree on the forename
    and the title says what the army list says. Dropping it silently is what turned a
    rank into a Christian name.
    """
    parsed = cre.split_name(name)
    if not parsed:
        return None
    surname, given = parsed
    titles = [t for t in given if t in TITLES]
    forenames = [t for t in given if t not in TITLES]
    return surname, forenames, titles


def compatible(a, b) -> tuple[bool, str]:
    """Do two readings of a name name the same person, on the name alone?

    The same standard the directory forename test uses (T-0515): a full forename against
    the same word, against an initial that opens it, or a name one reading does not print
    at all. Nothing looser — 'G. S.' against 'G. T.' is not compatible, and never was.
    """
    _, fa, _ = a
    _, fb, _ = b
    if not fa or not fb:
        return False, "one reading prints no forename at all, which is R1 and never merges"
    for x, y in zip(fa, fb):
        if x == y:
            continue
        if len(x) == 1 and y.startswith(x):
            continue
        if len(y) == 1 and x.startswith(y):
            continue
        return False, f"the readings disagree at '{x}' against '{y}'"
    return True, ""


# ---------------------------------------------------------------------------
# reading the town


def town_cards() -> list:
    """One row per PERSON on a town card, with everything a ruling needs to see."""
    master = load(MASTER) or {}
    identity_of = {}
    for row in master.get("identities", []):
        for person_id in row.get("town_person_ids") or []:
            identity_of[person_id] = row["id"]
        if row.get("canonical_person_id"):
            identity_of.setdefault(row["canonical_person_id"], row["id"])
    cards = []
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        doc = load(path)
        if not isinstance(doc, dict) or doc.get("merged_into"):
            continue
        for person in doc.get("persons") or []:
            parsed = parse(person.get("name") or "")
            if not parsed:
                continue
            cards.append({
                "person_id": person.get("id"),
                "household_id": doc.get("id"),
                "name": person.get("name"),
                "relationship": person.get("relationship"),
                "grade": person.get("grade"),
                "ladder_rule": person.get("ladder_rule"),
                "occupation": ((person.get("occupation") or {}).get("value")
                               if isinstance(person.get("occupation"), dict) else None),
                "source_pass": doc.get("source_pass"),
                "identity": identity_of.get(person.get("id")),
                "sources": sorted(person.get("sources") or []),
                "lives_at": (doc.get("lives_at") or {}).get("value"),
                "_parsed": parsed,
            })
    return cards


def title_only(card) -> bool:
    """A card whose name prints a rank and a surname and no forename at all."""
    _, forenames, titles = card["_parsed"]
    return not forenames and bool(set(titles) - GENERIC_TITLES)


# `Mr`, `Mrs`, `Miss`, `Widow`, `Esq`, `Jr` say nothing about WHICH man: every second
# card could carry one. A rank or a doctorate is a discriminator, and 'Lieut Allen' is
# the case — a card the identity layer refuses on R1 (no forename, so it can never be
# merged) which one rank and one surname nevertheless identify, because the corpus
# names exactly one Lieut. Allen. It joins the cluster as a CANDIDATE; the ruling is
# still what merges it.
GENERIC_TITLES = {"mr", "mrs", "miss", "widow", "esq", "jr", "sr", "mme", "madame", "hon"}


def clusters(cards: list) -> list:
    """Surname buckets, then transitive closure over name-compatible pairs."""
    by_surname = defaultdict(list)
    for card in cards:
        by_surname[card["_parsed"][0]].append(card)
    out = []
    for surname in sorted(by_surname):
        group = sorted(by_surname[surname], key=lambda c: c["person_id"])
        parent = list(range(len(group)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                ok, _ = compatible(group[i]["_parsed"], group[j]["_parsed"])
                if not ok and (title_only(group[i]) or title_only(group[j])):
                    shared = (set(group[i]["_parsed"][2]) & set(group[j]["_parsed"][2])
                              - GENERIC_TITLES)
                    ok = bool(shared)
                if ok:
                    a, b = find(i), find(j)
                    if a != b:
                        parent[a] = b
        buckets = defaultdict(list)
        for i in range(len(group)):
            buckets[find(i)].append(group[i])
        for key in sorted(buckets, key=lambda k: group[k]["person_id"]):
            members = buckets[key]
            if len(members) < 2:
                continue
            out.append({"cluster_id": members[0]["person_id"], "surname": surname,
                        "cards": members})
    return sorted(out, key=lambda c: c["cluster_id"])


def pair_evidence(a: dict, b: dict) -> dict:
    """What argues FOR one man and what argues AGAINST, both stated, never weighed here."""
    for_, against = [], []
    shared = sorted(set(a["sources"]) & set(b["sources"]))
    if shared:
        for_.append(f"both cards cite {', '.join(shared)}")
    _, fa, ta = a["_parsed"]
    _, fb, tb = b["_parsed"]
    if fa == fb:
        for_.append(f"the forename is the same word on both readings ({' '.join(fa)})")
    elif len(fa) != len(fb) or any(len(x) == 1 or len(y) == 1 for x, y in zip(fa, fb)):
        for_.append("an initial on one reading against the full forename on the other")
    if len(fa) != len(fb):
        longer = " ".join(fa if len(fa) > len(fb) else fb)
        for_.append(f"one reading prints a middle name the other does not ({longer})")
    shared_titles = sorted((set(ta) & set(tb)) - GENERIC_TITLES)
    if shared_titles:
        for_.append(f"both readings print the same rank or style ({', '.join(shared_titles)})")
    elif ta or tb:
        for_.append("a title stands on one reading: "
                    + ", ".join(sorted(set(ta) | set(tb))))
    if not fa or not fb:
        for_.append("one reading prints a rank and a surname and no forename, so the "
                    "identity layer refuses it on R1 and only a ruling can reach it")
    if a["occupation"] and b["occupation"]:
        (for_ if a["occupation"] == b["occupation"] else against).append(
            f"the trade reads {a['occupation']} against {b['occupation']}")
    elif a["occupation"] or b["occupation"]:
        for_.append(f"one card carries a trade and the other none "
                    f"({a['occupation'] or b['occupation']})")
    if a["relationship"] != b["relationship"]:
        against.append(f"the cards stand in different roles — {a['relationship']} "
                       f"against {b['relationship']}")
    if a["lives_at"] and b["lives_at"] and a["lives_at"] != b["lives_at"]:
        against.append(f"the cards live at {a['lives_at']} and {b['lives_at']}")
    for x, y in zip(fa, fb):
        if x != y and len(x) > 1 and len(y) > 1:
            against.append(f"the forenames contradict — {x} against {y}")
        elif x != y and (len(x) == 1 or len(y) == 1):
            pass
    if len(fa) == len(fb) and fa != fb and all(len(x) == 1 for x in fa + fb):
        against.append("two initial-only readings that disagree")
    return {"a": a["person_id"], "b": b["person_id"], "for": for_, "against": against}


def build_candidates() -> dict:
    cards = town_cards()
    groups = clusters(cards)
    rows = []
    for group in groups:
        members = group["cards"]
        rows.append({
            "cluster_id": group["cluster_id"],
            "surname": group["surname"],
            "cards": [{k: v for k, v in card.items() if k != "_parsed" and v not in
                       (None, [], "")} for card in members],
            "pairs": [pair_evidence(members[i], members[j])
                      for i in range(len(members))
                      for j in range(i + 1, len(members))],
        })
    return {
        "schema": 1,
        "_doc": "GENERATED by tools/consolidate_town_cards.py --candidates. Every cluster "
                "of town cards that MIGHT be one person, with the evidence for and against "
                "each pair. A worklist, never a merge list: the rulings are in "
                "town_card_crosswalk.json and are made by hand. Hand-edit and --check "
                "says so.",
        "generated_by": GENERATED_BY,
        "not_a_reading": "a derivation over the town's own cards — it reads no source, so "
                         "it adjudicates nothing and must never be counted as research read",
        "counts": {
            "town_cards": len(cards),
            "clusters": len(rows),
            "cards_in_clusters": sum(len(r["cards"]) for r in rows),
        },
        "clusters": rows,
    }


# ---------------------------------------------------------------------------
# the rulings


def merge_families(merges: dict) -> dict:
    """folded/survivor person id -> the survivor that holds them."""
    home = {}
    for folded, row in merges.items():
        home[folded] = row["survivor_person_id"]
        home.setdefault(row["survivor_person_id"], row["survivor_person_id"])
    return home


def ruled_pairs(merges: dict, refused: dict, other: set) -> set:
    """Every candidate pair a ruling reaches, as a frozenset of the two person ids.

    A pair is reached three ways, and the third is the one worth stating: two cards
    ruled onto DIFFERENT survivors have been ruled apart, because a card can be one
    person's and only one. `hubbard_g` clustered with Gurdon Saltonstall Hubbard on an
    initial and is ruled onto Henry G. Hubbard; that ruling settles the Gurdon pair too.
    """
    home = merge_families(merges)
    family = defaultdict(set)
    for person, survivor in home.items():
        family[survivor].add(person)
    covered = set()
    for members in family.values():
        ordered = sorted(members)
        for i, x in enumerate(ordered):
            for y in ordered[i + 1:]:
                covered.add(frozenset((x, y)))
    for x, home_x in home.items():
        for y, home_y in home.items():
            if x < y and home_x != home_y:
                covered.add(frozenset((x, y)))
    # A RULING REACHES THE WHOLE FAMILY IT IS MADE AGAINST. Once 'J. S. C. Hogan' is one
    # card with John S. C. Hogan, the ruling that the parish's John Hogan is a different
    # man settles the J. S. C. pair too — asking for it a second time in the crosswalk
    # would be asking the same question twice and inviting two answers to it.
    for pair in set(refused) | set(other):
        a, b = sorted(pair)
        for x in family.get(home.get(a, a), {a}):
            for y in family.get(home.get(b, b), {b}):
                covered.add(frozenset((x, y)))
    return covered


def coverage() -> tuple[dict, list]:
    """(the ledger as committed, every candidate pair no ruling reaches)."""
    doc = load(CANDIDATES) or {}
    crosswalk = load(CROSSWALK) or {}
    merges = {row["folded_person_id"]: row for row in crosswalk.get("merges", [])}
    refused = {frozenset((r["a"], r["b"])) for r in crosswalk.get("refused_merges", [])}
    other = {frozenset((r["a"], r["b"])) for key in ("undecided", "deferred")
             for r in crosswalk.get(key, [])}
    covered = ruled_pairs(merges, refused, other)
    gaps = []
    for cluster in doc.get("clusters", []):
        for pair in cluster["pairs"]:
            if frozenset((pair["a"], pair["b"])) not in covered:
                gaps.append((cluster["cluster_id"], pair["a"], pair["b"]))
    return doc, gaps


# ---------------------------------------------------------------------------
# the merge itself


def survivor_union(merges: dict) -> dict:
    """survivor person id -> what the merged identity now offers that card.

    Derived from the identity master AFTER the fold, so it is the union by construction
    and `--check` can re-derive it. The evidence blocks are the MINT's own derivation,
    imported rather than reimplemented: a second reading of the same appearances would be
    a second answer to a question the mint has already answered.
    """
    import mint_civic_residents as civic
    master = load(MASTER) or {}
    proposal = load(RESEARCH / "grading_proposal.json") or {}
    rows = {r["identity"]: r for r in proposal.get("proposals", [])}
    out = {}
    for row in master.get("identities", []):
        canonical = row.get("canonical_person_id")
        if not canonical:
            continue
        folded = sorted({f for f, r in merges.items()
                         if r["survivor_person_id"] == canonical})
        if not folded:
            continue
        blocks, sources = civic.evidence_blocks(
            rows.get(row["id"], {"name": row.get("forename", "")}),
            [a for a in row.get("appearances", []) if a.get("domain") != "residents"])
        out[canonical] = {
            "folded": folded,
            "blocks": {k: v for k, v in blocks.items() if v},
            "sources": sorted(set(sources)),
        }
    return out


def merged_from_block(folded: list, cards: dict, merges: dict) -> list:
    return [{
        "person_id": person_id,
        "household_id": cards.get(person_id, {}).get("household_id"),
        "name": cards.get(person_id, {}).get("name"),
        "ruled_in": merges[person_id].get("ruled_in"),
        "redirect": "data/residents/redirects.json",
    } for person_id in folded]


def card_index() -> dict:
    """person id -> (household path, household doc), for every card on disk."""
    out = {}
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        doc = load(path)
        if not isinstance(doc, dict):
            continue
        for person in doc.get("persons") or []:
            out[person.get("id")] = {"path": path, "doc": doc, "name": person.get("name"),
                                     "household_id": doc.get("id")}
    return out


def build_redirects(merges: dict, live: dict, prior: dict) -> dict:
    """The folded cards, kept WHOLE. This is what 'lose nothing' means mechanically.

    A folded card stops being minted the moment its identity is folded, so the file
    leaves the tree — and with it the research note a mint does not write, the arrival
    bound, the prose. All of it is captured here VERBATIM, keyed by the ids other files
    cite, before the mint ever runs. A redirect is not a tombstone: it is the record,
    plus a pointer to the card that now carries the man.
    """
    kept = {row["person_id"]: row for row in (prior or {}).get("redirects", [])}
    rows = []
    for folded in sorted(merges):
        ruling = merges[folded]
        survivor = ruling["survivor_person_id"]
        was = kept.get(folded)
        if folded in live:
            record = live[folded]["doc"]
            household = record.get("id")
        elif was:
            record, household = was["record"], was["household_id"]
        else:
            raise SystemExit(f"{folded} is neither on a card nor already redirected — "
                             f"run --apply before the mint deletes it")
        rows.append({
            "person_id": folded,
            "household_id": household,
            "merged_into_person_id": survivor,
            "merged_into_household_id": (live.get(survivor) or {}).get("household_id")
                                        or (was or {}).get("merged_into_household_id"),
            "ruled_in": ruling.get("ruled_in"),
            "ruled_on": ruling.get("ruled_on"),
            "rule": "D3",
            "evidence": ruling.get("evidence"),
            "record": record,
        })
    return {
        "schema": 1,
        "_doc": "GENERATED by tools/consolidate_town_cards.py --apply. Every town card "
                "folded onto another by a T-0839 ruling, kept WHOLE and keyed by the ids "
                "other files cite, so no person_id or household_id in this repository "
                "stops resolving. `record` is the card exactly as it stood the moment it "
                "was folded.",
        "generated_by": "tools/consolidate_town_cards.py --apply",
        "counts": {"redirects": len(rows)},
        "redirects": rows,
    }


def apply() -> int:
    crosswalk = load(CROSSWALK) or {}
    merges = {row["folded_person_id"]: row for row in crosswalk.get("merges", [])}
    live = card_index()
    prior = load(REDIRECTS)
    redirects = build_redirects(merges, live, prior)
    REDIRECTS.write_text(dumps(redirects), encoding="utf-8")

    union = survivor_union(merges)
    written = 0
    for survivor, gained in sorted(union.items()):
        card = live.get(survivor)
        if card is None:
            continue
        doc, path = card["doc"], card["path"]
        person = next(p for p in doc["persons"] if p.get("id") == survivor)
        person["sources"] = sorted(set(person.get("sources") or []) | set(gained["sources"]))
        # The CIVIC pass derives the evidence blocks itself, from the same merged
        # identity, and re-derives them every run; writing them here as well would be a
        # second author for one key. Every other survivor has no pass that would, so the
        # union would simply be lost.
        if doc.get("source_pass") != "civic":
            for key, value in gained["blocks"].items():
                person[key] = value
        doc["merged_from"] = merged_from_block(gained["folded"], live, merges)
        path.write_text(dumps(doc), encoding="utf-8")
        written += 1
    print(f"   {len(redirects['redirects'])} card(s) redirected; {written} survivor(s) "
          f"carry the union")
    return 0


def check() -> int:
    problems = []
    fresh = build_candidates()
    if CANDIDATES.exists() and CANDIDATES.read_text(encoding="utf-8") != dumps(fresh):
        problems.append(f"{CANDIDATES.relative_to(ROOT)} does not match the derivation; "
                        f"run --candidates")
    elif not CANDIDATES.exists():
        problems.append(f"{CANDIDATES.relative_to(ROOT)} is missing; run --candidates")

    crosswalk = load(CROSSWALK) or {}
    merges = {row["folded_person_id"]: row for row in crosswalk.get("merges", [])}
    live = card_index()
    redirects = load(REDIRECTS) or {}
    by_id = {row["person_id"]: row for row in redirects.get("redirects", [])}
    for folded, ruling in sorted(merges.items()):
        if folded in live:
            problems.append(f"{folded} is ruled MERGE into "
                            f"{ruling['survivor_person_id']} and still stands on its own "
                            f"card {live[folded]['household_id']}")
        if folded not in by_id:
            problems.append(f"{folded} is ruled MERGE and has no redirect: the record "
                            f"would be lost")
        elif by_id[folded]["merged_into_person_id"] != ruling["survivor_person_id"]:
            problems.append(f"{folded} redirects to "
                            f"{by_id[folded]['merged_into_person_id']} and the ruling "
                            f"says {ruling['survivor_person_id']}")
        if ruling["survivor_person_id"] not in live:
            problems.append(f"{folded} redirects to "
                            f"{ruling['survivor_person_id']}, which is on no card")
    for row in redirects.get("redirects", []):
        if row["person_id"] not in merges:
            problems.append(f"{row['person_id']} is redirected and no ruling says so")
        if not row.get("record"):
            problems.append(f"{row['person_id']} is redirected with no record kept")
    union = survivor_union(merges)
    for survivor, gained in sorted(union.items()):
        card = live.get(survivor)
        if card is None:
            continue
        person = next((p for p in card["doc"]["persons"] if p.get("id") == survivor), None)
        if person is None:
            continue
        missing = sorted(set(gained["sources"]) - set(person.get("sources") or []))
        if missing:
            problems.append(f"{survivor} absorbed {', '.join(gained['folded'])} and its "
                            f"card has not learned {', '.join(missing)}")
        if card["doc"].get("source_pass") != "civic":
            for key, value in gained["blocks"].items():
                if person.get(key) != value:
                    problems.append(f"{survivor}'s {key} is not the union of the cards "
                                    f"folded onto it; run --apply")
    for problem in problems:
        print(f"   {problem}")
    if problems:
        print(f"   {len(problems)} problem(s)")
        return 1
    print(f"   OK: {len(merges)} ruled merge(s) landed, every folded id resolves, "
          f"{len(union)} survivor(s) carry the union")
    return 0


def gate() -> int:
    doc, gaps = coverage()
    crosswalk = load(CROSSWALK) or {}
    if gaps:
        for cluster_id, a, b in gaps:
            print(f"   {cluster_id}: {a} against {b} — no ruling")
        print(f"   {len(gaps)} candidate pair(s) no ruling reaches. Rule them in "
              f"{CROSSWALK.relative_to(ROOT)} — merge, distinct, or undecided with both "
              f"readings — or the town keeps minting one man twice.")
        return 1
    counts = crosswalk.get("counts", {})
    print(f"   OK: {len(doc.get('clusters', []))} candidate cluster(s), every pair ruled "
          f"({counts.get('merges', 0)} merge, {counts.get('distinct', 0)} distinct, "
          f"{counts.get('undecided', 0)} undecided, {counts.get('deferred', 0)} deferred)")
    return 0


def report() -> int:
    doc, gaps = coverage()
    crosswalk = load(CROSSWALK) or {}
    merges = {row["folded_person_id"]: row for row in crosswalk.get("merges", [])}
    print(f"{len(doc.get('clusters', []))} cluster(s) of town cards that might be one person")
    for cluster in doc.get("clusters", []):
        print(f"\n  {cluster['cluster_id']} — {len(cluster['cards'])} cards")
        for card in cluster["cards"]:
            mark = ("→ " + merges[card["person_id"]]["survivor_person_id"]
                    if card["person_id"] in merges else "kept")
            print(f"    {card['person_id']:28s} {card.get('name',''):34s} {mark}")
    for key in ("undecided", "deferred"):
        rows = crosswalk.get(key, [])
        if rows:
            print(f"\n  {len(rows)} {key}:")
            for row in rows:
                print(f"    {row['a']} against {row['b']}"
                      + (f"  → {row['to']}" if row.get("to") else ""))
    if gaps:
        print(f"\n  {len(gaps)} pair(s) NO RULING REACHES")
    return 0


def self_test() -> int:
    a = parse("Lieut. James Allen")
    b = parse("James Allen")
    c = parse("Lieut Allen")
    assert a == ("allen", ["james"], ["lieut"]), a
    assert c == ("allen", [], ["lieut"]), c
    assert compatible(a, b)[0], "a rank must not hold a forename apart from itself"
    assert not compatible(a, c)[0], "R1 must still refuse a name with no forename"
    assert compatible(parse("G S Hubbard"), parse("Gurdon S Hubbard"))[0]
    assert not compatible(parse("G S Hubbard"), parse("G T Hubbard"))[0], \
        "two middle initials that disagree are not one man"
    assert not compatible(parse("William Smith"), parse("Alonzo Smith"))[0]
    merges = {"x": {"survivor_person_id": "s"}, "y": {"survivor_person_id": "t"}}
    covered = ruled_pairs(merges, set(), set())
    assert frozenset(("x", "y")) in covered, \
        "two cards ruled onto different survivors have been ruled apart"
    assert frozenset(("x", "s")) in covered
    assert frozenset(("x", "z")) not in covered
    doc, gaps = coverage()
    assert doc.get("clusters"), "the candidates ledger is missing"
    print(f"   OK: the town-card consolidation's assertions hold "
          f"({len(doc['clusters'])} clusters, {len(gaps)} unruled pair(s))")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.candidates:
        CANDIDATES.write_text(dumps(build_candidates()), encoding="utf-8")
        print(f"wrote {CANDIDATES.relative_to(ROOT)}")
        return 0
    if args.apply:
        return apply()
    if args.check:
        return check()
    if args.gate:
        return gate()
    if args.report:
        return report()
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
