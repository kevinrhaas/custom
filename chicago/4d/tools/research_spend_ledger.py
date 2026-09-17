#!/usr/bin/env python3
"""Build and validate the closed, unit-level research-spend ledger (T-1143)."""
from __future__ import annotations

import copy
import gzip
import json
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "research" / "domains.json"
LEDGER = ROOT / "data" / "research" / "research_spend_ledger.json.gz"
REPORT = ROOT / "docs" / "RESEARCH" / "research-spend-ledger-2026-09-15.md"
AS_OF = "2026-09-15"

DISPOSITIONS = (
    "asserted", "later_only", "outside_chicago", "aggregate_only", "refused", "unresolved",
)
OPEN_TICKET_STATES = {"open", "claimed", "review", "in-progress"}
STRUCTURED_CONFIDENCE = {"attested", "inferred", "documented"}
NAME_FIELDS = ("normalized", "as_read", "quote")


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def write_json(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_ledger(path: Path = LEDGER):
    try:
        return json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        return None


def write_ledger(path: Path, doc) -> None:
    """Write deterministic compressed JSON; the Markdown report is the review surface."""
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(doc, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))


def pointer_part(value) -> str:
    return str(value).replace("~", "~0").replace("/", "~1")


def resolve_pointer(doc, pointer: str):
    if pointer == "":
        return doc
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise KeyError(pointer)
    node = doc
    for raw in pointer[1:].split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            node = node[int(key)]
        elif isinstance(node, dict):
            node = node[key]
        else:
            raise KeyError(pointer)
    return node


def ticket_states(root: Path = ROOT) -> dict[str, str]:
    states = {}
    for path in sorted((root / "tickets").glob("T-*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        tid = re.search(r"(?m)^id:\s*(T-\d+)\s*$", text)
        state = re.search(r"(?m)^state:\s*([^\s#]+)", text)
        if tid and state:
            states[tid.group(1)] = state.group(1)
    return states


def declared_containers(doc: dict) -> list[str]:
    out = ["records", "claims"]
    if isinstance(doc.get("units_in"), str) and doc["units_in"].strip():
        out.append(doc["units_in"].strip())
    return out


def raw_identifier(row: dict, source_pointer: str) -> str:
    for key in ("id", "person_id", "record_id", "claim_id", "familysearch_id"):
        if row.get(key) is not None:
            return str(row[key])
    return source_pointer


def extract_units(root: Path, registry: dict) -> tuple[list[dict], list[str]]:
    """Return every registered reading unit and every registry fault.

    A file pattern owns rows only through its declared containers. The stable id is
    the row's explicit id where one exists and otherwise its file-relative JSON
    pointer — the rule recorded beside the pattern in domains.json.
    """
    research = root / "data" / "research"
    entries = registry.get("domains") or []
    faults = []
    units = []
    known = {Path(entry.get("path", "")).name for entry in entries}
    present = {p.name for p in research.iterdir() if p.is_dir()}
    for name in sorted(present - known):
        faults.append(f"unregistered research domain: data/research/{name}/")
    for name in sorted(known - present):
        faults.append(f"registered research domain has no directory: data/research/{name}/")

    seen_sources = set()
    for entry in entries:
        domain = entry.get("id")
        domain_dir = root / entry.get("path", "")
        patterns = entry.get("ledger_units")
        if not domain or not isinstance(patterns, list) or not patterns:
            faults.append(f"{domain or '<unnamed>'}: no ledger unit patterns")
            continue
        for pattern in patterns:
            glob = pattern.get("glob")
            containers = pattern.get("containers")
            if not isinstance(glob, str) or not glob:
                faults.append(f"{domain}: ledger pattern has no glob")
                continue
            paths = sorted(p for p in domain_dir.glob(glob) if p.is_file())
            if not paths:
                faults.append(f"{domain}: ledger pattern {glob!r} matches no file")
            for path in paths:
                doc = read_json(path)
                rel = path.relative_to(root).as_posix()
                if not isinstance(doc, dict):
                    faults.append(f"{rel}: registered research file is not a JSON object")
                    continue
                if containers == "$declared" and (
                        "crosswalk" in path.name or doc.get("not_a_reading")):
                    continue
                use = declared_containers(doc) if containers == "$declared" else containers
                if not isinstance(use, list) or not all(isinstance(c, str) for c in use):
                    faults.append(f"{domain} {glob}: containers must be a list or $declared")
                    continue
                for container in use:
                    rows = doc.get(container)
                    if rows is None:
                        continue
                    if not isinstance(rows, list):
                        faults.append(f"{rel}#/{container}: registered unit container is not a list")
                        continue
                    for index, row in enumerate(rows):
                        pointer = f"/{pointer_part(container)}/{index}"
                        if not isinstance(row, dict):
                            faults.append(f"{rel}#{pointer}: research row is not an object")
                            continue
                        name_fields = pattern.get("name_fields")
                        if isinstance(name_fields, list) and not any(row.get(k) for k in name_fields):
                            continue
                        raw_id = raw_identifier(row, pointer)
                        key = f"{domain}:{rel}#{container}/{pointer_part(raw_id)}"
                        source_key = (rel, pointer)
                        if source_key in seen_sources:
                            faults.append(f"{rel}#{pointer}: row matched more than one ledger pattern")
                            continue
                        seen_sources.add(source_key)
                        source_ids = []
                        for candidate in (doc.get("source_id"), doc.get("source_record"),
                                          row.get("source_id")):
                            if isinstance(candidate, str) and candidate:
                                source_ids.append(candidate)
                        for value in (doc.get("source_ids"), row.get("sources")):
                            if isinstance(value, list):
                                source_ids.extend(v for v in value if isinstance(v, str) and v)
                        units.append({
                            "unit_id": key,
                            "domain": domain,
                            "source_file": rel,
                            "source_pointer": pointer,
                            "source_record_id": raw_id,
                            "source_ids": sorted(set(source_ids)),
                            "record": row,
                        })
    units.sort(key=lambda u: u["unit_id"])
    return units, faults


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from strings(value)


def cited_sources(node) -> set[str]:
    found = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "sources" and isinstance(value, list):
                found.update(v for v in value if isinstance(v, str))
            else:
                found.update(cited_sources(value))
    elif isinstance(node, list):
        for value in node:
            found.update(cited_sources(value))
    return found


def target_index(root: Path, raw_ids: set[str]) -> dict[str, list[dict]]:
    """Index source-bearing structured resident assertions by the unit ids they name."""
    found = defaultdict(list)

    def walk(node, parts, root_id, rel):
        if isinstance(node, dict):
            confidence = node.get("confidence")
            sources_here = cited_sources(node) if confidence in STRUCTURED_CONFIDENCE else set()
            if sources_here:
                tokens = set()
                for value in strings(node):
                    if value in raw_ids:
                        tokens.add(value)
                    tokens.update(t for t in re.findall(r"[A-Za-z0-9_.:-]+", value) if t in raw_ids)
                for raw_id in tokens:
                    found[raw_id].append({
                        "kind": "resident_record",
                        "id": root_id,
                        "file": rel,
                        "field_path": "".join("/" + pointer_part(p) for p in parts),
                        "sources": sorted(sources_here),
                    })
            for key, value in node.items():
                walk(value, parts + [key], root_id, rel)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, parts + [index], root_id, rel)

    for path in sorted((root / "data" / "residents").rglob("*.json")):
        doc = read_json(path)
        if not isinstance(doc, dict) or not doc.get("id"):
            continue
        walk(doc, [], str(doc["id"]), path.relative_to(root).as_posix())
    return found


def year_in(row: dict) -> int | None:
    for key in ("describes_date", "event_date", "date", "year"):
        value = row.get(key)
        if isinstance(value, (str, int)):
            match = re.search(r"\b(17\d\d|18\d\d|19\d\d)\b", str(value))
            if match:
                return int(match.group(1))
    return None


def resident_finding(root: Path, unit: dict) -> dict | None:
    name = Path(unit["source_file"]).name
    match = re.match(r"pass_(\d\d)_.*_cohort\.json$", name)
    if not match:
        return None
    path = root / "data" / "research" / "residents" / f"pass_{match.group(1)}_findings.json"
    doc = read_json(path)
    if not isinstance(doc, dict):
        return None
    person = unit["source_record_id"]
    overrides = doc.get("overrides") or {}
    finding = copy.deepcopy(overrides.get(person) or {}) if isinstance(overrides, dict) else {}
    completed = doc.get("completed_person_ids")
    # Passes 2-4 predate the completed array but their whole fixed cohort was reviewed;
    # an absent override is the file's declared default no-find.
    finding["completed"] = (person in completed) if isinstance(completed, list) else True
    finding["default_summary"] = doc.get("default_summary") or "The completed pass recorded no new defensible fact."
    return finding


def classify(root: Path, unit: dict, targets: dict[str, list[dict]]) -> dict:
    row = unit["record"]
    domain = unit["domain"]
    source = f"{unit['source_file']}#{unit['source_pointer']}"

    if domain == "residents":
        name = Path(unit["source_file"]).name
        if name == "scene_window_trade_audit.json":
            # T-1229 emptied this file: the six standing rows became dated pre-scene
            # roles and the audit's population is zero, so nothing classifies here today.
            # The pointer moves off T-1145 because that ticket was SPLIT and a split
            # parent is not an open state — a row arriving tomorrow would have cited a
            # ticket this gate cannot resolve, and said so in a message about a dead
            # pointer rather than about the trade. T-1223 is the open successor that
            # owns what is left of the role migration.
            return {"disposition": "unresolved", "ticket": "T-1223",
                    "reason": "The dated plural-role migration owns this temporal role ruling."}
        if name == "letter_list_reading_suspicions.json":
            return {"disposition": "unresolved", "ticket": "T-1146",
                    "reason": "The structured resident-fact pass owns this surviving name suspicion."}
        finding = resident_finding(root, unit)
        if finding:
            outcome = str(finding.get("outcome") or "no_corroboration")
            if outcome.startswith("no_") or outcome in {"refused", "not_found"}:
                return {"disposition": "refused", "rule": outcome,
                        "evidence": finding.get("summary") or finding["default_summary"]}
            if not finding.get("completed"):
                return {"disposition": "unresolved", "ticket": "T-1146",
                        "reason": "The resident research pass has not completed this reserved person."}
        # The pilot is a reservation without a committed findings file; positive
        # pass findings that have no exact structured target also remain owned here.
        candidates = targets.get(unit["source_record_id"], [])
        for target in candidates:
            if not unit["source_ids"] or set(unit["source_ids"]) & set(target["sources"]):
                target = {k: v for k, v in target.items() if k != "sources"}
                return {"disposition": "asserted", "target": target}
        return {"disposition": "unresolved", "ticket": "T-1146",
                "reason": "No exact source-bearing structured resident field is named yet."}

    if domain == "newberry_index":
        return {"disposition": "refused", "rule": "finding_aid_only",
                "evidence": "A Newberry index card locates a genealogy; it does not attest an 1835 person fact."}
    if domain in {"census_1840", "old_settlers"}:
        return {"disposition": "later_only",
                "reason": "This domain is later evidence and cannot by itself assert an 1835 fact."}
    if row.get("superseded_by"):
        return {"disposition": "refused", "rule": "superseded_reading",
                "evidence": str(row["superseded_by"])}
    if row.get("kind") == "turned_line":
        return {"disposition": "refused", "rule": "continuation_not_subject",
                "evidence": "The printed continuation belongs to the preceding entry and names no new subject."}
    if row.get("outside_chicago") is True or row.get("at_chicago") is False:
        return {"disposition": "outside_chicago", "reason": f"The source row explicitly marks the finding outside Chicago ({source})."}
    year = year_in(row)
    if year is not None and year > 1835:
        return {"disposition": "later_only",
                "reason": f"The unit describes {year}, later than the 1835 scene date."}
    if row.get("town_finding") is False:
        return {"disposition": "aggregate_only",
                "reason": "The committed reading explicitly says it is not a town finding."}

    for target in targets.get(unit["source_record_id"], []):
        if not unit["source_ids"] or set(unit["source_ids"]) & set(target["sources"]):
            target = {k: v for k, v in target.items() if k != "sources"}
            return {"disposition": "asserted", "target": target}

    kind = row.get("kind")
    owner = "T-1147" if kind in {"business", "building", "street", "infrastructure"} else "T-1146"
    reason = ("The place and enterprise completion pass owns this unasserted unit."
              if owner == "T-1147" else
              "The structured resident-fact pass owns this unasserted unit.")
    return {"disposition": "unresolved", "ticket": owner, "reason": reason}


def build_document(root: Path = ROOT) -> tuple[dict, list[str]]:
    registry = read_json(root / "data" / "research" / "domains.json")
    if not isinstance(registry, dict):
        return {}, ["data/research/domains.json is missing or unreadable"]
    units, faults = extract_units(root, registry)
    ids = {unit["source_record_id"] for unit in units}
    targets = target_index(root, ids)
    rows = []
    for unit in units:
        row = {k: unit[k] for k in (
            "unit_id", "domain", "source_file", "source_pointer", "source_record_id")}
        row.update(classify(root, unit, targets))
        rows.append(row)
    by_domain = defaultdict(Counter)
    for row in rows:
        by_domain[row["domain"]][row["disposition"]] += 1
    totals = Counter(row["disposition"] for row in rows)
    doc = {
        "schema": 1,
        "as_of": AS_OF,
        "generated_by": "tools/measure_research_spend.py --ledger-build",
        "dispositions": list(DISPOSITIONS),
        "unit_count": len(rows),
        "totals": {name: totals[name] for name in DISPOSITIONS},
        "domains": {
            domain: {name: counts[name] for name in DISPOSITIONS}
            for domain, counts in sorted(by_domain.items())
        },
        "units": rows,
    }
    return doc, faults


def validate_document(doc: dict, root: Path = ROOT,
                      states: dict[str, str] | None = None) -> list[str]:
    faults = []
    states = ticket_states(root) if states is None else states
    rows = doc.get("units") if isinstance(doc, dict) else None
    if not isinstance(rows, list):
        return ["ledger has no units array"]
    seen = set()
    json_cache = {}

    def cached(relative):
        key = str(relative or "")
        if key not in json_cache:
            json_cache[key] = read_json(root / key)
        return json_cache[key]

    for index, row in enumerate(rows):
        where = f"ledger unit {index}"
        if not isinstance(row, dict):
            faults.append(f"{where}: is not an object")
            continue
        uid = row.get("unit_id")
        where = str(uid or where)
        if not uid:
            faults.append(f"{where}: has no stable unit_id")
        elif uid in seen:
            faults.append(f"{where}: duplicate unit_id")
        seen.add(uid)
        disposition = row.get("disposition")
        if disposition not in DISPOSITIONS:
            faults.append(f"{where}: unclassified disposition {disposition!r}")
            continue
        source_doc = cached(row.get("source_file"))
        if not isinstance(source_doc, dict):
            faults.append(f"{where}: source file is missing or unreadable: {row.get('source_file')}")
        else:
            try:
                resolve_pointer(source_doc, row.get("source_pointer"))
            except (KeyError, IndexError, TypeError, ValueError):
                faults.append(f"{where}: source pointer is dead: {row.get('source_pointer')}")
        if disposition == "asserted":
            target = row.get("target")
            if not isinstance(target, dict):
                faults.append(f"{where}: asserted row names no target")
                continue
            target_doc = cached(target.get("file"))
            if not isinstance(target_doc, dict) or target_doc.get("id") != target.get("id"):
                faults.append(f"{where}: asserted target is dead or its id does not agree")
                continue
            try:
                field = resolve_pointer(target_doc, target.get("field_path"))
            except (KeyError, IndexError, TypeError, ValueError):
                faults.append(f"{where}: asserted field_path is dead")
                continue
            if not isinstance(field, dict) or field.get("confidence") not in STRUCTURED_CONFIDENCE:
                faults.append(f"{where}: asserted fact exists only in prose or lacks attested/inferred confidence")
            if not cited_sources(field):
                faults.append(f"{where}: asserted structured field names no source")
        elif disposition == "unresolved":
            ticket = row.get("ticket")
            if states.get(ticket) not in OPEN_TICKET_STATES:
                faults.append(f"{where}: unresolved ticket {ticket!r} is missing or not open")
            if not str(row.get("reason") or "").strip():
                faults.append(f"{where}: unresolved row gives no reason")
        elif disposition == "refused":
            if not str(row.get("rule") or "").strip() or not str(row.get("evidence") or "").strip():
                faults.append(f"{where}: refusal must name both rule and evidence")
        elif not str(row.get("reason") or "").strip():
            faults.append(f"{where}: {disposition} row gives no reason")
    counts = Counter(row.get("disposition") for row in rows if isinstance(row, dict))
    if doc.get("unit_count") != len(rows):
        faults.append("ledger unit_count does not equal its rows")
    if doc.get("totals") != {name: counts[name] for name in DISPOSITIONS}:
        faults.append("ledger disposition totals do not equal its rows")
    return faults


def report_text(doc: dict, legacy_rows: list[dict]) -> str:
    before_read = sum(row["read"] for row in legacy_rows)
    before_spent = sum(row["spent"] for row in legacy_rows)
    before_unspent = sum(row["unspent"] for row in legacy_rows)
    reached = sum(row["reached"] for row in legacy_rows)
    wrote = sum(row["wrote"] for row in legacy_rows)
    unwritten = sum(row["unwritten"] for row in legacy_rows)
    unsourced = sum(row["unsourced"] for row in legacy_rows)
    out = [
        "# Closed research-spend ledger — 2026-09-15", "",
        "Generated by `tools/measure_research_spend.py --ledger-build`. The compressed JSON "
        "ledger is the machine-readable authority; this report is its review surface.", "",
        "## Before and after", "",
        "| Measure | Before T-1143 | Closed ledger |", "| --- | ---: | ---: |",
        f"| Research units in the legacy read/spent measure | {before_read:,} | {before_read:,} |",
        f"| Legacy spend rulings | {before_spent:,} | {before_spent:,} |",
        f"| Legacy units without a spend ruling | {before_unspent:,} | dispositioned below |",
        f"| All registered reading units | not closed | {doc['unit_count']:,} |",
        f"| Unclassified registered units | not measured | 0 |", "",
        "The historical read/spent comparison remains unchanged so new accounting cannot "
        "launder its backlog. The closed ledger adds the durable outcome for every registered "
        "unit, including newspapers, Genealogy Trails, and resident research passes.", "",
        "## Dispositions by domain", "",
        "| Domain | Asserted | Later only | Outside Chicago | Aggregate only | Refused | Unresolved | Total |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for domain, counts in doc["domains"].items():
        total = sum(counts.values())
        out.append(f"| {domain} | {counts['asserted']:,} | {counts['later_only']:,} | "
                   f"{counts['outside_chicago']:,} | {counts['aggregate_only']:,} | "
                   f"{counts['refused']:,} | {counts['unresolved']:,} | {total:,} |")
    totals = doc["totals"]
    out.append(f"| **Total** | **{totals['asserted']:,}** | **{totals['later_only']:,}** | "
               f"**{totals['outside_chicago']:,}** | **{totals['aggregate_only']:,}** | "
               f"**{totals['refused']:,}** | **{totals['unresolved']:,}** | "
               f"**{doc['unit_count']:,}** |")
    out += ["", "## Second-hop preservation", "",
            f"The pre-ledger resident-card measure is preserved: **{reached:,}** rulings reach "
            f"a town person, **{wrote:,}** are on a card, **{unwritten:,}** are unwritten, "
            f"and **{unsourced:,}** state no source.", "", "## Unresolved ownership", "",
            "Only tickets whose current state is open may own an unresolved unit.", "",
            "| Ticket | Units |", "| --- | ---: |"]
    unresolved = Counter(row["ticket"] for row in doc["units"]
                         if row["disposition"] == "unresolved")
    for ticket, count in sorted(unresolved.items()):
        out.append(f"| {ticket} | {count:,} |")
    out += ["", "Nonzero `later_only`, `outside_chicago`, `aggregate_only`, and `refused` "
            "counts are closed decisions, not missing work. The gate fails only when a unit "
            "is unclassified, an asserted target dies, an unresolved owner closes or "
            "disappears, or an assertion survives only as prose.", ""]
    return "\n".join(out)


def build(legacy_rows: list[dict], root: Path = ROOT) -> list[str]:
    doc, faults = build_document(root)
    faults.extend(validate_document(doc, root))
    if faults:
        return faults
    write_ledger(root / LEDGER.relative_to(ROOT), doc)
    report = root / REPORT.relative_to(ROOT)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(report_text(doc, legacy_rows), encoding="utf-8")
    return []


def check(legacy_rows: list[dict], root: Path = ROOT) -> list[str]:
    expected, faults = build_document(root)
    ledger = read_ledger(root / LEDGER.relative_to(ROOT))
    if not isinstance(ledger, dict):
        return faults + ["closed research-spend ledger is missing or unreadable"]
    faults.extend(validate_document(ledger, root))
    if ledger != expected:
        faults.append("closed research-spend ledger is stale — run --ledger-build")
    report = root / REPORT.relative_to(ROOT)
    if not report.exists() or report.read_text(encoding="utf-8") != report_text(expected, legacy_rows):
        faults.append("research-spend report is stale — run --ledger-build")
    return faults


def self_test() -> int:
    """Mutate one green row in memory and prove each closure assertion fires."""
    failures = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        source = root / "data/research/civic/records/fixture.json"
        target = root / "data/residents/hh_fixture.json"
        write_json(source, {"records": [{"id": "r1", "normalized": "One"}]})
        write_json(target, {"id": "hh_fixture", "facts": [{
            "value": "One", "confidence": "attested", "sources": ["fixture_source"]}]})
        base = {"unit_id": "civic:r1", "domain": "civic",
                "source_file": "data/research/civic/records/fixture.json",
                "source_pointer": "/records/0", "source_record_id": "r1",
                "disposition": "asserted", "target": {"kind": "resident_record",
                    "id": "hh_fixture", "file": "data/residents/hh_fixture.json",
                    "field_path": "/facts/0"}}

        def run(label, mutate, want, states=None):
            row = copy.deepcopy(base)
            mutate(row)
            doc = {"units": [row], "unit_count": 1,
                   "totals": {name: int(row.get("disposition") == name) for name in DISPOSITIONS}}
            got = validate_document(doc, root, states or {})
            if not any(want in fault for fault in got):
                failures.append(f"{label}: expected {want!r}, got {got!r}")
            else:
                print(f"  fires: {label}")

        run("an unclassified unit", lambda r: r.pop("disposition"), "unclassified")
        run("a dead asserted target", lambda r: r["target"].update(file="data/residents/nope.json"),
            "target is dead")
        run("an assertion left only in prose", lambda r: r["target"].update(field_path="/id"),
            "only in prose")
        run("an unresolved unit owned by a closed ticket",
            lambda r: (r.update(disposition="unresolved", ticket="T-1", reason="fixture"),
                       r.pop("target")), "missing or not open", {"T-1": "closed"})
        duplicate = {"units": [base, copy.deepcopy(base)], "unit_count": 2,
                     "totals": {name: (2 if name == "asserted" else 0) for name in DISPOSITIONS}}
        got = validate_document(duplicate, root, {})
        if not any("duplicate unit_id" in fault for fault in got):
            failures.append("duplicate unit id did not fire")
        else:
            print("  fires: a duplicate stable unit id")
    for failure in failures:
        print("   SILENT: " + failure)
    print("LEDGER SELF-TEST %s — 5 case(s)" % ("FAIL" if failures else "PASS"))
    return 1 if failures else 0
