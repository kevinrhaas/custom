#!/usr/bin/env python3
"""Robert Fergus's *Directory of the City of Chicago, Illinois, for 1843* — read
entry by entry (T-0571).

`--build` reads the committed page text under
`data/research/directories/text/fergus_1843_page_00N.txt` and writes
`data/research/directories/claims/fergus_1843_directory_entries.json`.
`--check` rebuilds in memory and compares, so a hand-edit of the generated file
is caught the way `read_norris_1844.py` catches one; it also holds the per-page
counts declared in `coverage.json` to what the text actually yields, because a
declared page that quietly loses forty entries is exactly the hole coverage
exists to catch.

TWO SHAPES ON FOUR PAGES, and the segmenting rule is different for each because
the printer set them differently.

  Page 1, the BUSINESS DIRECTORY (lines 752-1204). Fergus groups these by trade
  under an ALL-CAPS heading and sets each card's subject in FULL CAPITALS at the
  head of its entry. So the heading is a line that shouts and ends in a stop, an
  entry begins where a line begins with a shouted name, and every other line is
  the turn of the entry above. The heading is carried onto the claim as
  `trade_heading`: it is the printer's own classification of the business and is
  worth more than anything a parser could infer from the prose.

  "Shouted" has to be defined carefully, because these cards list their partners
  and their eastern agents in the running prose and the transcription wraps them
  onto a line of their own: "J. R. Hall, Boston, agents", "W. Smith, Patrick
  Ballingall." both open a line with a capital. The head of a card is the leading
  run of tokens that are each an initial, an ampersand, or a word carrying two
  consecutive capitals — and it is a head only if at least one of those words
  does carry them. "C. McDONNELL" and "FREER & DeWOLF" are heads; "A. Rindge" and
  "J. Henry" are the middle of somebody's card.

  Pages 2-4, the ALPHABETICAL DIRECTORY. Fergus sets it in one alphabetical
  sequence broken by letter sections ("-A- Surnames", "H Surnames"). The web
  transcription this project holds wraps the long entries, and it does NOT
  indent the turn — so the indent trick that works for Norris is unavailable.
  The rule here is the directory's own organising principle instead: an entry
  begins where a line begins with a surname IN THE CURRENT LETTER SECTION. A
  turned line that opens with a capital opens with a place or a date — "Ill.,
  Nov. 25,1893, a. 80. ]" under A, "Feb. 22,1862" under B — and its initial is
  not the section's. Where the capital IS the section's letter and the head
  carries no comma, the entry grammar is absent too, and alphabetical order
  decides: `Cass` arriving after `Clarke & Co.` is the tail of that firm's
  address, not a new name.

  Seven times on page 2 the transcription runs a new entry onto the same line as
  the tail of the one before — "aged 84-6. Ballantine, David (B. & Sherman), ..."
  Those are cut mid-line and located with `spans`, which is what `spans` is for.

1843 IS EIGHT YEARS LATE, and Fergus compiled it in 1896 out of the 1844 canvass.
Nothing here is an 1835 fact. Every claim carries `describes_date: "1843"`, and
the crosswalk is the only place a name in this volume may touch a person standing
in the scene of 1 July 1835.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = os.path.join(ROOT, "data/research/directories/text")
OUT = os.path.join(ROOT, "data/research/directories/claims/fergus_1843_directory_entries.json")
COVERAGE = os.path.join(ROOT, "data/research/directories/coverage.json")

PAGE = "fergus_1843_page_%03d"

# Page 1. The business directory and nothing else: the INTRODUCTORY, the civic
# and statistical account before it and the facsimile title-page after it are all
# prose or list-of-office shaped, and coverage.json says whose they are.
BUSINESS_FROM, BUSINESS_TO = 752, 1204

# The transcriber's own furniture, which appears on every page and is not Fergus.
FURNITURE = {"©2007 Kim Torp", "Genealogy Trails", "Back to the Index Page", "Surnames"}

SECTION = re.compile(r"^[-\s]*([A-Z])[-\s]*Surnames\s*$")
HEADING = re.compile(r"^[A-Z][A-Z&,\.\-' ]*\.$")
CAPS_RUN = re.compile(r"[A-Z]{2,}")
INITIAL = re.compile(r"^[A-Z][\.,\-]*$")
BRACKET = re.compile(r"\[[^\[\]]*\]")
FIRM = re.compile(r"\s&\s|&\s*Co\b|\bBrothers\b|\bHouse\b|\bMarket\b", re.I)
TITLES = {"mrs", "miss", "mr", "dr", "capt", "col", "rev", "gen", "maj", "jr", "sr", "sen"}
# Fergus's own abbreviation list, printed in his REMARKS: bet for between, res for
# residence, bds for boards. `cor` and `op.` are his too. The address begins at the
# first of them. Deliberately NOT `at`: "attorney at law" is a trade, and an `at`
# in the list cut sixteen hundred of them in half.
PLACE = re.compile(r"\b(?:res|bds|bet|cor|house|boards|residence|opp?|near|over)\.?\s", re.I)


def lines_of(page: int):
    with open(os.path.join(TEXT, PAGE % page + ".txt"), encoding="utf-8") as fh:
        return fh.read().splitlines()


def fold_surname(s: str) -> str:
    return re.sub(r"[^a-z]", "", (s or "").lower())


def split_name(rest: str):
    """The leading run of name-shaped tokens after the surname comma.

    Stops at the first token that is lower-case or opens a parenthesis, which is
    where Fergus's trade begins: "Adams, Mrs. Maria, laundress" gives "Mrs.
    Maria"; "Allen, James Pierce (J. P A. & Co.) res 9 River" gives "James
    Pierce" and leaves the firm to the occupation.
    """
    given = []
    toks = rest.split()
    for tok in toks:
        bare = tok.strip(".,'\"()").lower()
        if tok.startswith("("):
            break
        if bare in TITLES or re.fullmatch(r"[A-Z]", tok.strip(".,")) or (
                tok[:1].isupper() and len(given) < 4):
            given.append(tok)
            continue
        break
    given_s = " ".join(given).strip(" ,.")
    return given_s, rest[len(" ".join(given)):].strip(" ,.")


def split_entry(flat: str, shouted: bool):
    """name / occupation / address, best effort, out of one printed entry.

    Best effort is the honest word: nineteenth-century directory punctuation is
    not a grammar, `as_printed` carries the whole line, and `quote` carries it
    unedited. What the split is FOR is the crosswalk, which needs a surname and
    an initial and nothing else to be safe.
    """
    notes = [m.group(0)[1:-1].strip() for m in BRACKET.finditer(flat)]
    body = BRACKET.sub(" ", flat)
    body = re.sub(r"\s+", " ", body).strip(" ,.")
    # Fergus sets a handful of his own notes as a whole bracketed entry, in place
    # in the alphabet — "[Jackson Hall, 45 LaSalle, erected 1847 ...]". Stripping
    # the bracket leaves nothing, so the bracket IS the entry: read it as the body
    # and say so, rather than filing a claim with no name in it.
    editorial = not body and len(notes) == 1
    if editorial:
        body = notes[0]
    if shouted:
        # The business directory: the subject is the shouted run at the head.
        printed = shouted_head(body) or body.split(",")[0].strip(" ,.")
        rest = body[len(printed):].strip(" ,.")
        surname = given = None
        if not ("&" in printed or " AND " in printed):
            parts = [p for p in printed.split() if p.strip(".,")]
            if len(parts) >= 2:
                surname = parts[-1].strip(".,").title()
                given = " ".join(t if len(t.strip(".,")) <= 1 else t.title()
                                 for t in parts[:-1])
        firm = surname is None
    else:
        head = body.split(",")[0].strip()
        firm = bool(FIRM.search(head)) or "&" in head
        if firm:
            printed, rest = head.strip(" ,."), body[len(head):].strip(" ,.")
            surname = given = None
        else:
            surname = head.strip(" .")
            given, rest = split_name(body[len(head):].strip(" ,."))
            printed = surname + (", " + given if given else "")
    m = PLACE.search(rest)
    occupation = (rest[:m.start()] if m else rest).strip(" ,.")
    address = (rest[m.start():] if m else "").strip(" ,.")
    return {
        "printed_name": printed,
        "surname": surname,
        "given": given or None,
        "firm": bool(firm),
        "editorial_bracket": editorial,
        "occupation": occupation or None,
        "address": address or None,
        "bracket_notes": notes,
    }


def shouted_head(line: str):
    """The leading run of shouted tokens, or None when the line does not shout.

    A token counts when it is an initial ("J.", "B.-"), an ampersand, or a word
    with two consecutive capitals in it. The run is a HEAD only when at least one
    of its words carries those two capitals, which is what separates "C.
    McDONNELL," opening a card from "J. R. Hall, Boston," turning one.
    """
    keep = []
    for tok in line.split():
        bare = tok.strip(".,;:-'’")
        if tok.startswith("(") or not bare:
            break
        if bare in ("&", "AND") or INITIAL.match(tok) or CAPS_RUN.search(bare):
            keep.append(tok)
            if tok.rstrip("'’").endswith(","):
                break
            continue
        break
    head = " ".join(keep).strip(" ,.-")
    if not head or not CAPS_RUN.search(head):
        return None
    return head


def business_entries(lines):
    """(heading, first_line, last_line) for every card in the business directory."""
    out, heading = [], None
    for i in range(BUSINESS_FROM, BUSINESS_TO + 1):
        line = lines[i - 1]
        s = line.strip()
        if not s or s in FURNITURE:
            continue
        if HEADING.match(s) and len(s) <= 40:
            heading = s.rstrip(".")
            continue
        if shouted_head(line):
            out.append([heading, i, i])
        elif out:
            out[-1][2] = i
    return out


def alpha_entries(lines):
    """(section, first, last, cut) for every entry on an alphabetical page.

    `cut` is None for an entry that owns whole lines, or the character offset in
    `first` at which it begins when the transcription ran it onto the tail of the
    entry above. An entry that is cut always ends on its own last line.
    """
    out, section, started, last_surname = [], None, False, ""
    for i, line in enumerate(lines, 1):
        s = line.strip()
        m = SECTION.match(s)
        if m:
            section, started, last_surname = m.group(1), True, ""
            continue
        if not started or not s or s in FURNITURE:
            continue
        lead = re.sub(r"^[^A-Za-z]+", "", line)
        starts = False
        if lead[:1].isupper() and lead[:1] == section:
            head = line[:45]
            surname = fold_surname(re.split(r"[,\.]", lead, 1)[0])
            # A head with a comma is entry grammar and is taken on sight. Without
            # one, alphabetical order is the test — the directory is sorted, and a
            # capitalised fragment that sorts BEFORE the entry above it is that
            # entry's tail, not a new name.
            starts = ("," in head) or surname >= last_surname
        if starts:
            out.append([section, i, i, None])
            last_surname = fold_surname(re.split(r"[,\.]", lead, 1)[0])
            continue
        if not out:
            continue
        out[-1][2] = i
        # A run-on: a new surname of this section, mid-line, after a closing
        # bracket or a stop. Seven of them, all on page 2.
        for mm in re.finditer(r"(?<=[\]\.\)])\s+([A-Z][a-z][A-Za-z'’\-]*),\s", line):
            if mm.group(1)[:1] != section:
                continue
            surname = fold_surname(mm.group(1))
            if surname < last_surname:
                continue
            cut = mm.end() - len(mm.group(0).lstrip())
            # The entry above now ENDS at the cut, so it needs spans too; the new
            # one begins there and runs on as usual.
            out[-1] = [out[-1][0], out[-1][1], i, out[-1][3], cut]
            out.append([section, i, i, cut])
            last_surname = surname
    return out


def locator(page, first, last, cut, ends_at, lines):
    if cut is None and ends_at is None:
        return {"text_file": PAGE % page + ".txt", "lines": [first, last],
                "page": PAGE % page, "printed_section": None}
    spans = []
    for n in range(first, last + 1):
        frm = cut if (n == first and cut is not None) else 0
        to = ends_at if (n == last and ends_at is not None) else len(lines[n - 1])
        spans.append({"line": n, "from": frm, "to": to})
    return {"text_file": PAGE % page + ".txt", "spans": spans, "page": PAGE % page,
            "printed_section": None}


def rebuild(locator_doc, lines):
    if "spans" in locator_doc:
        return "\n".join(lines[s["line"] - 1][s["from"]:s["to"]] for s in locator_doc["spans"])
    first, last = locator_doc["lines"]
    return "\n".join(lines[first - 1:last])


def build_claims():
    claims, per_page, warnings = [], {}, []
    n = 0

    lines = lines_of(1)
    for heading, first, last in business_entries(lines):
        n += 1
        loc = locator(1, first, last, None, None, lines)
        loc["printed_section"] = heading
        raw = rebuild(loc, lines)
        flat = re.sub(r"\s+", " ", raw).strip()
        norm = split_entry(flat, shouted=True)
        norm["as_printed"] = flat
        norm["section"] = "business directory"
        norm["trade_heading"] = heading
        claims.append(claim(n, norm, raw, loc, kind="business"))
    per_page[PAGE % 1] = n

    for page in (2, 3, 4):
        lines = lines_of(page)
        before = n
        rows = alpha_entries(lines)
        for row in rows:
            section, first, last, cut = row[0], row[1], row[2], row[3]
            ends_at = row[4] if len(row) > 4 else None
            n += 1
            loc = locator(page, first, last, cut, ends_at, lines)
            loc["printed_section"] = section
            raw = rebuild(loc, lines)
            flat = re.sub(r"\s+", " ", raw).strip()
            norm = split_entry(flat, shouted=False)
            norm["as_printed"] = flat
            norm["section"] = "alphabetical directory"
            norm["trade_heading"] = None
            if not norm["printed_name"]:
                warnings.append("page %d line %d: an entry with no name" % (page, first))
            kind = "building" if norm["editorial_bracket"] else (
                "business" if norm["firm"] else "person")
            claims.append(claim(n, norm, raw, loc, kind=kind))
        per_page[PAGE % page] = n - before
    return claims, per_page, warnings


def claim(n, norm, raw, loc, kind):
    return {
        "id": "f1843_e%04d" % n,
        "kind": kind,
        "reading": "transcription_mediated",
        "quote": raw,
        "normalized": norm,
        "locator": loc,
        "describes_date": "1843",
        "entities": [norm["printed_name"]] if norm["printed_name"] else [],
        "town_finding": False,
        "notes": None,
    }


DOC = ("GENERATED by tools/read_fergus_1843.py --build out of the committed page text in "
       "data/research/directories/text/. Hand-edit and --check says so. Every entry of the "
       "business directory on page 1 and of the alphabetical directory on pages 2-4, one "
       "claim each, quote verbatim off the transcription and the reading beside it. 1843, "
       "not 1835 — see the crosswalk.")


def payload(claims, per_page):
    people = sum(1 for c in claims if c["kind"] == "person")
    buildings = sum(1 for c in claims if c["kind"] == "building")
    return {
        "schema": 1,
        "_doc": DOC,
        "generated_by": "tools/read_fergus_1843.py --build",
        "source_id": "fergus_chicago_directory_1843",
        "corpus": {
            "item": "genealogytrails cook county / 1843directory_1..4",
            "url": "https://genealogytrails.com/ill/cook/1843directory_1.html",
            "what": "K. Torp's 2007 transcription, on Genealogy Trails, of Robert Fergus, "
                    "Directory of the City of Chicago, Illinois, for 1843 (Fergus Historical "
                    "Series No. 28; Chicago: Fergus Printing Company, 1896). Four web pages: "
                    "the civic account and business directory, then the alphabetical "
                    "directory in A-G, H-O and P-Z.",
            "committed": True,
            "how": "Cached into this repository on 2026-09-03 by "
                   "tools/read_genealogytrails.py and copied here byte for byte. The text "
                   "under data/research/directories/text/ is identical to the cache under "
                   "data/research/genealogytrails/text/, so a line number means the same "
                   "thing in both.",
        },
        "reading_note": "transcription_mediated throughout, and doubly so: this is a web "
                        "transcription of Fergus's 1896 printing of a canvass made in 1843, "
                        "and nobody on this project has seen the page. The transcriber's "
                        "damage is left in every quote on purpose — 'accidentially', "
                        "'John S.Wright', 'aged - .' — because a tidied quote cannot be "
                        "found again. The repair, where one is safe, is in normalized, and "
                        "normalized is best effort: the split of a printed line into name / "
                        "occupation / address is a heuristic over punctuation that is not a "
                        "grammar.",
        "counts": {"claims": len(claims), "person": people, "building": buildings,
                   "business": len(claims) - people - buildings, "by_page": per_page},
        "claims": claims,
    }


def declared_counts():
    """The per-page counts this domain's coverage.json declares for T-0571."""
    with open(COVERAGE, encoding="utf-8") as fh:
        cov = json.load(fh)
    for dec in cov.get("declarations") or []:
        if dec.get("ticket") == "T-0571":
            return dec.get("entries_by_item") or {}
    return {}


def main():
    claims, per_page, warnings = build_claims()
    doc = payload(claims, per_page)
    if "--check" in sys.argv:
        with open(OUT, encoding="utf-8") as fh:
            got = json.load(fh)
        if got != doc:
            print("fergus 1843: the committed entries do not match the text — "
                  "regenerate with --build", file=sys.stderr)
            return 1
        declared = declared_counts()
        if declared != per_page:
            print("fergus 1843: coverage.json declares %r and the text yields %r"
                  % (declared, per_page), file=sys.stderr)
            return 1
        print("fergus 1843: %d entries, and they match the committed text and the "
              "counts coverage.json declares" % len(claims))
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    for w in warnings:
        print("  warning:", w)
    print("fergus 1843: %d entries (%d person, %d business, %d building) → %s"
          % (len(claims), doc["counts"]["person"], doc["counts"]["business"],
             doc["counts"]["building"], os.path.relpath(OUT, ROOT)))
    print("  by page:", json.dumps(per_page))
    return 0


if __name__ == "__main__":
    sys.exit(main())
