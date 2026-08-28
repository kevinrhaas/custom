#!/usr/bin/env python3
"""The newspaper extraction schema, and the gazetteer the papers compile into.

    tools/compile_gazetteer.py --build       recompile gazetteer.json from extracted/*
    tools/compile_gazetteer.py --check       the gate
    tools/compile_gazetteer.py --self-test   the gate's assertions still fire

WHAT THIS IS FOR (T-0257). T-0256 made the 1833-1835 corpus citable: 86 issues with
a register, `data/research/newspapers/corpus.json`, that resolves a citation into the
owner's deposit. It did not say what a READING out of those issues looks like once it
has been made. This does. Every later pass in the PAPERS epic — the Democrat read in
three parts, the American, the July 1 register, the storefronts that take their places
on South Water — writes into the two structures here and is gated by the rules here.

NO MASS EXTRACTION HAPPENS IN THIS TICKET. What ships is the schema, the compiler, the
gate, and ONE worked issue: the scene-date Democrat of 1835-07-01.

THE OWNER'S THREE RULINGS, 2026-08-28, and where each one lives in the data:

  1. A LETTER-LIST NAME IS ENOUGH TO MINT A RESIDENT. The post-office letter lists name
     people by the hundred and a listed name alone makes a resident candidate — not
     merely a gazetteer entry. The two evidence strengths must stay distinguishable
     forever, so `letter_list_only` is a field on the person and not a note: a person
     known ONLY from letter lists carries `true`, and one named in any other kind of
     claim carries `false`. The compiler sets it from the claims; nothing hand-writes it.
  2. TRANSCRIPTION-MEDIATED READINGS GRADE `documented`, CARRYING A FLAG. The corpus is
     read through OCR-assisted transcriptions, not the page scans, so every claim carries
     `reading: transcription_mediated` — structurally, in a required field, because a
     flag that can be omitted is a flag that will be. This EXTENDS and does not overturn
     `data/sources/chicago_democrat_1833_11_26.json`: where a scan exists and is read,
     the scan is the authority (it caught 'C. & I. HARMON' where the transcription had
     'C. & L. Harmon'), and such a claim carries `reading: scan_verified` — which is why
     that value exists here before anything uses it.
  3. A DOCUMENTED BUSINESS IS BUILT AT THE SCENE DATE UNLESS CONTRADICTED. A dissolution,
     removal or replacement notice is the only veto. The compiler therefore computes two
     things it will not let an author assert by hand: `built_at_scene_date`, false only
     when a claim contradicts the business, and `survival_liberty_required`, true when
     the last ISSUE that carried the business is earlier than 1835 — existence documented,
     survival to the scene date assumed, and docs/LIBERTIES.md carries the liberty.

THE QUOTE IS MACHINE-CHECKED AGAINST THE TRANSCRIPTION, which is the one gate here that
is about provenance rather than shape. A claim names the exact line numbers its quote is
built from, and `--check` reassembles the quote out of the transcription and refuses any
claim whose text does not match, character for character. That is what makes "never
silently smoothed" enforceable instead of aspirational: a smoothed quote fails the gate,
and the smoothed reading has a field of its own to live in (`normalized`).

INTERLEAVED COLUMNS ARE THE NORMAL CASE, NOT AN EXCEPTION. The deposit's advertising type
is segmented into six physical columns per page and the segmenter frequently alternates
two of them line by line, so a single advertisement occupies a SUBSET of a line range with
another advertisement's lines woven through it. `locator.lines` is therefore the range
cited and `locator.lines_of_claim` is the subset the quote is built from; the gate checks
the subset lies inside the range and that the quote is exactly those lines. Unshuffling is
a judgement and it lives in `normalized`, beside the quote and never replacing it, with
`[…]` marking text the column edge cut away. `[…]` is a MARK OF ABSENCE, never a supply:
this file's fixture leaves 'a few doors below' unsupplied for exactly that reason, and
says where a fuller witness might be found.

WHERE THE DEPOSIT IS. The transcriptions are on `main` and not on `dev` (T-0275), so the
quote check runs against whatever text this branch can actually read: the 23 derived
files under `text/` always, the 66 deposit-held ones when the deposit is present. Same
three-state discipline as `tools/newspaper_corpus.py` — present, absent, partial — and
absent is green and reported, never silently skipped.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # chicago/4d
REPO = ROOT.parent.parent                              # repo root
DEPOSIT = REPO / "chicago" / "reference" / "newspapers" / "Transcriptions"
RESEARCH = ROOT / "data" / "research" / "newspapers"
CORPUS = RESEARCH / "corpus.json"
EXTRACTED = RESEARCH / "extracted"
IDENTITY = RESEARCH / "identity.json"
GAZETTEER = RESEARCH / "gazetteer.json"

SCHEMA_VERSION = 1
SCENE_DATE = date(1835, 7, 1)

# The claim vocabulary is closed. An open one becomes a synonym list within a week
# and then the gazetteer cannot be compiled from it.
KINDS = ("person", "business", "building", "street", "infrastructure",
         "event", "shipping", "price", "notice")

# Ruling 2. `transcription_mediated` is what every claim in the corpus carries today;
# `scan_verified` is what a claim read off the page images carries and outranks it.
READINGS = ("transcription_mediated", "scan_verified")

# A placement is how the paper says where a business IS. `corner` and `relative` are
# the two that can put a storefront on the ground; `street_only` and `none` are the
# honest answers when it cannot, and they are values rather than absences so that a
# later pass can count them.
PLACEMENT_CLASSES = ("corner", "relative", "street_only", "none")

# THE DEPOSIT SPEAKS TWO MARKER DIALECTS, and only one of them was written down.
#
# `data/research/newspapers/README.md` says page and column come from
# `===== ISSUE PAGE n / PDF PAGE m / COLUMN k OF 6 =====` markers "which every issue in
# both runs carries". Sixty-six of the eighty-six do — the ones the deposit delivered as
# committed `.txt`. The twenty-three delivered as `.docx` and extracted here by
# `tools/docx_text.py` carry the SAME facts as two prose headings instead:
#
#     Newspaper Page 1 — Source PDF Page 13
#     Column 1
#
# Found building this file's fixture, 2026-08-28. It matters more than it looks: the
# twenty-three are exactly the issues readable on `dev`, where the deposit is absent
# (T-0275), so a resolver that speaks only the first dialect can check a locator on no
# issue this branch can open. Both are read here and the README is corrected to say so.
COLUMN_MARKER = re.compile(
    r"^=====\s*ISSUE PAGE\s+(\d+)\s*/\s*PDF PAGE\s+(\d+)\s*/\s*COLUMN\s+(\d+)\s+OF\s+(\d+)\s*=====\s*$")
PAGE_HEADING = re.compile(r"^\s*Newspaper Page\s+(\d+)\b")
COLUMN_HEADING = re.compile(r"^\s*Column\s+(\d+)\s*$")


def sha256(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dumps(doc):
    """The one serialisation, so `--build` and `--check` cannot disagree by whitespace."""
    return json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def rel_to_repo(path):
    """A recorded path, repo-relative where it can be — and its name where it cannot.

    The self-test compiles the fixture inside a temporary directory, which is by
    construction not under the repo. Recording the bare name there keeps the compile
    reproducible in a sandbox without weakening what the committed file records.
    """
    path = Path(path)
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return path.name


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return s or "unnamed"


# --------------------------------------------------------------------------
# reading the transcription a locator points into


def issue_index(corpus):
    return {e["id"]: e for e in corpus.get("issues", [])}


def artifact_of(issue, role):
    for a in issue.get("artifacts", []):
        if a.get("role") == role:
            return a
    return None


def text_lines(recorded_path, deposit, repo):
    """The lines of a recorded repo-relative text path, or None if unreadable here.

    A deposit-rooted path is re-rooted onto `deposit` exactly as newspaper_corpus.py
    does, so `--deposit` works the same way in both tools and a citation is always
    RECORDED at its canonical `chicago/reference/...` home whatever branch reads it.
    """
    canon = DEPOSIT.relative_to(REPO).as_posix()
    if recorded_path.startswith(canon + "/"):
        target = Path(deposit) / recorded_path[len(canon) + 1:]
    else:
        target = Path(repo) / recorded_path
    if not target.exists():
        return None
    return target.read_text(encoding="utf-8").splitlines()


def column_starts(lines):
    """Every column boundary in a transcription, in both dialects: [(line, page, col)].

    In the heading dialect the page is carried by the most recent `Newspaper Page n`
    line, so a `Column k` before any page heading is skipped rather than guessed at.
    """
    starts = []
    page = None
    for n, line in enumerate(lines, 1):
        m = COLUMN_MARKER.match(line)
        if m:
            starts.append((n, int(m.group(1)), int(m.group(3))))
            continue
        m = PAGE_HEADING.match(line)
        if m:
            page = int(m.group(1))
            continue
        m = COLUMN_HEADING.match(line)
        if m and page is not None:
            starts.append((n, page, int(m.group(1))))
    return starts


def column_span(lines, issue_page, column):
    """The [first, last] 1-based line span of one printed column, or None.

    The marker line itself is excluded: it is the segmenter's, not the paper's.
    """
    starts = column_starts(lines)
    for i, (n, page, col) in enumerate(starts):
        if page == issue_page and col == column:
            end = starts[i + 1][0] - 1 if i + 1 < len(starts) else len(lines)
            return (n + 1, end)
    return None


# --------------------------------------------------------------------------
# compile


def claim_key(issue_id, claim):
    return "%s#%s" % (issue_id, claim.get("id"))


def person_key(name):
    """The identity key: the normalized name, whole.

    Keying on the WHOLE name is the identity policy's first half doing its work
    structurally rather than by inspection — 'Cohen, P.' and 'Cohen, J.' are two keys
    and can never coalesce by accident. The second half (an OCR-variant merge needs a
    stated rule) is `identity.json`, applied below and refused when it is silent.
    """
    return slug(name)


def compile_gazetteer(files, identity, corpus, quiet=True):
    """Compile extracted/* into the gazetteer. Returns (doc, problems).

    Deterministic by construction: inputs are read in sorted filename order, every
    output list is sorted by a stable key, and nothing here reads the clock.
    """
    problems = []
    issues = issue_index(corpus)
    persons = {}
    businesses = {}
    claim_count = 0

    for path in sorted(files, key=lambda p: Path(p).name):
        doc = load_json(path)
        issue_id = doc.get("issue_id")
        issue = issues.get(issue_id)
        if issue is None:
            problems.append("%s: issue_id %r is not in corpus.json"
                            % (Path(path).name, issue_id))
            continue
        issue_date = issue.get("date")
        for claim in doc.get("claims", []):
            claim_count += 1
            key = claim_key(issue_id, claim)
            for ent in claim.get("entities", []):
                name = ent.get("normalized") or ent.get("as_printed")
                pk = person_key(name)
                p = persons.setdefault(pk, {
                    "id": "person_" + pk, "name": name, "variants": [], "mentions": [],
                    "first_seen": issue_date, "last_seen": issue_date,
                    "letter_list_only": True, "occupations": [], "associated_places": [],
                })
                p["variants"].append({"as_printed": ent.get("as_printed"), "claim": key})
                p["mentions"].append(key)
                p["first_seen"] = min(p["first_seen"], issue_date)
                p["last_seen"] = max(p["last_seen"], issue_date)
                # Ruling 1: the two evidence strengths stay distinguishable. A person
                # named in anything OTHER than a letter list has stronger evidence than
                # a listed name, so one such mention retires the flag for good.
                if not claim.get("letter_list_only"):
                    p["letter_list_only"] = False
                for occ in ent.get("occupations", []):
                    if occ not in p["occupations"]:
                        p["occupations"].append(occ)
                for place in ent.get("associated_places", []):
                    if place not in p["associated_places"]:
                        p["associated_places"].append(place)

            biz = claim.get("business")
            if biz:
                bk = slug(biz.get("name"))
                b = businesses.setdefault(bk, {
                    "id": "business_" + bk, "name": biz.get("name"), "proprietors": [],
                    "trade": biz.get("trade"), "goods": [], "street": biz.get("street"),
                    "placement": biz.get("placement"),
                    "evidence": {"first_issue": issue_date, "last_issue": issue_date,
                                 "copy_dates": []},
                    "contradicted_by": [], "mentions": [],
                })
                b["mentions"].append(key)
                b["evidence"]["first_issue"] = min(b["evidence"]["first_issue"], issue_date)
                b["evidence"]["last_issue"] = max(b["evidence"]["last_issue"], issue_date)
                for who in biz.get("proprietors", []):
                    if who not in b["proprietors"]:
                        b["proprietors"].append(who)
                for good in biz.get("goods", []):
                    if good not in b["goods"]:
                        b["goods"].append(good)
                copy_date = (claim.get("ad_copy_date") or {}).get("iso")
                if copy_date and copy_date not in b["evidence"]["copy_dates"]:
                    b["evidence"]["copy_dates"].append(copy_date)
                # Ruling 3's only veto, and it is a CLAIM that carries it — a
                # dissolution or removal notice naming the business, never a hand-set
                # flag on the business itself.
                if claim.get("contradicts"):
                    b["contradicted_by"].append(
                        {"claim": key, "kind": claim.get("kind"), "issue": issue_date})

    # THE MERGES, and every one of them has to say why. `identity.json` is the only
    # place two differently-spelled names may become one person, and the rules below
    # are the whole of the identity policy the ticket names.
    for rule in identity.get("merges", []):
        into, frm = rule.get("into"), rule.get("from")
        why = (rule.get("merge_rule") or "").strip()
        label = "identity.json merge %r <- %r" % (into, frm)
        if not into or not frm:
            problems.append("%s: a merge needs both `into` and `from`" % label)
            continue
        if not why:
            problems.append("%s: no merge_rule — an unexplained merge is a compile error, "
                            "because a wrong one is invisible afterwards" % label)
            continue
        if into not in why or frm not in why:
            problems.append("%s: merge_rule must name BOTH spellings verbatim, so the "
                            "judgement can be read back without the code" % label)
            continue
        if surname(into) == surname(frm) and initials(into) != initials(frm):
            problems.append("%s: same surname, different initials — this project never "
                            "merges those, with or without a rule (the letter lists are "
                            "full of families)" % label)
            continue
        a, b = person_key(into), person_key(frm)
        if a not in persons or b not in persons:
            missing = [n for n, k in ((into, a), (frm, b)) if k not in persons]
            problems.append("%s: %s is not a name any claim carries — a merge rule for a "
                            "person who is not in the corpus is a rule nobody can check"
                            % (label, ", ".join(repr(m) for m in missing)))
            continue
        src = persons.pop(b)
        dst = persons[a]
        dst["variants"].extend(src["variants"])
        dst["mentions"].extend(src["mentions"])
        dst["first_seen"] = min(dst["first_seen"], src["first_seen"])
        dst["last_seen"] = max(dst["last_seen"], src["last_seen"])
        dst["letter_list_only"] = dst["letter_list_only"] and src["letter_list_only"]
        dst["occupations"] = sorted(set(dst["occupations"]) | set(src["occupations"]))
        dst["associated_places"] = sorted(
            set(dst["associated_places"]) | set(src["associated_places"]))
        dst.setdefault("merged", []).append({"from": frm, "merge_rule": why})

    for b in businesses.values():
        # Ruling 3, computed and never asserted: a documented business stands in the
        # 1835 town unless a claim contradicts it, and one whose last issue predates
        # 1835 stands on a survival liberty that has to be written down.
        b["built_at_scene_date"] = not b["contradicted_by"]
        last = date.fromisoformat(b["evidence"]["last_issue"])
        b["survival_liberty_required"] = b["built_at_scene_date"] and last.year < SCENE_DATE.year
        b["goods"].sort()
        b["mentions"].sort()
        b["evidence"]["copy_dates"].sort()
    for p in persons.values():
        p["mentions"].sort()
        p["variants"].sort(key=lambda v: (v["claim"], v["as_printed"] or ""))
        p["occupations"].sort()
        p["associated_places"].sort()

    doc = {
        "schema": SCHEMA_VERSION,
        "generated_by": "tools/compile_gazetteer.py --build",
        "scene_date": SCENE_DATE.isoformat(),
        "compiled_from": [
            {"file": rel_to_repo(p), "sha256": sha256(p)}
            for p in sorted(files, key=lambda p: Path(p).name)
        ],
        "counts": {"claims": claim_count, "persons": len(persons),
                   "businesses": len(businesses)},
        "persons": sorted(persons.values(), key=lambda p: p["id"]),
        "businesses": sorted(businesses.values(), key=lambda b: b["id"]),
    }
    if not quiet:
        print("  ok    %d claim(s) → %d person(s), %d business(es)"
              % (claim_count, len(persons), len(businesses)))
    return doc, problems


def surname(name):
    """'Work, James Houston' → 'work'; 'Peter Cohen' → 'cohen'."""
    name = (name or "").strip()
    if "," in name:
        return slug(name.split(",", 1)[0])
    return slug(name.split()[-1]) if name.split() else ""


def initials(name):
    """The forename initials, in order — the half of a name the letter lists turn on."""
    name = (name or "").strip()
    fore = name.split(",", 1)[1] if "," in name else " ".join(name.split()[:-1])
    return tuple(w[0].lower() for w in re.findall(r"[A-Za-z]+", fore))


# --------------------------------------------------------------------------
# check


def check(extracted=EXTRACTED, gazetteer=GAZETTEER, identity=IDENTITY, corpus=CORPUS,
          deposit=DEPOSIT, repo=REPO, quiet=False):
    bad = []
    corpus_doc = load_json(corpus)
    issues = issue_index(corpus_doc)
    files = sorted(Path(extracted).glob("*.json")) if Path(extracted).exists() else []
    identity_doc = load_json(identity) if Path(identity).exists() else {"merges": []}

    seen_claims = set()
    unresolved = 0
    checked_quotes = 0
    for path in files:
        at = path.name
        try:
            doc = load_json(path)
        except json.JSONDecodeError as exc:
            bad.append("%s is not JSON: %s" % (at, exc))
            continue
        if doc.get("schema") != SCHEMA_VERSION:
            bad.append("%s: schema is %r, this tool speaks %d"
                       % (at, doc.get("schema"), SCHEMA_VERSION))
        issue_id = doc.get("issue_id")
        if path.stem != issue_id:
            bad.append("%s: filename does not match issue_id %r — one file per issue, "
                       "named for it" % (at, issue_id))
        issue = issues.get(issue_id)
        if issue is None:
            bad.append("%s: issue_id %r does not resolve against corpus.json" % (at, issue_id))
            continue
        claims = doc.get("claims") or []
        if not claims:
            bad.append("%s: no claims — an extraction file with nothing in it is a file "
                       "that says the issue was read, and it was not" % at)
        for claim in claims:
            key = claim_key(issue_id, claim)
            if not claim.get("id"):
                bad.append("%s: a claim has no id" % at)
            elif key in seen_claims:
                bad.append("%s: claim id %r is used twice — claim ids are how the "
                           "gazetteer cites, so they must be unique" % (at, claim["id"]))
            seen_claims.add(key)

            # The three fields a claim cannot be made without. `reading` is here
            # rather than defaulted because ruling 2's flag must be impossible to omit.
            for field in ("quote", "locator", "reading"):
                if not claim.get(field):
                    bad.append("%s %s: no %s — a claim without one cannot be made"
                               % (at, key, field))
            if claim.get("kind") not in KINDS:
                bad.append("%s %s: kind %r is not one of %s"
                           % (at, key, claim.get("kind"), "/".join(KINDS)))
            if claim.get("reading") and claim["reading"] not in READINGS:
                bad.append("%s %s: reading %r is not one of %s"
                           % (at, key, claim["reading"], "/".join(READINGS)))
            if claim.get("quote") and not claim.get("normalized"):
                bad.append("%s %s: a quote with no normalized reading — the normalized "
                           "reading sits BESIDE the quote, it does not replace it, and "
                           "an absent one means the judgement was never written down"
                           % (at, key))
            biz = claim.get("business")
            if biz:
                place = biz.get("placement") or {}
                if place.get("class") not in PLACEMENT_CLASSES:
                    bad.append("%s %s: placement class %r is not one of %s"
                               % (at, key, place.get("class"), "/".join(PLACEMENT_CLASSES)))
                if place.get("class") in ("corner", "relative") and not place.get("anchor"):
                    bad.append("%s %s: a %s placement with no anchor places nothing"
                               % (at, key, place.get("class")))
                if place.get("class") == "relative" and not place.get("offset_text"):
                    bad.append("%s %s: a relative placement must carry the paper's own "
                               "offset text verbatim — that text IS the evidence" % (at, key))
            ad = claim.get("ad_copy_date")
            if ad is not None:
                if not ad.get("verbatim"):
                    bad.append("%s %s: ad_copy_date with no verbatim dateline" % (at, key))
                try:
                    date.fromisoformat(ad.get("iso") or "")
                except ValueError:
                    bad.append("%s %s: ad_copy_date.iso %r does not parse"
                               % (at, key, ad.get("iso")))

            loc = claim.get("locator") or {}
            if not loc:
                continue
            role = loc.get("artifact_role")
            art = artifact_of(issue, role)
            if art is None:
                bad.append("%s %s: locator names artifact role %r, which this issue does "
                           "not have" % (at, key, role))
                continue
            span = loc.get("lines")
            if not (isinstance(span, list) and len(span) == 2
                    and all(isinstance(n, int) for n in span) and span[0] <= span[1]):
                bad.append("%s %s: locator.lines must be [first, last]" % (at, key))
                continue
            used = loc.get("lines_of_claim") or list(range(span[0], span[1] + 1))
            if sorted(used) != used or len(set(used)) != len(used):
                bad.append("%s %s: lines_of_claim must be sorted and unique" % (at, key))
            outside = [n for n in used if not span[0] <= n <= span[1]]
            if outside:
                bad.append("%s %s: lines_of_claim %s fall outside the cited range %s"
                           % (at, key, outside, span))

            lines = text_lines(art.get("text_path", ""), deposit, repo)
            if lines is None:
                unresolved += 1
                continue
            if span[1] > len(lines):
                bad.append("%s %s: cites line %d of a %d-line transcription"
                           % (at, key, span[1], len(lines)))
                continue
            col = column_span(lines, loc.get("issue_page"), loc.get("column"))
            if col is None:
                bad.append("%s %s: the transcription carries no ISSUE PAGE %r / COLUMN %r "
                           "marker" % (at, key, loc.get("issue_page"), loc.get("column")))
            elif not (col[0] <= span[0] and span[1] <= col[1]):
                bad.append("%s %s: lines %s are not inside issue page %s column %s, which "
                           "runs %s — the locator's page and column come from the "
                           "transcription's own markers"
                           % (at, key, span, loc.get("issue_page"), loc.get("column"), list(col)))
            # THE QUOTE IS THE TRANSCRIPTION'S, character for character.
            want = "\n".join(lines[n - 1] for n in used)
            if claim.get("quote") is not None and claim["quote"] != want:
                bad.append("%s %s: the quote is not what lines %s of the transcription "
                           "say. A quote is verbatim including its uncertainty brackets; "
                           "the smoothed reading belongs in `normalized`." % (at, key, used))
            else:
                checked_quotes += 1

    doc, compile_problems = compile_gazetteer(files, identity_doc, corpus_doc, quiet=True)
    bad.extend(compile_problems)

    # Determinism, asserted rather than assumed: the same inputs twice, byte for byte.
    again, _ = compile_gazetteer(files, identity_doc, corpus_doc, quiet=True)
    if dumps(doc) != dumps(again):
        bad.append("the compile is not deterministic — two runs over the same inputs "
                   "produced different bytes")

    # THE HAND-EDIT CHECK. gazetteer.json is generated, so the committed file must be
    # exactly what the compiler produces from the committed claims. A hand-edit — a
    # tidied name, an added occupation, a placement nudged to fit a lot — shows up here
    # as a diff and nowhere else, because nothing downstream can tell.
    if not Path(gazetteer).exists():
        bad.append("gazetteer.json is missing — run `--build`")
    elif Path(gazetteer).read_text(encoding="utf-8") != dumps(doc):
        bad.append("gazetteer.json is not what the compiler produces from extracted/* — "
                   "it is GENERATED and was hand-edited or left stale. Fix the claims and "
                   "run `tools/compile_gazetteer.py --build`.")

    for entry in doc["persons"] + doc["businesses"]:
        if not entry.get("mentions"):
            bad.append("%s has no mention — every entry is compiled FROM a claim, so an "
                       "entry with none cannot have come from one" % entry["id"])

    if not quiet:
        state = "present" if Path(deposit).exists() else "absent (this branch has no deposit)"
        print("  ok    %d extraction file(s), %d claim(s), deposit %s"
              % (len(files), len(seen_claims), state))
        print("  ok    %d quote(s) reassembled from the transcription and identical"
              % checked_quotes)
        print("  ok    %d person(s), %d business(es), compile deterministic and committed"
              % (len(doc["persons"]), len(doc["businesses"])))
        if unresolved:
            print("  note  %d claim(s) cite deposit-held text not readable here — it is on "
                  "`main` (T-0275), so their quotes are checked there" % unresolved)
    return bad


def build():
    corpus_doc = load_json(CORPUS)
    identity_doc = load_json(IDENTITY) if IDENTITY.exists() else {"merges": []}
    files = sorted(EXTRACTED.glob("*.json")) if EXTRACTED.exists() else []
    doc, problems = compile_gazetteer(files, identity_doc, corpus_doc, quiet=False)
    for p in problems:
        print("  FAIL  " + p, file=sys.stderr)
    if problems:
        return 1
    GAZETTEER.write_text(dumps(doc), encoding="utf-8")
    print("  wrote %s" % GAZETTEER.relative_to(REPO))
    return 0


# --------------------------------------------------------------------------
# self-test: every assertion above must be capable of firing.


def text_backed_fixture(corpus):
    """A valid extraction file citing a transcription this branch can actually read.

    Built at run time out of the first issue whose primary text is DERIVED — those
    files are committed, so they resolve on `dev` where the deposit does not. The quote
    is assembled from the file rather than written down, which is the point: the cases
    that mutate it are then unambiguously about the gate and not about a stale copy.
    """
    for issue in corpus.get("issues", []):
        art = artifact_of(issue, "primary")
        if not art or art.get("text_path_kind") != "derived":
            continue
        lines = text_lines(art["text_path"], DEPOSIT, REPO)
        if not lines:
            continue
        for n, page, col in column_starts(lines):
            if n + 1 <= len(lines) and lines[n].strip():
                return {
                    "schema": SCHEMA_VERSION,
                    "issue_id": issue["id"],
                    "extracted": "self-test",
                    "claims": [{
                        "id": "s001",
                        "kind": "notice",
                        "reading": "transcription_mediated",
                        "quote": lines[n],
                        "normalized": "(the self-test's own reading)",
                        "locator": {
                            "artifact_role": "primary",
                            "issue_page": page,
                            "column": col,
                            "lines": [n + 1, n + 1],
                            "lines_of_claim": [n + 1],
                        },
                        "entities": [{"as_printed": "A Name", "normalized": "A Name"}],
                    }],
                }
    return None


def self_test():
    failures = []
    corpus_doc = load_json(CORPUS)
    fixtures = sorted(EXTRACTED.glob("*.json"))
    base = load_json(fixtures[0]) if fixtures else None
    if base is None:
        print("FAIL: no extraction fixture to break", file=sys.stderr)
        return 1

    def run(mutate, want, label, identity=None):
        d = copy.deepcopy(base)
        ident = copy.deepcopy(identity) if identity else {"merges": []}
        mutate(d, ident)
        with tempfile.TemporaryDirectory() as td:
            ex = Path(td) / "extracted"
            ex.mkdir()
            (ex / ("%s.json" % d.get("issue_id", "x"))).write_text(
                json.dumps(d, ensure_ascii=False), encoding="utf-8")
            ip = Path(td) / "identity.json"
            ip.write_text(json.dumps(ident), encoding="utf-8")
            gz = Path(td) / "gazetteer.json"
            doc, _ = compile_gazetteer(sorted(ex.glob("*.json")), ident, corpus_doc)
            gz.write_text(dumps(doc), encoding="utf-8")
            bad = check(extracted=ex, gazetteer=gz, identity=ip, corpus=CORPUS,
                        deposit=DEPOSIT, repo=REPO, quiet=True)
        if want is None:
            if bad:
                failures.append("%s: expected a clean run, got %r" % (label, bad))
        elif not any(want in b for b in bad):
            failures.append("%s: expected a failure mentioning %r, got %r" % (label, want, bad))

    # The control: the fixture as committed, re-compiled into a fresh tree, is green.
    run(lambda d, i: None, None, "the fixture itself")

    run(lambda d, i: d["claims"][0].pop("locator"), "no locator", "a claim with no locator")
    run(lambda d, i: d["claims"][0].pop("reading"), "no reading", "a claim with no reading flag")
    run(lambda d, i: d["claims"][0].pop("quote"), "no quote", "a claim with no quote")
    run(lambda d, i: d["claims"][0].update(reading="i read it somewhere"),
        "is not one of", "a reading outside the vocabulary")
    run(lambda d, i: d["claims"][0].update(kind="rumour"), "kind", "a kind outside the vocabulary")
    run(lambda d, i: d["claims"][0].pop("normalized"), "sits BESIDE the quote",
        "a quote with no normalized reading")
    run(lambda d, i: d["claims"][0]["locator"].update(artifact_role="imaginary"),
        "which this issue does not have", "an artifact role the issue lacks")
    run(lambda d, i: d["claims"][0]["locator"].update(lines_of_claim=[1]),
        "fall outside the cited range", "a claim line outside the cited range")
    run(lambda d, i: d.update(issue_id="chicago_democrat_1999_01_01"),
        "does not resolve against corpus.json", "an issue that is not in the corpus")
    run(lambda d, i: d.update(claims=[]), "no claims", "an extraction file with no claims")
    run(lambda d, i: d.update(schema=99), "schema is", "a schema bump")

    # The identity policy, both halves.
    run(lambda d, i: i["merges"].append({"into": "Peter Cohen", "from": "J. S. C. Hogan"}),
        "no merge_rule", "a merge with no stated reason")
    run(lambda d, i: i["merges"].append(
            {"into": "Peter Cohen", "from": "J. S. C. Hogan", "merge_rule": "they look alike"}),
        "name BOTH spellings", "a merge rule that does not name what it merges")
    run(lambda d, i: i["merges"].append(
            {"into": "Cohen, P.", "from": "Cohen, J.",
             "merge_rule": "Cohen, P. and Cohen, J. are surely the same man"}),
        "same surname, different initials", "a silent cross-initial merge")
    run(lambda d, i: i["merges"].append(
            {"into": "Peter Cohen", "from": "Nobody At All",
             "merge_rule": "Peter Cohen and Nobody At All, on a whim"}),
        "not a name any claim carries", "a merge rule for a person nobody claimed")

    # THE ASSERTIONS THAT NEED A TRANSCRIPTION TO READ, and they must fire on `dev`,
    # where the deposit is absent. So they are run against an issue whose text is
    # DERIVED and therefore committed — the American run — with the claim built out of
    # that file at run time, so the control case cannot drift as the corpus grows.
    backed = text_backed_fixture(corpus_doc)
    if backed is None:
        failures.append("no derived-text issue to build the text-backed cases from")
    else:
        def run_backed(mutate, want, label):
            d = copy.deepcopy(backed)
            mutate(d)
            with tempfile.TemporaryDirectory() as td:
                ex = Path(td) / "extracted"
                ex.mkdir()
                (ex / ("%s.json" % d["issue_id"])).write_text(
                    json.dumps(d, ensure_ascii=False), encoding="utf-8")
                ip = Path(td) / "identity.json"
                ip.write_text(json.dumps({"merges": []}), encoding="utf-8")
                doc, _ = compile_gazetteer(sorted(ex.glob("*.json")), {"merges": []}, corpus_doc)
                gz = Path(td) / "gazetteer.json"
                gz.write_text(dumps(doc), encoding="utf-8")
                bad = check(extracted=ex, gazetteer=gz, identity=ip, corpus=CORPUS,
                            deposit=DEPOSIT, repo=REPO, quiet=True)
            if want is None:
                if bad:
                    failures.append("%s: expected a clean run, got %r" % (label, bad))
            elif not any(want in b for b in bad):
                failures.append("%s: expected a failure mentioning %r, got %r"
                                % (label, want, bad))

        run_backed(lambda d: None, None, "a claim read out of a committed transcription")
        run_backed(lambda d: d["claims"][0]["locator"].update(issue_page=99),
                   "no ISSUE PAGE", "a page the transcription does not have")
        run_backed(lambda d: d["claims"][0]["locator"].update(
                       lines=[1, 1], lines_of_claim=[1]),
                   "not inside issue page", "a line range outside its own column")
        run_backed(lambda d: d["claims"][0].update(
                       quote=d["claims"][0]["quote"].replace("\n", " ") + " "),
                   "not what lines", "a quote tidied after the fact")
        run_backed(lambda d: d["claims"][0]["locator"].update(
                       lines=[10 ** 7, 10 ** 7], lines_of_claim=[10 ** 7]),
                   "of a", "a line past the end of the transcription")

    # A hand-edit to the generated file, which is the fault nothing downstream can see.
    with tempfile.TemporaryDirectory() as td:
        ex = Path(td) / "extracted"
        ex.mkdir()
        (ex / ("%s.json" % base["issue_id"])).write_text(
            json.dumps(base, ensure_ascii=False), encoding="utf-8")
        ip = Path(td) / "identity.json"
        ip.write_text(json.dumps({"merges": []}), encoding="utf-8")
        doc, _ = compile_gazetteer(sorted(ex.glob("*.json")), {"merges": []}, corpus_doc)
        doc["persons"][0]["occupations"].append("merchant, surely")
        gz = Path(td) / "gazetteer.json"
        gz.write_text(dumps(doc), encoding="utf-8")
        bad = check(extracted=ex, gazetteer=gz, identity=ip, corpus=CORPUS,
                    deposit=DEPOSIT, repo=REPO, quiet=True)
        if not any("hand-edited" in b for b in bad):
            failures.append("a hand-edit to gazetteer.json was not caught")
        gz.unlink()
        bad = check(extracted=ex, gazetteer=gz, identity=ip, corpus=CORPUS,
                    deposit=DEPOSIT, repo=REPO, quiet=True)
        if not any("is missing" in b for b in bad):
            failures.append("a missing gazetteer.json was not caught")

    if failures:
        for f in failures:
            print("FAIL: " + f, file=sys.stderr)
        return 1
    print("  ok    every gazetteer assertion fires when broken (23 cases)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--deposit", type=Path, default=DEPOSIT)
    args = ap.parse_args(argv)
    if args.build:
        return build()
    if args.self_test:
        return self_test()
    bad = check(deposit=args.deposit)
    for b in bad:
        print("  FAIL  " + b, file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
