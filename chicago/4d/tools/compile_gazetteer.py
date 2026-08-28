#!/usr/bin/env python3
"""What the newspapers say about the town, compiled — and the gate that keeps it honest.

    tools/compile_gazetteer.py --build       recompile gazetteer.json from extracted/*.json
    tools/compile_gazetteer.py --check       the gate
    tools/compile_gazetteer.py --self-test   the gate's assertions still fire

T-0256 made 86 issues citable. This is the pair of structures every extraction
pass writes into, and the rules that stop them drifting into fiction.

TWO FILES, ONE OF THEM GENERATED.

  data/research/newspapers/extracted/<issue_id>.json   HAND-MADE, one per issue.
  data/research/newspapers/gazetteer.json              GENERATED, never hand-edited.

The gazetteer is a compile of the extraction files and nothing else. `--check`
recompiles it in memory and compares BYTES with what is committed, so a hand edit
to the compiled file is not a matter of etiquette — it fails the gate. The compile
is deterministic (sorted keys, sorted lists, no clock anywhere), so the comparison
means what it says.

THE OWNER'S THREE RULINGS, 2026-08-28, and where each one lives in the code.

  1. A LETTER-LIST NAME IS ENOUGH TO MINT A RESIDENT. The post-office lists name
     people by the hundred and a listed name alone makes a resident candidate. But
     the two evidence strengths must stay distinguishable forever, so a claim taken
     from a list carries `letter_list: true` and the compiler sets a person's
     `letter_list_only` to true only when EVERY mention of them is such a claim.
     One advertisement anywhere in the corpus turns it off, permanently.
  2. TRANSCRIPTION-MEDIATED READINGS GRADE `documented`, CARRYING A FLAG. The
     corpus is read through OCR-assisted transcriptions, not the page scans, so
     every claim carries `reading: transcription_mediated` STRUCTURALLY — a claim
     that omits it is refused rather than defaulted, because a default is how a
     scan-read and a transcription-read stop being distinguishable. This extends
     and does not overturn the standard in `chicago_democrat_1833_11_26.json`:
     where a scan exists and is read, the scan wins, and it has already caught the
     transcription out ('C. & I. HARMON' against 'C. & L. Harmon').
  3. A DOCUMENTED BUSINESS IS BUILT AT THE SCENE DATE UNLESS CONTRADICTED. Only a
     dissolution, removal or replacement notice keeps one out of the 1835 town, so
     `built_1835` is true unless a `notice` claim names the business in its
     `contradicts` list. A business whose last evidence predates 1835-07-01 is
     built anyway and flagged `survival_liberty: true` — existence documented,
     survival to the scene date assumed — which is what docs/LIBERTIES.md carries.

WHAT A QUOTE IS, AND WHAT A NORMALIZED READING IS. `quote` is verbatim, including
the transcriber's own square-bracketed uncertainty notes, and it is never smoothed.
`normalized` sits BESIDE it and never replaces it: interleaved columns unshuffled,
rn/m-class confusions corrected, and any word RESTORED rather than read written in
ANGLE brackets, so the two kinds of bracket can never be confused. Where the gate
can open the witness — the deposit is on `main`, so on `dev` it usually cannot —
it checks the quote against the file, byte for byte.

IDENTITY IS DECLARED, NEVER GUESSED. There is no fuzzy matching in this file. Two
mentions become one person because an extraction gave them the same `id`, and that
is a MERGE, which must be explained: if one id carries two spellings the file needs
a `merge_rule` naming both and stating the judgement, or the compile fails. If the
two spellings share a surname and disagree on initials the rule must additionally
say `cross_initial: true`. The fixture holds Caroline Gooding and Charles Gooding
two lines apart in one letter list so the general refusal is exercised against real
data rather than a toy; the cross-initial bar is exercised in the self-test.

THIS IS RESEARCH, NOT PAYLOAD. `data/research/` is not copied by publish.sh; the
corpus gate already asserts nothing under it reaches `site/chicago/4d/`.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # chicago/4d
REPO = ROOT.parent.parent                              # repo root
RESEARCH = ROOT / "data" / "research" / "newspapers"
CORPUS = RESEARCH / "corpus.json"
EXTRACTED = RESEARCH / "extracted"
GAZETTEER = RESEARCH / "gazetteer.json"

SCHEMA_VERSION = 1
SCENE_DATE = date(1835, 7, 1)
READING = "transcription_mediated"

KINDS = {"person", "business", "building", "street", "infrastructure",
         "event", "shipping", "price", "notice"}
ENTITY_KINDS = {"person", "business", "place"}
PLACEMENT_CLASSES = {"corner", "relative", "street_only", "none"}
NEEDS_ANCHOR = {"corner", "relative"}


# --------------------------------------------------------------------------
# helpers


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(doc):
    """The one serialisation. Sorted keys, no clock, trailing newline."""
    return json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def fold(name):
    """Case- and punctuation-folded name, for asking whether two spellings differ."""
    return re.sub(r"[^a-z0-9 ]+", "", (name or "").lower()).strip()


def surname_and_initials(normalized):
    """('Gooding', 'C') out of 'Charles Gooding'; ('Hogan', 'JSC') out of 'J. S. C. Hogan'.

    Deliberately crude: it exists to ASK whether a merge crosses initials, and a
    crude reading errs towards asking, which is the safe direction.
    """
    parts = [p for p in re.split(r"\s+", (normalized or "").strip()) if p]
    if not parts:
        return "", ""
    surname = fold(parts[-1])
    initials = "".join(fold(p)[:1] for p in parts[:-1] if fold(p))
    return surname, initials


def extraction_files(directory=EXTRACTED):
    return sorted(Path(directory).glob("*.json"))


# --------------------------------------------------------------------------
# reading the extraction files


def evidence_date(claim, issue_date):
    """The date a claim is evidence FOR.

    An advertisement's own dateline, where it has one, and the issue date
    otherwise. The distinction is the whole point of `ad_copy_date`: Peter
    Cohen's ad in the 1835-07-01 Democrat was placed on 1834-11-03, and an
    evidence window built from the issue date would silently claim eight months
    of continuous trading nobody documented.
    """
    return claim.get("ad_copy_date") or issue_date


def collect(files):
    """Read every extraction file into (docs, claims-in-order). No validation here."""
    docs, claims = [], []
    for f in files:
        doc = load(f)
        doc["_file"] = Path(f).name
        docs.append(doc)
        for c in doc.get("claims") or []:
            claims.append((doc, c))
    return docs, claims


# --------------------------------------------------------------------------
# the compile


def compile_gazetteer(files=None, directory=EXTRACTED):
    """Compile extracted/* into the gazetteer document. Raises on an unexplained merge.

    Returns (doc, errors). Errors that make the compile meaningless are raised
    as ValueError; everything else is reported so the gate can print them all.
    """
    files = extraction_files(directory) if files is None else list(files)
    docs, claims = collect(files)
    errors = []

    merge_rules = {}
    for doc in docs:
        for rule in doc.get("merge_rules") or []:
            merge_rules.setdefault(rule.get("id"), []).append(rule)

    persons, businesses, places = {}, {}, {}

    for doc, claim in claims:
        issue_date = doc.get("issue_date")
        when = evidence_date(claim, issue_date)
        cid = claim.get("id")
        listed = bool(claim.get("letter_list"))

        for ent in claim.get("entities") or []:
            eid, kind = ent.get("id"), ent.get("kind")
            if kind == "person":
                e = persons.setdefault(eid, {
                    "id": eid, "names": [], "mentions": [], "occupations": [],
                    "places": [], "first_seen": when, "last_seen": when,
                    "letter_list_only": True,
                })
            elif kind == "place":
                e = places.setdefault(eid, {
                    "id": eid, "names": [], "mentions": [],
                    "first_seen": when, "last_seen": when,
                })
            elif kind == "business":
                e = businesses.setdefault(eid, {
                    "id": eid, "names": [], "mentions": [], "proprietors": [],
                    "trade": None, "goods": [], "street": None,
                    "placement": None, "contradicted_by": [],
                    "first_seen": when, "last_seen": when,
                })
            else:
                continue

            e["names"].append({"as_printed": ent.get("as_printed"),
                               "normalized": ent.get("normalized"),
                               "claim": cid})
            if cid not in e["mentions"]:
                e["mentions"].append(cid)
            if when:
                e["first_seen"] = min(e["first_seen"] or when, when)
                e["last_seen"] = max(e["last_seen"] or when, when)

            if kind == "person":
                if not listed:
                    e["letter_list_only"] = False
                occ = claim.get("occupation")
                if occ and ent.get("role") != "reference" and occ not in e["occupations"]:
                    e["occupations"].append(occ)
                for other in claim.get("entities") or []:
                    if other.get("kind") == "place" and other["id"] not in e["places"]:
                        e["places"].append(other["id"])

        block = claim.get("business")
        if block:
            bid = block.get("id")
            b = businesses.setdefault(bid, {
                "id": bid, "names": [], "mentions": [], "proprietors": [],
                "trade": None, "goods": [], "street": None,
                "placement": None, "contradicted_by": [],
                "first_seen": when, "last_seen": when,
            })
            if cid not in b["mentions"]:
                b["mentions"].append(cid)
            for field in ("trade", "street"):
                if block.get(field) and not b[field]:
                    b[field] = block[field]
            for g in block.get("goods") or []:
                if g not in b["goods"]:
                    b["goods"].append(g)
            if block.get("placement") and not b["placement"]:
                b["placement"] = dict(block["placement"])
            for ent in claim.get("entities") or []:
                if ent.get("kind") == "person" and ent.get("role") == "proprietor" \
                        and ent["id"] not in b["proprietors"]:
                    b["proprietors"].append(ent["id"])

        if claim.get("kind") == "notice":
            for target in claim.get("contradicts") or []:
                b = businesses.setdefault(target, {
                    "id": target, "names": [], "mentions": [], "proprietors": [],
                    "trade": None, "goods": [], "street": None,
                    "placement": None, "contradicted_by": [],
                    "first_seen": when, "last_seen": when,
                })
                entry = {"claim": cid, "date": when}
                if entry not in b["contradicted_by"]:
                    b["contradicted_by"].append(entry)

    # --- the identity policy, enforced ---------------------------------------
    for pid, p in sorted(persons.items()):
        forms = sorted({fold(n["normalized"]) for n in p["names"] if n.get("normalized")})
        if len(forms) <= 1:
            continue
        rules = merge_rules.get(pid) or []
        rule = rules[0] if rules else None
        if not rule or not (rule.get("judgment") or "").strip():
            errors.append(
                "%s carries %d spellings (%s) under one id and no merge_rule "
                "states the judgement — an unexplained merge is a compile error"
                % (pid, len(forms), ", ".join(repr(f) for f in forms)))
            continue
        stated = {fold(s) for s in rule.get("spellings") or []}
        missing = [f for f in forms if f not in stated]
        if missing:
            errors.append("%s: merge_rule does not name the spelling(s) %s"
                          % (pid, ", ".join(repr(m) for m in missing)))
        sigs = {surname_and_initials(n["normalized"]) for n in p["names"]
                if n.get("normalized")}
        surnames = {s for s, _ in sigs}
        initials = {i for _, i in sigs if i}
        if len(surnames) == 1 and len(initials) > 1 and not rule.get("cross_initial"):
            errors.append(
                "%s merges the same surname across different initials (%s) and its "
                "merge_rule does not say cross_initial: true — same surname plus "
                "different initials never merges silently"
                % (pid, ", ".join(sorted(initials))))

    # --- ruling 3, applied ---------------------------------------------------
    for b in businesses.values():
        b["built_1835"] = not b["contradicted_by"]
        last = b["last_seen"]
        b["survival_liberty"] = bool(
            b["built_1835"] and last and date.fromisoformat(last) < SCENE_DATE)

    def tidy(entries, extra=()):
        out = []
        for e in sorted(entries.values(), key=lambda x: x["id"]):
            e = dict(e)
            e["names"] = sorted(e["names"], key=lambda n: (n["claim"],
                                                           n["as_printed"] or "",
                                                           n["normalized"] or ""))
            e["mentions"] = sorted(e["mentions"])
            for key in extra:
                if isinstance(e.get(key), list):
                    e[key] = sorted(e[key], key=lambda v: json.dumps(v, sort_keys=True))
            out.append(e)
        return out

    inputs = [{"file": d["_file"],
               "sha256": sha256_text(dump(strip_private(d)))} for d in docs]
    inputs.sort(key=lambda i: i["file"])

    doc = {
        "schema": SCHEMA_VERSION,
        "generated_by": "tools/compile_gazetteer.py --build",
        "generated_from": [i["file"] for i in inputs],
        "input_digest": sha256_text(dump(inputs)),
        "scene_date": SCENE_DATE.isoformat(),
        "reading": READING,
        "counts": {"persons": len(persons), "businesses": len(businesses),
                   "places": len(places),
                   "claims": sum(len(d.get("claims") or []) for d in docs)},
        "persons": tidy(persons, ("occupations", "places")),
        "businesses": tidy(businesses, ("goods", "proprietors", "contradicted_by")),
        "places": tidy(places),
    }
    return doc, errors


def strip_private(doc):
    return {k: v for k, v in doc.items() if not k.startswith("_")}


# --------------------------------------------------------------------------
# the gate


def check_extractions(docs, corpus, repo=REPO, quiet=False):
    """Structural rules on the hand-made files. Returns (failures, notes)."""
    bad, notes = [], []
    issues = {e["id"]: e for e in (corpus.get("issues") or [])}
    seen_claim_ids = set()
    unreadable = 0

    for doc in docs:
        name = doc.get("_file", "?")
        if doc.get("schema") != SCHEMA_VERSION:
            bad.append("%s: schema is %r, this tool speaks %d"
                       % (name, doc.get("schema"), SCHEMA_VERSION))
        iid = doc.get("issue_id")
        if name != "%s.json" % iid:
            bad.append("%s: file is named for %r and declares issue_id %r — one "
                       "extraction file per issue, named for it" % (name, name[:-5], iid))
        issue = issues.get(iid)
        if not issue:
            bad.append("%s: issue_id %r does not resolve against corpus.json" % (name, iid))
            continue
        if doc.get("issue_date") != issue.get("date"):
            bad.append("%s: issue_date %r, corpus says %r"
                       % (name, doc.get("issue_date"), issue.get("date")))
        if doc.get("publication") != issue.get("publication"):
            bad.append("%s: publication %r, corpus says %r"
                       % (name, doc.get("publication"), issue.get("publication")))
        if doc.get("reading") != READING:
            bad.append("%s: file-level reading is %r and must be %r (ruling 2)"
                       % (name, doc.get("reading"), READING))

        # Witnesses are artifacts of THIS issue, at the sha256 the corpus recorded.
        arts = {a.get("text_path"): a for a in issue.get("artifacts") or []}
        witnesses = doc.get("witnesses") or {}
        if not witnesses:
            bad.append("%s: no witnesses declared" % name)
        for wname, w in sorted(witnesses.items()):
            art = arts.get(w.get("path"))
            if not art:
                bad.append("%s: witness %r names %r, which is not a text artifact of "
                           "%s in corpus.json" % (name, wname, w.get("path"), iid))
                continue
            if w.get("sha256") != art.get("text_sha256"):
                bad.append("%s: witness %r records sha256 %s, the corpus records %s "
                           "— the line numbers below were read against a different "
                           "text" % (name, wname, str(w.get("sha256"))[:12],
                                     str(art.get("text_sha256"))[:12]))

        for claim in doc.get("claims") or []:
            cid = claim.get("id") or "<no id>"
            def fail(msg):
                bad.append("%s %s: %s" % (name, cid, msg))
            if cid in seen_claim_ids:
                fail("duplicate claim id")
            seen_claim_ids.add(cid)
            if not str(cid).startswith(iid + "#"):
                fail("claim id must begin with its issue id")
            if claim.get("kind") not in KINDS:
                fail("kind %r is not one of %s" % (claim.get("kind"), sorted(KINDS)))
            for field in ("quote", "normalized"):
                if not (claim.get(field) or "").strip():
                    fail("no %s" % field)
            if claim.get("reading") != READING:
                fail("reading is %r and must be %r, carried structurally so no claim "
                     "can omit it (ruling 2)" % (claim.get("reading"), READING))

            loc = claim.get("locator")
            if not isinstance(loc, dict):
                fail("no locator — a claim that cannot say where it was read cannot "
                     "be made")
                continue
            wname = claim.get("witness")
            w = witnesses.get(wname)
            if not w:
                fail("witness %r is not declared by this file" % wname)
                continue
            if not w.get("column_markers"):
                fail("witness %r carries no page/column markers, so nothing may be "
                     "CITED from it — use it as a corroboration instead" % wname)
            else:
                for field in ("issue_page", "column"):
                    if not isinstance(loc.get(field), int):
                        fail("locator has no %s, and a claim that cannot name its "
                             "column cannot be made" % field)
            a, b = loc.get("line_start"), loc.get("line_end")
            if not isinstance(a, int) or not isinstance(b, int) or a < 1 or b < a:
                fail("locator line range %r-%r does not make sense" % (a, b))
                continue

            unreadable += verify_quote(w, claim, loc, claim.get("quote"), loc.get("column"),
                                       loc.get("issue_page"), fail, repo)

            for corr in claim.get("corroborations") or []:
                cw = witnesses.get(corr.get("witness"))
                if not cw:
                    fail("corroboration names undeclared witness %r" % corr.get("witness"))
                    continue
                cl = corr.get("locator") or {}
                ca, cb = cl.get("line_start"), cl.get("line_end")
                if not isinstance(ca, int) or not isinstance(cb, int) or ca < 1 or cb < ca:
                    fail("corroboration line range %r-%r does not make sense" % (ca, cb))
                    continue
                unreadable += verify_quote(cw, claim, cl, corr.get("quote"), None, None,
                                           fail, repo)

            ents = claim.get("entities") or []
            if not ents:
                fail("no entities")
            for ent in ents:
                if ent.get("kind") not in ENTITY_KINDS:
                    fail("entity kind %r is not one of %s"
                         % (ent.get("kind"), sorted(ENTITY_KINDS)))
                if not ent.get("id") or not ent.get("as_printed") \
                        or not ent.get("normalized"):
                    fail("entity %r needs id, as_printed and normalized — the name as "
                         "printed and the normalisation guess are both kept"
                         % ent.get("id"))
                elif not str(ent["id"]).startswith(ent["kind"] + ":"):
                    fail("entity id %r does not begin with its kind" % ent["id"])

            if claim.get("letter_list"):
                if claim.get("kind") != "person":
                    fail("letter_list is for person claims")
                target = claim.get("letter_list_of")
                if not target:
                    fail("letter_list claim does not say which list it is from")

            block = claim.get("business")
            if block:
                bid = block.get("id")
                if bid not in {e.get("id") for e in ents}:
                    fail("business block %r is not among the claim's entities" % bid)
                pl = block.get("placement") or {}
                cls = pl.get("class")
                if cls not in PLACEMENT_CLASSES:
                    fail("placement class %r is not one of %s"
                         % (cls, sorted(PLACEMENT_CLASSES)))
                elif cls in NEEDS_ANCHOR:
                    if not pl.get("anchor") or not pl.get("offset_text"):
                        fail("a %r placement needs the anchor's name and the offset "
                             "text verbatim" % cls)
                elif cls == "street_only" and not block.get("street"):
                    fail("a street_only placement needs a street")
                elif cls == "none" and (pl.get("anchor") or pl.get("offset_text")):
                    fail("placement class none carries an anchor or an offset")

    # Every letter_list_of, and every anchor_id, resolves to something that exists.
    for doc in docs:
        for claim in doc.get("claims") or []:
            target = claim.get("letter_list_of")
            if target and target not in seen_claim_ids:
                bad.append("%s %s: letter_list_of names %r, which is not a claim"
                           % (doc.get("_file"), claim.get("id"), target))
    if unreadable and not quiet:
        notes.append("%d quote(s) could not be checked against their witness — the "
                     "deposit is on `main` (T-0275). Their sha256 is pinned, so they "
                     "will be checked the moment the text is on this branch."
                     % unreadable)
    return bad, notes


def verify_quote(witness, claim, loc, quote, column, issue_page, fail, repo):
    """Check a quote against its witness where the file is on this branch.

    Returns 1 when the witness could not be opened here, 0 when it was checked.
    A missing witness is NOT a failure: the reconciled transcriptions live on
    `main` with the deposit, and the sha256 recorded beside every line number is
    what makes this deferrable rather than unfalsifiable.
    """
    path = repo / witness.get("path", "")
    if not path.exists():
        return 1
    lines = path.read_text(encoding="utf-8").split("\n")
    a, b = loc["line_start"], loc["line_end"]
    if b > len(lines):
        fail("locator runs to line %d and the witness has %d" % (b, len(lines)))
        return 0
    actual = "\n".join(lines[a - 1:b])
    if quote != actual:
        fail("quote does not match lines %d-%d of its witness" % (a, b))
    if column is not None and witness.get("column_markers"):
        marker, page_seen, col_seen = None, None, None
        for line in lines[:a - 1]:
            m = re.match(r"=====\s*ISSUE PAGE (\d+) / PDF PAGE (\d+) / COLUMN (\d+)", line)
            if m:
                marker, page_seen, col_seen = m, int(m.group(1)), int(m.group(3))
        if marker is None:
            fail("no page/column marker precedes line %d" % a)
        elif (page_seen, col_seen) != (issue_page, column):
            fail("locator says page %s column %s; the marker above line %d says "
                 "page %d column %d" % (issue_page, column, a, page_seen, col_seen))
    return 0


def check(directory=EXTRACTED, gazetteer=GAZETTEER, corpus_path=CORPUS,
          repo=REPO, quiet=False):
    """Returns a list of failure strings. Empty means green."""
    bad = []
    if not Path(corpus_path).exists():
        return ["%s is missing — the gazetteer resolves its citations against it"
                % corpus_path]
    corpus = load(corpus_path)

    files = extraction_files(directory)
    if not files:
        return ["%s holds no extraction files" % directory]
    docs, _ = collect(files)

    structural, notes = check_extractions(docs, corpus, repo=repo, quiet=quiet)
    bad += structural

    doc, errors = compile_gazetteer(files=files, directory=directory)
    bad += errors

    again, _ = compile_gazetteer(files=files, directory=directory)
    if dump(doc) != dump(again):
        bad.append("the compile is not deterministic — two runs over the same "
                   "inputs produced different bytes")

    path = Path(gazetteer)
    if not path.exists():
        bad.append("%s is missing — run --build" % path)
    else:
        committed = path.read_text(encoding="utf-8")
        if committed != dump(doc):
            bad.append("%s does not match a fresh compile of extracted/* — it is "
                       "generated and must never be hand-edited; run --build"
                       % path.name)

    for entry in doc["businesses"]:
        pl = entry.get("placement") or {}
        anchor = pl.get("anchor_id")
        if anchor and anchor not in {e["id"] for e in doc["places"]} \
                | {e["id"] for e in doc["businesses"]}:
            bad.append("%s is placed against anchor %r, which the gazetteer does "
                       "not hold" % (entry["id"], anchor))
    for group in ("persons", "businesses", "places"):
        for entry in doc[group]:
            if not entry.get("mentions"):
                bad.append("%s has no mention — every entry is compiled from a claim"
                           % entry["id"])

    if not quiet and not bad:
        c = doc["counts"]
        print("  ok    %d claim(s) in %d issue file(s) resolve against corpus.json"
              % (c["claims"], len(files)))
        print("  ok    %d person(s), %d business(es), %d place(s); the committed "
              "gazetteer is byte-identical to a fresh compile"
              % (c["persons"], c["businesses"], c["places"]))
        for n in notes:
            print("  note  " + n)
    return bad


# --------------------------------------------------------------------------
# self-test: the negative fixtures, and every assertion above firing


def self_test():
    import tempfile
    base = load(extraction_files()[0])
    base.pop("_file", None)
    corpus = load(CORPUS)
    failures = []

    def run(mutate, want, label, also_gazetteer=None):
        d = copy.deepcopy(base)
        mutate(d)
        with tempfile.TemporaryDirectory() as td:
            ex = Path(td) / "extracted"
            ex.mkdir()
            name = "%s.json" % d.get("issue_id", "x")
            (ex / name).write_text(dump(d), encoding="utf-8")
            g = Path(td) / "gazetteer.json"
            built, _ = compile_gazetteer(directory=ex)
            g.write_text(dump(built) if also_gazetteer is None else also_gazetteer,
                         encoding="utf-8")
            bad = check(directory=ex, gazetteer=g, corpus_path=CORPUS,
                        repo=REPO, quiet=True)
        if not any(want in b for b in bad):
            failures.append("%s: expected a failure mentioning %r, got %r"
                            % (label, want, bad))

    def claim(d, i=0):
        return d["claims"][i]

    # --- the three the ticket names ----------------------------------------
    run(lambda d: claim(d).pop("locator"), "cannot say where it was read",
        "a claim with no locator")
    run(lambda d: claim(d)["locator"].pop("column"), "cannot name its column",
        "a claim with no column")

    def cross_initial_merge(d):
        # Charles Gooding is re-identified as Caroline Gooding's id: same surname,
        # different initials, no rule. This is the merge the policy exists to stop.
        for c in d["claims"]:
            for e in c["entities"]:
                if e["id"] == "person:charles_gooding":
                    e["id"] = "person:caroline_gooding"
    run(cross_initial_merge, "unexplained merge", "a silent cross-initial merge")

    def stated_but_not_cross_initial(d):
        # Caroline and Charles share an initial, so the cross-initial bar needs a
        # pair that genuinely disagrees on one: the letter list two lines further
        # down prints an Anson Gooding, and folding him into Caroline is exactly
        # the merge the paper's own initials refuse.
        for c in d["claims"]:
            for e in c["entities"]:
                if e["id"] == "person:charles_gooding":
                    e["id"] = "person:caroline_gooding"
                    e["as_printed"] = "Gooding, Anson"
                    e["normalized"] = "Anson Gooding"
        d["merge_rules"] = [{"id": "person:caroline_gooding",
                             "spellings": ["Caroline Gooding", "Anson Gooding"],
                             "judgment": "they looked similar"}]
    run(stated_but_not_cross_initial, "cross_initial",
        "a stated merge that does not admit it crosses initials")

    def stated_and_admitted(d):
        stated_but_not_cross_initial(d)
        d["merge_rules"][0]["cross_initial"] = True
    d = copy.deepcopy(base)
    stated_and_admitted(d)
    with tempfile.TemporaryDirectory() as td:
        ex = Path(td) / "extracted"
        ex.mkdir()
        (ex / "chicago_democrat_1835_07_01.json").write_text(dump(d), encoding="utf-8")
        _, errs = compile_gazetteer(directory=ex)
    if errs:
        failures.append("a merge that names both spellings, states its judgement and "
                        "admits it crosses initials was still refused: %r" % errs)

    run(lambda d: None, "must never be hand-edited", "a hand-edited gazetteer",
        also_gazetteer=dump({"schema": 1, "persons": [], "businesses": [],
                             "places": [], "counts": {}}))

    # --- and the rest of the gate ------------------------------------------
    run(lambda d: claim(d).pop("reading"), "carried structurally",
        "a claim missing its reading flag")
    run(lambda d: d.update(reading="scan"), "ruling 2", "a file-level reading override")
    run(lambda d: claim(d).update(quote=""), "no quote", "an empty quote")
    run(lambda d: claim(d).update(normalized=" "), "no normalized",
        "a normalized reading that is only whitespace")
    run(lambda d: claim(d)["quote"] and claim(d).update(kind="rumour"),
        "is not one of", "an invented claim kind")
    run(lambda d: d.update(issue_id="chicago_democrat_1899_01_01"),
        "does not resolve against corpus.json", "an issue that is not in the corpus")
    run(lambda d: d["witnesses"]["primary"].update(sha256="0" * 64),
        "read against a different text", "a witness at the wrong sha256")
    run(lambda d: d["witnesses"]["primary"].update(
        path="chicago/4d/data/research/newspapers/text/chicago_american_1835_06_08.txt"),
        "not a text artifact", "a witness borrowed from another issue")
    run(lambda d: d.update(issue_date="1835-07-02"), "corpus says",
        "an issue date that disagrees with the corpus")
    run(lambda d: claim(d)["locator"].update(line_end=1), "does not make sense",
        "a backwards line range")
    run(lambda d: claim(d)["entities"][0].update(normalized=None),
        "needs id, as_printed and normalized", "an entity with no normalisation")
    run(lambda d: claim(d)["entities"][0].update(id="peter_cohen"),
        "does not begin with its kind", "an entity id without its kind")
    run(lambda d: claim(d)["business"]["placement"].update(class_=None) or
        claim(d)["business"]["placement"].update({"class": "vaguely"}),
        "is not one of", "an invented placement class")
    run(lambda d: claim(d)["business"]["placement"].update(offset_text=None),
        "offset text verbatim", "a relative placement with no offset text")
    run(lambda d: claim(d)["business"].update(id="business:nobody"),
        "not among the claim's entities", "a business block naming no entity")
    run(lambda d: d["claims"][5].update(letter_list_of="chicago_democrat_1835_07_01#c99"),
        "which is not a claim", "a letter list pointing at nothing")
    run(lambda d: d["claims"].append(copy.deepcopy(d["claims"][0])),
        "duplicate claim id", "the same claim twice")
    run(lambda d: claim(d)["business"]["placement"].update(
        anchor_id="business:nobody_at_all"),
        "which the gazetteer does not hold", "an anchor that resolves to nothing")

    # The quote check must fire on a witness this branch CAN open. The alternate
    # transcription is committed, so the corroboration on c01 is checkable here.
    run(lambda d: claim(d)["corroborations"][0].update(quote="not what it says"),
        "does not match lines", "a corroboration quote that was retyped")
    run(lambda d: claim(d)["corroborations"][0]["locator"].update(line_end=99999),
        "the witness has", "a corroboration running off the end of its witness")

    # Ruling 3: a notice is the only veto, and it must actually work.
    def contradicted(d):
        d["claims"].append({
            "id": "chicago_democrat_1835_07_01#c99", "kind": "notice",
            "witness": "primary", "reading": READING,
            "locator": {"issue_page": 4, "pdf_page": 36, "column": 5,
                        "line_start": 5037, "line_end": 5037},
            "quote": "x", "normalized": "x",
            "contradicts": ["business:peter_cohen_store"],
            "entities": [{"id": "business:peter_cohen_store", "kind": "business",
                          "role": "subject", "as_printed": "x", "normalized": "x"}],
        })
    d = copy.deepcopy(base)
    contradicted(d)
    with tempfile.TemporaryDirectory() as td:
        ex = Path(td) / "extracted"
        ex.mkdir()
        (ex / "chicago_democrat_1835_07_01.json").write_text(dump(d), encoding="utf-8")
        built, _ = compile_gazetteer(directory=ex)
    cohen = [b for b in built["businesses"] if b["id"] == "business:peter_cohen_store"][0]
    if cohen["built_1835"]:
        failures.append("a dissolution notice did not keep a business out of the town")
    if not cohen["contradicted_by"]:
        failures.append("a contradicting notice was not recorded on the business")

    # ...and the positive side of ruling 3 and ruling 1, on the real fixture.
    live, errs = compile_gazetteer()
    if errs:
        failures.append("the committed fixture does not compile cleanly: %r" % errs)
    else:
        cohen = [b for b in live["businesses"]
                 if b["id"] == "business:peter_cohen_store"][0]
        if not cohen["built_1835"] or not cohen["survival_liberty"]:
            failures.append("Cohen's 1834 advertisement should build WITH a survival "
                            "liberty, and did not")
        if "Newberry" not in (cohen["placement"] or {}).get("offset_text", ""):
            failures.append("Cohen's entry lost its verbatim offset text")
        if (cohen["placement"] or {}).get("anchor_id") != "business:newberry_and_dole":
            failures.append("Cohen's entry lost the Newberry & Dole anchor")
        hogan = [p for p in live["persons"] if p["id"] == "person:j_s_c_hogan"][0]
        if hogan["letter_list_only"]:
            failures.append("a man who advertises a store was compiled letter_list_only")
        if "postmaster" not in hogan["occupations"]:
            failures.append("Hogan's occupation did not survive the compile")
        morrison = [p for p in live["persons"]
                    if p["id"] == "person:orsemus_morrison"][0]
        if not morrison["letter_list_only"]:
            failures.append("a name known only from a letter list was not flagged "
                            "letter_list_only (ruling 1)")

    if failures:
        for f in failures:
            print("FAIL: " + f, file=sys.stderr)
        return 1
    print("  ok    every gazetteer assertion fires when broken (27 cases), and the "
          "three rulings hold on the committed fixture")
    return 0


# --------------------------------------------------------------------------


def build():
    doc, errors = compile_gazetteer()
    for e in errors:
        print("  FAIL  " + e, file=sys.stderr)
    if errors:
        return 1
    GAZETTEER.write_text(dump(doc), encoding="utf-8")
    c = doc["counts"]
    print("wrote %s — %d persons, %d businesses, %d places from %d claims"
          % (GAZETTEER.relative_to(REPO), c["persons"], c["businesses"],
             c["places"], c["claims"]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.build:
        return build()
    if args.self_test:
        return self_test()
    bad = check()
    for b in bad:
        print("  FAIL  " + b, file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
