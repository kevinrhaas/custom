#!/usr/bin/env python3
"""*Fergus' Directory of the City of Chicago, 1839* — read entry by entry (T-0506).

`--build` reads the committed page text under
`data/research/directories/text/fergus_1839_leaf_*.txt` and writes two claims files:
`claims/fergus_1839_directory_entries.json`, the alphabetical directory on printed
pages 5-36, and `claims/fergus_1839_town_findings.json`, the churches, hotels and
public places on printed page 37. `--check` rebuilds in memory and compares, so a
hand-edit of either generated file is caught the way `read_norris_1844.py` catches
one.

THE STRUCTURE IS THE INDENT, exactly as in Norris 1844: an entry is set flush left
and its continuation is turned in, and the committed text keeps that with two
leading spaces taken off the word coordinates of the scan.

1839 IS FOUR YEARS LATE, and this volume is later still. Two facts about it govern
every use downstream, and both are the compiler's own words on printed page 3:

  * The 1839 original was six blank pages at the back of the City's Laws and
    Ordinances, filled with "the names of the business men of the City ... no
    canvass was necessary, and the names were never written". What is printed here
    is Fergus's 1876 COMPLETION of that list out of the recollections of the Old
    Settlers he names on printed page 4 — so an entry is 1839 evidence recalled in
    1876, not an 1839 record.
  * "There were no numbers on any street (except Lake Street,) at that time — the
    numbers now given are those of the present day." EVERY STREET NUMBER IN THIS
    DIRECTORY EXCEPT ON LAKE STREET IS AN 1876 NUMBER. It locates nothing in 1839
    and less in 1835. The street NAME is the reading that survives; the number is
    carried in `as_printed` and marked in `normalized.number_is_1876`.

Nothing here is an 1835 fact. Every claim carries `describes_date: "1839"`, and the
crosswalk is the only place a name in this volume may touch a person in the scene.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = os.path.join(ROOT, "data/research/directories/text")
OUT = os.path.join(ROOT, "data/research/directories/claims/fergus_1839_directory_entries.json")
OUT_TOWN = os.path.join(ROOT, "data/research/directories/claims/fergus_1839_town_findings.json")

# The alphabetical directory: leaves 17-48 of the scan, printed pages 5-36.
FIRST_LEAF, LAST_LEAF, LEAF_TO_PRINTED = 17, 48, -12
# The churches, hotels and public places, printed page 37.
TOWN_LEAF = 49

# Prose and furniture inside the directory pages, skipped by line number because no
# rule separates it from an entry — it is the compiler talking, or the scanner.
SKIP = {
    44: (55, 56),  # the footnote on the man hanged in 1840 — two lines, not an entry
}

# The specks the left margin of this scan collects — a stray backslash, a bullet, a
# lone digit — land in the OCR as their own line and are indented enough to read as
# turned. A turned line carrying fewer than three letters is one of those, and it is
# left in the committed text and attached to no entry.
def dropping(line: str) -> bool:
    return sum(c.isalpha() for c in line) < 3

FIRM = re.compile(r"^[^,]{0,40}\s&\s|&\s*Co\b|\bBrothers\b", re.I)
TITLES = {"mrs", "miss", "mr", "dr", "capt", "col", "rev", "gen", "maj", "jr", "sr",
          "sen", "hon", "esq", "prof", "lieut", "gov", "judge"}
PLACE = re.compile(r"\b(?:h|house|res|residence|r|boards|bds|b)\.?\s", re.I)
# A street number, and whether it is on Lake street — the one street the compiler
# says was numbered in 1839.
NUMBER = re.compile(r"\b\d{1,3}\b")
LAKE = re.compile(r"\bLake\b", re.I)

STREET_WORD = r"(?:st|street|streets|sts|ave|avenue|av|road|rd|alley|place|court|square)"
STREET = re.compile(
    r"\b((?:North|South|East|West|N|S|E|W|No|So)\.?\s+)?"
    r"([A-Z][A-Za-z'’]+(?:\s+[A-Z][A-Za-z'’]+)?)\s+" + STREET_WORD + r"\b\.?", re.I)


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
    path = os.path.join(TEXT, "fergus_1839_leaf_%03d.txt" % leaf)
    return open(path, encoding="utf-8").read().splitlines()


def clean_head(text: str) -> str:
    """Strip the scanner's marginal droppings from the front of an entry line."""
    return re.sub(r"^[^A-Za-z]*(?:[a-zA-Z]\s)?", "", text).strip()


def streets_in(text: str):
    """Every street named in an address, as printed. A clue, not a gazetteer."""
    found, seen = [], set()
    for m in STREET.finditer(text or ""):
        s = re.sub(r"\s+", " ", m.group(0)).strip(" .")
        key = s.lower()
        if key not in seen:
            seen.add(key)
            found.append(s)
    return found


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
    if firm:
        keep = []
        for tok in head.split(",")[0].split():
            if tok.islower() and tok.strip(".") not in ("and", "of", "the", "de", "du", "van"):
                break
            keep.append(tok)
        printed = " ".join(keep).strip(" ,.") or head.split(",")[0].strip()
    else:
        printed = surname + (", " + given_s if given_s else "")
    # The trade and the address are not reliably separated by the comma in this
    # volume — many entries run "carpenter, Monroe street, near Dearborn". Take the
    # address as everything from the first street name onward when PLACE found none.
    if not address:
        sm = STREET.search(occupation)
        if sm:
            cut = sm.start()
            # A house number stands in front of its street: "carpenter, 154 Clark
            # street" splits after the trade, not after the number.
            back = re.search(r"(\d{1,3})\s*$", occupation[:cut])
            if back:
                cut = back.start(1)
            address, occupation = occupation[cut:].strip(" ,."), \
                occupation[:cut].strip(" ,.")
    streets = streets_in(address)
    numbers = NUMBER.findall(address or "")
    return {
        "printed_name": printed,
        "surname": None if firm else surname,
        "given": None if firm else (given_s or None),
        "firm": firm,
        "occupation": occupation or None,
        "address": address or None,
        "streets": streets,
        # The compiler's own warning, applied: a number off Lake street is 1876's.
        "number_is_1876": bool(numbers) and not LAKE.search(address or ""),
    }


def build_entries():
    claims, warnings = [], []
    n = 0
    for leaf in range(FIRST_LEAF, LAST_LEAF + 1):
        lines = leaf_lines(leaf)
        printed = leaf + LEAF_TO_PRINTED
        skip = SKIP.get(leaf, ())
        entries = []  # [first_line, last_line]
        for i, line in enumerate(lines, 1):
            if i in skip:
                continue
            if i <= 3 and header_like(line):
                continue
            if line.startswith("  "):
                if dropping(line):
                    continue
                if entries and entries[-1][1] == i - 1:
                    entries[-1][1] = i
                else:
                    warnings.append("leaf %d line %d: a turned line with no entry above it"
                                    % (leaf, i))
                continue
            if not line.strip():
                continue
            entries.append([i, i])
        for first, last in entries:
            n += 1
            raw = "\n".join(lines[first - 1:last])
            flat = re.sub(r"\s+", " ", raw.replace("-\n", "")).strip()
            norm = split_entry(flat)
            norm["as_printed"] = flat
            claims.append({
                "id": "f1839_e%04d" % n,
                "kind": "business" if norm["firm"] else "person",
                "reading": "transcription_mediated",
                "quote": raw,
                "normalized": norm,
                "locator": {
                    "text_file": "fergus_1839_leaf_%03d.txt" % leaf,
                    "lines": [first, last],
                    "page": "fergus_1839_leaf_%03d" % leaf,
                    "printed_page": printed,
                },
                "describes_date": "1839",
                "entities": [norm["printed_name"]] if norm["printed_name"] else [],
                "town_finding": False,
                "notes": None,
            })
    return claims, warnings


# Printed page 37 is not a name list: it is the town itself, set out in four blocks
# the page separates by heading and by nothing else. The line map is written out
# here rather than sniffed, because forty lines read by eye beat a rule that has to
# guess whether "Egan Row" is a building or a business.
TOWN_LINES = [
    (2, 9, "building", "church"),
    (11, 25, "business", "hotel"),
    (26, 33, "building", "public_office"),
    (34, 37, "building", "public_room"),
    (38, 39, "building", "row"),
    (40, 40, "landscape", "settlement"),
    (41, 42, "event", "fire"),
]
TOWN_SKIP = {10}  # the centred HOTELS. heading


def build_town():
    lines = leaf_lines(TOWN_LEAF)
    claims, n = [], 0
    for first, last, kind, category in TOWN_LINES:
        i = first
        while i <= last:
            if i in TOWN_SKIP:
                i += 1
                continue
            end = i
            while end + 1 <= last and lines[end].startswith("  ") and not dropping(lines[end]) \
                    and (end + 1) not in TOWN_SKIP:
                end += 1
            n += 1
            raw = "\n".join(lines[i - 1:end])
            flat = re.sub(r"\s+", " ", raw).strip()
            name = clean_head(flat).split(",")[0].strip()
            claims.append({
                "id": "f1839_t%03d" % n,
                "kind": kind,
                "reading": "transcription_mediated",
                "quote": raw,
                "normalized": {
                    "as_printed": flat,
                    "name": name,
                    "category": category,
                    "streets": streets_in(flat),
                },
                "locator": {
                    "text_file": "fergus_1839_leaf_%03d.txt" % TOWN_LEAF,
                    "lines": [i, end],
                    "page": "fergus_1839_leaf_%03d" % TOWN_LEAF,
                    "printed_page": TOWN_LEAF + LEAF_TO_PRINTED,
                },
                "describes_date": "1839",
                "entities": [name] if name else [],
                "town_finding": True,
                "notes": None,
            })
            i = end + 1
    return claims


CORPUS = {
    "item": "fergusdirectoryo00ferg",
    "url": "https://archive.org/details/fergusdirectoryo00ferg",
    "what": "Allen County Public Library Genealogy Center scan of Robert Fergus, "
            "Fergus' Directory of the City of Chicago, 1839 (Chicago: Fergus Printing "
            "Company, 1876). 86 leaves.",
    "committed": True,
    "how": "The word coordinates of archive.org's OCR (fergusdirectoryo00ferg_djvu.xml) "
           "give each line its left edge; a line set more than 25 px right of the "
           "MEDIAN line start of its own page — the page is 2238 px wide and the turn "
           "measures about 50 px — is a turned line and is committed with two leading "
           "spaces. Nothing else about the text is touched.",
}

READING_NOTE = (
    "transcription_mediated throughout: this is archive.org's OCR of the printed page, "
    "machine-read and not checked against the image by eye. The damage is left in every "
    "quote on purpose — 'CHICAGO DIEECTQEY' for the title, 'lxls' for 'bds', 'Columbian "
    "blouse' for 'Columbian House' — because a tidied quote cannot be found again. The "
    "repair, where one is safe, is in normalized, and normalized is best effort: the split "
    "of one printed line into name / trade / address is a heuristic over inconsistent "
    "nineteenth-century punctuation.")

DATE_NOTE = (
    "TWO WARNINGS FROM THE COMPILER HIMSELF, printed page 3, and they bind every use of "
    "this file. (1) The 1839 original was six pages of business men's names set up from "
    "memory at the back of the City's Laws and Ordinances; what is printed here is "
    "Fergus's 1876 completion of it from the recollections of the Old Settlers he thanks "
    "on printed page 4. An entry is 1839 evidence RECALLED IN 1876. (2) 'There were no "
    "numbers on any street (except Lake Street,) at that time — the numbers now given are "
    "those of the present day.' Every street number here off Lake street is an 1876 "
    "number and locates nothing in 1839; normalized.number_is_1876 says which. The street "
    "NAME is the reading that survives.")


def payload(claims, town=False):
    if town:
        return {
            "schema": 1,
            "_doc": "GENERATED by tools/read_fergus_1839.py --build out of the committed page "
                    "text. Printed page 37 of the volume: the churches, the hotels, the public "
                    "offices and rooms, the two named rows and the Dutch Settlement, one claim "
                    "each, with the footnote that records the Tremont House fire of 27 October "
                    "1839. Town findings, not names.",
            "generated_by": "tools/read_fergus_1839.py --build",
            "source_id": "fergus_chicago_directory_1839",
            "corpus": CORPUS,
            "reading_note": READING_NOTE,
            "date_note": DATE_NOTE,
            "counts": {"claims": len(claims)},
            "claims": claims,
        }
    people = sum(1 for c in claims if c["kind"] == "person")
    return {
        "schema": 1,
        "_doc": "GENERATED by tools/read_fergus_1839.py --build out of the committed page text "
                "in data/research/directories/text/. Hand-edit and --check says so. Every entry "
                "in the alphabetical directory, printed pages 5-36, one claim each, quote "
                "verbatim off the OCR and the reading beside it. 1839, not 1835 — see the "
                "crosswalk.",
        "generated_by": "tools/read_fergus_1839.py --build",
        "source_id": "fergus_chicago_directory_1839",
        "corpus": CORPUS,
        "reading_note": READING_NOTE,
        "date_note": DATE_NOTE,
        "counts": {"claims": len(claims), "person": people,
                   "business": len(claims) - people},
        "claims": claims,
    }


def main():
    claims, warnings = build_entries()
    town = build_town()
    docs = [(OUT, payload(claims)), (OUT_TOWN, payload(town, town=True))]
    if "--check" in sys.argv:
        for path, doc in docs:
            got = json.load(open(path, encoding="utf-8"))
            if got != doc:
                print("fergus 1839: %s does not match the committed text — regenerate "
                      "with --build" % os.path.relpath(path, ROOT), file=sys.stderr)
                return 1
        print("fergus 1839: %d entries and %d town findings, and they match the "
              "committed text" % (len(claims), len(town)))
        return 0
    for path, doc in docs:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
    for w in warnings:
        print("  warning:", w)
    print("fergus 1839: %d entries (%d person, %d business) and %d town findings"
          % (len(claims), payload(claims)["counts"]["person"],
             payload(claims)["counts"]["business"], len(town)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
