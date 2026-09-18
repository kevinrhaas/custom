#!/usr/bin/env python3
"""Where every standing household, person and grade came from (T-1144 acceptance 6).

    python3 tools/report_convergence_closing.py             the accounting, read out
    python3 tools/report_convergence_closing.py --build     write the table and the report
    python3 tools/report_convergence_closing.py --check     it re-derives, and nothing drifted
    python3 tools/report_convergence_closing.py --self-test the rules below, held over fixtures

WHAT THIS IS. T-1144's sixth acceptance asks the convergence pass to rebuild the five
derived resident artefacts and then give "the exact household/person/grade deltas" and
"every retired id's redirect". The five rebuilds are gated in check.sh already — the index
by `rebuild_resident_index.py --check`, the sidecars by `compile_scene.py --all --check`,
the town census by `town_census.py --check`, the published layer by
`check_published_residents.mjs` and the final audit by `export_resident_audit.py --check` —
so each of them is a fixed point that a lap re-proves. What has never existed is the
report: a reader who asks *what is this layer made of, and what did the passes retire to
get there* has had to walk 1,258 cards and join them to a 66-row redirect table by hand.

THE DELTA IS AN ACCOUNTING, NOT A DIFF AGAINST A DATE. A diff against a remembered
yesterday would need a snapshot nothing derives, and a snapshot nothing derives is the
exact failure the last pass found in `index.json`'s `merged` table. So the delta here is
the one every card can be asked for directly: **which pass put this household in the tree**
(`source_pass`, written by the mint that minted it), what each pass contributed, and what
left — the 66 retirements with the redirect each one resolves to. Minted plus authored
equals standing; retired plus standing equals everything the passes ever held. Both sums
are asserted, so the table cannot quietly stop adding up.

PERSONS ARE ATTRIBUTED TO THEIR HOUSEHOLD'S PASS, and that is stated rather than hidden: a
person record carries a grade and no pass of its own, because a mint mints a household and
the persons inside it together. Where a later writer adds a person to a card another pass
minted — which is what the reconstruction programme does — the person is counted under the
card's pass and named separately below, so the two readings never get confused.

WHAT IT REFUSES. Four faults, each of which fails `--build` as well as `--check`, because
writing one of them down publishes it:

  * `index_disagrees` — `data/residents/index.json`'s counts must equal the tree the cards
    make. The index is the file every reader and every renderer takes these numbers from;
    if it and the cards part company, everything below is arithmetic on a stale header.
  * `mint_owns_reconstructed` — no person graded `reconstructed` may sit in a household a
    MINT minted. This is T-1144 acceptance 8 asked of the TREE rather than of the writers:
    `refuse_reconstructed_grade.py` proves the four mints CALL the refusal, and this proves
    the refusal's promise actually holds in the committed records. Two gates on one rule,
    from opposite ends, because the grade is the boundary the reconstruction bands turn on.
  * `redirect_does_not_arrive` — a retired id whose redirect names no live card. Acceptance
    6 asks this report to NAME every redirect, and a named dead end is worse than an
    unnamed one. `rebuild_resident_index.py` owns this rule where the table is written;
    this re-asks it where the table is read.
  * `unknown_pass` — a `source_pass` this report has no accounting row for. A fifth mint
    arriving is fine; a fifth mint arriving and being silently dropped out of the sum is
    not, so the vocabulary is closed and a new pass must be added here on purpose.

WHAT IT DOES NOT DO. It re-decides nothing and it grades nobody. Every count is a tally of
committed fields; every retirement's rule, cluster and ticket are copied off the row that
the merge ruling wrote. The one place it draws a distinction of its own is among the
households NO pass owns, and that distinction is read off the card's own prose: a card
whose `research_note` opens `RECONSTRUCTED HOUSEHOLD` is a survivor of the retired
invented-name programme (T-0489), and the rest are the authored core the mints were built
on top of. The self-test holds that split directly, because it is the one line here a later
change could quietly move.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
HOUSEHOLDS = DATA / "residents" / "households"
INDEX = DATA / "residents" / "index.json"
OUT = DATA / "research" / "convergence_closing.json"
REPORT = ROOT / "docs" / "RESEARCH" / "convergence-closing-2026-09.md"

SCENE_DATE = "1835-07-01"
TICKET = "T-1144"
AS_OF = "2026-09-18"

# The closed vocabulary of writers. `None` is not a pass: it is a card no mint minted.
# Each mint is named with the tool that owns it so a reader can go and run the writer.
MINTS = {
    "civic": "tools/mint_civic_residents.py",
    "documented": "tools/mint_documented_residents.py",
    "letter_list": "tools/mint_letter_list_residents.py",
    "placed": "tools/mint_placed_residents.py",
}
AUTHORED = "authored"          # the label this report gives `source_pass: null`
GRADES = ("attested", "inferred", "reconstructed")

# The five artefacts acceptance 6 names, and the gate step that re-derives each. This is a
# pointer table, not a second gate: check.sh runs these, and the report cites them so the
# reader knows the counts below stand on a fixed point rather than on a lucky tree.
FIXED_POINTS = [
    ("data/residents/index.json", "python3 tools/rebuild_resident_index.py --check"),
    ("the scene sidecars", "python3 tools/compile_scene.py --all --check"),
    ("the town census", "python3 tools/town_census.py --check"),
    ("the published residents layer", "node tools/check_published_residents.mjs"),
    ("the final resident audit", "python3 tools/export_resident_audit.py --check"),
]

# The one derivation in this layer that is NOT a fixed point, named rather than blessed.
# Stated here so the report cannot read as "everything re-derives" when one thing does not.
NOT_A_FIXED_POINT = {
    "tool": "tools/mint_letter_list_residents.py",
    "drift": "798 file(s) differ under --check",
    "ticket": "T-1222",
    "why": (
        "byte-identity is the wrong contract for a pass that is not the last writer of its "
        "own files: tools/synthesize_resident_research.py rewrites the letter_list_only "
        "cohort's grade, subtype and note after this mint runs, so re-deriving over the "
        "committed tree REVERTS that work. T-0662 read the drift and T-1228 holds the "
        "field-level ownership settlement it wants instead. data/research/"
        "check_gate_baseline.json carries the standing row."
    ),
}


# ---------------------------------------------------------------------------
# the rules, each a pure function so --self-test can hold it over a fixture
# ---------------------------------------------------------------------------

def pass_of(household: dict) -> str:
    """The writer that put this card in the tree, or `authored` where none did."""
    value = household.get("source_pass")
    return AUTHORED if value is None else str(value)


def unowned_kind(household: dict) -> str:
    """Among the cards NO mint minted, which of the two kinds is this one?

    Read off the card's own prose and nothing else. The retired invented-name programme
    (T-0489) opened every note it wrote with the same two words, and the cards it left
    behind still carry them; everything else with no pass is the authored core the mints
    were built on top of.
    """
    note = household.get("research_note") or ""
    return "invented_name_survivor" if note.startswith("RECONSTRUCTED HOUSEHOLD") \
        else "authored_core"


def grades_of(household: dict) -> Counter:
    return Counter(person.get("grade") for person in household.get("persons", []))


def redirect_arrives(row: dict, live_households: set, live_persons: set) -> bool:
    """A retirement resolves onto a card that is actually standing, and is not itself
    retired. A redirect naming a retired id is a chain, and a chain is a dead end one hop
    further away."""
    household = row.get("merged_into_household")
    person = row.get("merged_into_person")
    if not household or not person:
        return False
    return household in live_households and person in live_persons


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def load_households() -> list[dict]:
    return [json.loads(Path(f).read_text(encoding="utf-8"))
            for f in sorted(glob.glob(str(HOUSEHOLDS / "*.json")))]


def build(households: list[dict] | None = None, index: dict | None = None) -> dict:
    """The accounting. Both inputs are injectable so `--self-test` can hold the four
    refusals over fixtures WITHOUT writing a broken file into the tree: a gate that has to
    corrupt a committed record to prove itself can leave one behind when it is interrupted.
    """
    households = load_households() if households is None else households
    index = json.loads(INDEX.read_text(encoding="utf-8")) if index is None else index

    live_households = {h["id"] for h in households}
    live_persons = {p["id"] for h in households for p in h.get("persons", [])}

    by_pass: dict[str, dict] = {}
    unowned: dict[str, list] = defaultdict(list)
    faults: list[dict] = []

    for household in households:
        label = pass_of(household)
        if label != AUTHORED and label not in MINTS:
            faults.append({
                "fault": "unknown_pass", "household": household["id"], "pass": label,
                "detail": "no accounting row for this source_pass — add it to MINTS",
            })
        row = by_pass.setdefault(label, {
            "households": 0, "persons": 0,
            "grades": {g: 0 for g in GRADES}, "letter_list_only_persons": 0,
        })
        grades = grades_of(household)
        row["households"] += 1
        row["persons"] += sum(grades.values())
        for grade, count in grades.items():
            if grade in row["grades"]:
                row["grades"][grade] += count
        row["letter_list_only_persons"] += sum(
            1 for p in household.get("persons", []) if p.get("letter_list_only"))

        if label == AUTHORED:
            unowned[unowned_kind(household)].append({
                "household": household["id"],
                "head": next((p.get("name") for p in household.get("persons", [])), None),
                "grades": {g: c for g, c in sorted(grades.items())},
            })
        elif grades.get("reconstructed"):
            faults.append({
                "fault": "mint_owns_reconstructed", "household": household["id"],
                "pass": label,
                "detail": f"{grades['reconstructed']} reconstructed person(s) in a card "
                          f"{MINTS[label]} minted — T-1144 acceptance 8 forbids it",
            })

    # The reconstruction programme's own people, named where they stand. They are counted
    # under their household's pass above; this is the second reading, kept separate.
    reconstructed = []
    for household in households:
        for person in household.get("persons", []):
            if person.get("grade") != "reconstructed":
                continue
            basis = person.get("basis") or {}
            reconstructed.append({
                "person": person["id"], "name": person.get("name"),
                "household": household["id"], "household_pass": pass_of(household),
                "basis_kind": basis.get("kind"), "basis_id": basis.get("id"),
                "has_seed": person.get("seed") is not None,
                "has_replaceable_by": person.get("replaceable_by") is not None,
            })

    # The retirements, with the redirect each one resolves to.
    retirements = []
    for row in index.get("merged", []):
        arrives = redirect_arrives(row, live_households, live_persons)
        retirements.append({
            "household": row.get("household"), "person": row.get("person"),
            "name": row.get("name"),
            "into_household": row.get("merged_into_household"),
            "into_person": row.get("merged_into_person"),
            "rule": row.get("rule"), "cluster": row.get("cluster"),
            "ticket": row.get("ticket"), "arrives": arrives,
        })
        if not arrives:
            faults.append({
                "fault": "redirect_does_not_arrive", "household": row.get("household"),
                "pass": None,
                "detail": f"redirect names {row.get('merged_into_household')} / "
                          f"{row.get('merged_into_person')}, which is no live card",
            })

    standing = {
        "households": len(households),
        "persons": len(live_persons),
        "by_grade": {g: sum(r["grades"][g] for r in by_pass.values()) for g in GRADES},
        "retired": len(retirements),
    }
    index_counts = index.get("counts", {})
    for key, derived in (("households", standing["households"]),
                         ("persons", standing["persons"]),
                         ("merged_away", standing["retired"])):
        if index_counts.get(key) != derived:
            faults.append({
                "fault": "index_disagrees", "household": None, "pass": None,
                "detail": f"index.json counts.{key} is {index_counts.get(key)}, "
                          f"the cards make {derived}",
            })
    if index_counts.get("by_grade") != standing["by_grade"]:
        faults.append({
            "fault": "index_disagrees", "household": None, "pass": None,
            "detail": f"index.json counts.by_grade is {index_counts.get('by_grade')}, "
                      f"the cards make {standing['by_grade']}",
        })

    # The cohort the letter-list mint minted and a later pass carried out of its cohort.
    # This is the pipeline-ordering fact T-1222 owns, measured from the other side: these
    # are the cards a re-run of the mint would put BACK into the cohort.
    carried_out = [
        {"household": h["id"],
         "head": next((p.get("name") for p in h.get("persons", [])), None),
         "grades": {g: c for g, c in sorted(grades_of(h).items())}}
        for h in households
        if pass_of(h) == "letter_list"
        and not any(p.get("letter_list_only") for p in h.get("persons", []))
    ]

    return {
        "_doc": f"{TICKET} acceptance 6 — where every standing household, person and "
                f"grade came from, and what was retired to get there. Derived by "
                f"tools/report_convergence_closing.py; --check re-derives it.",
        "ticket": TICKET,
        "scene_date": SCENE_DATE,
        "as_of": AS_OF,
        "standing": standing,
        "by_pass": {k: by_pass[k] for k in sorted(by_pass)},
        "unowned": {k: sorted(unowned[k], key=lambda r: r["household"])
                    for k in sorted(unowned)},
        "reconstructed_persons": sorted(reconstructed, key=lambda r: r["person"]),
        "retirements": sorted(retirements, key=lambda r: (r["household"] or "")),
        "letter_list_carried_out_of_cohort": sorted(carried_out,
                                                    key=lambda r: r["household"]),
        "fixed_points": [{"artefact": a, "verify": v} for a, v in FIXED_POINTS],
        "not_a_fixed_point": NOT_A_FIXED_POINT,
        "faults": sorted(faults, key=lambda f: (f["fault"], f["household"] or "",
                                                f["detail"])),
    }


# ---------------------------------------------------------------------------
# the report
# ---------------------------------------------------------------------------

def _n(value: int) -> str:
    return f"{value:,}"


def report(doc: dict) -> str:
    standing = doc["standing"]
    by_pass = doc["by_pass"]
    out = [
        f"# Closing convergence accounting — {doc['as_of']}",
        "",
        f"Generated by `tools/report_convergence_closing.py --build`; `--check` re-derives "
        f"it. {doc['ticket']} acceptance 6: the five derived resident artefacts rebuilt, "
        f"the household, person and grade deltas stated exactly, and every retired id's "
        f"redirect named. It signs nothing off — T-1157 is the signature and this is one "
        f"of its evidence sections.",
        "",
        "## 1. What the layer is made of",
        "",
        f"**{_n(standing['households'])} households, {_n(standing['persons'])} persons "
        f"standing on {doc['scene_date']}, and {_n(standing['retired'])} ids retired into "
        f"them.** Every card says which writer put it in the tree, in its own "
        f"`source_pass` field; the rows below are that field tallied, and the persons are "
        f"attributed to their household's writer because a mint mints a card and the "
        f"people on it together.",
        "",
        "| Writer | Households | Persons | attested | inferred | reconstructed |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label in sorted(by_pass):
        row = by_pass[label]
        name = f"`{label}` — {MINTS[label]}" if label in MINTS else \
            f"`{label}` — no writer derives these"
        out.append(
            f"| {name} | {_n(row['households'])} | {_n(row['persons'])} | "
            f"{_n(row['grades']['attested'])} | {_n(row['grades']['inferred'])} | "
            f"{_n(row['grades']['reconstructed'])} |")
    out += [
        f"| **Standing total** | **{_n(standing['households'])}** | "
        f"**{_n(standing['persons'])}** | **{_n(standing['by_grade']['attested'])}** | "
        f"**{_n(standing['by_grade']['inferred'])}** | "
        f"**{_n(standing['by_grade']['reconstructed'])}** |",
        "",
        f"The totals are asserted against `data/residents/index.json`'s own `counts` "
        f"block on every run: a disagreement is the `index_disagrees` fault and fails this "
        f"tool in `--build` as well as `--check`, because the index is the header every "
        f"reader and every renderer takes these numbers from.",
        "",
        "## 2. The cards no writer derives",
        "",
    ]
    core = doc["unowned"].get("authored_core", [])
    survivors = doc["unowned"].get("invented_name_survivor", [])
    out += [
        f"**{_n(len(core) + len(survivors))} households carry no `source_pass` at all.** "
        f"That is not drift by itself — the mints were built on top of an authored core, "
        f"and {_n(len(core))} of these are it: Beaubien, Kinzie, Caldwell, Calhoun, "
        f"Carpenter and the rest of the deeply-written cards the passes were designed to "
        f"extend rather than replace.",
        "",
    ]
    if survivors:
        out += [
            f"**The other {_n(len(survivors))} are survivors of the retired invented-name "
            f"programme** (T-0489), and they are named here because nothing else names "
            f"them. Each one's own `research_note` opens `RECONSTRUCTED HOUSEHOLD`, each "
            f"sits in an `hh_inf_<trade>_<division>_<nn>` container the programme composed, "
            f"and no pass in the pipeline re-derives any of them — so a lap that rebuilt "
            f"every writer would leave all five exactly where they are. T-1294 found one "
            f"of them from the register side; this is the full list.",
            "",
            "| Household | Person on the card | Grades |",
            "| --- | --- | --- |",
        ]
        for row in survivors:
            grades = ", ".join(f"{g} × {c}" for g, c in row["grades"].items()) or "—"
            out.append(f"| `{row['household']}` | {row['head'] or '—'} | {grades} |")
        out += [
            "",
            "**This report does not rule on them.** Whether each is a real reading in a "
            "container the programme happened to build, or a container with a real name "
            "dropped into it, is a card-by-card question with evidence behind it; naming "
            "the five as one cohort is what acceptance 6 can honestly do.",
            "",
        ]
    out += [
        "## 3. The reconstructed grade, and who is allowed to write it",
        "",
    ]
    rc = doc["reconstructed_persons"]
    out += [
        f"**{_n(len(rc))} persons are graded `reconstructed`**, and none of them stands in "
        f"a card a mint minted. That is {doc['ticket']} acceptance 8 asked of the tree: "
        f"`tools/refuse_reconstructed_grade.py` proves the four mints CALL the refusal on "
        f"the way out, and the `mint_owns_reconstructed` fault here proves the refusal's "
        f"promise holds in the committed records. Two gates on one rule, from opposite "
        f"ends, because this grade is the boundary the reconstruction bands turn on.",
        "",
        "| Person | Household | Household's writer | Basis | Seed | Replaceable by |",
        "| --- | --- | --- | --- | :-: | :-: |",
    ]
    for row in rc:
        basis = f"`{row['basis_kind']}` / `{row['basis_id']}`" if row["basis_kind"] else "—"
        out.append(
            f"| {row['name']} (`{row['person']}`) | `{row['household']}` | "
            f"`{row['household_pass']}` | {basis} | "
            f"{'yes' if row['has_seed'] else 'NO'} | "
            f"{'yes' if row['has_replaceable_by'] else 'NO'} |")
    out += [
        "",
        "## 4. Every retired id and where it goes",
        "",
        f"**{_n(len(doc['retirements']))} retirements**, each with the merge rule that "
        f"made it and the ticket that ruled it. `Arrives` is asked fresh here: the "
        f"redirect must name a household card and a person card that are both standing, "
        f"and a redirect pointing at another retired id is a chain, which is a dead end "
        f"one hop further away. "
        f"{_n(sum(1 for r in doc['retirements'] if r['arrives']))} of "
        f"{_n(len(doc['retirements']))} arrive.",
        "",
        "| Retired | Name | Redirects to | Rule | Cluster | Ticket | Arrives |",
        "| --- | --- | --- | :-: | --- | --- | :-: |",
    ]
    for row in doc["retirements"]:
        out.append(
            f"| `{row['household']}` | {row['name'] or '—'} | `{row['into_household']}` | "
            f"{row['rule'] or '—'} | {row['cluster'] or '—'} | {row['ticket'] or '—'} | "
            f"{'yes' if row['arrives'] else '**NO**'} |")
    carried = doc["letter_list_carried_out_of_cohort"]
    out += [
        "",
        "## 5. The one derivation that is not a fixed point",
        "",
        f"The five artefacts acceptance 6 names all re-derive, and check.sh proves each "
        f"one on every run:",
        "",
        "| Artefact | Re-derived by |",
        "| --- | --- |",
    ]
    for row in doc["fixed_points"]:
        out.append(f"| {row['artefact']} | `{row['verify']}` |")
    nfp = doc["not_a_fixed_point"]
    out += [
        "",
        f"**`{nfp['tool']}` is not one of them** — {nfp['drift']}, and it carries its own "
        f"ticket ({nfp['ticket']}). It is named here rather than blessed with a baseline: "
        f"{nfp['why']}",
        "",
        f"Measured from the other side, this is what that ordering looks like in the "
        f"cards. **{_n(len(carried))} households the letter-list mint minted hold no "
        f"`letter_list_only` person any more**: a later pass found independent evidence, "
        f"graded them `attested` and carried them out of the cohort. Re-running the mint "
        f"over the committed tree would put all {_n(len(carried))} back into it, which is "
        f"a confidence DOWNGRADE by re-derivation and is exactly why byte-identity is the "
        f"wrong contract for this pass.",
        "",
        "| Household | Person on the card | Grades |",
        "| --- | --- | --- |",
    ]
    for row in carried:
        grades = ", ".join(f"{g} × {c}" for g, c in row["grades"].items()) or "—"
        out.append(f"| `{row['household']}` | {row['head'] or '—'} | {grades} |")
    out += [
        "",
        "## 6. Faults",
        "",
    ]
    if doc["faults"]:
        out += ["| Fault | Household | Detail |", "| --- | --- | --- |"]
        for fault in doc["faults"]:
            out.append(f"| `{fault['fault']}` | `{fault['household'] or '—'}` | "
                       f"{fault['detail']} |")
    else:
        out.append("None. The four refusals above all hold on this tree.")
    out += [
        "",
        "Reproduce: `python3 tools/report_convergence_closing.py --check`.",
        "",
    ]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# build / check / self-test
# ---------------------------------------------------------------------------

def write(doc: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report(doc), encoding="utf-8")


def read_committed():
    try:
        return json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        return None


def summary(doc: dict) -> str:
    standing = doc["standing"]
    passes = "; ".join(f"{k} {v['households']}" for k, v in sorted(doc["by_pass"].items()))
    return (f"{standing['households']} households, {standing['persons']} persons, "
            f"{standing['retired']} retired — {passes}")


def faults_report(doc: dict) -> int:
    if not doc["faults"]:
        return 0
    for fault in doc["faults"]:
        print(f"FAULT {fault['fault']}: {fault['household'] or '—'} — {fault['detail']}",
              file=sys.stderr)
    print(f"{len(doc['faults'])} fault(s) — see the four refusals in this tool's docstring",
          file=sys.stderr)
    return 1


def check(quiet: bool = False) -> int:
    doc = build()
    if faults_report(doc):
        return 1
    committed = read_committed()
    if committed is None:
        print(f"MISSING: {OUT.relative_to(ROOT)} — run --build", file=sys.stderr)
        return 1
    if committed != doc:
        drifted = [key for key in sorted(set(doc) | set(committed))
                   if doc.get(key) != committed.get(key)]
        print(f"DRIFT: {OUT.relative_to(ROOT)} no longer re-derives "
              f"({', '.join(drifted)}) — run --build", file=sys.stderr)
        return 1
    if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report(doc):
        print(f"DRIFT: {REPORT.relative_to(ROOT)} no longer re-derives — run --build",
              file=sys.stderr)
        return 1
    if not quiet:
        print(summary(doc))
    return 0


def self_test() -> int:
    """Each rule, held over a fixture, and proved to move when its input moves."""
    failures = []

    def ok(label, condition):
        if condition:
            print(f"  ok   {label}")
        else:
            failures.append(label)
            print(f"  FAIL {label}")

    ok("a card minted by a pass is attributed to it",
       pass_of({"source_pass": "letter_list"}) == "letter_list")
    ok("a card with no pass is `authored`, never a pass named null",
       pass_of({"source_pass": None}) == AUTHORED)
    ok("…and a card missing the field entirely is `authored` too",
       pass_of({}) == AUTHORED)

    survivor = {"id": "hh_inf_cooper_north_04",
                "research_note": "RECONSTRUCTED HOUSEHOLD - fourth of 4 cooper households"}
    core = {"id": "hh_kinzie_john_h",
            "research_note": "THE OLDEST HOUSEHOLD IN THE 1835 TOWN"}
    ok("a card whose note opens RECONSTRUCTED HOUSEHOLD is an invented-name survivor",
       unowned_kind(survivor) == "invented_name_survivor")
    ok("an authored card with a different note is the authored core",
       unowned_kind(core) == "authored_core")
    ok("a card with no note at all is the authored core, not a survivor",
       unowned_kind({"id": "hh_x"}) == "authored_core")
    ok("the two words must OPEN the note, not merely appear in it",
       unowned_kind({"research_note": "This is not a RECONSTRUCTED HOUSEHOLD at all"})
       == "authored_core")

    ok("grades are tallied per person, not per card",
       grades_of({"persons": [{"grade": "attested"}, {"grade": "attested"},
                              {"grade": "inferred"}]})
       == Counter({"attested": 2, "inferred": 1}))
    ok("a card with no persons tallies nothing", grades_of({}) == Counter())

    live_h, live_p = {"hh_a"}, {"a"}
    ok("a redirect onto a live pair arrives",
       redirect_arrives({"merged_into_household": "hh_a", "merged_into_person": "a"},
                        live_h, live_p))
    ok("a redirect onto a household that is not standing does not",
       not redirect_arrives({"merged_into_household": "hh_gone",
                             "merged_into_person": "a"}, live_h, live_p))
    ok("a redirect onto a person who is on no card does not",
       not redirect_arrives({"merged_into_household": "hh_a",
                             "merged_into_person": "gone"}, live_h, live_p))
    ok("a redirect missing either field does not arrive",
       not redirect_arrives({"merged_into_household": "hh_a"}, live_h, live_p)
       and not redirect_arrives({"merged_into_person": "a"}, live_h, live_p))

    # The four refusals, each proved to FIRE — the failure shape a gate exists for is a
    # refusal that has quietly stopped firing, so each is exercised on a broken fixture.
    # The four refusals, each proved to FIRE over an in-memory fixture. The failure shape
    # a gate exists for is a refusal that has quietly stopped firing, so each is exercised
    # on a broken input — and none of it touches a file, because build() takes both.
    def faults_of(doc_: dict, kind: str) -> list:
        return [f for f in doc_["faults"] if f["fault"] == kind]

    def card(hid, source_pass, grades, note=None):
        return {"id": hid, "source_pass": source_pass, "research_note": note,
                "persons": [{"id": f"{hid}_p{i}", "name": f"Person {i}", "grade": g}
                            for i, g in enumerate(grades)]}

    cards = [card("hh_a", "documented", ["attested"]),
             card("hh_b", None, ["inferred"], note="An authored card.")]
    sound = {"counts": {"households": 2, "persons": 2,
                        "by_grade": {"attested": 1, "inferred": 1, "reconstructed": 0},
                        "merged_away": 1},
             "merged": [{"household": "hh_old", "person": "old", "name": "An Old Name",
                         "merged_into_household": "hh_a", "merged_into_person": "hh_a_p0",
                         "rule": "C3", "cluster": "a", "ticket": "T-0000"}]}
    ok("a sound fixture raises no fault", not build(cards, sound)["faults"])

    off_by_one = json.loads(json.dumps(sound))
    off_by_one["counts"]["households"] += 1
    ok("an index whose household count is one out raises index_disagrees",
       faults_of(build(cards, off_by_one), "index_disagrees"))
    off_grade = json.loads(json.dumps(sound))
    off_grade["counts"]["by_grade"]["attested"] += 1
    ok("…and so does one whose grade tally is one out",
       faults_of(build(cards, off_grade), "index_disagrees"))

    dead_end = json.loads(json.dumps(sound))
    dead_end["merged"][0]["merged_into_household"] = "hh_nowhere_at_all"
    ok("a redirect onto no live card raises redirect_does_not_arrive",
       faults_of(build(cards, dead_end), "redirect_does_not_arrive"))

    minted_rc = [card("hh_a", "documented", ["attested", "reconstructed"]), cards[1]]
    rc_index = json.loads(json.dumps(sound))
    rc_index["counts"] = {"households": 2, "persons": 3,
                          "by_grade": {"attested": 1, "inferred": 1, "reconstructed": 1},
                          "merged_away": 1}
    ok("a mint-minted card holding a reconstructed person raises mint_owns_reconstructed",
       faults_of(build(minted_rc, rc_index), "mint_owns_reconstructed"))
    authored_rc = [cards[0], card("hh_b", None, ["inferred", "reconstructed"],
                                  note="An authored card.")]
    ok("…and the same person in an authored card does not, because that is where the "
       "reconstruction programme writes",
       not faults_of(build(authored_rc, rc_index), "mint_owns_reconstructed"))

    fifth = [card("hh_a", "a_fifth_mint", ["attested"]), cards[1]]
    ok("a source_pass outside the closed vocabulary raises unknown_pass rather than being "
       "dropped out of the sum",
       faults_of(build(fifth, sound), "unknown_pass"))

    ok("the committed tree itself raises no fault", not build()["faults"])
    doc = build()

    # The report is a pure function of the table: the same doc must render the same bytes,
    # or --check's report comparison is meaningless.
    ok("the report renders identically from the same table",
       report(doc) == report(json.loads(json.dumps(doc))))

    total = 22
    print(f"self-test: {total - len(failures)}/{total} assertions hold")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(add_help=True, description=__doc__)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", dest="self_test", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.check:
        return check(quiet=args.quiet)
    if args.report:
        print(report(read_committed() or build()), end="")
        return 0
    if args.build:
        doc = build()
        if faults_report(doc):
            return 1
        write(doc)
        print(f"wrote {OUT.relative_to(ROOT)} and {REPORT.relative_to(ROOT)} — "
              f"{summary(doc)}")
        return 0
    print(summary(build()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
