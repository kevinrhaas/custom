#!/usr/bin/env python3
"""What the town's residents and households look like — every figure, re-derivable.

WHY THIS EXISTS, in the owner's words (2026-09-03): "then i would like a summary of what
the residents and households look like, since you have good census data now on many you
should be able to improve that."

A snapshot pasted into a document rots the week after it is written; this project has
already lost `docs/RESEARCH/residents_1835.md` that way, which sat for a month printing
"72 households, 96 person entries" while the layer grew past 1,300. So the summary is a
COMMAND, and `docs/RESEARCH/residents-households-summary-2026-09.md` cites one section of
it beside every table it prints. A later run re-runs the section and gets today's town.

    tools/residents_summary.py --list             the section names
    tools/residents_summary.py --section totals   one section
    tools/residents_summary.py --all              every section, in document order

WHAT IT READS, and nothing else: `data/residents/index.json` (the manifest),
`data/residents/households/*.json` (the records, which are authoritative — the manifest is
a denormalised copy the validator holds to them), `data/town_census.json` (the derived
town ledger) and `data/research/residents/identity_master.json` (the research ledger).

WHAT IT DOES NOT DO. It grades nobody, mints nobody and writes nothing into `data/`. It
counts committed records. Where it has to name a thing that is not in the data — the
seven evidence DOMAINS, and the #668 baseline it measures drift against — the naming is a
literal table below, printed by `--section evidence` and `--section baseline` respectively,
so a reader can see the judgement rather than infer it.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOUSEHOLDS = sorted(glob.glob(str(ROOT / "data/residents/households/*.json")))
INDEX = ROOT / "data/residents/index.json"
TOWN_CENSUS = ROOT / "data/town_census.json"
IDENTITY_MASTER = ROOT / "data/research/residents/identity_master.json"

# ------------------------------------------------------------------ the one naming table
#
# The seven evidence DOMAINS the ticket asks coverage across, named as `data/research/
# domains.json` names them, each mapped to the key a person record carries when a reading
# of that domain has landed on them. THE KEYS ARE NOT ASSERTED: `--section evidence`
# discovers every `*_evidence` key present in the layer and refuses to run if this table
# names one that is absent or misses one that is there. That is what stopped this file
# printing a tidy `census_1830_evidence: 0` — there is no such key, because the 1830
# domain has never reached a card, and a zero row would have read as coverage measured
# rather than coverage absent.
DOMAINS = [
    ("newspaper", "press_evidence", "the Democrat and American runs, advertisements and notices"),
    ("civic", "civic_evidence", "polls, tax and voter lists, the 1832 muster"),
    ("book", "book_evidence", "Andreas, Fergus, the old-settler notices and the printed histories"),
    ("church", "church_evidence", "the St Cyr register and the parish books"),
    ("census_1840", "census_evidence", "the 1840 federal schedules, read as 1840"),
    ("biographical", "biographical_evidence", "a life dated from a printed biography"),
]
# The domain with no key at all, and the source id that would carry it. Held here so
# `--section evidence` can PROVE the absence rather than leave it unmentioned.
DOMAINS_WITH_NO_KEY = [
    ("census_1830", "census_1830_peoria_county_chicago_precinct",
     "Chicago was enumerated in Peoria County in 1830; the named schedule is read in "
     "`data/research/census_1830/` and no ruling from it has been carried to a person."),
]
# Not a person key: a household's later printed directory entries hang off the HOUSEHOLD.
HOUSEHOLD_EVIDENCE_KEY = ("directory", "directories",
                          "a household's later printed directory entries")

# The layer as PR #668 left it, 2026-09-02. Quoted in T-0517's ask; this is the only place
# the numbers are written down, so drift is measured rather than remembered.
BASELINE_668 = {
    "households": 824,
    "persons": 848,
    "attested": 117,
    "inferred": 731,
    "projected_resident": 706,
}


def load_households():
    return [json.loads(Path(f).read_text()) for f in HOUSEHOLDS]


def persons(hhs):
    for h in hhs:
        for p in h.get("persons", []):
            yield h, p


def attr(block):
    """A graded attribute block's value, or None. Records carry {value, confidence, ...}."""
    if isinstance(block, dict):
        return block.get("value")
    return block


def pct(n, d):
    return f"{100.0 * n / d:5.1f}%" if d else "    —"


def row(label, n, d, width=42):
    print(f"  {label:<{width}} {n:>6}  {pct(n, d)}")


# ------------------------------------------------------------------------------ sections

def s_totals(hhs):
    """Households and persons, by grade and by subtype."""
    idx = json.loads(INDEX.read_text())
    ps = [p for _, p in persons(hhs)]
    print(f"households (record files)      {len(hhs):>6}")
    print(f"persons (entries in them)      {len(ps):>6}")
    print(f"index.json says                {idx['counts']['households']:>6} households, "
          f"{idx['counts']['persons']} persons"
          f"   {'AGREES' if idx['counts']['households'] == len(hhs) and idx['counts']['persons'] == len(ps) else 'DRIFTED'}")
    print()
    print("person grade — the resident-evidence axis:")
    g = Counter(p.get("grade") for p in ps)
    for k in ("attested", "inferred", "reconstructed"):
        row(k, g.get(k, 0), len(ps))
    other = {k: v for k, v in g.items() if k not in ("attested", "inferred", "reconstructed")}
    if other:
        print(f"  OFF-VOCABULARY {other}")
    print()
    print("resident_subtype — the weakest inferred subset:")
    st = Counter(p.get("resident_subtype") for p in ps)
    row("projected_resident", st.get("projected_resident", 0), len(ps))
    row("(no subtype)", st.get(None, 0), len(ps))
    print()
    print("the two flags the manifest counts separately:")
    row("letter_list_only persons", sum(1 for p in ps if p.get("letter_list_only")), len(ps))
    row("civic_mint persons", sum(1 for p in ps if p.get("civic_mint")), len(ps))
    row("later_census (1840-linked) persons", sum(1 for p in ps if p.get("later_census")), len(ps))
    row("carry a resident_research row", sum(1 for p in ps if p.get("resident_research")), len(ps))
    print()
    print("household letter_list_only (every person in it):")
    row("letter-list households", sum(1 for h in hhs if all(p.get("letter_list_only") for p in h.get("persons", []))), len(hhs))


def s_division(hhs):
    """Households by division, and by presence on the scene date."""
    d = Counter(h.get("division") for h in hhs)
    print("by division:")
    for k, v in d.most_common():
        row(str(k), v, len(hhs))
    print()
    print("present_on_scene_date (1835-07-01):")
    p = Counter(attr(h.get("present_on_scene_date")) for h in hhs)
    for k, v in p.most_common():
        row(str(k), v, len(hhs))
    print()
    print("confidence on that presence claim:")
    c = Counter((h.get("present_on_scene_date") or {}).get("confidence")
                if isinstance(h.get("present_on_scene_date"), dict) else None for h in hhs)
    for k, v in c.most_common():
        row(str(k), v, len(hhs))
    print()
    print("placement — what the record says about where they are:")
    row("lives_at names a structure", sum(1 for h in hhs if attr(h.get("lives_at"))), len(hhs))
    row("works_at names a structure", sum(1 for h in hhs if attr(h.get("works_at"))), len(hhs))
    row("neither", sum(1 for h in hhs if not attr(h.get("lives_at")) and not attr(h.get("works_at"))), len(hhs))


def s_sex(hhs):
    """Sex where a source records it, and what is inferable from a relationship."""
    ps = [p for _, p in persons(hhs)]
    s = Counter(p.get("sex") for p in ps)
    print("sex, as recorded on the person:")
    for k in sorted(s, key=lambda k: (k is None, str(k))):
        row(str(k) if k else "(not recorded)", s[k], len(ps))
    print()
    recorded = sum(v for k, v in s.items() if k)
    print(f"recorded on {recorded} of {len(ps)} persons ({pct(recorded, len(ps)).strip()}) — the layer is")
    print("a layer of NAMED HEADS from lists that print a name and no sex, so this is expected")
    print("to stay low until the census households are read into persons.")
    print()
    ll = Counter((p.get("sex"), bool(p.get("letter_list_only"))) for p in ps if p.get("sex"))
    print("WHERE A RECORDED SEX COMES FROM, and why the split matters:")
    for sx in ("male", "female"):
        print(f"  {sx:<8} from a source that says so   {ll.get((sx, False), 0):>4}")
        print(f"  {sx:<8} from a letter-list honorific {ll.get((sx, True), 0):>4}")
    print("  A letter-list sex is read off the printed 'Mr'/'Mrs' and is only as good as the")
    print("  compositor: `codding_sally` is 'Codding, Sally Mr' in the Democrat of 1 July 1835")
    print("  and carries `male` on that honorific alone. Treat the honorific rows as the")
    print("  weakest column in this section.")
    print()
    print("relationships that imply a sex, whether or not `sex` is written:")
    gendered = {"wife": "female", "husband": "male", "son": "male", "daughter": "female",
                "mother": "female", "father": "male", "brother": "male", "sister": "female"}
    r = Counter(p.get("relationship") for p in ps)
    for k in sorted(gendered):
        if r.get(k):
            row(f"{k} (implies {gendered[k]})", r[k], len(ps))
    imply = sum(r.get(k, 0) for k in gendered)
    row("TOTAL implied by relationship", imply, len(ps))
    conflict = [p["id"] for p in ps
                if p.get("sex") and gendered.get(p.get("relationship"))
                and p["sex"] != gendered[p["relationship"]]]
    print(f"  relationship and recorded sex disagree on {len(conflict)}: {conflict[:10]}")


def s_occupation(hhs):
    """Occupation coverage: who carries a trade, at what confidence, from which source."""
    ps = [p for _, p in persons(hhs)]
    have, none_rec, missing = [], 0, 0
    conf = Counter()
    by_source = Counter()
    for p in ps:
        o = p.get("occupation")
        v = attr(o)
        if v in (None, ""):
            missing += 1
            continue
        if v == "none_recorded":
            none_rec += 1
            continue
        have.append(p)
        if isinstance(o, dict):
            conf[o.get("confidence")] += 1
            for sid in o.get("sources") or []:
                by_source[sid] += 1
    print("does this person carry a trade?")
    row("yes — a named occupation", len(have), len(ps))
    row("no — occupation is `none_recorded`", none_rec, len(ps))
    row("no — no occupation block at all", missing, len(ps))
    print()
    print("confidence on the trade, for those that carry one:")
    for k, v in conf.most_common():
        row(str(k), v, len(have))
    print()
    print("which source stands behind the trade (a trade may cite more than one):")
    for k, v in by_source.most_common(20):
        row(k, v, len(have))
    print()
    print("the twelve commonest trades in the town:")
    t = Counter(attr(p.get("occupation")) for p in have)
    for k, v in t.most_common(12):
        row(str(k), v, len(have))
    print(f"  distinct trades named: {len(t)}")
    print()
    print("WHERE THE TRADES COME FROM, as two numbers:")
    heavy = {"andreas_1884_v1", "chicago_democrat_1833_1835",
             "chicago_democrat_1833_11_26", "chicago_american_1835"}
    from_heavy = {p["id"] for p in have
                  if set((p.get("occupation") or {}).get("sources") or []) & heavy}
    row("trade from Andreas or a newspaper", len(from_heavy), len(have))
    print()
    print("THE DIRECTORIES, which print a trade beside nearly every name they carry:")
    dirs = {"fergus_chicago_directory_1839", "fergus_chicago_directory_1843",
            "norris_directory_1844"}
    cited = {p["id"] for p in ps if dirs & set(p.get("sources") or [])}
    from_dir = [p["id"] for p in have
                if dirs & set((p.get("occupation") or {}).get("sources") or [])]
    print(f"  persons whose IDENTITY cites a directory   {len(cited):>6}")
    print(f"  persons whose TRADE cites a directory      {len(from_dir):>6}   {from_dir}")
    print("  That gap is the largest unspent thing this section can see: the trades are")
    print("  already read and adjudicated in data/research/directories/, and they are not")
    print("  on the cards.")


def s_size(hhs):
    """Household size distribution."""
    sizes = Counter(len(h.get("persons", [])) for h in hhs)
    total = sum(k * v for k, v in sizes.items())
    print("persons per household record:")
    for k in sorted(sizes):
        row(f"{k} person" + ("" if k == 1 else "s"), sizes[k], len(hhs))
    print()
    print(f"  mean {total / len(hhs):.2f} persons per household over {len(hhs)} households")
    print("  the largest: " + ", ".join(
        f"{h['id']} ({len(h['persons'])})"
        for h in sorted(hhs, key=lambda h: -len(h.get("persons", [])))[:5]))
    print()
    print("WHAT THE SHAPE MEANS. A household of one is not a man living alone; it is a")
    print("household whose head is the only person a source NAMES. The town census of")
    print("November 1835 counted 3,265 people in 398 dwellings — 8.2 to a dwelling — so the")
    print("distribution above measures THE READING, not the town. Closing that gap is the")
    print("1840 schedules' job: they print a household's composition by age band, which is")
    print("why the 1840 bridge is a bridge and not a back-projection.")


def s_evidence(hhs):
    """Evidence coverage per domain, and the overlap between domains."""
    ps = [p for _, p in persons(hhs)]

    # The table above is held to the layer before a single number is printed.
    present = {k for p in ps for k in p if k.endswith("_evidence")}
    named = {k for _, k, _ in DOMAINS}
    if present != named:
        print(f"REFUSED: the DOMAINS table and the layer disagree.\n"
              f"  in the layer, not in the table: {sorted(present - named)}\n"
              f"  in the table, not in the layer: {sorted(named - present)}\n"
              f"  Fix the table in tools/residents_summary.py — do not print around it.",
              file=sys.stderr)
        return 1

    print("the domains, and the key a landed reading writes onto the record:")
    for name, key, what in DOMAINS:
        print(f"  {name:<13} person.{key:<24} {what}")
    dn, dk, dw = HOUSEHOLD_EVIDENCE_KEY
    print(f"  {dn:<13} household.{dk:<21} {dw}")
    for name, sid, why in DOMAINS_WITH_NO_KEY:
        print(f"  {name:<13} {'(no key)':<32} {why}")
    print()

    have = defaultdict(set)
    for h, p in persons(hhs):
        for name, key, _ in DOMAINS:
            if p.get(key):
                have[name].add(p["id"])
        if h.get(dk):
            have[dn].add(p["id"])
    order = [n for n, _, _ in DOMAINS] + [dn]

    print("persons a reading of that domain has been carried onto:")
    for name in order:
        row(name, len(have[name]), len(ps))
    for name, sid, _ in DOMAINS_WITH_NO_KEY:
        reached = sum(1 for p in ps if sid in (p.get("sources") or []))
        row(f"{name} (via {sid})", reached, len(ps))
        if reached:
            print(f"  NOTE: {name} now reaches a card; it needs an evidence key and a row above.")
    print()
    covered = set().union(*have.values()) if have else set()
    row("ANY domain", len(covered), len(ps))
    row("NO domain at all", len(ps) - len(covered), len(ps))
    print()

    counts = Counter(sum(1 for name in order if p["id"] in have[name]) for p in ps)
    print("how many domains stand behind one person:")
    for k in sorted(counts):
        row(f"{k} domain" + ("" if k == 1 else "s"), counts[k], len(ps))
    print()

    print("the overlap, pairwise (persons carried onto by BOTH):")
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            both = have[a] & have[b]
            if both:
                print(f"  {a:<13} n {b:<13} {len(both):>6}".replace(" n ", " \u2229 "))
    print()

    print("distinct source ids cited by persons[].sources:")
    src = Counter()
    for p in ps:
        for sid in p.get("sources") or []:
            src[sid] += 1
    for k, v in src.most_common(15):
        row(k, v, len(ps))
    print(f"  distinct source ids: {len(src)}")
    print()
    print("how many source ids stand behind one person:")
    row("one source", sum(1 for p in ps if len(set(p.get("sources") or [])) == 1), len(ps))
    row("two or more", sum(1 for p in ps if len(set(p.get("sources") or [])) >= 2), len(ps))
    row("none", sum(1 for p in ps if not p.get("sources")), len(ps))
    return 0


def s_town(hhs):
    """The residents layer set beside the town it is reconstructing."""
    tc = json.loads(TOWN_CENSUS.read_text())
    im = json.loads(IDENTITY_MASTER.read_text())
    pe, bl = tc["people"], tc["buildings"]
    print("data/town_census.json — DERIVED, regenerated by tools/town_census.py:")
    print(f"  the town of November 1835, as Andreas prints it  {pe['town_total']:>6} people")
    print(f"                                                   {pe['town_total_dwellings']:>6} dwellings")
    print(f"  persons this layer HOUSES in a standing building {pe['housed']:>6}")
    print(f"  households housed                                {pe['households_housed']:>6}")
    print(f"  households with no dwelling                      {pe['households_without_a_dwelling']:>6}")
    print(f"  buildings standing in the scene                  {bl['standing']:>6} of {bl['target']}")
    print()
    print(f"  NAMED of the town's {pe['town_total']}: {len(list(persons(hhs)))} persons "
          f"= {pct(len(list(persons(hhs))), pe['town_total']).strip()}")
    print(f"  HOUSED of the {pe['town_total']}: {pe['housed']} = {pct(pe['housed'], pe['town_total']).strip()}")
    print()
    print("data/research/residents/identity_master.json — the research ledger behind them:")
    for k, v in im["counts"].items():
        print(f"  {k:<46} {v:>6}")


def s_baseline(hhs):
    """Drift against the layer as PR #668 left it, 2026-09-02."""
    ps = [p for _, p in persons(hhs)]
    now = {
        "households": len(hhs),
        "persons": len(ps),
        "attested": sum(1 for p in ps if p.get("grade") == "attested"),
        "inferred": sum(1 for p in ps if p.get("grade") == "inferred"),
        "projected_resident": sum(1 for p in ps if p.get("resident_subtype") == "projected_resident"),
    }
    print("the #668 baseline is a literal table in this file — the only place it is written:")
    print(f"  {'':<22}{'#668':>8}{'now':>8}{'change':>9}")
    for k, was in BASELINE_668.items():
        d = now[k] - was
        print(f"  {k:<22}{was:>8}{now[k]:>8}{d:>+9}")
    print()
    print("READ IT THIS WAY. `attested` rising while `persons` rises is the sweep MINTING")
    print("people from civic evidence, not regrading the ones already there; `projected_")
    print("resident` is the letter-list floor and falls only when a second source reaches a")
    print("name. The two move independently and a single 'net' figure would hide both.")


def s_gaps(hhs):
    """What is unresearched, unplaced or unresolved."""
    ps = [p for _, p in persons(hhs)]
    gaps = [
        ("no resident_research row", sum(1 for p in ps if not p.get("resident_research")), len(ps)),
        ("rests on the letter lists alone", sum(1 for p in ps if p.get("letter_list_only")), len(ps)),
        ("rests on ONE source id", sum(1 for p in ps if len(set(p.get("sources") or [])) == 1), len(ps)),
        ("no source id at all", sum(1 for p in ps if not p.get("sources")), len(ps)),
        ("no trade (none_recorded or absent)", sum(1 for p in ps if attr(p.get("occupation")) in (None, "", "none_recorded")), len(ps)),
        ("no sex recorded", sum(1 for p in ps if not p.get("sex")), len(ps)),
        ("no 1840 linkage", sum(1 for p in ps if not p.get("later_census")), len(ps)),
    ]
    print("PERSONS:")
    for label, n, d in gaps:
        row(label, n, d)
    print()
    hgaps = [
        ("division `unplaced`", sum(1 for h in hhs if h.get("division") == "unplaced"), len(hhs)),
        ("no lives_at", sum(1 for h in hhs if not attr(h.get("lives_at"))), len(hhs)),
        ("no works_at", sum(1 for h in hhs if not attr(h.get("works_at"))), len(hhs)),
        ("no origin", sum(1 for h in hhs if not attr(h.get("origin"))), len(hhs)),
        ("no reason_for_coming", sum(1 for h in hhs if not attr(h.get("reason_for_coming"))), len(hhs)),
        ("no party_size_on_arrival", sum(1 for h in hhs if not attr(h.get("party_size_on_arrival"))), len(hhs)),
        ("review_required", sum(1 for h in hhs if h.get("review_required")), len(hhs)),
        ("touches_removal", sum(1 for h in hhs if h.get("touches_removal")), len(hhs)),
    ]
    print("HOUSEHOLDS:")
    for label, n, d in hgaps:
        row(label, n, d)
    print()
    print("ARRIVAL precision — how sharply the layer can date a household's arrival:")
    prec = Counter((h.get("arrival") or {}).get("precision") if isinstance(h.get("arrival"), dict) else None
                   for h in hhs)
    for k, v in prec.most_common():
        row(str(k), v, len(hhs))


SECTIONS = [
    ("totals", s_totals),
    ("division", s_division),
    ("sex", s_sex),
    ("occupation", s_occupation),
    ("size", s_size),
    ("evidence", s_evidence),
    ("town", s_town),
    ("baseline", s_baseline),
    ("gaps", s_gaps),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--section", help="one section name")
    ap.add_argument("--all", action="store_true", help="every section, in document order")
    ap.add_argument("--list", action="store_true", help="the section names")
    a = ap.parse_args()
    if a.list:
        for name, fn in SECTIONS:
            print(f"{name:<12} {fn.__doc__}")
        return 0
    hhs = load_households()
    if a.all:
        for name, fn in SECTIONS:
            print(f"=== {name} ===")
            fn(hhs)
            print()
        return 0
    if not a.section:
        ap.print_help()
        return 2
    for name, fn in SECTIONS:
        if name == a.section:
            fn(hhs)
            return 0
    print(f"no such section: {a.section}; try --list", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
