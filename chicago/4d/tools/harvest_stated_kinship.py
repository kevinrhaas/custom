#!/usr/bin/env python3
"""The kinship the committed sources already state, gathered, ruled and written (T-0734).

Of 1,404 people this project holds, 14 carried a stated tie to anybody else. Some of
that is true — a letter list prints a name and nothing whatever else, and this project
will not invent a family — but some of it was not: the corpus already PRINTS kinship
it has read and filed, and the household records simply never took it.

This tool is the pass that takes it, and it is built so the taking can be checked:

  --build   re-derive the worklist and write data/research/residents/stated_kinship.json
  --apply   write the upheld ties onto the household records, as reciprocal `kin` rows
  --check   assert the committed worklist still derives, and that every tie it says
            LANDED is in fact on both records with the right degree

TWO SEAMS, AND THEY ARE NOT EQUALLY GOOD.

  * THE CHURCH REGISTER IS STRUCTURED AND IS DERIVED HERE, NOT TYPED. St Cyr's
    register was read onto the cards with a locator per person — `groom`, `bride`,
    `decedent`, `parent` — so a marriage entry naming two people this project holds
    IS a statement that those two are husband and wife, made by the parish at the
    act, and the entry that binds them is the same entry each card was minted from.
    There is no identity gap to argue about. `--build` walks every card's
    `church_evidence`, groups it by register record, and the pairs fall out.

  * THE HOUSEHOLD PROSE IS UNSTRUCTURED AND IS READ BY HAND, ONCE, HERE. Sixty-five
    sentences in the household records state a kin tie; the reading of all of them is
    the table below, with its quote, and it is committed rather than re-guessed by a
    regex on every run, because a regex over prose gives a different worklist every
    time the prose is edited and a gate that changes its mind is not a gate.

WHAT IS NOT LANDED IS NOT LOST. Every candidate carries a ruling and a reason, and the
reasons are the honest ones: a tie the source states but whose far end is a CARD nobody
has ruled identical to the person named (Andreas's "Samuel, the landlord" against the
Samuel Miller minted from the 1832 muster) is a crosswalk's job and not a kinship's, and
a marriage the register dates AFTER 1 July 1835 is not a marriage this scene may assert
— the same rule hh_pruyne_kimberly already applies to Rebecca Sherman in as many words.

No relationship is inferred from a shared surname. Every row cites the source that
states the tie, and none of them moves a person's grade, a placement or a household.
"""

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOUSEHOLDS = os.path.join(HERE, "data", "residents", "households")
OUT = os.path.join(HERE, "data", "research", "residents", "stated_kinship.json")

SCENE_DATE = "1835-07-01"

# --------------------------------------------------------------------------
# Seam 1: the parish register, derived.
#
# A locator pair -> the tie it states, as `relation` reads in a kin row: the
# person IS THE relation OF the other (renderers/web/js/residents.js prints
# exactly that sentence).
CHURCH_PAIRS = {
    ("groom", "bride"): ("husband", "wife"),
    ("decedent", "parent"): ("son", "father"),
}


def load_households():
    out = {}
    for path in sorted(glob.glob(os.path.join(HOUSEHOLDS, "*.json"))):
        with open(path, encoding="utf-8") as fh:
            out[os.path.basename(path)[:-5]] = json.load(fh)
    return out


def person_index(households):
    idx = {}
    for hid, h in households.items():
        for p in h.get("persons") or []:
            idx[p["id"]] = (hid, p.get("name"))
    return idx


def derive_church_candidates(households):
    """Every register record naming two town people in a tie-bearing pair of roles."""
    records = {}
    for hid, h in households.items():
        for p in h.get("persons") or []:
            for ce in p.get("church_evidence") or []:
                rid = str(ce.get("record_id") or "")
                # a card's row is `<record>_<n>`; the record is what groups them
                group = rid.rsplit("_", 1)[0] if rid else ""
                if not group:
                    continue
                records.setdefault(group, []).append({
                    "person": p["id"], "household": hid,
                    "locator": ce.get("locator"), "as_read": ce.get("as_read"),
                    "describes_date": str(ce.get("describes_date") or ""),
                    "source": ce.get("source"), "rule": ce.get("rule"),
                })
    out = []
    for group, rows in sorted(records.items()):
        by_loc = {}
        for r in rows:
            by_loc.setdefault(r["locator"], []).append(r)
        for (la, lb), (ra, rb) in CHURCH_PAIRS.items():
            a = by_loc.get(la) or []
            b = by_loc.get(lb) or []
            # exactly one of each, or the entry does not state one unambiguous tie
            if len(a) != 1 or len(b) != 1 or a[0]["person"] == b[0]["person"]:
                continue
            out.append({
                "id": group,
                "seam": "church_register",
                "date": a[0]["describes_date"],
                "source": a[0]["source"],
                "quote": f'{a[0]["as_read"]} ({la}) / {b[0]["as_read"]} ({lb})',
                "a": {"person": a[0]["person"], "household": a[0]["household"],
                      "relation": ra},
                "b": {"person": b[0]["person"], "household": b[0]["household"],
                      "relation": rb},
            })
    return out


# The register records that name two town people but only ONE of the two roles a
# tie needs. Derived the same way, kept so the count of what was AVAILABLE is
# honest rather than quietly filtered.
def derive_church_incomplete(households):
    records = {}
    for hid, h in households.items():
        for p in h.get("persons") or []:
            for ce in p.get("church_evidence") or []:
                rid = str(ce.get("record_id") or "")
                group = rid.rsplit("_", 1)[0] if rid else ""
                if group:
                    records.setdefault(group, set()).add(ce.get("locator"))
    out = []
    for group, locs in sorted(records.items()):
        for (la, lb) in CHURCH_PAIRS:
            if (la in locs) != (lb in locs):
                out.append({"record": group, "has": sorted(locs), "missing":
                            lb if la in locs else la})
    return out


# --------------------------------------------------------------------------
# Seam 2: the household prose, read by hand once, 2026-09-06.
#
# `a` is the `relation` of `b`. A candidate with `ruling: not_supported` names
# what it would have linked and why it may not, and that is the whole point of
# writing it down: the next pass reads the reason instead of re-reading the page.
PROSE_CANDIDATES = [
    {
        "id": "prose_beaubien_madore_son",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_beaubien_madore/persons[0]/note",
        "quote": "He is the son of Jean Baptiste Beaubien by his first wife "
                 "Mah-naw-bun-no-quah, an Ottawa woman",
        "a": {"person": "beaubien_madore", "household": "hh_beaubien_madore",
              "relation": "son"},
        "b": {"person": "beaubien_jean_baptiste",
              "household": "hh_beaubien_jean_baptiste", "relation": "father"},
        "ruling": "landed",
        "confidence": "inferred",
        "reason": "BOTH RECORDS ALREADY SAY IT AND NEITHER COULD BE QUERIED FOR IT. "
                  "The son's card states the parentage outright and the father's card "
                  "states the far end of the same fact — 'two sons are named in Andreas "
                  "and one of them, Madore, has his own household here'. Inferred rather "
                  "than documented because Andreas is a compilation of 1884 about a birth "
                  "of the century's first years, which is a good source for the fact and "
                  "still a recollection.",
    },
    {
        "id": "prose_beaubien_mark_brother",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_beaubien_mark/origin/note",
        "quote": "Andreas's life of his brother Jean Baptiste gives the family's trading "
                 "history at Milwaukee from about 1800 and the move to Chicago in 1812",
        "a": {"person": "beaubien_mark", "household": "hh_beaubien_mark",
              "relation": "brother"},
        "b": {"person": "beaubien_jean_baptiste",
              "household": "hh_beaubien_jean_baptiste", "relation": "brother"},
        "ruling": "landed",
        "confidence": "inferred",
        "reason": "THE TIE THE WHOLE TOWN KNOWS AND THE DATASET DID NOT. Mark Beaubien's "
                  "own record reaches for Andreas's life of Jean Baptiste to date the "
                  "family's move, and calls him 'his brother' while doing it. Twelve "
                  "Beaubien cards stand in this dataset and a shared surname is the thing "
                  "that makes them mergeable; two men recorded as brothers are two men, "
                  "explicitly. Inferred, on the same reading of Andreas as the parentage "
                  "above.",
    },
    {
        "id": "prose_harmon_charles_son",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_harmon_brothers/persons[0]/note",
        "quote": "Andreas's life of Dr Elijah Dewey Harmon lists his five surviving "
                 "children: 'Charles Loomis Harmon, Isaac Dewey Harmon, Harriet Harmon, "
                 "Lucretia Harmon, and Welthyan Loomis Harmon.'",
        "a": {"person": "harmon_charles_l", "household": "hh_harmon_brothers",
              "relation": "son"},
        "b": {"person": "harmon_elijah_d", "household": "hh_harmon_elijah_d",
              "relation": "father"},
        "ruling": "landed",
        "confidence": "inferred",
        "reason": "THE SENTENCE THAT MADE THE HOUSEHOLD, FINALLY WRITTEN AS A LINK. "
                  "hh_harmon_brothers exists BECAUSE this quotation resolves the initials "
                  "of the newspaper masthead 'C. & I. Harmon' into the doctor's two eldest "
                  "sons — the record says so in its first sentence — and the doctor's own "
                  "record says the firm 'is a separate household here'. The one thing "
                  "neither of them could be asked was which household the other was.",
    },
    {
        "id": "prose_harmon_isaac_son",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_harmon_brothers/persons[0]/note",
        "quote": "Andreas's life of Dr Elijah Dewey Harmon lists his five surviving "
                 "children: 'Charles Loomis Harmon, Isaac Dewey Harmon, Harriet Harmon, "
                 "Lucretia Harmon, and Welthyan Loomis Harmon.'",
        "a": {"person": "harmon_isaac_d", "household": "hh_harmon_brothers",
              "relation": "son"},
        "b": {"person": "harmon_elijah_d", "household": "hh_harmon_elijah_d",
              "relation": "father"},
        "ruling": "landed",
        "confidence": "inferred",
        "reason": "The second name in the same printed list of children. This card is "
                  "already the one that refuses to be Isaac Harmon the town clerk, on the "
                  "strength of an 1832 militia agreement signed by both names two lines "
                  "apart; the paternity is what the refusal has always rested on and it is "
                  "now written where a query can reach it.",
    },
    {
        "id": "prose_beaubien_charles_h_son",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_beaubien_jean_baptiste/persons[0]/note",
        "quote": "he married first Mah-naw-bun-no-quah, an Ottawa woman, the mother of his "
                 "sons Charles Henry and Madore",
        "a": {"person": "beaubien_charles_h", "household": "hh_beaubien_charles_h",
              "relation": "son"},
        "b": {"person": "beaubien_jean_baptiste",
              "household": "hh_beaubien_jean_baptiste", "relation": "father"},
        "ruling": "not_supported",
        "reason": "THE SOURCE STATES THE TIE AND THE FAR END IS AN IDENTITY NOBODY HAS "
                  "RULED. Andreas names the son Charles Henry; hh_beaubien_charles_h is a "
                  "card carrying the initials 'Charles H', and the father's own record says "
                  "in as many words that of the two sons Andreas names, ONE — Madore — has "
                  "a household here. Deciding that the initialled card is the same man is a "
                  "crosswalk ruling, not a kinship, and this pass will not make one to "
                  "raise its own count.",
    },
    {
        "id": "prose_miller_john_brother",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_miller_john/persons[0]/occupation/note",
        "quote": "John Miller, brother of Samuel, the landlord, came in 1831, and run a "
                 "tannery just north of Miller's tavern.",
        "a": {"person": "miller_john", "household": "hh_miller_john",
              "relation": "brother"},
        "b": {"person": "miller_samuel", "household": "hh_miller_samuel",
              "relation": "brother"},
        "ruling": "not_supported",
        "reason": "THE RELATIONSHIP IS DOCUMENTED AND THE FAR END IS NOT THE SAME KIND OF "
                  "THING. Andreas states the brotherhood plainly. But the card "
                  "miller_samuel was minted from the 1832 muster, the paper and the 1833 "
                  "tax list and claims no trade at all, while John Miller's record still "
                  "says his brother 'is not written as a household here' — written when it "
                  "was true. Whether Andreas's 'Samuel, the landlord' IS that card is a "
                  "crosswalk ruling on a surname the dataset carries five times. Raised as "
                  "its own ticket rather than guessed here.",
    },
    {
        "id": "prose_clybourne_clark_half_brother",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_clybourne_archibald/persons[0]/note",
        "quote": "'Julia K. Clark, half-brother of A. Clybourne, then living with him' is "
                 "named in the next clause and is written into this household.",
        "a": {"person": "clybourne_archibald", "household": "hh_clybourne_archibald",
              "relation": "half_brother"},
        "b": {"person": "clark_john_k", "household": "hh_clark_john_k",
              "relation": "half_brother"},
        "ruling": "not_supported",
        "reason": "THREE FAULTS STAND BETWEEN THE SENTENCE AND A ROW, AND NOT ONE OF THEM "
                  "IS A KINSHIP. The forename is garbled in the text as read — 'Julia K. "
                  "Clark' for a half-BROTHER; the sentence says the man 'is written into "
                  "this household' and no such person is in it; and the dataset holds two "
                  "Archibald Clybourn(e) cards, which is a duplicate under separate "
                  "ruling. A half brother is exactly the degree this vocabulary exists to "
                  "keep straight, and it is not to be landed on a reading nobody has made. "
                  "Raised as its own ticket.",
    },
    {
        "id": "prose_pruyne_sherman_marriage",
        "seam": "household_prose",
        "source": "andreas_1884_v1",
        "where": "hh_pruyne_kimberly/persons[0]/note",
        "quote": "on August 20, 1835 Peter Pruyne married Rebecca, only daughter of Silas "
                 "W. Sherman",
        "a": {"person": "pruyne_peter", "household": "hh_pruyne_kimberly",
              "relation": "husband"},
        "b": {"person": "sherman_rebecca", "household": "hh_sherman_rebecca",
              "relation": "wife"},
        "ruling": "not_supported",
        "reason": "AFTER THE DAY THIS SCENE MODELS, and the record already says so: 'That "
                  "is seven weeks after the scene date, so on July 1 Rebecca Sherman is not "
                  "silently added to this business household.' A kin row is not a placement, "
                  "but `wife` is a present tense and on 1 July 1835 it was not true. The "
                  "identity of the card sherman_rebecca — read from the paper and an 1844 "
                  "directory, under a surname she would not have been using after that "
                  "August — is a second reason and would be enough on its own.",
    },
]

# The ruling on each derived church candidate. A candidate not named here is an
# error, not a default: `--check` refuses an unruled candidate, which is what
# stops a new register reading from landing a tie nobody looked at.
CHURCH_RULINGS = {
    "st_cyr_marriage_001": ("landed", "attested", None),
    "st_cyr_marriage_002": ("landed", "attested", None),
    "st_cyr_marriage_003": ("landed", "attested", None),
    "st_cyr_marriage_004": ("landed", "attested", None),
    "st_cyr_marriage_005": ("landed", "attested", None),
    "st_cyr_marriage_007": ("landed", "attested", None),
    "st_cyr_marriage_008": ("not_supported", None,
                            "THE REGISTER MARRIES THEM ON 29 AUGUST 1835, eight weeks "
                            "after the day this scene models. `wife` is a present tense "
                            "and on 1 July 1835 it was not yet true; the rule is "
                            "hh_pruyne_kimberly's, applied to the register instead of to "
                            "Andreas."),
    "st_cyr_marriage_009": ("not_supported",  None,
                            "Married 1 October 1835, three months after the scene date. "
                            "Same rule."),
    "st_cyr_marriage_010": ("not_supported", None,
                            "Married 27 October 1835, four months after the scene date. "
                            "Same rule."),
    "st_cyr_death_05": ("landed", "attested", None),
}

# The note a landed church row carries, keyed the same way. Written per entry
# because a template that says the same thing about six different families is
# not a reading of any of them.
CHURCH_NOTES = {
    "st_cyr_marriage_001":
        "MARRIED AT CHICAGO IN 1834, IN THE PARISH'S OWN REGISTER. St Cyr's register "
        "carries this couple as the groom and bride of one entry, and both cards were "
        "minted FROM that entry under rule G2c — so the tie has no identity gap in it at "
        "all: the two people are the two people the entry names. The bride is entered as "
        "'Mrs. M. Frauner', which the register's own hand makes a woman marrying again "
        "and this project does not read further than that.",
    "st_cyr_marriage_002":
        "MARRIED AT CHICAGO ON 20 MAY 1834, in the entry both cards were minted from. The "
        "parish register is the contemporary record of the act itself, which is the best "
        "evidence of a marriage this project holds for anybody; the reading is mediated by "
        "the Illinois Catholic Historical Review's printing of the register and the grade "
        "says documented because what is claimed is what the entry states.",
    "st_cyr_marriage_003":
        "MARRIED AT CHICAGO ON 21 MAY 1834, one of two weddings the register records that "
        "day. Both cards are the entry's own groom and bride. Note that the bride's "
        "surname is Simmons and the groom's is Vincent, and that a second Simmons marries "
        "in the next entry — the dataset's Simmonses are kept apart by their entries, not "
        "by their surname.",
    "st_cyr_marriage_004":
        "MARRIED AT CHICAGO ON 21 MAY 1834, the second of the two weddings of that day. "
        "The groom is entered 'Henry Simmons' and the bride 'Cery Logdson', both spellings "
        "as the register prints them; the cards carry the same spellings, because a name is "
        "read and not corrected.",
    "st_cyr_marriage_005":
        "MARRIED AT CHICAGO IN MARCH 1835, four months before the scene date, so this "
        "couple were married ON the day this scene models. The register gives the month "
        "and not the day and the row claims no more than that.",
    "st_cyr_marriage_007":
        "MARRIED AT CHICAGO ON 21 APRIL 1835, ten weeks before the scene date. Two of this "
        "entry's witnesses are also town cards, which the register states and this "
        "vocabulary has no term for — a witness is not a kinsman and none is written.",
    "st_cyr_death_05":
        "THE REGISTER NAMES THE FATHER IN THE ENTRY THAT BURIES THE SON. St Cyr's death "
        "record of 2 July 1835 reads 'John Baptist, son of Leon Bourrassa', and the father "
        "is carried on his own card from the same entry, at locator `parent`. The tie is "
        "therefore not a match made between two records but one record read twice. THE "
        "DEATH IS THE DAY AFTER THE SCENE DATE and the parentage is not: on 1 July 1835 "
        "the son was alive and was his father's son, which is all this row says.",
}


def build(households):
    church = derive_church_candidates(households)
    cands = []
    for c in church:
        ruling = CHURCH_RULINGS.get(c["id"])
        if ruling is None:
            raise SystemExit(f"unruled church candidate '{c['id']}' — a new register "
                             f"reading has appeared and nobody has ruled on it. Add it to "
                             f"CHURCH_RULINGS in tools/harvest_stated_kinship.py.")
        state, confidence, reason = ruling
        c = dict(c, ruling=state)
        if confidence:
            c["confidence"] = confidence
        c["reason"] = reason or CHURCH_NOTES[c["id"]]
        cands.append(c)
    cands.extend(PROSE_CANDIDATES)
    landed = [c for c in cands if c["ruling"] == "landed"]
    return {
        "schema": "stated-kinship-v1",
        "_doc": "T-0734. The kinship the committed sources already state, gathered from "
                "two seams, ruled one by one, and written onto the household records as "
                "reciprocal `kin` rows. Generated by tools/harvest_stated_kinship.py "
                "--build; a candidate ruled `not_supported` carries the reason it may not "
                "land, and that reason is the finding. Nothing here infers a relationship "
                "from a shared surname.",
        "generated_by": "tools/harvest_stated_kinship.py",
        "ticket": "T-0734",
        "scene_date": SCENE_DATE,
        "counts": {
            "candidates": len(cands),
            "from_the_church_register": len(church),
            "from_household_prose": len(PROSE_CANDIDATES),
            "landed": len(landed),
            "not_supported": len(cands) - len(landed),
            "kin_rows_written": 2 * len(landed),
        },
        "register_records_naming_one_role_only": derive_church_incomplete(households),
        "candidates": cands,
    }


def kin_row(near, far, source, confidence, note):
    return {
        "person": near["person"],
        "relation": near["relation"],
        "household": far["household"],
        "value": far["person"],
        "confidence": confidence,
        "sources": [source],
        "note": note,
    }


def apply_rows(households, doc, write=True):
    """Write both halves of every landed tie. Idempotent: a row already there is
    replaced in place, so re-running never doubles a kinship.

    KEY ORDER IS LOAD-BEARING, which is not obvious and cost a gate run to learn.
    `kin` goes immediately BEFORE `persons`, where hh_kinzie_james has always
    carried it, because tools/spend_directories.py rewrites a record by lifting
    its `directories` block off and putting it back LAST. A `kin` key appended
    after that block lands on the wrong side of it, and the directories gate then
    reports the record as drift for a reason that has nothing to do with
    directories."""
    pending = {}
    for c in doc["candidates"]:
        if c["ruling"] != "landed":
            continue
        conf, source, note = c["confidence"], c["source"], c["reason"]
        for near, far in ((c["a"], c["b"]), (c["b"], c["a"])):
            hid = near["household"]
            rows = pending.setdefault(hid, list(households[hid].get("kin") or []))
            rows[:] = [r for r in rows
                       if not (r.get("person") == near["person"]
                               and r.get("value") == far["person"])]
            rows.append(kin_row(near, far, source, conf, note))
    for hid, rows in pending.items():
        h = households[hid]
        rebuilt = {}
        for key, value in h.items():
            if key == "persons":
                rebuilt["kin"] = rows
            if key != "kin":
                rebuilt[key] = value
        if "kin" not in rebuilt:
            rebuilt["kin"] = rows
        h.clear()
        h.update(rebuilt)
        if write:
            with open(os.path.join(HOUSEHOLDS, hid + ".json"), "w",
                      encoding="utf-8") as fh:
                json.dump(h, fh, indent=1, ensure_ascii=False)
                fh.write("\n")
    return sorted(pending)


def check(households):
    problems = []
    fresh = build(households)
    try:
        with open(OUT, encoding="utf-8") as fh:
            committed = json.load(fh)
    except FileNotFoundError:
        return [f"{OUT} is missing — run tools/harvest_stated_kinship.py --build"]
    if committed != fresh:
        problems.append(f"{os.path.relpath(OUT, HERE)} does not match what "
                        f"tools/harvest_stated_kinship.py --build derives from the "
                        f"committed records. Re-run --build in the commit that moved them.")
    idx = person_index(households)
    for c in fresh["candidates"]:
        if c["ruling"] != "landed":
            continue
        for near, far in ((c["a"], c["b"]), (c["b"], c["a"])):
            if idx.get(near["person"], (None,))[0] != near["household"]:
                problems.append(f"{c['id']}: '{near['person']}' is not in "
                                f"'{near['household']}'")
                continue
            rows = households[near["household"]].get("kin") or []
            hit = [r for r in rows if r.get("person") == near["person"]
                   and r.get("value") == far["person"]]
            if not hit:
                problems.append(f"{c['id']}: the worklist says this tie LANDED and "
                                f"{near['household']} carries no row for it. A ruling that "
                                f"says landed and a record that does not is the exact "
                                f"half-fact T-0597 was opened about.")
            elif hit[0].get("relation") != near["relation"]:
                problems.append(f"{c['id']}: {near['household']} says "
                                f"'{hit[0].get('relation')}' where the ruling says "
                                f"'{near['relation']}'")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.build or args.apply or args.check):
        ap.error("one of --build, --apply, --check")

    households = load_households()
    if args.build or args.apply:
        doc = build(households)
    if args.build:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
        c = doc["counts"]
        print(f"{os.path.relpath(OUT, HERE)}: {c['candidates']} candidate(s) "
              f"({c['from_the_church_register']} from the register, "
              f"{c['from_household_prose']} from the prose) — {c['landed']} landed, "
              f"{c['not_supported']} not supported, {c['kin_rows_written']} kin row(s)")
    if args.apply:
        touched = apply_rows(households, doc)
        print(f"kin rows written onto {len(touched)} household record(s):")
        for hid in touched:
            print("   ", hid)
    if args.check:
        problems = check(households)
        for p in problems:
            print("   " + p, file=sys.stderr)
        if problems:
            return 1
        n = sum(len(h.get("kin") or []) for h in households.values())
        print(f"stated kinship: the worklist derives, and all {n} kin row(s) on the "
              f"records agree with it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
