#!/usr/bin/env python3
"""One person, one card: the candidate ledger, the rulings, and the merge (T-0839).

    python3 tools/merge_resident_cards.py --candidates   rebuild the candidate ledger
    python3 tools/merge_resident_cards.py --apply        land every MERGE ruling
    python3 tools/merge_resident_cards.py --check        the gate (no writes)
    python3 tools/merge_resident_cards.py --self-test    the mechanics, on fixtures

THE FAULT. Each source pass minted the name the way its source printed it and no pass
asked whether the town already had the man. Lieut. James Allen, the harbour engineer,
stood on four cards: the one the ladder graded best knew nothing about the army, and the
one that knew his trade the ladder had never reached. Split, he was four thin men in a
town that counted 1,404 people it did not have.

THE CANDIDATE PASS is surname plus a COMPATIBLE forename, and nothing looser — the same
standard tools/name_agreement.py already writes for the directory crosswalks:

  * two full forenames agree by name_agreement.agrees (same, prefix, a printed
    contraction, or one letter apart at five letters or more);
  * an initial stands against a full name only when it is the SAME LETTER, in the same
    position, and every later initial finds a later token — "G. S." reaches Gurdon
    Saltonstall, "E. Kirby" does not reach Elded;
  * a card that prints a TITLE and no forename at all — "Lieut Allen", "Mrs Temple" —
    joins only cards carrying THE SAME TITLE. Without that guard one titled card chains
    every bearer of the surname into one cluster, which is how a first cut of this pass
    reported nine Smiths as one man.

A cluster is a WORKLIST, never a merge list. John H. and James Kinzie are brothers; Jean
Baptiste and John S. Beaubien are two men; the Temple cluster is a household. So every
cluster is RULED, in writing, in data/research/residents/merge_rulings.json, and the
ruling is what this tool acts on — MERGE lands here, DISTINCT is recorded so no later
pass re-asks, UNDECIDED goes to the owner with both readings.

A MERGE LOSES NOTHING, and that is the constraint the rest of the design serves:

  * the surviving card takes the UNION — sources, evidence blocks, the directories
    block, resident_research, kinship, the household's arrival/origin/lives_at/works_at
    blocks wherever the survivor's value is null and the folded card's is not;
  * the folded card is NOT deleted. It moves to data/residents/merged/<id>.json as a
    REDIRECT STUB carrying `merged_into`, the date, the ticket, the rule, the ruling's
    reasoning — and the whole original card, byte for byte, under `card_before_merge`.
    So the merge is reversible and no reading is thrown away;
  * data/residents/index.json gains a `merged` redirect table. Hundreds of committed
    files cite these person ids by hardcoded value — the crosswalks, identity_master,
    the newspaper register, the smoke cohorts — and rewriting all of them would put
    every one of those derived artifacts out of step with its own generator. The table
    is what makes them resolve instead, and --check is what holds it to that.

WHY THE STUBS LEAVE data/residents/households/. Twenty-odd tools glob that directory for
the town's people, and validate.py refuses a household with no persons. A stub left in
the households directory would therefore be read back as a person by every one of them,
which is the fault this ticket exists to end. The stub is kept, in full, one directory
across.

THE GRADE AFTER A MERGE IS THE LADDER'S, re-run — never the best of the folded grades.
This tool does not grade. It marks each survivor `regrade_pending` for
consolidate_resident_evidence.py --build and mint_civic_residents.py --regrade, and
--check reports how many survivors are still waiting.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import consolidate_resident_evidence as C          # noqa: E402  (split_name)
import name_agreement as NA                        # noqa: E402  (agrees)

HOUSEHOLDS = ROOT / "data/residents/households"
MERGED = ROOT / "data/residents/merged"
INDEX = ROOT / "data/residents/index.json"
CANDIDATES = ROOT / "data/research/residents/merge_candidates.json"
RULINGS = ROOT / "data/research/residents/merge_rulings.json"
TICKET = "T-0839"

# A title standing where a forename should be. HONORIFICS in the consolidation is the
# set the SPLITTER strips; these are the ones that survive into the forename tokens,
# because the town's cards print them as part of the name ("Lieut Allen").
TITLES = {"lieut", "lieutenant", "capt", "captain", "col", "colonel", "gen", "general",
          "maj", "major", "rev", "reverend", "dr", "doctor", "hon", "mr", "mrs", "miss",
          "widow", "sergt", "sgt", "lt", "esq", "mme", "madame", "judge", "elder",
          "deacon", "jun", "sen", "jr", "sr"}

RULINGS_ALLOWED = ("MERGE", "DISTINCT", "UNDECIDED", "DEFERRED")

# `none_recorded` is the vocabulary's word for "this card states no trade". It is a
# value, so a naive union reads it as one and refuses the trade the other card knows —
# which is exactly how Lieut. James Allen's `army_officer` failed to reach the card the
# ladder had graded.
NO_TRADE = (None, "", "none_recorded")


# --------------------------------------------------------------------------
# the candidate pass

def parse(name: str):
    """(surname, titles, forename tokens) for a town card's printed name, or None."""
    split = C.split_name(name or "")
    if not split:
        return None
    surname, given = split
    return surname, [t for t in given if t in TITLES], [t for t in given if t not in TITLES]


def _initials_reach(short: list[str], long: list[str]) -> bool:
    """Every initial finds a token, in order, starting at the first."""
    if not short or not long or short[0][0] != long[0][0]:
        return False
    i = 0
    for token in long:
        if i < len(short) and short[i][0] == token[0]:
            i += 1
    return i == len(short)


def compatible(a, b) -> tuple[bool, str]:
    """Do two parsed names name a person the other could be? (verdict, the rule)."""
    _, ta, ca = a
    _, tb, cb = b
    if not ca or not cb:
        shared = sorted(set(ta) & set(tb))
        if shared:
            return True, f"a title and no forename, against the same title ({shared[0]})"
        return False, "a title and no forename, and the other card carries no such title"
    if ca[0][0] != cb[0][0]:
        return False, "the forenames begin with different letters"
    full_a, full_b = len(ca[0]) > 1, len(cb[0]) > 1
    if full_a and full_b:
        ok, why = NA.agrees(ca[0], cb[0])
        return ok, f"two full forenames: {why}"
    # at least one side leads with an initial
    short, long = (ca, cb) if not full_a else (cb, ca)
    if not _initials_reach(short, long):
        return False, "an initial that no token of the other name answers, in order"
    rest_short = [t for t in short[1:] if len(t) > 1]
    rest_long = [t for t in long if len(t) > 1]
    if rest_short and rest_long:
        if not any(NA.agrees(x, y)[0] for x in rest_short for y in rest_long):
            return False, ("an initial leads, and the full names behind it disagree "
                           "(E. Kirby against Elded)")
    return True, "an initial reaching a full name"


def town_cards() -> list[dict]:
    rows = []
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        card = json.loads(path.read_text())
        for person in card.get("persons") or []:
            rows.append({"household_id": card["id"], "person_id": person.get("id"),
                         "name": person.get("name") or "", "card": card, "person": person})
    return rows


def clusters(rows: list[dict]) -> list[dict]:
    parsed = [(r, parse(r["name"])) for r in rows]
    by_surname: dict = {}
    for row, p in parsed:
        if p:
            by_surname.setdefault(p[0], []).append((row, p))
    out = []
    for surname, group in sorted(by_surname.items()):
        if len(group) < 2:
            continue
        parent = list(range(len(group)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        pairs: dict = {}
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                ok, why = compatible(group[i][1], group[j][1])
                if ok:
                    pairs[(group[i][0]["person_id"], group[j][0]["person_id"])] = why
                    parent[find(i)] = find(j)
        members: dict = {}
        for i in range(len(group)):
            members.setdefault(find(i), []).append(group[i][0])
        for root, member_rows in members.items():
            if len(member_rows) < 2:
                continue
            ids = sorted(r["person_id"] for r in member_rows)
            out.append({"id": f"mc_{surname}_{ids[0]}", "surname": surname,
                        "cards": member_rows,
                        "links": [{"pair": list(k), "rule": v} for k, v in sorted(pairs.items())
                                  if k[0] in set(ids) and k[1] in set(ids)]})
    out.sort(key=lambda c: (-len(c["cards"]), c["id"]))
    return out


def _sources_of(row) -> list:
    card, person = row["card"], row["person"]
    seen = list(person.get("sources") or [])
    for block in ("arrival", "origin", "lives_at", "works_at", "present_on_scene_date"):
        seen += list((card.get(block) or {}).get("sources") or [])
    seen += list((person.get("occupation") or {}).get("sources") or [])
    out = []
    for s in seen:
        if s not in out:
            out.append(s)
    return out


def _sketch(row) -> dict:
    card, person = row["card"], row["person"]
    return {
        "household_id": row["household_id"],
        "person_id": row["person_id"],
        "name": row["name"],
        "grade": person.get("grade"),
        "rung": person.get("ladder_rule"),
        "occupation": (person.get("occupation") or {}).get("value"),
        "sex": person.get("sex"),
        "division": card.get("division"),
        "arrival": (card.get("arrival") or {}).get("value"),
        "lives_at": (card.get("lives_at") or {}).get("value"),
        "works_at": (card.get("works_at") or {}).get("value"),
        "present": (card.get("present_on_scene_date") or {}).get("value"),
        "relationship": person.get("relationship"),
        "letter_list_only": bool(person.get("letter_list_only")),
        "civic_mint": bool(person.get("civic_mint")),
        "directories": len(card.get("directories") or []),
        "kin": len(card.get("kin") or []),
        "sources": _sources_of(row),
    }


def evidence(cluster) -> dict:
    """What speaks FOR one man and what speaks AGAINST, stated rather than scored."""
    sketches = [_sketch(r) for r in cluster["cards"]]
    for_, against = [], []
    shared = set(sketches[0]["sources"])
    for s in sketches[1:]:
        shared &= set(s["sources"])
    if shared:
        for_.append(f"every card cites {', '.join(sorted(shared))}")
    trades = {s["occupation"] for s in sketches if s["occupation"]}
    if len(trades) == 1 and sum(1 for s in sketches if s["occupation"]) > 1:
        for_.append(f"the trade agrees on every card that states one: {trades.pop()}")
    elif len(trades) > 1:
        against.append(f"the cards state different trades: {', '.join(sorted(trades))}")
    sexes = {s["sex"] for s in sketches if s["sex"]}
    if len(sexes) > 1:
        against.append(f"the cards state different sexes: {', '.join(sorted(sexes))}")
    seats = {s["lives_at"] for s in sketches if s["lives_at"]}
    if len(seats) > 1:
        against.append(f"the cards seat the household at different structures: "
                       f"{', '.join(sorted(seats))}")
    rels = {s["relationship"] for s in sketches if s["relationship"]}
    if rels - {"head"}:
        against.append(f"not every card's person is a head: {', '.join(sorted(rels))}")
    per_source: dict = {}
    for s in sketches:
        for src in s["sources"]:
            per_source.setdefault(src, []).append(s["person_id"])
    both = {k: v for k, v in per_source.items() if len(v) > 1}
    if both:
        against.append("one source prints more than one of these cards, which is a source "
                       "naming two people on one page unless the printings are the same "
                       "line: " + "; ".join(f"{k} -> {', '.join(v)}" for k, v in sorted(both.items())))
    return {"for": for_, "against": against, "cards": sketches}


def build_candidates() -> dict:
    rows = town_cards()
    found = clusters(rows)
    rulings = load_rulings()
    doc = {
        "schema": "chicago4d.residents.merge_candidates.v1",
        "_doc": ("Surname plus a compatible forename over every person in "
                 "data/residents/households/. A WORKLIST, not a merge list: the ruling "
                 "for each cluster is in merge_rulings.json and the merge itself is "
                 "landed by tools/merge_resident_cards.py --apply."),
        "generated_by": "tools/merge_resident_cards.py --candidates",
        "ticket": TICKET,
        "counts": {
            "town_persons": len(rows),
            "clusters": len(found),
            "cards_in_clusters": sum(len(c["cards"]) for c in found),
        },
        "clusters": [],
    }
    for c in found:
        ruling = rulings.get(c["id"]) or {}
        doc["clusters"].append({
            "id": c["id"],
            "surname": c["surname"],
            "person_ids": sorted(r["person_id"] for r in c["cards"]),
            "links": c["links"],
            "evidence": evidence(c),
            "ruling": ruling.get("ruling"),
            "why": ruling.get("why"),
        })
    return doc


# --------------------------------------------------------------------------
# the rulings, and the merge

def load_rulings() -> dict:
    if not RULINGS.exists():
        return {}
    doc = json.loads(RULINGS.read_text())
    return {r["cluster"]: r for r in doc.get("rulings", [])}


def _union_list(a, b):
    out = list(a or [])
    for item in b or []:
        if item not in out:
            out.append(item)
    return out


BLOCK_KEYS = ("arrival", "party_size_on_arrival", "origin", "reason_for_coming",
              "lives_at", "works_at", "present_on_scene_date")

LIST_PERSON_KEYS = ("press_evidence", "civic_evidence", "book_evidence", "church_evidence",
                    "census_evidence", "biographical_evidence", "later_census",
                    "letter_list_returns", "resident_research")

# `ladder_rule` and `resident_subtype` are DELIBERATELY ABSENT. They are the ladder's
# own verdict on a card, and carrying one off a folded card onto a survivor the ladder
# graded differently is how a merge produces "4 projected residents are not inferred" —
# a projected-resident subtype riding onto an attested man. The grade after a merge is
# the ladder's, re-run; this tool never writes one.
SCALAR_PERSON_KEYS = ("sex", "birth_year", "age_on_scene_date")


def merge_person(survivor: dict, folded: dict, notes: list) -> None:
    survivor["sources"] = _union_list(survivor.get("sources"), folded.get("sources"))
    s_occ, f_occ = survivor.get("occupation") or {}, folded.get("occupation") or {}
    if s_occ.get("value") in NO_TRADE and f_occ.get("value") not in NO_TRADE:
        survivor["occupation"] = json.loads(json.dumps(f_occ))
        notes.append(f"the trade `{f_occ['value']}` comes from {folded['id']}, whose card "
                     f"stated it and whose grade the ladder had not reached")
    elif s_occ.get("value") not in NO_TRADE and f_occ.get("value") == s_occ.get("value"):
        s_occ["sources"] = _union_list(s_occ.get("sources"), f_occ.get("sources"))
    for key in LIST_PERSON_KEYS:
        if key in folded:
            merged = _union_list(survivor.get(key), folded.get(key))
            if merged:
                survivor[key] = merged
    for key in SCALAR_PERSON_KEYS:
        if survivor.get(key) in (None, "") and folded.get(key) not in (None, ""):
            survivor[key] = folded[key]
            notes.append(f"`{key}` comes from {folded['id']}")
    if folded.get("civic_mint"):
        survivor["civic_mint"] = True
    if "letter_list_only" in survivor or "letter_list_only" in folded:
        # A person the letter list is not the ONLY witness for is not letter-list-only.
        survivor["letter_list_only"] = bool(survivor.get("letter_list_only")) and \
            bool(folded.get("letter_list_only"))


def merge_household(survivor: dict, folded: dict, notes: list) -> None:
    for key in BLOCK_KEYS:
        s, f = survivor.get(key) or {}, folded.get(key) or {}
        if not isinstance(s, dict) or not isinstance(f, dict):
            continue
        if s.get("value") in (None, "") and f.get("value") not in (None, ""):
            survivor[key] = json.loads(json.dumps(f))
            notes.append(f"`{key}` = {f.get('value')!r} comes from {folded['id']}")
        elif key == "present_on_scene_date" and s.get("value") == "uncertain" \
                and f.get("value") == "present":
            survivor[key] = json.loads(json.dumps(f))
            notes.append("`present_on_scene_date` rises to `present` on "
                         f"{folded['id']}'s evidence")
        elif s.get("value") == f.get("value"):
            s["sources"] = _union_list(s.get("sources"), f.get("sources"))
    if survivor.get("division") == "unplaced" and folded.get("division") not in (None, "unplaced"):
        survivor["division"] = folded["division"]
        notes.append(f"the division comes from {folded['id']}")
    if folded.get("directories"):
        survivor["directories"] = _union_list(survivor.get("directories"),
                                              folded.get("directories"))
    if folded.get("kin"):
        survivor["kin"] = _union_list(survivor.get("kin"), folded.get("kin"))
    if folded.get("touches_removal"):
        survivor["touches_removal"] = True


def stub_for(folded_card: dict, survivor_card: dict, survivor_person: str,
             folded_person: str, ruling: dict, today: str) -> dict:
    return {
        "schema": "chicago4d.residents.merged_card.v1",
        "id": folded_card["id"],
        "merged_into": survivor_card["id"],
        "person_merged_into": survivor_person,
        "person_id": folded_person,
        "name_as_minted": folded_card.get("name"),
        "merged_on": today,
        "ticket": TICKET,
        "rule": ruling.get("rule") or "surname plus a compatible forename, ruled MERGE",
        "why": ruling.get("why"),
        "_doc": ("A REDIRECT, NOT A DELETION. This card was folded into "
                 f"{survivor_card['id']} because the two named one person. Every file "
                 "that cites the ids above still resolves, through the `merged` table in "
                 "data/residents/index.json. The whole card as it stood before the merge "
                 "is kept below, so the merge can be read back and undone."),
        "card_before_merge": folded_card,
    }


def _accounted(cluster_ids: set, ruling: dict) -> set:
    """Every card a ruling speaks for: the survivor, the folded, the held apart."""
    named = set()
    if ruling.get("survivor"):
        named.add(ruling["survivor"])
    named |= set(ruling.get("folded") or [])
    named |= {h["person_id"] for h in ruling.get("held_apart") or []}
    return cluster_ids - named


def write_held_apart(cards: dict, rows: dict, ruling: dict, today: str,
                     problems: list) -> int:
    """A refusal is written onto the card, so the next pass does not re-ask (T-0839)."""
    written = 0
    for held in ruling.get("held_apart") or []:
        pid, verdict = held.get("person_id"), held.get("ruling")
        if verdict not in ("DISTINCT", "UNDECIDED", "DEFERRED"):
            problems.append(f"{ruling['cluster']}: held_apart {pid!r} carries ruling "
                            f"{verdict!r}, which is not DISTINCT, UNDECIDED or DEFERRED")
            continue
        if not (held.get("why") or "").strip():
            problems.append(f"{ruling['cluster']}: held_apart {pid!r} owes its reasoning")
            continue
        if pid not in rows:
            problems.append(f"{ruling['cluster']}: held_apart {pid!r} is not a town person")
            continue
        if held.get("defer_write"):
            continue
        card = cards[rows[pid]["household_id"]]
        person = next(p for p in card["persons"] if p["id"] == pid)
        # `reasoning`, not `why`: tools/measure_layer_reads.py scans the renderers for a
        # BARE LEAF NAME, and `.why` is already read there (ground.js's not-modelled
        # zones), so a figure called `why` on a resident card would be counted as read by
        # a renderer that never sees it. The word the card carries is its own.
        row = {"ticket": TICKET, "on": today, "ruling": verdict,
               "against": [x for x in held.get("against") or [] if x != pid],
               "reasoning": held["why"]}
        existing = [r for r in person.get("identity_rulings") or []
                    if not (r.get("ticket") == TICKET and r.get("ruling") == verdict
                            and r.get("against") == row["against"])]
        person["identity_rulings"] = existing + [row]
        written += 1
    return written


def apply_rulings(write=True, refusals_only=False) -> int:
    rows = {r["person_id"]: r for r in town_cards()}
    found = {c["id"]: c for c in clusters(list(rows.values()))}
    rulings = load_rulings()
    today = date.today().isoformat()
    problems, landed, redirects = [], [], []
    cards: dict = {}
    for path in HOUSEHOLDS.glob("*.json"):
        cards[path.stem] = json.loads(path.read_text())

    for cid, ruling in sorted(rulings.items()):
        if ruling.get("ruling") not in RULINGS_ALLOWED:
            problems.append(f"{cid}: ruling {ruling.get('ruling')!r} is not one of "
                            f"{RULINGS_ALLOWED}")
            continue
        if not (ruling.get("why") or "").strip():
            problems.append(f"{cid}: a ruling owes its reasoning")
        cluster_ids = {r["person_id"] for r in (found.get(cid) or {}).get("cards", [])}
        loose = _accounted(cluster_ids, ruling)
        if loose:
            problems.append(f"{cid}: {', '.join(sorted(loose))} stand in this cluster and "
                            f"the ruling does not speak for them. Every card is the "
                            f"survivor, folded, or held apart with a reason")
        held_written = write_held_apart(cards, rows, ruling, today, problems)
        if ruling["ruling"] != "MERGE" or refusals_only:
            if write and held_written:
                for held in ruling.get("held_apart") or []:
                    pid = held.get("person_id")
                    if pid in rows and not held.get("defer_write"):
                        card = cards[rows[pid]["household_id"]]
                        (HOUSEHOLDS / f"{card['id']}.json").write_text(
                            json.dumps(card, indent=1, ensure_ascii=False) + "\n")
            continue
        survivor_pid = ruling.get("survivor")
        if survivor_pid not in rows:
            problems.append(f"{cid}: survivor {survivor_pid!r} is not a town person")
            continue
        survivor_card = cards[rows[survivor_pid]["household_id"]]
        survivor_person = next(p for p in survivor_card["persons"] if p["id"] == survivor_pid)
        notes: list = []
        if ruling.get("survivor_name") and survivor_person["name"] != ruling["survivor_name"]:
            notes.append(f"the name rises from {survivor_person['name']!r} to "
                         f"{ruling['survivor_name']!r}, which is the fullest reading the "
                         f"folded cards carry")
            survivor_person["name"] = ruling["survivor_name"]
        for folded_pid in ruling.get("folded") or []:
            if folded_pid not in rows:
                problems.append(f"{cid}: folded {folded_pid!r} is not a town person")
                continue
            folded_hid = rows[folded_pid]["household_id"]
            folded_card = cards[folded_hid]
            if len(folded_card.get("persons") or []) != 1:
                problems.append(f"{cid}: {folded_hid} holds more than one person; a "
                                f"multi-person card is not folded by this tool")
                continue
            folded_person = folded_card["persons"][0]
            merge_person(survivor_person, folded_person, notes)
            if len(survivor_card.get("persons") or []) == 1:
                merge_household(survivor_card, folded_card, notes)
            else:
                notes.append(
                    f"the household blocks of {folded_hid} were NOT unioned: "
                    f"{survivor_card['id']} holds other people, and an arrival or a "
                    f"dwelling carried onto a shared card would be claimed for them too. "
                    f"They stand, whole, in the stub")
            survivor_person["also_known_as"] = _union_list(
                survivor_person.get("also_known_as"), [folded_person.get("name")])
            survivor_card["merged_from"] = _union_list(survivor_card.get("merged_from"), [{
                "household_id": folded_hid, "person_id": folded_pid,
                "name": folded_person.get("name"), "merged_on": today, "ticket": TICKET,
            }])
            redirects.append({"household_id": folded_hid, "person_id": folded_pid,
                              "merged_into": survivor_card["id"],
                              "person_merged_into": survivor_pid,
                              "name_as_minted": folded_person.get("name"),
                              "merged_on": today, "ticket": TICKET,
                              "stub": f"merged/{folded_hid}.json"})
            if write:
                MERGED.mkdir(parents=True, exist_ok=True)
                stub = stub_for(folded_card, survivor_card, survivor_pid, folded_pid,
                                ruling, today)
                (MERGED / f"{folded_hid}.json").write_text(
                    json.dumps(stub, indent=1, ensure_ascii=False) + "\n")
                (HOUSEHOLDS / f"{folded_hid}.json").unlink()
            cards.pop(folded_hid, None)
        if notes:
            survivor_card["research_note"] = (
                survivor_card.get("research_note", "").rstrip()
                + f" MERGED UNDER {TICKET} ON {today}: this card absorbed "
                + ", ".join(f"`{f['person_id']}`" for f in survivor_card["merged_from"])
                + ". " + ruling["why"].strip()
                + " The union carried: " + "; ".join(notes)
                + ". THE GRADE IS NOT THE BEST OF THE FOLDED GRADES — it is the ladder's, "
                  "and it is re-derived by consolidate_resident_evidence.py --build and "
                  "mint_civic_residents.py --regrade; `regrade_pending` says so until it "
                  "has been. Every folded card is kept whole at data/residents/merged/, "
                  "and the redirect table in index.json is what makes the ids the "
                  "crosswalks cite still resolve.")
            survivor_card["regrade_pending"] = True
        landed.append({"cluster": cid, "survivor": survivor_pid,
                       "folded": list(ruling.get("folded") or [])})
        if write:
            for held in ruling.get("held_apart") or []:
                pid = held.get("person_id")
                if pid in rows and not held.get("defer_write"):
                    other = cards[rows[pid]["household_id"]]
                    (HOUSEHOLDS / f"{other['id']}.json").write_text(
                        json.dumps(other, indent=1, ensure_ascii=False) + "\n")
            (HOUSEHOLDS / f"{survivor_card['id']}.json").write_text(
                json.dumps(survivor_card, indent=1, ensure_ascii=False) + "\n")

    for cid in sorted(found):
        if cid not in rulings and cid not in {r["cluster"] for r in landed}:
            problems.append(f"{cid}: a candidate cluster with no written ruling")

    if write and redirects:
        rewrite_index(redirects, today)
    for p in problems:
        print(f"  ! {p}")
    print(f"merge: {len(landed)} cluster(s) ruled MERGE, {len(redirects)} card(s) folded, "
          f"{len(problems)} problem(s)")
    return 1 if problems else 0


def rewrite_index(redirects: list, today: str) -> None:
    index = json.loads(INDEX.read_text())
    folded_hids = {r["household_id"] for r in redirects}
    survivors = {r["merged_into"] for r in redirects}
    index["households"] = [h for h in index["households"] if h["id"] not in folded_hids]
    cards = {p.stem: json.loads(p.read_text()) for p in HOUSEHOLDS.glob("*.json")}
    for row in index["households"]:
        if row["id"] not in survivors:
            continue
        card = cards[row["id"]]
        grades: dict = {}
        for person in card["persons"]:
            grades[person["grade"]] = grades.get(person["grade"], 0) + 1
        row["persons"] = len(card["persons"])
        row["grades"] = grades
        row["division"] = card.get("division")
        row["lives_at"] = (card.get("lives_at") or {}).get("value")
        row["works_at"] = (card.get("works_at") or {}).get("value")
        row["present_on_scene_date"] = (card.get("present_on_scene_date") or {}).get("value")
        if "letter_list_only" in row:
            row["letter_list_only"] = all(p.get("letter_list_only")
                                          for p in card["persons"])
        if "projected_resident" in row:
            row["projected_resident"] = any(
                p.get("resident_subtype") == "projected_resident" for p in card["persons"])
    totals: dict = {"attested": 0, "inferred": 0, "reconstructed": 0}
    persons = 0
    for row in index["households"]:
        persons += row["persons"]
        for grade, n in (row.get("grades") or {}).items():
            totals[grade] = totals.get(grade, 0) + n
    index["counts"]["households"] = len(index["households"])
    index["counts"]["persons"] = persons
    index["counts"]["by_grade"] = totals
    index["counts"]["letter_list_only"] = sum(1 for r in index["households"]
                                              if r.get("letter_list_only"))
    index["counts"]["projected_residents"] = sum(1 for r in index["households"]
                                                 if r.get("projected_resident"))
    index["counts"]["merged_away"] = len(redirects)
    index["merged"] = sorted(redirects, key=lambda r: r["person_id"])
    index["_merged_doc"] = (
        "THE REDIRECT TABLE (T-0839). One person stood on several cards, and the merge "
        "left these ids behind. They are not dead: hundreds of committed files — the "
        "crosswalks, data/research/residents/identity_master.json, the newspaper "
        "register, the smoke cohorts — cite them by hardcoded value, and rewriting all "
        "of them would put every one of those derived artifacts out of step with the "
        "generator that wrote it. A reader that meets one of these ids resolves it "
        "here. The folded card itself is kept whole at data/residents/merged/.")
    INDEX.write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------
# the gate

def check() -> int:
    problems: list = []
    pending: list = []
    rows = {r["person_id"]: r for r in town_cards()}
    found = clusters(list(rows.values()))
    rulings = load_rulings()
    for c in found:
        ruling = rulings.get(c["id"])
        if not ruling:
            problems.append(f"{c['id']} ({', '.join(r['name'] for r in c['cards'])}): a "
                            f"candidate cluster with no written ruling. Every cluster is "
                            f"ruled MERGE, DISTINCT, UNDECIDED or DEFERRED in "
                            f"data/research/residents/merge_rulings.json")
            continue
        cluster_ids = {r["person_id"] for r in c["cards"]}
        loose = _accounted(cluster_ids, ruling)
        if loose:
            problems.append(f"{c['id']}: {', '.join(sorted(loose))} stand in this cluster "
                            f"and the ruling does not speak for them")
        if ruling.get("ruling") == "MERGE" and set(ruling.get("folded") or []) & cluster_ids:
            pending.append(c["id"])
        for held in ruling.get("held_apart") or []:
            if held.get("defer_write") or held["person_id"] not in rows:
                continue
            if c["id"] in pending:
                continue      # the fold has not landed; the write lands with it
            person = rows[held["person_id"]]["person"]
            if not any(r.get("ticket") == TICKET
                       for r in person.get("identity_rulings") or []):
                problems.append(f"{c['id']}: {held['person_id']} is held apart and the "
                                f"card does not carry the ruling, so the next pass "
                                f"re-asks")
    index = json.loads(INDEX.read_text())
    listed = {h["id"] for h in index.get("households", [])}
    for entry in index.get("merged", []):
        stub = ROOT / "data/residents" / entry["stub"]
        if not stub.exists():
            problems.append(f"{entry['person_id']}: the redirect names {entry['stub']}, "
                            f"which does not exist")
        if entry["merged_into"] not in listed:
            problems.append(f"{entry['person_id']}: redirects to {entry['merged_into']}, "
                            f"which is not a household in the index")
        if entry["household_id"] in listed:
            problems.append(f"{entry['household_id']}: folded and still in the index")
        if entry["person_merged_into"] not in rows:
            problems.append(f"{entry['person_id']}: redirects to person "
                            f"{entry['person_merged_into']}, who is not a town person")
    for path in MERGED.glob("*.json"):
        stub = json.loads(path.read_text())
        if stub.get("schema") != "chicago4d.residents.merged_card.v1":
            problems.append(f"data/residents/merged/{path.name} is not a redirect stub")
        if not stub.get("card_before_merge"):
            problems.append(f"data/residents/merged/{path.name} kept no card: a merge "
                            f"that loses the folded reading is not reversible")
        if stub.get("id") not in {e["household_id"] for e in index.get("merged", [])}:
            problems.append(f"data/residents/merged/{path.name} is in no redirect table")
    regrade = sum(1 for r in rows.values() if r["card"].get("regrade_pending"))
    for p in problems:
        print(f"  ! {p}")
    if pending:
        print(f"  … {len(pending)} cluster(s) ruled MERGE and not yet folded, which is "
              f"T-0842's piece of T-0839 — the ruling stands, the cards have not moved "
              f"yet: {', '.join(sorted(pending))}")
    print(f"merge gate: {len(found)} candidate cluster(s), "
          f"{len(index.get('merged', []))} card(s) folded, {len(pending)} ruled MERGE and "
          f"not yet landed, {regrade} survivor(s) awaiting the ladder's regrade, "
          f"{len(problems)} problem(s)")
    return 1 if problems else 0


# --------------------------------------------------------------------------

def self_test() -> int:
    fails = []

    def eq(got, want, what):
        if got != want:
            fails.append(f"{what}: {got!r} != {want!r}")

    # the compatibility rule
    eq(compatible(parse("Gurdon S Hubbard"), parse("Gurdon Saltonstall Hubbard"))[0],
       True, "a full forename against itself")
    eq(compatible(parse("G S Hubbard"), parse("Gurdon Saltonstall Hubbard"))[0],
       True, "initials reaching the tokens they stand for")
    eq(compatible(parse("E Kirby Smith"), parse("Elded Smith"))[0],
       False, "an initial leads and the full names behind it disagree")
    eq(compatible(parse("Lieut Allen"), parse("Lieut. James Allen"))[0],
       True, "a title and no forename, against the same title")
    eq(compatible(parse("Lieut Allen"), parse("William Allen"))[0],
       False, "a title must not chain a whole surname")
    eq(compatible(parse("James Kinzie"), parse("John Harris Kinzie"))[0],
       False, "two brothers are not one man")
    eq(compatible(parse("Th J V Owen"), parse("Thomas Jefferson Vance Owen"))[0],
       True, "a printed contraction")

    # the union, on fixtures
    survivor = {"id": "a", "name": "A", "relationship": "head", "grade": "attested",
                "occupation": {"value": None, "confidence": "reconstructed"},
                "sources": ["s1"], "note": "", "letter_list_only": True}
    folded = {"id": "b", "name": "B", "relationship": "head", "grade": "inferred",
              "occupation": {"value": "army_officer", "confidence": "attested",
                             "sources": ["s2"]},
              "sources": ["s2"], "note": "", "letter_list_only": False, "sex": "male"}
    notes: list = []
    merge_person(survivor, folded, notes)
    eq(survivor["sources"], ["s1", "s2"], "sources are unioned")
    eq(survivor["occupation"]["value"], "army_officer", "a stated trade beats a null one")
    eq(survivor["sex"], "male", "a scalar the survivor lacked is carried over")
    eq(survivor["letter_list_only"], False,
       "a person the letter list is not the only witness for is not letter-list-only")
    eq(survivor["grade"], "attested",
       "the merge does not grade — that is the ladder's, re-run")

    hs = {"id": "ha", "division": "unplaced",
          "arrival": {"value": None}, "lives_at": {"value": None},
          "present_on_scene_date": {"value": "uncertain"}}
    hf = {"id": "hb", "division": "north", "arrival": {"value": "1834-08-13",
          "sources": ["s2"]}, "lives_at": {"value": None},
          "present_on_scene_date": {"value": "present"}, "directories": [{"d": 1}]}
    notes = []
    merge_household(hs, hf, notes)
    eq(hs["arrival"]["value"], "1834-08-13", "a stated arrival beats a null one")
    eq(hs["division"], "north", "a placed division beats unplaced")
    eq(hs["present_on_scene_date"]["value"], "present", "presence rises on evidence")
    eq(hs["directories"], [{"d": 1}], "the directories block is carried over")

    for f in fails:
        print(f"  ! {f}")
    print(f"self-test: {len(fails)} failure(s)")
    return 1 if fails else 0


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if arg == "--candidates":
        doc = build_candidates()
        CANDIDATES.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print(f"{CANDIDATES.relative_to(ROOT)}: {doc['counts']['clusters']} cluster(s), "
              f"{doc['counts']['cards_in_clusters']} card(s), "
              f"{doc['counts']['town_persons']} town persons")
        return 0
    if arg == "--apply":
        return apply_rulings(write=True)
    if arg == "--apply-refusals":
        # The refusals alone: DISTINCT and UNDECIDED written onto the cards they speak
        # for, with no card folded. That is T-0841's half of the sweep — a refusal has
        # to reach the record or the next pass re-asks the same question.
        return apply_rulings(write=True, refusals_only=True)
    if arg == "--check":
        return check()
    if arg == "--self-test":
        return self_test()
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
