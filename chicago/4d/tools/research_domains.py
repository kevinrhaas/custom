#!/usr/bin/env python3
"""One home and one gate for the six source domains beside the newspapers.

    tools/research_domains.py --build       write/normalise each domain's scaffold
    tools/research_domains.py --check       the gate
    tools/research_domains.py --self-test   the gate's assertions still fire when broken

WHAT THIS IS FOR. The project has exactly one research pipeline that works — the
newspapers' — and its shape is the reason it works: a register that says where a
passage IS, hand-authored claims that say what was read out of it, a CLOSED kind
vocabulary, a required reading grade, verbatim quotes the gate rebuilds out of the
committed text, a coverage declaration, and an identity layer that declares its
refusals as carefully as its merges.

Six more domains are about to be read in parallel — the civic lists, the 1830
census, the 1840 census, a church register, books and directories — by ten runs
that cannot see each other. If each invents its own file shape, the consolidation
(T-0513) spends its whole run re-reading ten dialects, and the refusals nobody
wrote down have to be made again. So the shape is fixed HERE, before the sweep
starts, and this file is the gate that holds it.

TWO SHAPES, AND THE DIFFERENCE IS THE SOURCE AND NOT THE DOMAIN.

  records — for a LIST. A voter roll, a census line, a baptism entry, a directory
            entry: one printed row, read as it stands (`as_read`) and again as this
            project spells it (`normalized`). A row is not a claim about the town;
            it is a claim about what the page says.

  claims  — for PROSE. A book paragraph that says something about 1835 Chicago.
            Same shape as the newspaper claims, because it is the same act: a
            `kind`, a verbatim `quote`, a `normalized` reading, the `entities` it
            names, and `town_finding` for whether it bears on the reconstruction at
            all — the reminiscence that is only about the author is worth recording
            and is not worth placing.

A domain may hold both. `books` and `directories` are the two the verbatim-quote
gate binds, because they are the two whose text this repo commits.

`data/research/` IS RESEARCH, NOT PAYLOAD, and this subtree inherits that: nothing
here is published, `tools/publish.sh` does not copy it, and
`tools/newspaper_corpus.py --check` already asserts the whole of `data/research/`
stays out of `site/chicago/4d/`.

NOTHING IN HERE AUTHORS A READING. --build writes empty scaffolds and a manifest;
the claims and the records are hand-authored, one ticket at a time, by the runs
this file exists to make consistent.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # chicago/4d
RESEARCH = ROOT / "data" / "research"
SOURCES = ROOT / "data" / "sources"
MANIFEST = RESEARCH / "domains.json"

SCHEMA_VERSION = 1

# The six domains, in the order the owner named them, with what each is FOR. The
# order is the manifest's order and the READMEs' order; it is not alphabetical on
# purpose, because "civic first, books last" is the reading order too.
DOMAINS = {
    "civic": {
        "title": "Civic lists",
        "holds": "records",
        "what": "The town's own lists of its own people — the poll books and voter "
                "rolls of 1833-1835, and the officers, jurors and subscribers printed "
                "beside them.",
    },
    "census_1830": {
        "title": "The 1830 federal census",
        "holds": "records",
        "what": "Chicago was enumerated in Peoria County in 1830. The named schedule "
                "is the object; the county aggregates this project already holds are "
                "not it.",
    },
    "census_1840": {
        "title": "The 1840 federal census",
        "holds": "records",
        "what": "Seventy-five page images and a head-of-household index. 1840 is "
                "LATER EVIDENCE and never an 1835 household fact on its own.",
    },
    "church": {
        "title": "Church registers",
        "holds": "records",
        "what": "Baptisms, marriages and burials — St Mary's 1833-1835 first, because "
                "eleven images of its register are already deposited and unread.",
    },
    "books": {
        "title": "Books and reminiscences",
        "holds": "claims",
        "what": "Prose: Fergus' Historical Series, Hubbard's autobiography, H. H. "
                "Porter's Short Autobiography, and the memoirs printed beside them.",
    },
    "directories": {
        "title": "Directories",
        "holds": "claims",
        "what": "The 1839 Chicago directory and its successors — entry by entry, "
                "structured, and crosswalked rather than quoted at second hand.",
    },
    # The seventh, added by T-0562 when the owner put the Newberry Library's
    # genealogical index on the Internet Archive. It is not one of his six original
    # domains and it is not a source of facts at all: it is a FINDING AID, and it
    # earns a domain here because it is list-shaped, it is large, and the one thing
    # it must never do — put a surname behind a person — is a thing only a gate can
    # stop. `tools/read_newberry_index.py --check` is that gate; this entry is what
    # makes the records, the coverage and the crosswalk answer to this one too.
    "newberry_index": {
        "title": "The Newberry genealogical index",
        "holds": "records",
        "what": "A four-volume photostat of the Newberry Library's genealogical card "
                "index (G. K. Hall, 1960), read for the cards whose citation names "
                "Chicago, Cook County or Illinois. A card says where a genealogy IS; "
                "it never places a person, and nothing here may grade one.",
    },
}

# The claim vocabulary is closed. An open one becomes a synonym list within a week
# and then nothing can be compiled from it — the same reason `compile_gazetteer.py`
# closes the newspapers'. These are the newspapers' nine, plus four the new domains
# need and the papers never did: `landscape` for what a reminiscence says the ground
# looked like, `appearance` for what a building or a person looked like, `household`
# for a census line's composition, and `civic` for an office, a poll or an ordinance.
KINDS = ("person", "business", "building", "street", "infrastructure",
         "event", "shipping", "price", "notice",
         "landscape", "appearance", "household", "civic")

# Ruling 2, unchanged from the papers. `transcription_mediated` is a reading made
# through somebody else's transcription; `scan_verified` is a reading made off the
# page image itself and OUTRANKS it. There is no third value, and the field is
# required — a reading whose grade is unstated is the one that gets cited as though
# it were the stronger one.
READINGS = ("transcription_mediated", "scan_verified")

# What a record row may claim about itself. Deliberately the confidence vocabulary
# the rest of the project uses, so a row can be promoted into a resident record
# without a translation step.
CONFIDENCES = ("documented", "inferred", "conjectural")

RECORD_FIELDS = ("id", "as_read", "normalized", "locator", "reading", "confidence", "notes")
CLAIM_FIELDS = ("id", "kind", "reading", "quote", "normalized", "locator",
                "describes_date", "entities", "town_finding", "notes")

# A coverage declaration says WHAT WAS READ, in the units the source is delivered
# in. An undeclared item is not read yet, which is not a fault and must never be
# reported as one; a DECLARED item nothing reaches is a hole, and that is the whole
# point of the file.
COVERAGE_UNITS = ("list", "image", "page")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def surname_only(name: str) -> bool:
    """True when a name carries nothing but a surname.

    The 1835 lists are full of families and a bare surname separates none of them,
    so a merge on one is always a refusal — the same rule `identity.json` states
    for two read initials that disagree, one step further down.
    """
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    parts = [p for p in parts if p.lower() not in ("mr", "mr.", "mrs", "mrs.", "miss", "dr", "dr.")]
    return len(parts) < 2


def source_ids(sources: Path) -> set:
    ids = set()
    if not sources.exists():
        return ids
    for path in sorted(sources.glob("*.json")):
        try:
            doc = load(path)
        except Exception:
            continue
        if isinstance(doc, dict) and doc.get("id"):
            ids.add(str(doc["id"]))
    return ids


def coverage_key(unit: str, item) -> str:
    return "%s:%s" % (unit, item)


def locator_reached(locator: dict) -> list:
    """The coverage keys a locator reaches. One locator may reach exactly one item."""
    if not isinstance(locator, dict):
        return []
    keys = []
    for unit in COVERAGE_UNITS:
        if locator.get(unit) is not None:
            keys.append(coverage_key(unit, locator[unit]))
    return keys


def rebuild_quote(domain_dir: Path, locator: dict):
    """Reassemble a claim's quote out of the domain's committed text.

    Returns (text, error). The rules are the newspapers': `lines` is an inclusive
    [first, last] pair of 1-based line numbers into `text_file`, and `spans` — for
    the case where a segmenter wove two columns into one line — names the exact
    substring taken from each. Never smoothed: the smoothed reading has a field of
    its own to live in, and it is `normalized`.
    """
    rel = locator.get("text_file")
    if not rel:
        return None, "names no text_file"
    path = domain_dir / "text" / rel
    if not path.exists():
        return None, "names text_file %r, which is not committed" % rel
    lines = path.read_text(encoding="utf-8").splitlines()
    spans = locator.get("spans")
    if spans:
        out = []
        for span in spans:
            n = int(span.get("line", 0))
            if n < 1 or n > len(lines):
                return None, "span names line %d, which %s does not have" % (n, rel)
            out.append(lines[n - 1][int(span["from"]):int(span["to"])])
        return "\n".join(out), None
    pair = locator.get("lines")
    if not pair or len(pair) != 2:
        return None, "names neither spans nor a [first, last] lines pair"
    first, last = int(pair[0]), int(pair[1])
    if first < 1 or last < first or last > len(lines):
        return None, "names lines %d-%d, which %s does not have" % (first, last, rel)
    return "\n".join(lines[first - 1:last]), None


def check_crosswalk(doc, label: str, bad: list) -> None:
    """`crosswalk.json` is `identity.json`'s shape, and it is held to its rules.

    A merge needs a written rule; the rule must name BOTH spellings verbatim, so it
    reads back without the code; a surname-only merge is refused however good the
    rule is; and a refusal is declared as explicitly as a merge, naming both
    spellings, because the ABSENCE of a merge reads exactly like a pair nobody has
    looked at yet and the next sweep does the work again.
    """
    for i, merge in enumerate(doc.get("merges") or []):
        where = "%s merge %d" % (label, i)
        into, frm = str(merge.get("into") or ""), str(merge.get("from") or "")
        if not into or not frm:
            bad.append("%s: a merge names fewer than two spellings" % where)
            continue
        rule = str(merge.get("rule") or "")
        if not rule.strip():
            bad.append("%s: a merge with no rule — %r into %r" % (where, frm, into))
            continue
        if into not in rule or frm not in rule:
            bad.append("%s: the merge rule does not name both spellings verbatim — "
                       "%r into %r" % (where, frm, into))
        if surname_only(into) or surname_only(frm):
            bad.append("%s: a surname-only merge is always a refusal — %r into %r"
                       % (where, frm, into))
        if not (merge.get("evidence") or []):
            bad.append("%s: a merge with no evidence[] — %r into %r" % (where, frm, into))
    for i, refusal in enumerate(doc.get("refusals") or []):
        where = "%s refusal %d" % (label, i)
        a, b = str(refusal.get("a") or ""), str(refusal.get("b") or "")
        if not a or not b:
            bad.append("%s: a refusal naming only one spelling — %r against %r" % (where, a, b))
            continue
        rule = str(refusal.get("rule") or "")
        if not rule.strip():
            bad.append("%s: a refusal with no rule — %r against %r" % (where, a, b))
            continue
        if a not in rule or b not in rule:
            bad.append("%s: the refusal rule does not name both spellings verbatim — "
                       "%r against %r" % (where, a, b))
        if not (refusal.get("evidence") or []):
            bad.append("%s: a refusal with no evidence[] — %r against %r" % (where, a, b))


def check_domain(name: str, spec: dict, research: Path, known_sources: set, bad: list) -> dict:
    domain_dir = research / name
    counts = {"records": 0, "claims": 0, "declared": 0}
    if not domain_dir.exists():
        bad.append("%s: the domain has no directory — run --build" % name)
        return counts
    if not (domain_dir / "README.md").exists():
        bad.append("%s: no README.md — every domain says in prose what is hand-authored "
                   "here and what is generated" % name)

    coverage_path = domain_dir / "coverage.json"
    declared = {}
    if not coverage_path.exists():
        bad.append("%s: no coverage.json — a reading pass declares the range it read" % name)
    else:
        cov = load(coverage_path)
        for i, dec in enumerate(cov.get("declarations") or []):
            unit = dec.get("unit")
            if unit not in COVERAGE_UNITS:
                bad.append("%s coverage %d: unit %r is outside %s"
                           % (name, i, unit, list(COVERAGE_UNITS)))
                continue
            if not dec.get("ticket"):
                bad.append("%s coverage %d: a declaration with no ticket" % (name, i))
            for item in dec.get("items") or []:
                declared[coverage_key(unit, item)] = dec.get("ticket") or "?"
    counts["declared"] = len(declared)

    reached = set()

    for path in sorted((domain_dir / "records").glob("*.json")) if (domain_dir / "records").exists() else []:
        doc = load(path)
        label = "%s/records/%s" % (name, path.name)
        sid = doc.get("source_id")
        if not sid:
            bad.append("%s: names no source_id" % label)
        elif known_sources and sid not in known_sources:
            bad.append("%s: cites source id %r, which names no source record" % (label, sid))
        seen = set()
        for row in doc.get("records") or []:
            counts["records"] += 1
            rid = row.get("id")
            where = "%s %s" % (label, rid or "<no id>")
            for field in RECORD_FIELDS:
                if field not in row:
                    bad.append("%s: a record with no %s" % (where, field))
            if rid in seen:
                bad.append("%s: duplicate record id" % where)
            seen.add(rid)
            if row.get("reading") not in READINGS:
                bad.append("%s: reading %r is outside %s"
                           % (where, row.get("reading"), list(READINGS)))
            if row.get("confidence") not in CONFIDENCES:
                bad.append("%s: confidence %r is outside %s"
                           % (where, row.get("confidence"), list(CONFIDENCES)))
            reached.update(locator_reached(row.get("locator") or {}))

    for path in sorted((domain_dir / "claims").glob("*.json")) if (domain_dir / "claims").exists() else []:
        doc = load(path)
        label = "%s/claims/%s" % (name, path.name)
        sid = doc.get("source_id")
        if not sid:
            bad.append("%s: names no source_id" % label)
        elif known_sources and sid not in known_sources:
            bad.append("%s: cites source id %r, which names no source record" % (label, sid))
        seen = set()
        for claim in doc.get("claims") or []:
            counts["claims"] += 1
            cid = claim.get("id")
            where = "%s %s" % (label, cid or "<no id>")
            for field in CLAIM_FIELDS:
                if field not in claim:
                    bad.append("%s: a claim with no %s" % (where, field))
            if cid in seen:
                bad.append("%s: duplicate claim id" % where)
            seen.add(cid)
            if claim.get("kind") not in KINDS:
                bad.append("%s: kind %r is outside the closed vocabulary %s"
                           % (where, claim.get("kind"), list(KINDS)))
            if claim.get("reading") not in READINGS:
                bad.append("%s: reading %r is outside %s"
                           % (where, claim.get("reading"), list(READINGS)))
            if not isinstance(claim.get("town_finding"), bool):
                bad.append("%s: town_finding is not a boolean" % where)
            locator = claim.get("locator") or {}
            reached.update(locator_reached(locator))
            # The verbatim gate, and it binds the two domains whose text this repo
            # commits. A tidied quote is invisible to every other check here.
            if spec["holds"] == "claims":
                rebuilt, err = rebuild_quote(domain_dir, locator)
                if err:
                    bad.append("%s: %s" % (where, err))
                elif rebuilt != claim.get("quote"):
                    bad.append("%s: the quote is not what the committed text says at "
                               "that locator" % where)

    for key, ticket in sorted(declared.items()):
        if key not in reached:
            bad.append("%s: coverage hole — %s is declared read by %s and nothing in "
                       "the domain reaches it" % (name, key, ticket))
    return counts


def build(research: Path = RESEARCH, sources: Path = SOURCES, quiet: bool = False) -> int:
    """Write the scaffold. Idempotent, and it never overwrites a hand-authored file."""
    for name, spec in DOMAINS.items():
        d = research / name
        (d / "records").mkdir(parents=True, exist_ok=True)
        (d / "claims").mkdir(parents=True, exist_ok=True)
        (d / "text").mkdir(parents=True, exist_ok=True)
        for sub in ("records", "claims", "text"):
            keep = d / sub / ".gitkeep"
            if not keep.exists():
                keep.write_text("", encoding="utf-8")
        cov = d / "coverage.json"
        if not cov.exists():
            dump(cov, {
                "schema": SCHEMA_VERSION,
                "domain": name,
                "generated_by": "hand — a reading pass declares the range it read, and "
                                "the gate checks it",
                "note": "An UNDECLARED item is not read yet and is not a fault. A "
                        "DECLARED item nothing reaches is a hole, and that is what "
                        "this file is for.",
                "declarations": [],
            })
        cross = d / "crosswalk.json"
        if not cross.exists():
            dump(cross, {
                "schema": SCHEMA_VERSION,
                "domain": name,
                "note": "The ONLY place two differently-spelled names in this domain may "
                        "become one person, in data/research/newspapers/identity.json's "
                        "shape and under its rules: a merge needs a rule, the rule names "
                        "BOTH spellings verbatim, and a surname-only merge is always a "
                        "refusal. A refusal is declared as explicitly as a merge — the "
                        "absence of one reads like a pair nobody has looked at yet.",
                "passes": [],
                "merges": [],
                "refusals": [],
            })
    manifest = {
        "schema": SCHEMA_VERSION,
        "_doc": "GENERATED by tools/research_domains.py --build. The six source domains "
                "beside the newspapers, their shape and their home. Hand-edit and the "
                "gate says so.",
        "generated_by": "tools/research_domains.py --build",
        "kinds": list(KINDS),
        "readings": list(READINGS),
        "confidences": list(CONFIDENCES),
        "coverage_units": list(COVERAGE_UNITS),
        "record_fields": list(RECORD_FIELDS),
        "claim_fields": list(CLAIM_FIELDS),
        "domains": [
            {"id": name, "title": spec["title"], "holds": spec["holds"], "what": spec["what"],
             "path": "data/research/%s/" % name}
            for name, spec in DOMAINS.items()
        ],
    }
    dump(research / "domains.json", manifest)
    if not quiet:
        print("research domains: %d scaffolded, manifest written" % len(DOMAINS))
    return 0


def check(research: Path = RESEARCH, sources: Path = SOURCES, quiet: bool = False) -> list:
    bad = []
    known = source_ids(sources)
    totals = {"records": 0, "claims": 0, "declared": 0}
    for name, spec in DOMAINS.items():
        counts = check_domain(name, spec, research, known, bad)
        for k in totals:
            totals[k] += counts[k]
        cross = research / name / "crosswalk.json"
        if not cross.exists():
            bad.append("%s: no crosswalk.json — the identity layer is declared before "
                       "it is needed, not after" % name)
        else:
            check_crosswalk(load(cross), "%s/crosswalk.json" % name, bad)

    manifest_path = research / "domains.json"
    if not manifest_path.exists():
        bad.append("data/research/domains.json is missing — run --build")
    else:
        want = json.loads(json.dumps({
            "schema": SCHEMA_VERSION,
            "kinds": list(KINDS), "readings": list(READINGS),
            "confidences": list(CONFIDENCES), "coverage_units": list(COVERAGE_UNITS),
            "record_fields": list(RECORD_FIELDS), "claim_fields": list(CLAIM_FIELDS),
            "domains": [{"id": n, "title": s["title"], "holds": s["holds"],
                         "what": s["what"], "path": "data/research/%s/" % n}
                        for n, s in DOMAINS.items()],
        }))
        got = load(manifest_path)
        if {k: got.get(k) for k in want} != want:
            bad.append("data/research/domains.json is stale or hand-edited; "
                       "regenerate it with --build")

    if not quiet:
        for b in bad:
            print("  FAIL  " + b)
        print("  %d domain(s); %d record(s), %d claim(s), %d declared coverage item(s)"
              % (len(DOMAINS), totals["records"], totals["claims"], totals["declared"]))
    return bad


# --------------------------------------------------------------------------- #
# The self-test. Every assertion above is broken on a synthetic tree and must be
# reported; an assertion that has quietly stopped firing is worse than no
# assertion, because the file it guards looks checked.
# --------------------------------------------------------------------------- #

FIXTURE_TEXT = "the town was then a mere hamlet\nand the river ran black with mud\n"

FIXTURE_CLAIM = {
    "id": "c001",
    "kind": "landscape",
    "reading": "transcription_mediated",
    "quote": "the town was then a mere hamlet",
    "normalized": "The town was then a mere hamlet.",
    "locator": {"text_file": "fixture.txt", "lines": [1, 1], "page": 7},
    "describes_date": "1835",
    "entities": [],
    "town_finding": True,
    "notes": "fixture",
}

FIXTURE_RECORD = {
    "id": "r001",
    "as_read": "Jno. Kinzie",
    "normalized": "John Kinzie",
    "locator": {"list": "poll_1835", "line": 12},
    "reading": "scan_verified",
    "confidence": "documented",
    "notes": "fixture",
}


def _fixture(tmp: Path) -> Path:
    """A minimal but GREEN tree: one records domain, one claims domain, both covered."""
    research = tmp / "research"
    build(research=research, sources=tmp / "sources", quiet=True)
    # The six READMEs are hand-authored — --build deliberately does not write one,
    # because a stub that says nothing is worse than a missing page the gate names.
    for name in DOMAINS:
        (research / name / "README.md").write_text("fixture\n", encoding="utf-8")
    (tmp / "sources").mkdir(parents=True, exist_ok=True)
    dump(tmp / "sources" / "fixture_source.json", {"id": "fixture_source"})

    civic = research / "civic"
    dump(civic / "records" / "poll_1835.json", {
        "schema": 1, "domain": "civic", "source_id": "fixture_source",
        "records": [copy.deepcopy(FIXTURE_RECORD)],
    })
    dump(civic / "coverage.json", {
        "schema": 1, "domain": "civic", "generated_by": "fixture",
        "declarations": [{"unit": "list", "items": ["poll_1835"], "ticket": "T-9999"}],
    })

    books = research / "books"
    (books / "text").mkdir(parents=True, exist_ok=True)
    (books / "text" / "fixture.txt").write_text(FIXTURE_TEXT, encoding="utf-8")
    dump(books / "claims" / "fixture.json", {
        "schema": 1, "domain": "books", "source_id": "fixture_source",
        "claims": [copy.deepcopy(FIXTURE_CLAIM)],
    })
    dump(books / "coverage.json", {
        "schema": 1, "domain": "books", "generated_by": "fixture",
        "declarations": [{"unit": "page", "items": [7], "ticket": "T-9999"}],
    })
    return research


def self_test() -> int:
    failures = []
    cases = 0

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        research = _fixture(tmp)
        bad = check(research=research, sources=tmp / "sources", quiet=True)
        if bad:
            print("FAIL: the green fixture is not green: %r" % bad, file=sys.stderr)
            return 1

    def run(mutate, want, label):
        nonlocal cases
        cases += 1
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            research = _fixture(tmp)
            mutate(research, tmp)
            bad = check(research=research, sources=tmp / "sources", quiet=True)
        if not any(want in b for b in bad):
            failures.append("%s: expected a failure mentioning %r, got %r"
                            % (label, want, bad))
        else:
            print("  fires: %s" % label)

    def edit(path: Path, fn):
        doc = load(path)
        fn(doc)
        dump(path, doc)

    # 1. an unknown kind
    run(lambda r, t: edit(r / "books/claims/fixture.json",
                          lambda d: d["claims"][0].update(kind="atmosphere")),
        "outside the closed vocabulary", "a claim kind outside the closed vocabulary")

    # 2. a missing reading — on both shapes, because both require it
    run(lambda r, t: edit(r / "books/claims/fixture.json",
                          lambda d: d["claims"][0].pop("reading")),
        "a claim with no reading", "a claim with no reading grade")
    run(lambda r, t: edit(r / "civic/records/poll_1835.json",
                          lambda d: d["records"][0].pop("reading")),
        "a record with no reading", "a record with no reading grade")
    run(lambda r, t: edit(r / "civic/records/poll_1835.json",
                          lambda d: d["records"][0].update(reading="eyeballed")),
        "is outside", "a reading grade outside the two")

    # 3. a quote that differs by one character
    run(lambda r, t: edit(r / "books/claims/fixture.json",
                          lambda d: d["claims"][0].update(quote="the town was then a mere hamlets")),
        "not what the committed text says", "a quote that differs by one character")
    run(lambda r, t: edit(r / "books/claims/fixture.json",
                          lambda d: d["claims"][0]["locator"].update(text_file="nope.txt")),
        "which is not committed", "a quote citing text this repo does not hold")

    # 4. a coverage hole
    run(lambda r, t: edit(r / "books/coverage.json",
                          lambda d: d["declarations"][0]["items"].append(8)),
        "coverage hole", "a declared page nothing reaches")
    run(lambda r, t: edit(r / "civic/coverage.json",
                          lambda d: d["declarations"][0].update(unit="parish")),
        "is outside", "a coverage unit outside the vocabulary")

    # 5. a merge with no rule, and a rule that does not read back
    run(lambda r, t: edit(r / "civic/crosswalk.json",
                          lambda d: d["merges"].append(
                              {"into": "John Kinzie", "from": "Jno. Kinzie",
                               "evidence": ["fixture_source"]})),
        "a merge with no rule", "a merge with no rule")
    run(lambda r, t: edit(r / "civic/crosswalk.json",
                          lambda d: d["merges"].append(
                              {"into": "John Kinzie", "from": "Jno. Kinzie",
                               "rule": "the poll book and the roll are one man",
                               "evidence": ["fixture_source"]})),
        "does not name both spellings verbatim", "a merge rule that does not read back")

    # 6. a refusal naming only one spelling
    run(lambda r, t: edit(r / "civic/crosswalk.json",
                          lambda d: d["refusals"].append(
                              {"a": "John Kinzie", "rule": "two families",
                               "evidence": ["fixture_source"]})),
        "a refusal naming only one spelling", "a refusal naming only one spelling")

    # 7. a surname-only merge — refused however good the rule is
    run(lambda r, t: edit(r / "civic/crosswalk.json",
                          lambda d: d["merges"].append(
                              {"into": "Kinzie", "from": "Jno. Kinzie",
                               "rule": "Kinzie and Jno. Kinzie stand at the same entry",
                               "evidence": ["fixture_source"]})),
        "surname-only merge is always a refusal", "a surname-only merge")

    # 8. a claim citing a source id that does not resolve
    run(lambda r, t: edit(r / "books/claims/fixture.json",
                          lambda d: d.update(source_id="no_such_source")),
        "names no source record", "a claim file citing a source id that does not resolve")
    run(lambda r, t: edit(r / "civic/records/poll_1835.json",
                          lambda d: d.update(source_id="no_such_source")),
        "names no source record", "a records file citing a source id that does not resolve")

    # …and the structural half: the scaffold itself, and the manifest.
    run(lambda r, t: (r / "church" / "README.md").unlink(),
        "no README.md", "a domain that has lost its README")
    run(lambda r, t: (r / "church" / "crosswalk.json").unlink(),
        "no crosswalk.json", "a domain with no identity layer")
    run(lambda r, t: (r / "church" / "coverage.json").unlink(),
        "no coverage.json", "a domain that declares no coverage")
    run(lambda r, t: edit(r / "domains.json", lambda d: d["kinds"].append("atmosphere")),
        "stale or hand-edited", "a hand-edited manifest")
    run(lambda r, t: edit(r / "civic/records/poll_1835.json",
                          lambda d: d["records"].append(copy.deepcopy(FIXTURE_RECORD))),
        "duplicate record id", "two rows under one id")
    run(lambda r, t: edit(r / "books/claims/fixture.json",
                          lambda d: d["claims"][0].update(town_finding="yes")),
        "town_finding is not a boolean", "a town_finding that is not a boolean")

    if failures:
        for f in failures:
            print("FAIL: " + f, file=sys.stderr)
        return 1
    print("SELF-TEST PASS — every research-domain assertion fires when broken "
          "(%d cases)" % cases)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.build:
        return build()
    if args.check:
        bad = check()
        if bad:
            print("RESEARCH DOMAINS FAIL — %d problem(s)" % len(bad))
            return 1
        print("OK: the %d domains hold their shape" % len(DOMAINS))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
