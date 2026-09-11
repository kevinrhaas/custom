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

# FIRM OR PERSON IS DECIDED ON THE LEADING TOKENS, NOT ON THE FIRST COMMA (T-1013).
#
# The first version of this test read `FIRM` against the text before the first
# comma. That catches the style with no comma in it — `Sicar & Co. groceries and
# boarding house` — and misses the INVERTED style this volume uses constantly,
# where the surname is set first so the firm files under its alphabet:
#
#     Jones, B. & Co. dry goods and groceries, S. Water, b Clark and Dearborn
#
# Before the comma stands `Jones`, so thirty entries of that shape were read as
# people, and the firm filter in `crosswalk_norris_1844.py` — which exists so a
# company is never matched to a resident of 1835 — never saw them.
#
# THE RULE IS NOT "THE LINE CONTAINS `& Co.`". 124 entries carry that string and
# most of them are people: `Bradley, Joseph, clerk, at W. H. Adams & Co.'s` is a
# clerk naming his employer, and `Burley, A. G. of A. G. B. & Co.` is a partner
# giving his residence. What separates them is WHERE the marker stands. Norris
# sets the name first and the trade after it, so walk the leading tokens and stop
# at the first plain lower-case word (the trade has started) or at `of` (the
# partnership preposition, which can only follow a man's own name). A firm marker
# inside that prefix is a firm; the same marker after it belongs to somebody
# else's firm.
#
# The prefix is also the firm's NAME, so the two readings cannot disagree.
OF_STOP = re.compile(r"(?:^|[^A-Za-z])of(?![A-Za-z0-9])", re.I)
# Lower-case words that are still part of a name, not the start of a trade.
NAME_PARTICLES = {"and", "the", "de", "du", "van"}


def firm_name(prefix):
    """A firm's name ends where its marker does: the ampersand and the partner
    after it. Norris sets the address straight on — `Clyburn & Hovey, Clark st.
    b Lake and Water` — so a name that ran to the end of the prefix would take
    the street with it."""
    for i, tok in enumerate(prefix):
        if tok.startswith("&"):
            return prefix[:i + 2]
    return prefix


def name_prefix(head):
    """The leading run Norris sets before the trade — the name, however styled."""
    keep = []
    for tok in head.split():
        if OF_STOP.search(tok):
            break
        bare = tok.strip(".,'\"")
        if bare.islower() and bare not in NAME_PARTICLES:
            break
        keep.append(tok)
    return keep


# THE SCANNER WELDS `of` ONTO ITS NEIGHBOUR, AND THEN THE STOP WORD IS NOT A WORD.
#
# Three entries of the partner-residence shape lost the space around `of`, so the
# prefix walk above would run straight past the preposition, reach the firm marker
# and read a man as his own company. Two of them the boundary-insensitive OF_STOP
# catches on its own, because what follows `of` is not a letter:
#
#     Eddy, Ira B.-of Eddy & Co. res Michigan avenue
#     Smith, George, of'G. S. & Co. res City Hotel
#
# The third is character damage rather than a lost space — `ofJ5.` for `of B.` —
# and no rule about word boundaries can see it. It is repaired here on the same
# terms as the forename repairs below (T-0695): the reading moves, the quote and
# `as_printed` keep the damage, and the row cites the second hand that read the
# same line off the printed page. Widening OF_STOP to swallow `ofJ5` would also
# swallow every real word beginning in those two letters, which is why this is a
# table of named entries and not a looser regex.
WELDED_OF = [
    {"surname": "Raymond", "as_read": "ofJ5.", "reading": "of B.",
     "second_reading": "Raymond, B.W. of B.W.R. & Co., h Wash. b Clark & Lasalle",
     "file": "1844dir2.txt", "line": 350},
]


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


# THE FIRST COMMA IS NOT ALWAYS NORRIS'S NAME COMMA (T-1018).
#
# `split_entry` takes a person's name as everything before the first comma, which is
# how Norris set it — `Crissman, John M. laborer`. archive.org's OCR loses that comma
# constantly, setting a full stop or nothing at all, and then the name runs on into
# whatever follows: `Wells. Andrew S. of Johoimett W. & Co. h Rand st. b Lasalle and
# Wells` read as a surname of thirteen words, with the trade and the street lost
# inside it.
#
# `name_prefix()` (T-1013) already knows where a name ends — it walks the leading
# tokens and stops at the trade or at `of` — so the repair is to CAP the comma-derived
# name at that prefix. 69 entries read past it. The cap is right for 46 of them and
# would do damage in the other 23, so each of those four classes is refused by name
# and the refusal is written onto the claim.
#
#   firm_branch (7)    The entry is a firm, and the firm branch below never uses the
#                      comma at all — it takes the name from `firm_name(prefix)`. The
#                      overrun is in a span that is not read. Nothing to repair.
#
#   firm_conj (7)      The scanner set the ampersand as `<fc`, `6c` or `it`, so FIRM
#                      never fired and `Bowen & Cole` is read as a man. Capping would
#                      truncate it to `Bowen` and MINT A MAN WHO IS NOT IN THE BOOK —
#                      strictly worse than the run-on. The span is exactly
#                      `Name <conj> Name`, which is what this refusal tests. Widening
#                      FIRM to read those three tokens as ampersands is a separate
#                      ruling about firm/person classification, and `it` is an English
#                      word, so it is filed as its own ticket rather than smuggled in.
#
#   split_surname (4)  The comma IS Norris's name comma and the prefix stops INSIDE a
#                      surname the scanner broke in two: `Went worth, Geo. W.`,
#                      `Lurk in, Timothy`, `Woi thinglnm, Wm.`, `Brine kerb off, John`.
#                      `name_prefix` breaks on the lower-case second half. Capping
#                      would read Wentworth as `Went`. The tell is that the span holds
#                      no capitalised token after the first — no forename, no initial,
#                      so no trade can have started — and a forename stands after the
#                      comma.
#
#   empty_prefix (5)   The reading begins at the trade, so the prefix is empty and the
#                      cap would set the surname to `''` — which drops the claim out of
#                      crosswalk_norris_1844.py, silently, because it skips a claim
#                      with no surname. These are turned lines the entry-boundary rule
#                      mis-cut (`ady` for `<'ady, Dennis S.`) or margin droppings. They
#                      need a ruling of their own; an empty prefix is a REFUSAL.
#
# A refused entry reads exactly as it did before this ticket, and says so on the claim
# in `normalized.name_overrun`. `--self-test` asserts the counts of all five classes.
OVERRUN_CONJ = {"<fc", "6c", "it", "fc", "ic"}

# The 69, by class and by entry id — the self-test's ratchet (see there).
OVERRUN_CLASSES = {
    # --- repaired
    "n1844_e0104": "repaired",            # Bearup^ John I. teacher
    "n1844_e0139": "repaired",            # Birdf J. H. at Dr. Biuinard's
    "n1844_e0275": "repaired",            # Bir/.zard. S. laborer
    "n1844_e0429": "repaired",            # Crissman John M. laborer
    "n1844_e0430": "repaired",            # Crocker Josiah D. white washer
    "n1844_e0550": "repaired",            # Eachus. Virgil H. tailor
    "n1844_e0574": "repaired",            # Enos Wra. C. jr. at A. Clyburn's
    "n1844_e0615": "repaired",            # Flint. Mrs. house Adams st. b Clinton and Jefferson sfs
    "n1844_e0700": "repaired",            # Gilmorc. Win. laborer
    "n1844_e0706": "repaired",            # Godnrd. H. B. clerk
    "n1844_e0749": "repaired",            # Greyhnn. W. hostler
    "n1844_e0754": "repaired",            # Griswold. Clns. E. clerk
    "n1844_e0756": "repaired",            # JrisivoM. David D. res D. S. Griswold's
    "n1844_e0795": "repaired",            # Harmon Charles L. dry goods and groceries
    "n1844_e0918": "repaired",            # Hugunin. L. C. at United States Hotel
    "n1844_e0942": "repaired",            # Jeffries. Gco. warehouse man
    "n1844_e0948": "repaired",            # Jocelyn. J.H. barkeeper at Western Hotel
    "n1844_e1019": "repaired",            # Kimberly Ed. S. physician
    "n1844_e1031": "repaired",            # Kinzie. John H. register land office
    "n1844_e1123": "repaired",            # Lowe. Samuel A. clerk
    "n1844_e1354": "repaired",            # Norton. C. C. of N. & Case
    "n1844_e1388": "repaired",            # Paine. James S. saddler
    "n1844_e1418": "repaired",            # Penton. D. R. at Dr. Britickerhoff's
    "n1844_e1427": "repaired",            # Peterson. GPO. captain schooner St. Joseph
    "n1844_e1443": "repaired",            # Plagge G. shoemaker
    "n1844_e1451": "repaired",            # Powless. John shoemaker
    "n1844_e1460": "repaired",            # Ransom. J. W. res corner Monroe and Clark st
    "n1844_e1502": "repaired",            # Robinson. P. P. boot maker
    "n1844_e1522": "repaired",            # Rowlatt. W. Bethel clergyman
    "n1844_e1525": "repaired",            # Rowley Tlios. E. teamster
    "n1844_e1533": "repaired",            # Russell. C. G. of Rew & Russell
    "n1844_e1590": "repaired",            # Sharer.\"Geo. tailor
    "n1844_e1696": "repaired",            # Steel. J. H. h Lake st. b Water and Canal sts
    "n1844_e1700": "repaired",            # Stevens S. tailor
    "n1844_e1734": "repaired",            # Surdam. S. J. stoves
    "n1844_e1766": "repaired",            # Thompson. Leonard W. carpenter
    "n1844_e1783": "repaired",            # Truesdell. Geo. \\V. clothier
    "n1844_e1830": "repaired",            # Walker. Martin O. of Frink
    "n1844_e1839": "repaired",            # Walton. J. W. dry goods and groceries
    "n1844_e1844": "repaired",            # Ward Mrs. res near North Branch Bridge
    "n1844_e1868": "repaired",            # Wells. Andrew S. of Johoimett W. & Co. h Rand st. b Lasall
    "n1844_e1891": "repaired",            # Wicker. C. G. of C. G. Wicker & Go. res Tremont
    "n1844_e1893": "repaired",            # Wicker. J. H. at C. G. Wicker & Go's
    "n1844_e1936": "repaired",            # AVorcester. D. L. at H. Norton & Co.'s
    "n1844_e1966": "repaired",            # Dennis. Edward M. res Dr. Smith's
    "n1844_e1985": "repaired",            # Greenwood. Theophilus S. house Ontario st. b Dearborn and 
    # --- firm_branch
    "n1844_e0357": "firm_branch",         # Clarke & Co. druggists
    "n1844_e0547": "firm_branch",         # Dyer & Chapin dry goods and groceries
    "n1844_e0554": "firm_branch",         # Eddy & Co. dealers in iron
    "n1844_e1429": "firm_branch",         # Pfund & Co. bakers
    "n1844_e1623": "firm_branch",         # Sicar & Co. groceries
    "n1844_e1817": "firm_branch",         # WTadsworth. E. S. & J. dry goods and groceries
    "n1844_e1892": "firm_branch",         # Wicker. C. G. & Co. dry goods and groceries
    # --- firm_conj
    "n1844_e0063": "firm_conj",           # Ballentine <fc Sherman
    "n1844_e0168": "firm_conj",           # Bowen 6c Cole
    "n1844_e0180": "firm_conj",           # Bracken it Tuller
    "n1844_e0439": "firm_conj",           # Crauer <fc Sanser
    "n1844_e0719": "firm_conj",           # Gould it Dodge
    "n1844_e0787": "firm_conj",           # Hamilton <fc White
    "n1844_e1629": "firm_conj",           # Skinner 6c .Smith
    # --- split_surname
    "n1844_e0198": "split_surname",       # Brine kerb off
    "n1844_e1075": "split_surname",       # Lurk in
    "n1844_e1872": "split_surname",       # Went worth
    "n1844_e1937": "split_surname",       # Woi thinglnm
    # --- empty_prefix
    "n1844_e0009": "empty_prefix",        # house Clark street (See card)
    "n1844_e0276": "empty_prefix",        # ady
    "n1844_e0278": "empty_prefix",        # ilhoun
    "n1844_e0771": "empty_prefix",        # llageman
    "n1844_e1637": "empty_prefix",        # v; Smith
}


def _capitalised(tok: str) -> bool:
    bare = tok.strip(".,'\"<>;:&")
    return bool(bare) and bare[0].isupper()


def overrun_refusal(head: str, prefix, span: str):
    """Why the comma-derived name must NOT be capped at the prefix, or None."""
    toks = span.split()
    over = toks[len(prefix):]
    after = head.split(",", 1)[1].strip() if "," in head else ""
    first_after = after.split()[0] if after else ""
    if not prefix:
        return ("empty_prefix", "the reading begins at the trade, so there is no name to "
                "cap to; an empty surname would drop the claim out of the crosswalk")
    if len(toks) == 3 and over[0] in OVERRUN_CONJ and _capitalised(over[1]):
        return ("firm_conj", "the scanner set this firm's ampersand as %r, so the firm "
                "test never fired; capping would truncate it to a man who is not in "
                "the book" % over[0])
    if not any(_capitalised(t) for t in toks[1:]) and first_after and (
            _capitalised(first_after) or first_after.strip(".,").lower() in TITLES):
        return ("split_surname", "the comma is Norris's own, and the prefix stops inside "
                "a surname the scanner broke in two")
    return None


def split_entry(text: str):
    """name / occupation / address, best effort, out of one printed entry."""
    head, head_repair = repair_welded_of(clean_head(text))
    prefix = name_prefix(head)
    firm = bool(FIRM.search(" ".join(prefix) + ","))
    if "," in head:
        surname, rest = head.split(",", 1)
    else:
        surname, rest = head, ""
    # T-1018. The comma-derived name runs past the end of the name — cap it at the
    # prefix, unless one of the four named classes refuses.
    overrun = None
    capped = False
    if len(surname.split()) > len(prefix):
        reason = ("firm_branch", "the firm branch takes the name from firm_name(prefix) "
                  "and never reads the comma span") if firm else \
            overrun_refusal(head, prefix, surname)
        if reason:
            overrun = {"refused": reason[0], "why": reason[1],
                       "as_split_on_comma": surname.strip(" .&")}
        else:
            overrun = {"repaired": True, "name": " ".join(prefix),
                       "as_split_on_comma": surname.strip(" .&")}
            # With no name comma inside the prefix, Norris's surname is the first
            # token of it and every token after is a forename. `split(None, n)`
            # returns the untouched remainder as its last element, so the trade and
            # the street come back whole however the scanner spaced them.
            parts = head.split(None, len(prefix))
            surname, capped = prefix[0], True
            rest = parts[len(prefix)] if len(parts) > len(prefix) else ""
    surname, rest = surname.strip(" .&"), rest.strip()
    given = []
    if capped:
        # The forenames are the prefix tail, already delimited by the walk — not a
        # guess off the far side of a comma, so the token test below cannot help.
        given = prefix[1:]
    elif not firm:
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
        # A firm's name is the very run the test was decided on, and its trade is
        # what follows: "Sicar & Co. | groceries and boarding house".
        name = " ".join(firm_name(prefix))
        printed = name.strip(" ,.") or head.split(",")[0].strip()
        tail = head[len(name):].strip(" ,.")
        m = PLACE.search(tail)
        occupation = (tail[:m.start()] if m else tail).strip(" ,.")
        address = (tail[m.start():] if m else "").strip(" ,.")
    else:
        printed = surname + (", " + given_s if given_s else "")
    out = {
        "printed_name": printed,
        "surname": None if firm else surname,
        "given": None if firm else (given_s or None),
        "firm": firm,
        "occupation": occupation or None,
        "address": address or None,
    }
    if head_repair:
        out["head_repair"] = head_repair
    if overrun:
        out["name_overrun"] = overrun
    return out


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
UNREPAIRED = []

# T-0903. THE SECOND HAND CANNOT ALWAYS BE ASKED, AND SOMETIMES THERE IS NO NEED.
# The eleven repairs above rest on Kim Torp's transcription. UNREPAIRED held the one
# she could not lift and said what it would take — "It needs the page image" — and
# these four are read off that image. Two classes:
#
#   * Couch, where the second hand wrote "(can't read)" and only the scan can answer.
#   * The compositor's W set by the scanner as two V's. `name_agreement.garbled()`
#     looks for a character no compositor set, and `VV` is made entirely of letters,
#     so the sweep above cannot see this class at all — which is why three of them
#     sat in the file with nothing said about them. The self-test below now asserts
#     that every `VV` in a forename is accounted for here.
#
# The repair goes in the READING. The quote and as_printed keep the damage, and every
# row asserts the token it replaces, so a re-read that moves a line fails the build
# instead of writing the wrong forename onto the wrong man.
IMAGE_SOURCE = (
    "the archive.org scan the OCR is itself made from, item generaldirectory19norr. "
    "Each line was located by its own word coordinates in "
    "generaldirectory19norr_djvu.xml, cropped from the page image on that bounding "
    "box, enlarged and read by eye. The page images are at "
    "https://archive.org/download/generaldirectory19norr/page/leafNN.jpg.")

# THE COORDINATE SPACE IS PER LEAF, NOT PER BOOK (T-0900).
#
# The djvu XML writes each leaf's word boxes in that leaf's OWN pixel space, and this
# scan's leaves are not one size: leaf 31 is 1592 x 2860 and leaves 40, 42 and 49 are
# 1564 x 2912. The first version of this block quoted a single "1592 x 2860" for the
# whole book, which is the size of the first leaf T-0903 happened to read; a reader who
# took it for the coordinate space and cropped leaf 40 by it would land off the line and
# conclude the citation was invented. So every row below carries its OWN leaf size and
# the word box it was cropped on, and a reader reproduces the crop with:
#
#   leaf N's OBJECT in generaldirectory19norr_djvu.xml (index N-1) — its width/height
#   are `leaf_px`, and `word_box` is that WORD element's coords, left,bottom,right,top.
COORDINATE_SPACE = (
    "The word box is this leaf's own OBJECT coordinates in "
    "generaldirectory19norr_djvu.xml, left,bottom,right,top, and leaf_px is the pixel "
    "size of leafNN.jpg, which is that same space. The leaves of this scan are NOT all "
    "one size — do not carry one leaf's dimensions to another.")

IMAGE_REPAIRS = [
    {"surname": "Couch", "as_read": "Iia", "reading": "Ira", "leaf": 40,
     "leaf_px": [1564, 2912], "word_box": "271,2163,358,2125",
     "reads": "Couch, Ira, proprietor of the Tremont House, corner of Lake and Dearborn sts",
     "why": "the r of Ira read as an i. UNREPAIRED asked for this line by name: Kim "
            "Torp reads the same token '(can't read)', so the page image is the only "
            "witness there is, and it prints Ira.",
     "reread": "Ira — the second stroke is an r, with the shoulder and no dot",
     "second_reading": None},
    {"surname": "Abbott", "as_read": "VV", "reading": "W", "leaf": 31,
     "leaf_px": [1592, 2860], "word_box": "248,1776,328,1742",
     "reads": "Abbott, W. clerk at Ward Rathbone's, residence same",
     "why": "the compositor's W set by the scanner as two V's",
     "reread": "W. — one sort, and the Ward two words along is set from the same one",
     "second_reading": "Abbott, W., clerk at Ward Rathbone's, residence same"},
    {"surname": "Day", "as_read": "VVm. Lasalle House", "reading": "Wm. Lasalle House",
     "leaf": 42, "leaf_px": [1564, 2912], "word_box": "199,617,319,582",
     "reads": "Day, Wm. Lasalle House, corner of Lasalle and Randolph sts",
     "why": "the same W. Only the damaged token is repaired: the splitter reads "
            "'Lasalle House' as part of the given name because the line prints no "
            "comma after the forename, and that is a parse, not a transcription defect",
     "reread": "Wm. — and the line prints no comma after it, as the why says",
     "second_reading": "Day, Wm., Lasalle House, corner of Lasalle & Randolph sts"},
    {"surname": "Hequenbourg", "as_read": "G. VV", "reading": "G. W", "leaf": 49,
     "leaf_px": [1564, 2912], "word_box": "495,1758,574,1725",
     "reads": "Hequenbourg, G. W. clerk, at B. F. Sherman's, res same",
     "why": "the same W, on the second of two initials",
     "reread": "G. W. — the second initial is one sort, spaced as an initial",
     "second_reading": "Hequenbourg, G.W., clerk, at B.F. Sherman's, res same"},
]

# T-0900 RE-READ ALL FOUR, off the same leaf images and off nobody's notes.
#
# T-0900 was filed by T-0695 for the Couch line alone and T-0903 answered it the same
# day, so the ticket outlived its work. Closing it on T-0903's say-so would have been
# the cheap move and the wrong one: an image repair is a single hand on a token, and
# this project's whole case for `documented` is that a reading can be gone back to. So
# each row's box was re-cropped from the leaf image and read again, cold, by a second
# hand — the `reread` field above is what that hand saw. All four stand.
#
# It is also what found the coordinate-space defect: the crop only lands on the line
# when the leaf's own dimensions are used, which is how a reader learns that the one
# size quoted for the whole book was wrong.
REREAD_BY = ("T-0900, an independent second reading off the same leaf image, cropped "
             "on the word box recorded with the row.")

# The scanner's W. Letters only, so `name_agreement.garbled()` is blind to it and the
# self-test has to look for it by hand.
SCANNER_W = "VV"

REPAIR_SOURCE = ("Kim Torp's transcription of Norris 1844 for genealogytrails.com "
                 "(\u00a9 2002), cached at data/research/genealogytrails/text/ by "
                 "tools/read_genealogytrails.py --fetch. An independent hand, typed "
                 "from a different copy of the same printed book.")


def repair_welded_of(head):
    """Lift a `of` the scanner welded into its neighbour, so the prefix walk can
    see the stop word. Returns (head, repair record or None) — the caller keeps
    the damaged text in `quote` and `as_printed`."""
    for row in WELDED_OF:
        if head.startswith(row["surname"]) and row["as_read"] in head:
            return head.replace(row["as_read"], row["reading"], 1), {
                "as_read": row["as_read"],
                "reading": row["reading"],
                "why": "The scanner welded the partnership `of` into the token beside "
                       "it, so the entry read as its own firm rather than as a partner "
                       "giving his residence; the quote keeps the damage.",
                "evidence": {
                    "source": REPAIR_SOURCE,
                    "file": "data/research/genealogytrails/text/" + row["file"],
                    "line": row["line"],
                    "reads": row["second_reading"],
                },
                "ticket": "T-1013",
            }
    return head, None


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
    for row in IMAGE_REPAIRS:
        if norm["surname"] == row["surname"] and norm["given"] == row["as_read"]:
            norm["given"] = row["reading"]
            norm["printed_name"] = norm["surname"] + ", " + row["reading"]
            evidence = {
                "source": IMAGE_SOURCE,
                "image": "https://archive.org/download/generaldirectory19norr/page/"
                         "leaf%d.jpg" % row["leaf"],
                "leaf_px": row["leaf_px"],
                "word_box": row["word_box"],
                "coordinate_space": COORDINATE_SPACE,
                "reads": row["reads"],
                "read_a_second_time": {"by": REREAD_BY, "reads": row["reread"]},
            }
            if row["second_reading"]:
                evidence["and_the_second_hand_agrees"] = row["second_reading"]
            else:
                evidence["the_second_hand_cannot_help"] = (
                    "Kim Torp reads this token '(can't read)'. The page image is the "
                    "only witness, which is what UNREPAIRED said it would take.")
            norm["given_repair"] = {
                "as_read": row["as_read"],
                "reading": row["reading"],
                "why": row["why"],
                "evidence": evidence,
                "ticket": "T-0903",
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
    if repaired != len(REPAIRS) + len(IMAGE_REPAIRS):
        warnings.append("%d of %d garbled-forename repairs fired — see --self-test"
                        % (repaired, len(REPAIRS) + len(IMAGE_REPAIRS)))
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
    # T-0903. The page-image repairs, held to the same three rules as the eleven
    # above — fires exactly once, does not repair a reading that was already sound,
    # and does not tidy the quote — plus one the second hand cannot be asked for: an
    # image repair must name the leaf its reading was cropped from.
    for row in IMAGE_REPAIRS:
        hits = [c for c in claims
                if c["normalized"].get("given_repair", {}).get("as_read") == row["as_read"]
                and c["normalized"]["surname"] == row["surname"]]
        if len(hits) != 1:
            fired.append("image repair %s/%r fired on %d entries, not 1 — the reading "
                         "moved under the table" % (row["surname"], row["as_read"], len(hits)))
            continue
        norm = hits[0]["normalized"]
        if row["as_read"] == row["reading"]:
            fired.append("image repair %s/%r is a no-op" % (row["surname"], row["as_read"]))
        if row["as_read"] not in norm["as_printed"] or row["as_read"] not in hits[0]["quote"]:
            fired.append("image repair %s/%r tidied the quote — the damage must stand there"
                         % (row["surname"], row["as_read"]))
        ev = norm["given_repair"]["evidence"]
        if not ev.get("image"):
            fired.append("image repair %s/%r cites no page image, which is the only "
                         "thing that makes it checkable" % (row["surname"], row["as_read"]))
        # T-0900. A page image is only checkable if the reader can find the LINE on it.
        # The word box and the leaf's own pixel size are what make the crop reproducible,
        # and quoting one leaf's size for another is exactly the mistake this catches.
        if not re.fullmatch(r"\d+,\d+,\d+,\d+", row.get("word_box") or ""):
            fired.append("image repair %s/%r cites no word box, so the crop it was read "
                         "from cannot be reproduced" % (row["surname"], row["as_read"]))
        px = row.get("leaf_px") or []
        if len(px) != 2 or not all(isinstance(v, int) and 500 < v < 6000 for v in px):
            fired.append("image repair %s/%r states no plausible leaf size, which is the "
                         "coordinate space its word box is in"
                         % (row["surname"], row["as_read"]))
        elif row["word_box"]:
            l, b, r_, t = (int(v) for v in row["word_box"].split(","))
            if not (0 <= l < r_ <= px[0] and 0 <= t < b <= px[1]):
                fired.append("image repair %s/%r has a word box outside its own leaf: "
                             "%s is not inside %dx%d"
                             % (row["surname"], row["as_read"], row["word_box"], *px))
        if not (row.get("reread") or "").strip():
            fired.append("image repair %s/%r was read by one hand only — T-0900 requires "
                         "a second reading off the image"
                         % (row["surname"], row["as_read"]))

    # The scanner's W is letters only, so na.garbled() is blind to it: nothing above
    # would ever name this class. Assert it by hand instead of trusting the sweep.
    for c in claims:
        norm = c["normalized"]
        as_read = norm.get("given_repair", {}).get("as_read", norm.get("given")) or ""
        if SCANNER_W in as_read and (norm["surname"], as_read) not in \
                {(r["surname"], r["as_read"]) for r in IMAGE_REPAIRS}:
            fired.append("%s reads a forename carrying the scanner's %r with no row in "
                         "IMAGE_REPAIRS — garbled() cannot see this class"
                         % (c["id"], SCANNER_W))
        if SCANNER_W in (norm.get("given") or ""):
            fired.append("%s still reads the scanner's %r after repair"
                         % (c["id"], SCANNER_W))

    known = {(r["surname"], r["as_read"]) for r in REPAIRS}
    known |= {(r["surname"], r["as_read"]) for r in IMAGE_REPAIRS}
    known |= {(r["surname"], r["as_read"]) for r in UNREPAIRED}
    for c in claims:
        norm = c["normalized"]
        as_read = norm.get("given_repair", {}).get("as_read", norm.get("given"))
        if norm.get("given") and na.garbled(as_read or "") and (norm["surname"], as_read) not in known:
            fired.append("%s reads a garbled forename %r with no row in REPAIRS or "
                         "UNREPAIRED" % (c["id"], as_read))
    # T-1013. THE FIRM TEST, AND THE THREE ENTRIES THAT LOOK LIKE FIRMS AND ARE NOT.
    #
    # `& Co.` appears in 124 entries and most of them are people naming somebody
    # else's firm, so the test rests entirely on the marker standing INSIDE the
    # leading name run. Three partner-residence entries lost the space around the
    # `of` that ends that run — two to a boundary OF_STOP still sees, one to
    # character damage WELDED_OF lifts — and each would read as its own company
    # if the walk ran past the preposition. They are asserted by their printed
    # text, so a re-read that moves a line fails here instead of quietly minting
    # four men as firms.
    by_printed = {}
    for c in claims:
        by_printed.setdefault(c["normalized"]["as_printed"], []).append(c)
    for printed in ("Eddy, Ira B.-of Eddy & Co. res Michigan avenue",
                    "Smith, George, of'G. S. & Co. res City Hotel",
                    "Raymond, B. W. ofJ5. W. R. & Co. h Wash, b Clark and Lasalle"):
        hits = by_printed.get(printed, [])
        if len(hits) != 1:
            fired.append("the welded-`of` entry %r is in the reading %d times, not 1 — "
                         "the text moved under the test" % (printed[:40], len(hits)))
        elif hits[0]["normalized"]["firm"]:
            fired.append("%s reads %r as a firm: the walk ran past the partnership "
                         "`of` and made a man his own company"
                         % (hits[0]["id"], printed[:40]))
    for row in WELDED_OF:
        hits = [c for c in claims
                if c["normalized"].get("head_repair", {}).get("as_read") == row["as_read"]]
        if len(hits) != 1:
            fired.append("welded-`of` repair %r fired on %d entries, not 1"
                         % (row["as_read"], len(hits)))
            continue
        if row["as_read"] not in hits[0]["quote"]:
            fired.append("welded-`of` repair %r tidied the quote — the damage must "
                         "stand there" % row["as_read"])
        if OF_STOP.search(row["as_read"]):
            fired.append("welded-`of` repair %r repairs a token OF_STOP already sees, "
                         "so the table is doing the regex's work" % row["as_read"])
    # The two readings of a firm cannot disagree: the name is the run the test was
    # decided on, so a business whose name carries no firm marker is a contradiction.
    for c in claims:
        if c["normalized"]["firm"] and not FIRM.search(c["normalized"]["printed_name"] + ","):
            fired.append("%s is read as a business but its name %r carries no firm "
                         "marker" % (c["id"], c["normalized"]["printed_name"]))
    # T-1018. THE 69 ENTRIES WHOSE NAME RAN PAST THE END OF THE NAME, BY CLASS.
    #
    # The cap is right for 46 and would do damage in 23, so the four refusals are
    # asserted BY ENTRY ID, not by count: the whole risk of this repair is that a
    # re-read moves a line, a refusal stops firing, and the entry is quietly capped
    # to `Went` or to `''`. An entry that leaves its class fails here.
    #
    # `empty_prefix` is the one the acceptance names, because capping to an empty
    # surname is SILENT — crosswalk_norris_1844.py skips a claim with no surname and
    # says nothing — so it is asserted twice: by id, and by the surname it keeps.
    by_id = {c["id"]: c for c in claims}
    for cid, want in OVERRUN_CLASSES.items():
        c = by_id.get(cid)
        if c is None:
            fired.append("%s is named in OVERRUN_CLASSES and is not in the reading" % cid)
            continue
        got = c["normalized"].get("name_overrun")
        got = "repaired" if (got or {}).get("repaired") else (got or {}).get("refused")
        if got != want:
            fired.append("%s was %s by T-1018 and now reads %r — the line moved under "
                         "the classifier" % (cid, want, got))
    seen = {c["id"] for c in claims if c["normalized"].get("name_overrun")}
    for cid in sorted(seen - set(OVERRUN_CLASSES)):
        fired.append("%s reads past the end of its name with no row in OVERRUN_CLASSES: "
                     "%r" % (cid, by_id[cid]["normalized"]["name_overrun"]))
    for cid, want in OVERRUN_CLASSES.items():
        if want == "empty_prefix" and cid in by_id and not by_id[cid]["normalized"]["surname"]:
            fired.append("%s was capped to an empty surname, which drops it out of the "
                         "crosswalk with nothing said" % cid)
    if fired:
        for line in fired:
            print("  " + line, file=sys.stderr)
        print("norris 1844 --self-test: %d case(s) failed" % len(fired), file=sys.stderr)
        return 1
    from collections import Counter
    tally = Counter(OVERRUN_CLASSES.values())
    print("norris 1844 --self-test: %d forename repairs hold against the second hand "
          "and %d against the page image (each read twice, on a reproducible crop), "
          "%d left damaged on purpose"
          % (len(REPAIRS), len(IMAGE_REPAIRS), len(UNREPAIRED)))
    print("norris 1844 --self-test: %d names read past the end of the name — %d capped "
          "at the prefix, %s"
          % (len(OVERRUN_CLASSES), tally["repaired"],
             ", ".join("%d refused %s" % (n, k) for k, n in sorted(tally.items())
                       if k != "repaired")))
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
