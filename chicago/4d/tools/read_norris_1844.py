#!/usr/bin/env python3
"""Norris's *General Directory and Business Advertiser of the City of Chicago for
the Year 1844* — the directory proper, read entry by entry (T-0555).

`--build` reads the committed page text under
`data/research/directories/text/norris_1844_leaf_*.txt` and writes
`data/research/directories/claims/norris_1844_directory_entries.json`.
`--check` rebuilds in memory and compares, so a hand-edit of the generated file
is caught the way `read_voter_lists.py` catches one.

THE STRUCTURE IS THE INDENT. Norris sets every entry flush left and turns the
long ones in about half an inch. The committed text keeps that: a turned line
carries two leading spaces, taken off the word coordinates of the scan, so the
entry boundaries survive the trip from image to text and can be checked by eye.

1844 IS NINE YEARS LATE. Nothing here is an 1835 fact. Every claim carries
`describes_date: "1844"`, and the crosswalk is the only place a name in this
volume is allowed to touch a person in the 1835 scene.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = os.path.join(ROOT, "data/research/directories/text")
OUT = os.path.join(ROOT, "data/research/directories/claims/norris_1844_directory_entries.json")

# The directory proper: leaves 31-75 of the scan, printed pages 21-65.
FIRST_LEAF, LAST_LEAF, LEAF_TO_PRINTED = 31, 75, -10

# Prose inside the directory pages, skipped by line number because there is no
# rule that separates it from an entry — it is the compiler talking, not a name.
SKIP = {
    31: range(1, 26),   # the title band and Norris's REMARKS on abbreviations
    72: range(18, 28),  # the ADDENDA notice
    75: range(15, 30),  # Norris's own General Intelligence Agency card
}
# The addenda — "names accidentally omitted above" — begins mid-leaf 72.
ADDENDA_FROM = (72, 28)

FIRM = re.compile(r"^[^,]{0,40}\s&\s|&\s*Co\b|\bBrothers\b", re.I)
TITLES = {"mrs", "miss", "mr", "dr", "capt", "col", "rev", "gen", "maj", "jr", "sr", "sen"}
PLACE = re.compile(r"\b(?:h|house|res|residence|r|boards|bds|b)\.?\s", re.I)


def header_like(line: str) -> bool:
    """A running head: short, and either shouting or mostly scanner noise."""
    s = line.strip()
    if not s or len(s) > 45:
        return False
    if len(s) <= 3:
        return True
    letters = [c for c in s if c.isalpha()]
    return not letters or sum(c.isupper() for c in letters) / len(letters) > 0.7


def leaf_lines(leaf: int):
    path = os.path.join(TEXT, "norris_1844_leaf_%03d.txt" % leaf)
    return open(path, encoding="utf-8").read().splitlines()


def clean_head(text: str) -> str:
    """Strip the scanner's marginal droppings from the front of an entry line.

    The left margin of this scan collects specks — a stray quote, a bullet, a
    lone letter — which land in the OCR ahead of the surname. They are removed
    from the READING only; `quote` keeps them, because the quote has to be
    findable in the committed text.
    """
    return re.sub(r"^[^A-Za-z]*(?:[a-zA-Z]\s)?", "", text).strip()


def split_entry(text: str):
    """name / occupation / address, best effort, out of one printed entry."""
    head = clean_head(text)
    firm = bool(FIRM.search(head.split(",")[0] + ","))
    if "," in head:
        surname, rest = head.split(",", 1)
    else:
        surname, rest = head, ""
    surname, rest = surname.strip(" .&"), rest.strip()
    given = []
    if not firm:
        for tok in rest.split():
            bare = tok.strip(".,'\"").lower()
            if bare in TITLES or re.fullmatch(r"[A-Z]", tok.strip(".,")) or (
                    tok[:1].isupper() and len(given) < 3 and not PLACE.fullmatch(tok + " ")):
                given.append(tok)
                continue
            break
        rest = rest[len(" ".join(given)):].strip(" ,.")
    given_s = " ".join(given).strip(" ,.")
    m = PLACE.search(rest)
    occupation = (rest[:m.start()] if m else rest).strip(" ,.")
    address = (rest[m.start():] if m else "").strip(" ,.")
    if not occupation and address:
        occupation, address = "", address
    if firm:
        # A firm's name runs until the trade starts, and the trade starts at the
        # first plain lower-case word: "Sicar & Co. groceries and boarding house".
        keep = []
        for tok in head.split(",")[0].split():
            if tok.islower() and tok.strip(".") not in ("and", "of", "the", "de", "du", "van"):
                break
            keep.append(tok)
        printed = " ".join(keep).strip(" ,.") or head.split(",")[0].strip()
    else:
        printed = surname + (", " + given_s if given_s else "")
    return {
        "printed_name": printed,
        "surname": None if firm else surname,
        "given": None if firm else (given_s or None),
        "firm": firm,
        "occupation": occupation or None,
        "address": address or None,
    }


# GARBLED FORENAMES, REPAIRED (T-0695)
#
# archive.org's OCR sets characters no compositor ever did — `C!;as.` for Chas.,
# `Alonzt> C.` for Alonzo C., a stray quote welded onto Edward and Patrick.
# `tools/name_agreement.garbled()` names them, and a crosswalk refusal raised
# against one of them is a transcription defect, not two people disagreeing.
#
# THE REPAIR MOVES THE READING ONLY. `quote` and `normalized.as_printed` keep
# the damage — the reading_note below is the standing convention, and a tidied
# quote cannot be found again. `normalized.given`, `normalized.printed_name` and
# the claim's `entities` carry the repair, and every repaired claim states it in
# `normalized.given_repair`, so a reader of the card sees both readings.
#
# THE EVIDENCE IS THE SECOND READING, NOT THIS TOOL'S GUESS. Kim Torp typed this
# same directory from the printed page for genealogytrails.com in 2002, off a
# different copy; her transcription is cached at
# `data/research/genealogytrails/text/` and every row below cites it by file and
# line, so the repair can be argued with against a hand that was not this one.
# Where SHE cannot read the token either, the entry stays damaged — see
# UNREPAIRED. Nothing here is inferred from the person the crosswalk would like
# to match: `Hale, J>ctij. F.` reads Benj. F., not the John Hale of 1835.
#
# `surname` + `as_read` is the key, and `--self-test` fails if a row stops
# matching exactly one entry or if a new garbled forename appears with no row.
REPAIRS = [
    {"surname": "Barry", "as_read": 'Edward"', "reading": "Edward",
     "second_reading": "Barry, Edward, laborer, house near North Branch Bridge",
     "file": "1844directory.txt", "line": 109},
    {"surname": "Burch", "as_read": "G/H", "reading": "G.H",
     "second_reading": "Burch, G.H. of Newberry & B, res City Hotel",
     "file": "1844directory.txt", "line": 268},
    {"surname": "Frost", "as_read": "Ge>~", "reading": "Geo",
     "second_reading": "Frost, Geo., h Michigan ave",
     "file": "1844directory.txt", "line": 691},
    {"surname": "Hale", "as_read": "J>ctij. F", "reading": "Benj. F",
     "second_reading": "Hale, Benj. F., botanic physician, 185 Lake st res Wells st",
     "file": "1844directory.txt", "line": 817},
    {"surname": "Kane", "as_read": 'Patrick"', "reading": "Patrick",
     "second_reading": "Kane, Patrick, drayman, house Kinzie st b Clark & Lasalle sts",
     "file": "1844directory.txt", "line": 1032},
    {"surname": "Leach", "as_read": "Patrick^", "reading": "Patrick",
     "second_reading": "Leach, Patrick, laborer, N. Water st. b Dearborn & Wolcott sts",
     "file": "1844directory.txt", "line": 1132},
    {"surname": "Lill", "as_read": "V/m", "reading": "Wm",
     "second_reading": "Lill, Wm. of L. & Diversy, brewers, n Sand & Chicago Ave.",
     "file": "1844directory.txt", "line": 1153},
    {"surname": "Peck", "as_read": "A/.el", "reading": "Azel",
     "second_reading": "Peck, Azel, builder, h Clinton b Washington & Madison sts",
     "file": "1844dir2.txt", "line": 289},
    {"surname": "Perrior", "as_read": 'William"', "reading": "William",
     "second_reading": "Perrior, William, jailor, res Jail buildings",
     "file": "1844dir2.txt", "line": 305},
    {"surname": "Wesencraft", "as_read": "C!;as", "reading": "Chas",
     "second_reading": "Wesencraft, Chas., carpenter and wagon maker, c Clin and Monroe",
     "file": "1844dir2.txt", "line": 764},
    {"surname": "Wood", "as_read": "Alonzt> C", "reading": "Alonzo C",
     "second_reading": "Wood, Alonzo C., mason builder, house Cass st., b Indiana and Ohio",
     "file": "1844dir2.txt", "line": 815},
]

# The damage the second reading cannot lift either. Left exactly as the scanner
# set it, and named here so the next run does not spend itself rediscovering it.
UNREPAIRED = [
    {"surname": "Couch", "as_read": "Iia", "why":
     "The Tremont House entry, and Ira Couch of 1835 kept the Tremont — but Kim "
     "Torp reads this same token as '(can't read)' (1844directory.txt:449), so "
     "there is no second hand to correct it with, and reading 'Ira' into it would "
     "be reading the wanted match into the page. It needs the page image.",
     "file": "1844directory.txt", "line": 449},
]

REPAIR_SOURCE = ("Kim Torp's transcription of Norris 1844 for genealogytrails.com "
                 "(\u00a9 2002), cached at data/research/genealogytrails/text/ by "
                 "tools/read_genealogytrails.py --fetch. An independent hand, typed "
                 "from a different copy of the same printed book.")


def apply_repair(norm):
    """Repair a garbled forename READING in place, and say so. Returns the row."""
    for row in REPAIRS:
        if norm["surname"] == row["surname"] and norm["given"] == row["as_read"]:
            norm["given"] = row["reading"]
            norm["printed_name"] = norm["surname"] + ", " + row["reading"]
            norm["given_repair"] = {
                "as_read": row["as_read"],
                "reading": row["reading"],
                "why": "The printed forename as the scanner set it carries characters "
                       "no compositor did; the quote keeps them and the reading does not.",
                "evidence": {
                    "source": REPAIR_SOURCE,
                    "file": "data/research/genealogytrails/text/" + row["file"],
                    "line": row["line"],
                    "reads": row["second_reading"],
                },
                "ticket": "T-0695",
            }
            return row
    return None


def build_claims():
    claims, warnings = [], []
    n = repaired = 0
    for leaf in range(FIRST_LEAF, LAST_LEAF + 1):
        lines = leaf_lines(leaf)
        printed = leaf + LEAF_TO_PRINTED
        skip = SKIP.get(leaf, ())
        entries = []  # (first_line, last_line)
        for i, line in enumerate(lines, 1):
            if i in skip:
                continue
            if i <= 3 and header_like(line):
                continue
            if line.startswith("  "):
                if entries:
                    entries[-1][1] = i
                else:
                    warnings.append("leaf %d line %d: a turned line with no entry above it"
                                    % (leaf, i))
                continue
            entries.append([i, i])
        for first, last in entries:
            n += 1
            raw = "\n".join(lines[first - 1:last])
            flat = re.sub(r"\s+", " ", raw.replace("-\n", "")).strip()
            norm = split_entry(flat)
            if apply_repair(norm):
                repaired += 1
            norm["as_printed"] = flat
            after = (leaf, first) >= ADDENDA_FROM
            norm["section"] = "addenda" if after else "directory"
            claims.append({
                "id": "n1844_e%04d" % n,
                "kind": "business" if norm["firm"] else "person",
                "reading": "transcription_mediated",
                "quote": raw,
                "normalized": norm,
                "locator": {
                    "text_file": "norris_1844_leaf_%03d.txt" % leaf,
                    "lines": [first, last],
                    "page": "norris_1844_leaf_%03d" % leaf,
                    "printed_page": printed,
                },
                "describes_date": "1844",
                "entities": [norm["printed_name"]] if norm["printed_name"] else [],
                "town_finding": False,
                "notes": None,
            })
    if repaired != len(REPAIRS):
        warnings.append("%d of %d garbled-forename repairs fired — see --self-test"
                        % (repaired, len(REPAIRS)))
    return claims, warnings


DOC = ("GENERATED by tools/read_norris_1844.py --build out of the committed page text in "
       "data/research/directories/text/. Hand-edit and --check says so. Every entry in the "
       "directory proper and its addenda, one claim each, quote verbatim off the OCR and the "
       "reading beside it. 1844, not 1835 — see the crosswalk.")


def payload(claims):
    people = sum(1 for c in claims if c["kind"] == "person")
    return {
        "schema": 1,
        "_doc": DOC,
        "generated_by": "tools/read_norris_1844.py --build",
        "source_id": "norris_directory_1844",
        "corpus": {
            "item": "generaldirectory19norr",
            "url": "https://archive.org/details/generaldirectory19norr",
            "what": "University of Illinois scan of the T. F. Bohan republication (1903) of "
                    "J. W. Norris, General Directory and Business Advertiser of the City of "
                    "Chicago for the Year 1844 (Chicago: Ellis & Fergus). 132 leaves.",
            "committed": True,
            "how": "The word coordinates of archive.org's OCR (generaldirectory19norr_djvu.xml) "
                   "give each line its left edge; a line set in more than 45/400 inch from the "
                   "page's own margin is a turned line and is committed with two leading spaces. "
                   "Nothing else about the text is touched.",
        },
        "reading_note": "transcription_mediated throughout: this is archive.org's OCR of the "
                        "printed page, machine-read and not checked against the image by eye. "
                        "The damage is left in every quote on purpose — 'Win.' for 'Wm.', "
                        "'ISickalls' for 'Nickalls' — because a tidied quote cannot be found "
                        "again. The repair, where one is safe, is in normalized. A forename the "
                        "scanner garbled beyond a compositor's alphabet is repaired against Kim "
                        "Torp's independent transcription of the same directory, and the repaired "
                        "entry carries normalized.given_repair with both readings and the citation "
                        "(T-0695); where that second hand cannot read the token either, the damage "
                        "stands.",
        "counts": {"claims": len(claims), "person": people, "business": len(claims) - people,
                   "given_repairs": sum(1 for c in claims
                                        if "given_repair" in c["normalized"])},
        "claims": claims,
    }


def self_test():
    """The repair table against the book: every row fires exactly once, nothing
    is repaired that was not garbled, and nothing garbled is left unaccounted."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import name_agreement as na
    claims, _ = build_claims()
    fired = []
    for row in REPAIRS:
        hits = [c for c in claims
                if c["normalized"].get("given_repair", {}).get("as_read") == row["as_read"]
                and c["normalized"]["surname"] == row["surname"]]
        if len(hits) != 1:
            fired.append("repair %s/%r fired on %d entries, not 1 — the reading moved "
                         "under the table" % (row["surname"], row["as_read"], len(hits)))
            continue
        norm = hits[0]["normalized"]
        if not na.garbled(row["as_read"]):
            fired.append("repair %s/%r repairs a forename that is not garbled"
                         % (row["surname"], row["as_read"]))
        if na.garbled(norm["given"]):
            fired.append("repair %s/%r leaves the reading garbled: %r"
                         % (row["surname"], row["as_read"], norm["given"]))
        if row["as_read"] not in norm["as_printed"] or row["as_read"] not in hits[0]["quote"]:
            fired.append("repair %s/%r tidied the quote — the damage must stand there"
                         % (row["surname"], row["as_read"]))
    known = {(r["surname"], r["as_read"]) for r in REPAIRS}
    known |= {(r["surname"], r["as_read"]) for r in UNREPAIRED}
    for c in claims:
        norm = c["normalized"]
        as_read = norm.get("given_repair", {}).get("as_read", norm.get("given"))
        if norm.get("given") and na.garbled(as_read or "") and (norm["surname"], as_read) not in known:
            fired.append("%s reads a garbled forename %r with no row in REPAIRS or "
                         "UNREPAIRED" % (c["id"], as_read))
    if fired:
        for line in fired:
            print("  " + line, file=sys.stderr)
        print("norris 1844 --self-test: %d case(s) failed" % len(fired), file=sys.stderr)
        return 1
    print("norris 1844 --self-test: %d forename repairs hold, %d left damaged on purpose"
          % (len(REPAIRS), len(UNREPAIRED)))
    return 0


def main():
    if "--self-test" in sys.argv:
        return self_test()
    claims, warnings = build_claims()
    doc = payload(claims)
    if "--check" in sys.argv:
        got = json.load(open(OUT, encoding="utf-8"))
        if got != doc:
            print("norris 1844: the committed entries do not match the text — "
                  "regenerate with --build", file=sys.stderr)
            return 1
        print("norris 1844: %d entries, and they match the committed text" % len(claims))
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    for w in warnings:
        print("  warning:", w)
    print("norris 1844: %d entries (%d person, %d business) → %s"
          % (len(claims), doc["counts"]["person"], doc["counts"]["business"],
             os.path.relpath(OUT, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
