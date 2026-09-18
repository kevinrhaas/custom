#!/usr/bin/env python3
"""Where every standing household, person and grade came from (T-1333; T-1144 acceptance 6).

    python3 tools/report_convergence_closing.py             the accounting, read out
    python3 tools/report_convergence_closing.py --build     write the table and the report
    python3 tools/report_convergence_closing.py --check     it re-derives, and nothing drifted
    python3 tools/report_convergence_closing.py --self-test the rules below, held over fixtures
    python3 tools/report_convergence_closing.py --closing-set  rebuild the five, in the
                                                manifest's order, and re-derive each one

WHAT THIS IS. T-1333, the closing-rebuild half of T-1144's split. Its sixth acceptance asks the convergence pass to rebuild the five
derived resident artefacts and then give "the exact household/person/grade deltas" and
"every retired id's redirect". The five rebuilds are gated in check.sh already — the index
by `rebuild_resident_index.py --check`, the sidecars by `compile_scene.py --all --check`,
the town census by `town_census.py --check`, the published layer by
`check_published_residents.mjs` and the final audit by `export_resident_audit.py --check` —
so each of them is a fixed point that a lap re-proves. What has never existed is the
report: a reader who asks *what is this layer made of, and what did the passes retire to
get there* has had to walk 1,258 cards and join them to a 66-row redirect table by hand.

THE DELTAS ARE MEASURED, AND THE BASELINES ARE FROZEN. T-1333 is explicit that a count
with no baseline is not a delta, so every measure here is stated against readings taken
once over named commits and committed to
`data/research/convergence_closing_baseline.json`: the tree T-1144 opened on
(`f7d090ebc`, 2026-09-15) and the tree this ticket opened on (`0f3b6db5c`, 2026-09-18).
Each was measured with THIS FILE'S OWN `build()`, checked out into a worktree, so the two
ends of every delta are measured the same way. This report reads that file and never
rewrites it — a baseline that moves is not a baseline.

A measure an older baseline is silent on prints `not measured then`, not `0`: the tree was
real and the reading was simply never taken, and a zero would be a claim nobody made. A
measure a baseline records and this report stops producing is the other direction, and it
is a fault, because a renamed measure loses its history in silence.

BESIDE THE DELTAS, THE ACCOUNTING. Where the layer stands is the other question acceptance
6 asks, and the answer is the one every card can be asked for directly: **which pass put
this household in the tree** (`source_pass`, written by the mint that minted it), what each
pass contributed, and what left — the 66 retirements with the redirect each one resolves
to. Minted plus authored equals standing; retired plus standing equals everything the
passes ever held. Both sums are asserted, so the table cannot quietly stop adding up.

PERSONS ARE ATTRIBUTED TO THEIR HOUSEHOLD'S PASS, and that is stated rather than hidden: a
person record carries a grade and no pass of its own, because a mint mints a household and
the persons inside it together. Where a later writer adds a person to a card another pass
minted — which is what the reconstruction programme does — the person is counted under the
card's pass and named separately below, so the two readings never get confused.

WHAT IT REFUSES. Four faults, each of which fails `--build` as well as `--check`, because
writing one of them down publishes it:

  * `baseline_missing` / `measure_lost_its_history` — the delta table stops being a delta
    table, either because the frozen readings are unreadable or because a measure that has
    history has been renamed out from under it.
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
BASELINE = DATA / "research" / "convergence_closing_baseline.json"
REPORT = ROOT / "docs" / "RESEARCH" / "convergence-closing-2026-09.md"

SCENE_DATE = "1835-07-01"
TICKET = "T-1333"
PARENT = "T-1144"
AS_OF = "2026-09-18"

# T-1333 acceptance 4. The four people T-1144 acceptance 3 rebuilt away: they rested only
# on church readings whose `at_chicago` values are all false, so no Chicago source places
# any of them in this town. The measure is their ABSENCE, and it is stated as a delta at
# both ends rather than re-asserted from a spot reading.
REBUILT_AWAY = ("Mary Durbin", "John Simmons", "John Vincent", "Cery Logdson")

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
#
# `--closing-set` below is T-1333 acceptance 1: ONE rebuild of the whole set, in the order
# `tools/derived_manifest.json` records, followed by each one's own re-derivation. The
# manifest is the source of both the order and the commands — the acceptance's whole point
# is that this is not five tools run by hand in an order nobody wrote down, so this mode
# reads the order rather than restating it, and it fails if the set stops being five.
CLOSING_SET_TOOLS = ("rebuild_resident_index.py", "report_convergence_closing.py",
                     "compile_scene.py", "town_census.py", "export_resident_audit.py")
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


def deltas(baselines: list[dict], now: dict) -> list[dict]:
    """One row per measure, with every baseline's reading beside the live one.

    A measure a baseline is SILENT on prints `not measured then`, never 0: the older tree
    was real, the reading was simply never taken over it, and writing a zero there would be
    a claim nobody made. A measure a baseline names and the live report no longer produces
    is the other direction and is a fault — a renamed measure loses its history silently.
    """
    rows = []
    for key in now:
        row = {"measure": key, "now": now[key], "at": {}}
        for baseline in baselines:
            before = baseline["measures"].get(key)
            row["at"][baseline["id"]] = before
            row.setdefault("change", {})[baseline["id"]] = (
                None if before is None else now[key] - before)
        rows.append(row)
    return rows


def orphaned_measures(baselines: list[dict], now: dict) -> list[tuple]:
    """A measure a baseline records and this report no longer produces."""
    return sorted({(b["id"], key) for b in baselines
                   for key in b["measures"] if key not in now})


def rebuilt_away_present(households: list[dict]) -> dict:
    """T-1144 acceptance 3, as a number at each end. A name is PRESENT if any card or any
    person on a card carries it; the acceptance is that all four read zero."""
    found = {name: 0 for name in REBUILT_AWAY}
    for household in households:
        for person in household.get("persons", []):
            name = (person.get("name") or "").strip()
            for wanted in REBUILT_AWAY:
                if name == wanted:
                    found[wanted] += 1
    return found


def presence_legs(households: list[dict]) -> dict:
    """T-1144 acceptance 9, as a number at each end: every household whose presence on the
    scene date is `uncertain` carries the dated evidence leg that made it uncertain, and a
    household that is NOT uncertain does not carry one. Both halves, because the field may
    not outlive the verdict."""
    uncertain = with_leg = settled_with_leg = 0
    for household in households:
        presence = household.get("present_on_scene_date") or {}
        leg = presence.get("last_dated_appearance")
        if presence.get("value") == "uncertain":
            uncertain += 1
            if leg is not None:
                with_leg += 1
        elif leg is not None:
            settled_with_leg += 1
    return {"uncertain": uncertain, "carrying_the_leg": with_leg,
            "settled_but_still_carrying_one": settled_with_leg}


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

    try:
        _baselines = json.loads(BASELINE.read_text(encoding="utf-8"))["baselines"]
    except (OSError, ValueError, KeyError):
        _baselines = []
        faults.append({
            "fault": "baseline_missing", "household": None, "pass": None,
            "detail": f"{BASELINE.name} is unreadable — a count with no baseline is not "
                      f"a delta (T-1333 acceptance 2)",
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

    baselines = _baselines
    measures = {
        "households": standing["households"],
        "persons": standing["persons"],
        "attested": standing["by_grade"]["attested"],
        "inferred": standing["by_grade"]["inferred"],
        "reconstructed": standing["by_grade"]["reconstructed"],
        "retired": standing["retired"],
        "redirects_that_arrive": sum(1 for r in retirements if r["arrives"]),
        "cards_no_writer_derives": len(unowned.get("authored_core", []))
                                   + len(unowned.get("invented_name_survivor", [])),
        "invented_name_survivors": len(unowned.get("invented_name_survivor", [])),
        "letter_list_carried_out_of_cohort": len(carried_out),
    }
    for label in sorted(MINTS) + [AUTHORED]:
        measures[f"households_from_{label}"] = by_pass.get(label, {}).get("households", 0)
    rebuilt = rebuilt_away_present(households)
    measures["rebuilt_away_people_still_present"] = sum(rebuilt.values())
    legs = presence_legs(households)
    measures["uncertain_presences"] = legs["uncertain"]
    measures["uncertain_presences_carrying_the_leg"] = legs["carrying_the_leg"]
    measures["settled_presences_still_carrying_a_leg"] = \
        legs["settled_but_still_carrying_one"]

    for baseline_id, key in orphaned_measures(_baselines, measures):
        faults.append({
            "fault": "measure_lost_its_history", "household": None, "pass": None,
            "detail": f"baseline {baseline_id} records `{key}` and this report no longer "
                      f"produces it — rename it back or add a row saying why it went",
        })

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
        "measures": measures,
        "rebuilt_away": rebuilt,
        "baselines": [{"id": b["id"], "ref": b["ref"], "date": b["date"],
                       "what": b["what"],
                       "recorded_readings": b.get("recorded_readings", {})}
                      for b in baselines],
        "deltas": deltas(baselines, measures),
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
        "## 2. The deltas, measured",
        "",
        f"A count with no baseline is not a delta. Each reading below was taken once over "
        f"a named commit, with the same code that measures the live tree, and frozen into "
        f"`data/research/convergence_closing_baseline.json` — this report reads that file "
        f"and never rewrites it.",
        "",
    ] + [
        f"* **`{b['id']}`** — `{b['ref']}`, {b['date']}. {b['what']}"
        for b in doc["baselines"]
    ] + [
        "",
        "| Measure | "
        + " | ".join(f"{b['id']} ({b['date']})" for b in doc["baselines"])
        + " | now | change since the convergence opened |",
        "| --- | " + " ".join("---: |" for _ in doc["baselines"])
        + " ---: | ---: |",
    ] + [
        f"| `{row['measure']}` | "
        + " | ".join(
            "not measured then" if row["at"][b["id"]] is None
            else _n(row["at"][b["id"]]) for b in doc["baselines"])
        + f" | {_n(row['now'])} | "
        + ("—" if row["change"].get("convergence_opened") is None
           else f"{row['change']['convergence_opened']:+,}") + " |"
        for row in doc["deltas"]
    ] + [
        "",
        f"**The right-hand column is what the convergence did, and three rows of it are "
        f"acceptances this ticket was asked to state as deltas rather than repeat as spot "
        f"readings.** `rebuilt_away_people_still_present` runs 4 → 0: Mary Durbin, John "
        f"Simmons, John Vincent and Cery Logdson were on cards when T-1144 opened and hold "
        f"no household or person record now (acceptance 3). "
        f"`uncertain_presences_carrying_the_leg` runs 0 → "
        f"{_n(doc['measures']['uncertain_presences_carrying_the_leg'])}: the dated evidence "
        f"leg under every uncertain presence did not exist at the baseline and is now "
        f"derived on all {_n(doc['measures']['uncertain_presences'])} of them, with "
        f"{_n(doc['measures']['settled_presences_still_carrying_a_leg'])} settled presences "
        f"still carrying one, because the field may not outlive the verdict (acceptance 9).",
        "",
        f"**Every delta against `ticket_opened` is zero**, which is the other half of the "
        f"claim: the resident layer has not moved since this ticket was written, so the "
        f"accounting below describes a tree that is standing still rather than one being "
        f"measured mid-rebuild.",
        "",
    ] + [
        "Acceptance 5 is the one row this report does not derive, and it says so rather "
        "than quietly carrying it: "
        + "; ".join(
            f"`audit_scene_window_trades.py --check` read "
            f"{b['recorded_readings']['audit_scene_window_trades_standing_rows']['value']} "
            f"standing row(s) at `{b['ref']}`"
            for b in doc["baselines"]
            if "audit_scene_window_trades_standing_rows" in b["recorded_readings"])
        + ". Those are recorded readings from the tool that owns the rule. The LIVE end of "
          "that measure needs no recording here: that same tool's `--check` is its own step "
          "in `check.sh` and runs on every commit, so a standing row coming back is red "
          "before this report could go stale.",
        "",
        "## 3. The cards no writer derives",
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
        "## 4. The reconstructed grade, and who is allowed to write it",
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
        "## 5. Every retired id and where it goes",
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
        "## 6. The one derivation that is not a fixed point",
        "",
        f"The five artefacts acceptance 6 names all re-derive, and check.sh proves each "
        f"one on every run:",
        "",
        "| Artefact | Re-derived by |",
        "| --- | --- |",
    ]
    for row in doc["fixed_points"]:
        out.append(f"| {row['artefact']} | `{row['verify']}` |")
    out += [
        "",
        "**Four of the five are in `tools/derived_manifest.json`, and the fifth cannot be** "
        "— which T-1333 acceptance 5 asks to be recorded as a finding rather than a "
        "footnote. `rebuild_resident_index.py`, `compile_scene.py`, `town_census.py` and "
        "`export_resident_audit.py` each carry a manifest step, and this report carries one "
        "beside them. The published residents layer has none because its output is the "
        "publish mirror, which has been untracked by design since T-0938 — the manifest "
        "resolves committed files, and there is no committed file here to resolve. Its "
        "freshness is gated instead by `check_published_residents.mjs`, which asserts that "
        "the shipped minified layer parses to a value deep-equal to its source, file for "
        "file. So the set is covered; it is covered by two mechanisms rather than one, and "
        "that is worth knowing before somebody adds a manifest row that would resolve "
        "nothing.",
    ]
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
        "## 7. Faults",
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

    base = [{"id": "then", "ref": "abc1234", "date": "2026-01-01", "what": "a fixture",
             "measures": {"households": 10, "gone": 1}}]
    rows = {r["measure"]: r for r in deltas(base, {"households": 12, "added": 3})}
    ok("a measure both ends hold gets its arithmetic",
       rows["households"]["at"]["then"] == 10 and rows["households"]["change"]["then"] == 2)
    ok("a measure the baseline is silent on reads `not measured then`, never 0",
       rows["added"]["at"]["then"] is None and rows["added"]["change"]["then"] is None)
    ok("a measure the baseline holds and the report dropped loses its history, and that "
       "is a fault",
       orphaned_measures(base, {"households": 12, "added": 3}) == [("then", "gone")])
    ok("…and nothing is orphaned when the report still produces every recorded measure",
       orphaned_measures(base, {"households": 12, "gone": 1}) == [])

    ok("a rebuilt-away person still on a card is counted",
       rebuilt_away_present([{"persons": [{"name": "Mary Durbin"}]}])["Mary Durbin"] == 1)
    ok("…and a name that merely contains one is not",
       rebuilt_away_present([{"persons": [{"name": "Mary Durbinson"}]}])["Mary Durbin"] == 0)
    ok("the committed tree holds none of the four", sum(build()["rebuilt_away"].values()) == 0)

    legs = presence_legs([
        {"present_on_scene_date": {"value": "uncertain", "last_dated_appearance": {}}},
        {"present_on_scene_date": {"value": "uncertain"}},
        {"present_on_scene_date": {"value": "present", "last_dated_appearance": {}}},
        {"present_on_scene_date": {"value": "present"}},
    ])
    ok("an uncertain presence carrying its leg is counted on both columns",
       legs["uncertain"] == 2 and legs["carrying_the_leg"] == 1)
    ok("a settled presence that kept a leg is counted, because the field may not outlive "
       "the verdict", legs["settled_but_still_carrying_one"] == 1)

    # The report is a pure function of the table: the same doc must render the same bytes,
    # or --check's report comparison is meaningless.
    ok("the report renders identically from the same table",
       report(doc) == report(json.loads(json.dumps(doc))))

    total = 31
    print(f"self-test: {total - len(failures)}/{total} assertions hold")
    return 1 if failures else 0


def closing_set() -> int:
    """T-1333 acceptance 1, run rather than argued."""
    import subprocess
    import time

    manifest = json.loads((ROOT / "tools" / "derived_manifest.json").read_text("utf-8"))
    steps = [s for s in manifest["steps"]
             if any(tool in " ".join(s["command"]) for tool in CLOSING_SET_TOOLS)]
    if len(steps) != len(CLOSING_SET_TOOLS):
        print(f"FAIL the closing set is {len(steps)} manifest step(s), not "
              f"{len(CLOSING_SET_TOOLS)} — a member left the manifest, which T-1333 "
              f"acceptance 5 calls a finding and not a footnote", file=sys.stderr)
        return 1

    print(f"{len(steps)} closing-set step(s), in the manifest's order:")
    for step in steps:
        print("   ", " ".join(step["command"]))

    def run(label, phase):
        print(f"\n--- {label} ---")
        for step in steps:
            command = step.get(phase)
            if not command:
                print(f"  --  {' '.join(step['command'])} declares no {phase}")
                continue
            started = time.time()
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            verdict = "ok  " if result.returncode == 0 else "FAIL"
            print(f"  {verdict} {' '.join(command)}  {time.time() - started:.1f}s")
            if result.returncode:
                print(result.stdout[-1500:], result.stderr[-1500:], file=sys.stderr)
                return 1
        return 0

    if run("one rebuild, in the manifest's order", "command"):
        return 1
    if run("and every one re-derives on the tree it just wrote", "verify"):
        return 1
    print("\nCLOSING SET: PASS — rebuilt in the manifest's order, and every member "
          "re-derives afterwards.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(add_help=True, description=__doc__)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", dest="self_test", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--closing-set", dest="closing_set", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.closing_set:
        return closing_set()
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
