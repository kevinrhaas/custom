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
CORRECTIONS = os.path.join(ROOT, "data/research/directories/norris_1844_forename_corrections.json")

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


# T-0695. THE SCANNER'S DAMAGE, READ OFF THE PAGE IMAGE. A forename the OCR broke
# (`C!;as.` for `Chas.`, `Iia` for `Ira`) refuses a match no reader of the page would
# refuse. The repair goes in `normalized.given` and NOWHERE ELSE: `quote` and
# `as_printed` keep the damage, because a tidied quote cannot be found again, and the
# damaged token is kept beside the reading in `given_as_ocr` so the claim itself still
# shows what the machine saw. Every correction asserts the token it replaces, so if the
# text deposit is ever re-read and a line moves, the assertion fails loudly instead of
# writing the wrong forename onto the wrong man.
def load_corrections() -> dict:
    with open(CORRECTIONS, encoding="utf-8") as fh:
        return json.load(fh)["entries"]


def correct_given(claim_id: str, norm: dict, corrections: dict, warnings: list) -> None:
    fix = corrections.get(claim_id)
    if not fix or "given" not in fix:
        return
    was, read = fix["given"]["was"], fix["given"]["read"]
    if norm.get("given") != was:
        warnings.append("%s: the correction expects given %r and the text now reads %r "
                        "— re-read the page before trusting either"
                        % (claim_id, was, norm.get("given")))
        return
    norm["given"] = read
    norm["given_as_ocr"] = was


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


def build_claims():
    claims, warnings = [], []
    corrections = load_corrections()
    n = 0
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
            claim_id = "n1844_e%04d" % n
            norm = split_entry(flat)
            correct_given(claim_id, norm, corrections, warnings)
            norm["as_printed"] = flat
            after = (leaf, first) >= ADDENDA_FROM
            norm["section"] = "addenda" if after else "directory"
            claims.append({
                "id": claim_id,
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
                        "again. The repair, where one is safe, is in normalized.",
        "counts": {"claims": len(claims), "person": people, "business": len(claims) - people},
        "claims": claims,
    }


def self_test() -> int:
    """The corrections' own guard, proved to fire. T-0695: the whole safety of a
    hand-authored repair is that it names the token it replaces, so a re-read that
    moves a line cannot silently put the wrong forename on the wrong man."""
    ok = True

    def want(label, cond):
        nonlocal ok
        print("  %s  %s" % ("ok  " if cond else "FAIL", label))
        ok = ok and bool(cond)

    corrections = load_corrections()
    want("every correction names the token it replaces and the token it reads",
         all(set(f["given"]) >= {"was", "read", "why"} for f in corrections.values()))
    want("no correction is a no-op",
         all(f["given"]["was"] != f["given"]["read"] for f in corrections.values()))

    warnings = []
    norm = {"given": "C!;as"}
    correct_given("n1844_e1875", norm, corrections, warnings)
    want("a matching correction is applied, and keeps the OCR token beside it",
         norm["given"] == "Chas" and norm["given_as_ocr"] == "C!;as" and not warnings)

    warnings = []
    norm = {"given": "Chas"}
    correct_given("n1844_e1875", norm, corrections, warnings)
    want("a correction whose `was` no longer matches the text refuses to apply",
         norm["given"] == "Chas" and "given_as_ocr" not in norm and len(warnings) == 1)

    warnings = []
    norm = {"given": "Thomas L"}
    correct_given("n1844_e0001", norm, corrections, warnings)
    want("an uncorrected entry is left exactly as the text reads it",
         norm == {"given": "Thomas L"} and not warnings)

    claims, build_warnings = build_claims()
    corrected = [c for c in claims if "given_as_ocr" in c["normalized"]]
    want("every correction lands on a claim in the built file, and only there",
         len(corrected) == len(corrections)
         and {c["id"] for c in corrected} == set(corrections))
    want("the quote and as_printed keep the damage",
         all(c["normalized"]["given_as_ocr"] in c["normalized"]["as_printed"]
             or c["normalized"]["given_as_ocr"] in c["quote"] for c in corrected))
    want("the build itself warns about nothing that is a correction",
         not [w for w in build_warnings if "the correction expects given" in w])
    print("norris 1844 corrections self-test: %s" % ("all assertions fire" if ok else "BROKEN"))
    return 0 if ok else 1


def main():
    if "--self-test" in sys.argv:
        return self_test()
    claims, warnings = build_claims()
    doc = payload(claims)
    unmatched = [w for w in warnings if "the correction expects given" in w]
    if unmatched:
        for w in unmatched:
            print("  correction:", w, file=sys.stderr)
        print("norris 1844: %d hand-authored forename correction(s) no longer match the "
              "text they were written against" % len(unmatched), file=sys.stderr)
        return 1
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
