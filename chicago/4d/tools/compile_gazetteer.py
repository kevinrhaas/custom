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

AND A NAME IS NOT ALWAYS A PERSON (T-0359). The entities a claim carries are keyed on a
name and nothing else, so a signboard the papers name — "Haddock's Tavern", "the Eagle
Hotel" — arrives in the persons table and is then held to a policy written for people:
"Tavern" reads as the surname, "Haddock's" against "Maddock's" as forename initials, and
the families rule refuses a reconciliation the evidence closes. The rule is right and the
subject is wrong. `identity.json`'s `places` is where a name is declared NOT a person,
with the argument written out; `place_merges` then joins two spellings of one building
under a discriminator of its own. Neither touches the families rule, and a declaration
cannot reach a name whose every mention is a post-office letter list — which is what
keeps the letter lists' own Chester House and Rodney House the people they are.

IDENTITY IS DECLARED, NEVER INFERRED, AND FIRMS DECLARE IT DIFFERENTLY FROM PEOPLE
(T-0304). Both are keyed on the whole normalized name, so nothing coalesces by accident,
and `identity.json` is the only place a merge may be stated: `merges` for people,
`firm_merges` for houses, each rule naming both spellings verbatim — and, since T-0399,
`refused_firm_merges` for the groups the surname puts together that are NOT one house,
because the absence of a merge rule reads exactly like a group nobody has judged yet. The
guard is where
they part. A person with the same surname and a different forename initial NEVER merges,
because the letter lists are full of families. A firm cannot be held to that — a '& Co.'
style routinely elides or misprints the forename it trades under, and one Wilson house is
printed 'J. L.', 'Jno. L.', 'Jno. S.', 'Jno.' and bare 'L.' across eleven months — so what
a firm is held to is its PARTNERS: the same set of surnames on both sides, with or without
a rule, plus no street the papers contradict. THE ONE LOOSENING (T-0340) is the style that
names NO partner — a heading whose signature went with the woven half of the column —
because an empty set is not a different partnership, only a printing that did not say; that
escape is DECLARED in `firm_sign_names` and refused for any house a claim ever signed with a
proprietor. AND THE PROPRIETORS ARE A THIRD PLACE
AGAIN (T-0337): a partner's name on a business record is neither a gazetteer person nor a
firm style, so until that ticket one man read two ways stood as two proprietors of his own
house and nothing could see it. Two person-styled proprietors of ONE house sharing a
surname and carrying different read initials are REFUSED until `identity.json` declares
which they are — `proprietor_merges` to join two readings, `proprietor_distinctions` to
hold two men apart. The default is neither merge nor silence, because a house really does
hold brothers and really does hold one man read twice. Merging widens a record and never narrows
one, and ruling 3 below is recomputed afterwards, which is the point: three of that
Wilson house's five spellings were last seen in 1834 and were each claiming a survival
liberty the fourth and fifth disprove.

THE QUOTE IS MACHINE-CHECKED AGAINST THE TRANSCRIPTION, which is the one gate here that
is about provenance rather than shape. A claim names the exact line numbers its quote is
built from, and `--check` reassembles the quote out of the transcription and refuses any
claim whose text does not match, character for character. That is what makes "never
silently smoothed" enforceable instead of aspirational: a smoothed quote fails the gate,
and the smoothed reading has a field of its own to live in (`normalized`).

AND THE INTERLEAVE HAPPENS INSIDE A LINE TOO (T-0261). The Democrat's transcriptions
carry one line per printed line, so naming lines is enough to name an advertisement.
The American's do not: its densest advertising columns arrive as ONE line of up to
11,361 characters in which four separate advertisements and the segmenter's own
coordinate telemetry are woven together. Naming that line quotes seven other things,
which is not a citation. `locator.spans` is therefore the character-level sibling of
`lines_of_claim`: a list of {line, from, to} half-open character ranges, and when it
is present the quote is those ranges joined by a newline instead of those whole lines.
Every range is still verbatim and still machine-checked — the honesty is unchanged,
only the grain is finer. Optional and additive: a claim without `spans` behaves exactly
as it did before, which is why the fixture and the Democrat read need no edit.

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

WHERE THE DEPOSIT IS. The quote check runs against whatever text the branch can actually
read: the 23 derived files under `text/` always, the 66 deposit-held ones when the deposit
is present. Same three-state discipline as `tools/newspaper_corpus.py` — present, absent,
partial — and absent is green and reported, never silently skipped. It WAS absent on `dev`
for a week (T-0275) and ten reading passes ran `--check --deposit <a copy from main>`
because of it; the promotion back-merge has since carried it across, so on `dev` today
every path resolves and `--deposit` is only needed by a checkout that lacks it.
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
COVERAGE = RESEARCH / "coverage.json"

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

# AND A PLACEMENT CAN BELONG TO A HOUSE THE ADVERTISER IS SELLING (T-0412). A `building`
# claim carries an address because the notice gives one, and the extractor attaches the
# business the signature names to it — which is right where the signer KEEPS the house
# and wrong where he is only selling it. P. Pruyne signs "[W]E offer for sale the House
# on [the corner] of Lasalle and Lake streets. [It] is 16 by 30 feet"
# (chicago_democrat_1834_05_21 c001) as VENDOR, and T-0400 merged the record that minted
# into `P. Pruyne & Co.`, whose store the papers put between Clark and Dearborn streets
# across four printings. The corner then stood among that firm's `placement_readings` as
# though it were a second frontage of the store.
#
# It did no harm on this record, and that was luck rather than design: the minting
# claim's own placement was `none`, so `placement_rank` never promoted the corner. A
# vendor notice that happened to be the ONLY reading on its record would have moved a
# firm to a house it was selling — which is what the rule below refuses, once, for every
# such notice the corpus may yet carry.
#
# THE RULE: a claim of kind `building` whose own entities sign it as the VENDOR of that
# building contributes NO placing reading to the business the signature names. What the
# printing said about the firm's own ground is nothing, so it records `{"class": "none"}`
# — the same value every other silent printing records, and the claim key therefore
# still stands in the record's readings rather than being dropped out of the history.
# The notice is NOT thrown away: the printed placement, the address text and the claim go
# on the business as `vendor_placements`, so the judgement can be read back, and the
# claim itself — a documented Chicago house with a corner and a 16-by-30-foot footprint —
# is untouched in `extracted/` where it always was.
#
# WHAT IT DOES NOT REACH, deliberately. `role` is free prose in this corpus (some three
# hundred distinct strings), and a rule that read it loosely would silence an auctioneer
# selling at his own store house — `chicago_democrat_1834_04_16` c008 is exactly that,
# and its business is David Carver's own commission house. So the match is exact: the
# role is `vendor`, or `vendor` followed by a qualifier ("vendor at auction"). Anything
# else is a role somebody has to write a rule for, deliberately, having read it.
VENDOR_ROLES = ("vendor",)


def vendor_role(claim):
    """The role string by which this claim's signature says the advertiser is SELLING.

    Returns the role AS AUTHORED — so the record can quote it — or None. Only a
    `building` claim can carry one: the seller of a building, not its occupant. See the
    ruling above for why the match is exact rather than a search over prose.
    """
    if claim.get("kind") != "building":
        return None
    for ent in claim.get("entities") or []:
        role = (ent.get("role") or "").strip()
        low = role.lower()
        if low in VENDOR_ROLES or any(low.startswith(v + " ") for v in VENDOR_ROLES):
            return role
    return None

# AND A PAPER CAN SAY WHEN A HOUSE OPENED (T-0356). The register had no way to ask the
# question, so it answered a different one: a business whose FIRST issue postdated the
# scene date was excluded as `first_evidence_after_scene_date`, which is the absence of
# earlier evidence and not a statement about the business. Thirty-eight of them, and the
# re-read found Wm. H. Taylor's boot store advertising over a dateline of 8 July 1834 and
# Wm. H. Kennicott saying he had practised dentistry in the town "for the past year".
# Both were excluded from a town they demonstrably stood in.
#
# `announces_opening` is the field the ticket named, and the DATING is the whole of it,
# because the two shapes an opening notice comes in point in opposite directions:
#
#   stated    the notice names a date the business WILL open — "will open a Branch of
#             their House ... on the 14th inst.", "the first term will commence Monday
#             August 17". If that date falls after the scene date, the paper is saying
#             the house was not open on the scene date. THIS is what excludes.
#   effected  the notice announces an opening already made — "has opened", "has taken a
#             shop on Dearborn street". Its date is the LATEST the opening can have been,
#             never the earliest, so it can never exclude: an advertisement dated 7 August
#             is silent about 1 July. When the date falls on or before the scene date it is
#             positive evidence the house was standing, which is what clears the
#             backdating liberty in tools/compile_register.py.
#   undated   the notice announces an opening and dates it nowhere. It carries NO `iso`,
#             and the gate refuses one: a reading with no date behind it must not be given
#             a number to make the arithmetic tidy.
#
# THE FIELD WAS ALREADY THERE AS A BARE `true`, on twenty claims, and nothing read it.
# That is worse than absent: an author who sets it believes the register is listening. The
# gate below now refuses the boolean outright, so the twenty had to be re-read into dated
# readings before this could land — which is where the 8 July 1834 dateline came from.
#
# An `effected` announcement therefore carries the advertisement's OWN dateline and the
# gate refuses any other number, so the reading cannot become a free-hand date. Every
# announcement carries a `note` saying how its date was read ("the 14th inst." in an issue
# of 5 August 1835 is 14 August 1835), and its `verbatim` must appear character for
# character in the claim's `normalized` reading, which is itself tied to the
# machine-checked quote. A dateless opening notice records no field: the paper announced
# an opening and did not date it, and inventing a date is the one thing forbidden here.
OPENING_DATINGS = ("stated", "effected", "undated")

# THE DEPOSIT SPEAKS THREE RULED MARKER DIALECTS AND ONE PROSE ONE, and T-0257 could
# only see two of them.
#
# `data/research/newspapers/README.md` says page and column come from
# `===== ISSUE PAGE n / PDF PAGE m / COLUMN k OF 6 =====` markers "which every issue in
# both runs carries". Sixty-six of the eighty-six carry a ruled marker of some shape —
# the ones the deposit delivered as committed `.txt`. The twenty-three delivered as
# `.docx` and extracted here by `tools/docx_text.py` carry the SAME facts as two prose
# headings instead:
#
#     Newspaper Page 1 — Source PDF Page 13
#     Column 1
#
# THE THIRD RULED DIALECT IS THE MAJORITY ONE. Counted across the deposit on 2026-08-28
# while reading July 1834 (T-0289): 1,176 of the 1,266 ruled column markers name the scan
# page as `SOURCE PDF PAGE` and only 90 as the bare `PDF PAGE` this pattern was written
# against; four more say `ORIGINAL PDF PAGE`. EVERY issue of the second half of 1834 is in
# the majority dialect, so the pattern matched a column marker in none of them.
#
# Nothing caught it because the deposit is absent on `dev` (T-0275): `check` skips the
# page/column assertion outright when it cannot read the text, so a resolver that speaks
# no dialect and a resolver that speaks all three are indistinguishable on this branch.
# The word before `PDF PAGE` is optional here, and the self-test carries a case per ruled
# dialect plus a negative, so the next one cannot be added silently.
COLUMN_MARKER = re.compile(
    r"^=====\s*ISSUE PAGE\s+(\d+)\s*/\s*(?:\w+\s+)?PDF PAGE\s+(\d+)\s*/\s*COLUMN\s+(\d+)\s+OF\s+(\d+)\s*=====\s*$")
PAGE_HEADING = re.compile(r"^\s*Newspaper Page\s+(\d+)\b")
COLUMN_HEADING = re.compile(r"^\s*Column\s+(\d+)\s*$")

# AND A FIFTH SHAPE, WHICH IS THE WHOLE OF 1833 (T-0258). The five issues 1833-11-26 to
# 1833-12-24 separate page from column instead of ruling them onto one line: a page
# banner, then `--- Column 1 ---` before each column. Counted on 2026-08-28 across the
# thirty issues of Vol. I Nos. 1-30, the range T-0258 covers:
#
#     1833-11-26 .. 1833-12-24   5 issues   dash-column, 24-25 columns each, 0 ruled
#     1833-12-31 .. 1834-01-28   5 issues   the prose `Newspaper Page` / `Column` pair
#     1834-02-04 .. 1834-06-25  20 issues   ruled `===== ISSUE PAGE .. COLUMN .. =====`
#
# so a THIRD of this range spoke a dialect the resolver had never been shown, and — the
# same blind spot T-0289 recorded — `dev` cannot tell, because the deposit is not there
# to read and the page/column assertion is skipped outright when the text cannot be
# opened. It is not a rare shape: 121 column markers over five issues.
#
# The page banner comes in two shapes of its own, and only one of them states the page
# of the ISSUE:
#
#     ===== SOURCE PDF PAGE 9 / ISSUE PAGE 1 =====     1833-12-10 .. 1833-12-24
#     SOURCE PDF PAGE 1                                 1833-11-26, 1833-12-03
#
# The second names only the scan page, and the scan page is NOT the issue page — the
# Democrat of 1833-12-03 opens at PDF page 5 because No. 1 occupies 1-4. So the bare
# banner is resolved BY ORDINAL: the first page banner in a transcription is issue page
# 1, the second is issue page 2. That is a reading of the transcription's own stated
# method ("assembled in printed page and column order"), not an inference about the
# paper, and it is the only rule here that is not lifted verbatim off the line. It is
# not used when the banner states the issue page itself.
DASH_COLUMN_HEADING = re.compile(r"^\s*-{2,}\s*Column\s+(\d+)\s*-{2,}\s*$")
RULED_PAGE_BANNER = re.compile(
    r"^=====\s*(?:\w+\s+)?PDF PAGE\s+(\d+)\s*/\s*ISSUE PAGE\s+(\d+)\s*=====\s*$")
BARE_PAGE_BANNER = re.compile(r"^\s*(?:\w+\s+)?PDF PAGE\s+(\d+)\s*$")

# AND A SIXTH SHAPE AND A SEVENTH, WHICH ARE THE FIRST HALF OF 1835 (T-0298). Six of the
# eight Democrats between 1835-01-21 and 1835-06-24 resolved to ZERO columns before this,
# so every claim citing them would have failed the gate with "the transcription carries no
# ISSUE PAGE / COLUMN marker" and the reading pass could not have landed at all. Counted
# on 2026-08-29 over the whole deposit, they are the LAST two: after these, every one of
# the 89 artifacts in corpus.json resolves its columns except the 1833-11-26 alternate,
# which is a prose reading transcription with no column segmentation to find.
#
# T-0298 recorded three of the six as "bare `=====` rules carrying no page or column at
# all" and left open whether that was a transcription defect. IT IS NOT. The rules are
# decoration around a banner, and each column carries its own rule naming the scan page:
#
#   1835-01-21, the 03-25 Extra, 05-20   [Source PDF page 9; newspaper page 1; column 1]
#   1835-05-27, 06-04, 06-10             PRINTED PAGE 1 — SOURCE PDF PAGE 13
#                                        --- SOURCE PDF PAGE 13, COLUMN 1 ---
#
# 46 bracket markers over the first three issues, and 72 dash rules under 12 banners over
# the second three: 118 column markers that were invisible to a resolver already twice
# corrected for exactly this. Nothing else in the corpus moves — the other 83 artifacts
# resolve to the same columns before and after, asserted by re-running the census.
#
# The dash rule of the seventh dialect names its OWN scan page, so it is resolved through
# the banner that states that page rather than through the banner most recently passed.
# There is no ordering assumption here to be wrong about, which is the difference between
# this dialect and the bare 1833 banner that has to be counted ordinally.
#
# ONE MARKER IN THE SIXTH DIALECT CARRIES NO COLUMN NUMBER, and it is read as column 1:
# `[Source PDF page 8; Extra page 4; single-column subscription prospectus]`, the last
# page of the 1835-03-25 Extra. The warrant is the marker's own word and the same file's
# header line — "Extra pages 1–3 have 3 columns; page 4 is a single-column subscription
# prospectus" — so the page has one column and it is the first. That page is Calhoun's
# subscription list and naming people, so leaving it uncitable would have cost the read a
# page rather than saved it a guess.
BRACKET_COLUMN = re.compile(
    r"^\s*\[\s*(?:\w+\s+)?PDF page\s+(\d+)\s*;\s*\w+ page\s+(\d+)\s*;\s*"
    r"(?:column\s+(\d+)|single-column\b[^\]]*)\]\s*$", re.IGNORECASE)
PRINTED_PAGE_BANNER = re.compile(
    r"^\s*PRINTED PAGE\s+(\d+)\s*[\u2014\u2013-]\s*(?:\w+\s+)?PDF PAGE\s+(\d+)\s*$")
SCAN_DASH_COLUMN = re.compile(
    r"^\s*-{2,}\s*(?:\w+\s+)?PDF PAGE\s+(\d+)\s*,\s*COLUMN\s+(\d+)\s*-{2,}\s*$")


# THE ONE ARTIFACT IN THE CORPUS THAT RESOLVES NO COLUMN AND IS NOT A RESOLVER GAP.
# Measured over all 89 artifacts on 2026-08-29 (T-0325): every one of them resolves its
# columns except this, and this one has no column structure to resolve. A reading pass
# that needs 1833-11-26 cites the `primary`, which is what T-0308 did.
UNSEGMENTED = {
    ("chicago_democrat_1833_11_26", "alternate"):
        "a prose reading transcription made from the page images, which segments nothing: "
        "its pages are headed `SUPPLIED SCAN PAGE 1` and its columns described in words "
        "('Left-side news columns'). There is no marker in it to read.",
}


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


def printed_page_index(lines):
    """scan page -> issue page, from `PRINTED PAGE n — SOURCE PDF PAGE m` banners.

    The seventh dialect's column rules name their own SCAN page, so a column is resolved
    through the banner that states that page rather than through the banner most recently
    passed. Both facts are lifted off their own lines and nothing is counted.
    """
    index = {}
    for line in lines:
        m = PRINTED_PAGE_BANNER.match(line)
        if m:
            index.setdefault(int(m.group(2)), int(m.group(1)))
    return index


def column_starts(lines):
    """Every column boundary in a transcription, in every dialect: [(line, page, col)].

    In the dialects that separate page from column the page is carried by the most
    recent page line, so a column before any page line is skipped rather than guessed
    at. A bare `SOURCE PDF PAGE n` banner names the scan page and not the issue page, so
    it counts ordinally: the nth page banner of a transcription is issue page n. The
    seventh dialect is the exception and needs no ordinal at all: its column rules state
    the scan page themselves, so they are looked up in `printed_page_index`.
    """
    starts = []
    page = None
    banners = 0
    printed = printed_page_index(lines)
    for n, line in enumerate(lines, 1):
        m = COLUMN_MARKER.match(line)
        if m:
            starts.append((n, int(m.group(1)), int(m.group(3))))
            continue
        m = BRACKET_COLUMN.match(line)
        if m:
            # group 3 is absent on the Extra's single-column prospectus page, which the
            # marker and its file's own header agree has one column: it is column 1.
            starts.append((n, int(m.group(2)), int(m.group(3) or 1)))
            continue
        m = SCAN_DASH_COLUMN.match(line)
        if m:
            issue_page = printed.get(int(m.group(1)))
            if issue_page is not None:
                starts.append((n, issue_page, int(m.group(2))))
            continue
        m = PAGE_HEADING.match(line)
        if m:
            page = int(m.group(1))
            banners += 1
            continue
        m = PRINTED_PAGE_BANNER.match(line)
        if m:
            page = int(m.group(1))       # group 1 is the issue's page, group 2 the scan's
            banners += 1
            continue
        m = RULED_PAGE_BANNER.match(line)
        if m:
            page = int(m.group(2))       # group 1 is the scan page, group 2 the issue's
            banners += 1
            continue
        m = BARE_PAGE_BANNER.match(line)
        if m:
            banners += 1
            page = banners
            continue
        m = COLUMN_HEADING.match(line) or DASH_COLUMN_HEADING.match(line)
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


def quoted_text(lines, used, spans):
    """What the transcription says at a locator: whole lines, or named char ranges.

    `spans` is the finer grain (T-0261). Each entry is one verbatim piece and the
    pieces are joined by a newline, exactly as whole lines are — so the two forms
    differ in what they name, never in what a quote MEANS.
    """
    if spans:
        return "\n".join(lines[s["line"] - 1][s["from"]:s["to"]] for s in spans)
    return "\n".join(lines[n - 1] for n in used)


def span_problems(spans, used, lines):
    """Everything a `spans` list can be wrong about. Empty list means it is sound."""
    out = []
    if not isinstance(spans, list) or not spans:
        return ["locator.spans must be a non-empty list of {line, from, to}"]
    seen = []
    for sp in spans:
        if not isinstance(sp, dict) or not all(
                isinstance(sp.get(k), int) for k in ("line", "from", "to")):
            out.append("every span needs integer `line`, `from` and `to`")
            return out
        n = sp["line"]
        if n not in used:
            out.append("span cites line %d, which lines_of_claim does not name — a span "
                       "narrows a claimed line, it cannot add one" % n)
            continue
        if lines is not None:
            width = len(lines[n - 1])
            if not (0 <= sp["from"] < sp["to"] <= width):
                out.append("span %d[%d:%d] is not inside a %d-character line"
                           % (n, sp["from"], sp["to"], width))
                continue
        seen.append((n, sp["from"], sp["to"]))
    if seen != sorted(seen):
        out.append("spans must be in reading order, by line then by character")
    for a, b in zip(seen, seen[1:]):
        if a[0] == b[0] and b[1] < a[2]:
            out.append("spans %s and %s overlap — a quote cannot say the same "
                       "characters twice" % (list(a), list(b)))
    if lines is not None:
        named = {n for n, _, _ in seen}
        for n in used:
            if n not in named:
                out.append("line %d is claimed but no span quotes any of it — a claimed "
                           "line the quote does not use is a line that was not read" % n)
    return out


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
                # T-0412. The address in a vendor's for-sale notice is the house he is
                # selling, not the ground his own firm stands on, so it places nothing
                # here and the printing is recorded as the silence it is about the firm.
                printed_placement = biz.get("placement") or {}
                sold_by = vendor_role(claim)
                sold = bool(sold_by) and placement_rank(printed_placement) > 0
                placement = {"class": "none"} if sold else biz.get("placement")
                b = businesses.setdefault(bk, {
                    "id": "business_" + bk, "name": biz.get("name"), "proprietors": [],
                    "trade": biz.get("trade"), "goods": [], "street": biz.get("street"),
                    "placement": placement,
                    "evidence": {"first_issue": issue_date, "last_issue": issue_date,
                                 "copy_dates": []},
                    "contradicted_by": [], "opening_announced": [], "mentions": [],
                    "placement_readings": [],
                })
                b["mentions"].append(key)
                if sold:
                    # The notice, kept where the judgement can be read back off the
                    # record it was made about. Nothing downstream places on this.
                    b.setdefault("vendor_placements", []).append({
                        "claim": key,
                        "issue": issue_date,
                        "role": sold_by,
                        "printed_placement": printed_placement,
                        "address_text": biz.get("address_text"),
                        "rule": "T-0412: the advertiser signs this building notice as its "
                                "VENDOR, so the address is the house he is selling and not "
                                "the ground his own house stands on. It places nothing "
                                "here; the building itself stands in the claim.",
                    })
                # EVERY PRINTING'S OWN PLACEMENT, KEPT (T-0345). The dict above takes
                # the placement of whichever claim mints the key, and until now every
                # later printing's was thrown away — which is why a house whose printed
                # anchor CHANGES could not be represented at all. Mason & Co.'s standing
                # advertisement is set "nearly opposite Graves' Tavern" to 1834-07-16 and
                # "opposite the Tremont House" from 1834-09-10 under the same copy date,
                # and the gazetteer held only the first. Readings collapse on (class,
                # anchor) and carry their own dates: this is what each printing SAID and
                # when, not a judgement about it. The judgement is `anchor_changes`.
                record_reading(b, placement or {}, issue_date, key)
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
                # T-0356. The gazetteer says what was PRINTED, so every announcement a
                # printing carries is kept; which of them the scene date obeys is the
                # register's judgement and is made there.
                op = claim.get("announces_opening")
                if isinstance(op, dict):
                    b["opening_announced"].append(
                        {"claim": key, "issue": issue_date, "dating": op.get("dating"),
                         "iso": op.get("iso"), "verbatim": op.get("verbatim"),
                         "note": op.get("note")})

    # THE PLACES, and they are DECLARED, exactly the way a merge is (T-0359). The table
    # above is keyed on a name and knows nothing about what kind of thing a name is, so a
    # signboard the papers name — "Haddock's Tavern", "the Eagle Hotel" — is minted as a
    # person and then held to the identity policy for PEOPLE. That policy reads "Tavern"
    # as the surname and "Haddock's" against "Maddock's" as forename initials, and
    # refuses the merge under the families rule. The rule is not wrong; it is being
    # applied to something that is not a person. So a name leaves the persons table only
    # where `identity.json` declares it a place and says why, and the families rule for
    # actual people is untouched by every line below.
    #
    # Four guards, and each one is a way this declaration could quietly delete a person:
    #   1. a place needs a written reason that names it VERBATIM, so the judgement can be
    #      read back without the code — the merges' rule, for the same reason;
    #   2. the name has to be one some claim actually carries, or nobody can check it;
    #   3. a name known ONLY from the post office's lists of uncalled-for letters is
    #      somebody a correspondent wrote to. "Chester House" and "Rodney House" are
    #      exactly that shape — a surname House with a forename before it — and this
    #      guard is what stops a word-shaped rule turning two of the town's people into
    #      buildings. A genuine place will have a mention outside the lists;
    #   4. a name carrying an OCCUPATION is being read as a person by the very claim that
    #      mints it, and the two readings cannot both stand.
    places = {}
    for rule in identity.get("places", []):
        name = rule.get("name")
        why = (rule.get("why") or "").strip()
        label = "identity.json place %r" % name
        if not name:
            problems.append("identity.json place: a declaration needs a `name`")
            continue
        if not why:
            problems.append("%s: no `why` — an undeclared reason is a compile error, "
                            "because a name moved out of the persons table on nobody's "
                            "argument is a person silently deleted" % label)
            continue
        if name not in why:
            problems.append("%s: `why` must name the place VERBATIM, so the judgement "
                            "can be read back without the code" % label)
            continue
        pk = person_key(name)
        if pk not in persons:
            problems.append("%s: not a name any claim carries — a place declaration for "
                            "a name that is not in the corpus is a rule nobody can check"
                            % label)
            continue
        rec = persons[pk]
        if rec.get("letter_list_only"):
            problems.append("%s: every mention of this name is a post-office letter "
                            "list, and a letter list is a list of PEOPLE somebody wrote "
                            "to — declaring it a place deletes a resident. Bring a "
                            "mention from outside the lists first" % label)
            continue
        if rec.get("occupations"):
            problems.append("%s: this name carries an occupation (%s), so a claim is "
                            "reading it as a person — the two readings cannot both stand"
                            % (label, ", ".join(rec["occupations"])))
            continue
        rec = persons.pop(pk)
        rec["id"] = "place_" + pk
        rec["kind"] = rule.get("kind")
        rec["why"] = why
        rec.pop("letter_list_only", None)
        rec.pop("occupations", None)
        places[pk] = rec

    # AND THE REFUSALS, which are the same record kept the other way up. A name that
    # LOOKS like a building and is a person is the dangerous case here — the refusal is
    # what stops the next reader declaring it — so it is written down beside the
    # declarations and held to the same three shapes: the reason names the name verbatim,
    # the name is one some claim carries, and the file cannot both refuse and declare it.
    for rule in identity.get("refused_places", []):
        name = rule.get("name")
        why = (rule.get("refused_because") or "").strip()
        label = "identity.json refused_place %r" % name
        if not name:
            problems.append("identity.json refused_place: a refusal needs a `name`")
            continue
        if not why:
            problems.append("%s: no `refused_because` — a refusal nobody argued is a "
                            "refusal the next reader will overturn by accident" % label)
            continue
        if name not in why:
            problems.append("%s: `refused_because` must name the name VERBATIM, so the "
                            "judgement can be read back without the code" % label)
            continue
        pk = person_key(name)
        if pk in places:
            problems.append("%s: this name is DECLARED a place and refused as one in the "
                            "same file" % label)
            continue
        if pk not in persons:
            problems.append("%s: not a name any claim carries as a person — a refusal "
                            "about a name that is not in the persons table is a rule "
                            "nobody can check" % label)
            continue

    # THE PLACE MERGES. Two spellings of one signboard, and the discriminator is neither
    # the person one nor the firm one: a building has no forename initial to be a family
    # by and no partners to be a house by. What holds instead is that BOTH sides must
    # already be declared places above — so the loosening reaches exactly the names an
    # author has argued in writing are not people, and can never reach a person.
    for rule in identity.get("place_merges", []):
        into, frm = rule.get("into"), rule.get("from")
        why = (rule.get("merge_rule") or "").strip()
        label = "identity.json place_merge %r <- %r" % (into, frm)
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
        a, b = person_key(into), person_key(frm)
        if a == b:
            problems.append("%s: a place cannot be merged into itself" % label)
            continue
        if a not in places or b not in places:
            missing = [n for n, k in ((into, a), (frm, b)) if k not in places]
            problems.append("%s: %s is not a DECLARED place — a place merge is not held "
                            "to the families rule, so it may only join two names "
                            "`places` has already argued are not people"
                            % (label, ", ".join(repr(m) for m in missing)))
            continue
        src = places.pop(b)
        dst = places[a]
        dst["variants"].extend(src["variants"])
        dst["mentions"].extend(src["mentions"])
        dst["first_seen"] = min(dst["first_seen"], src["first_seen"])
        dst["last_seen"] = max(dst["last_seen"], src["last_seen"])
        dst["associated_places"] = sorted(
            set(dst["associated_places"]) | set(src["associated_places"]))
        dst.setdefault("merged", []).append({"from": frm, "merge_rule": why})

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

    # THE FIRM MERGES (T-0304), and they are the person merges' equivalent rather than
    # their copy. A firm is not a person and the discriminator differs: the letter lists
    # made a forename INITIAL decisive for people, but a '& Co.' style routinely elides
    # or misprints the forename it is trading under — 'Jno. L. Wilson & Co.' is printed
    # 'L. Wilson & Co.' in one paper and 'Jno. S. Wilson & Co' in another — so the same
    # rule applied to firms would refuse every merge a firm actually needs. What survives
    # unchanged is the SURNAME: a partnership's identity is who its partners are, so the
    # guard here is that the two styles must carry the same set of partner surnames, and
    # that guard has no escape, exactly as the person one has none. The second guard is
    # not about the name at all — two styles the papers put in different STREETS are not
    # one firm without a removal notice, and a removal notice is a claim, not a merge.
    # THE SIGN-NAME DECLARATIONS (T-0340), read before the merges because the guard
    # below runs on them. Each one splits a style verbatim into the partners it names
    # and the shop-sign it carries, and both halves have to put the style back together
    # exactly, so a declaration can neither invent a partner nor drop one. A style
    # declared to name NO partner at all must also be one no claim ever signed with a
    # proprietor: if a printing put a person's name to the house, the house names its
    # partners and the ordinary guard is the one that applies to it.
    signs, declared = {}, sign_name_index(identity)
    for decl in identity.get("firm_sign_names", []):
        style = decl.get("style")
        partners, sign = (decl.get("partners") or ""), (decl.get("sign") or "")
        label = "identity.json firm_sign_name %r" % style
        if not style or not sign:
            problems.append("%s: a sign-name declaration needs both `style` and `sign`"
                            % label)
            continue
        if not (decl.get("note") or "").strip():
            problems.append("%s: no note — an undeclared reason is a judgement nobody "
                            "can check afterwards" % label)
            continue
        rebuilt = re.match(r"^%s[,\s]*%s$" % (re.escape(partners), re.escape(sign)), style)
        if not rebuilt:
            problems.append("%s: `partners` + `sign` (%r + %r) do not put the style back "
                            "together verbatim — a split that loses or adds a word is a "
                            "hand-edit of the name" % (label, partners, sign))
            continue
        if slug(style) not in businesses:
            problems.append("%s: not a firm any claim carries — a sign-name declaration "
                            "for a business that is not in the corpus is a declaration "
                            "nobody can check" % label)
            continue
        if not partners and businesses[slug(style)]["proprietors"]:
            problems.append("%s: declared to name no partner, but the claims sign it with "
                            "%s — a printing that put a person to the house is a printing "
                            "that names its partners"
                            % (label, ", ".join(repr(x) for x in
                                                businesses[slug(style)]["proprietors"])))
            continue
        signs[style] = declared[style]

    for rule in identity.get("firm_merges", []):
        into, frm = rule.get("into"), rule.get("from")
        why = (rule.get("merge_rule") or "").strip()
        label = "identity.json firm_merge %r <- %r" % (into, frm)
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
        a, b = slug(into), slug(frm)
        if a == b:
            problems.append("%s: a firm cannot be merged into itself" % label)
            continue
        if a not in businesses or b not in businesses:
            missing = [n for n, k in ((into, a), (frm, b)) if k not in businesses]
            problems.append("%s: %s is not a firm any claim carries — a merge rule for a "
                            "business that is not in the corpus is a rule nobody can check"
                            % (label, ", ".join(repr(m) for m in missing)))
            continue
        # THE PARTNER GUARD, and T-0340 is the one loosening it has ever had. Two styles
        # that each NAME partners must name the same ones — a partnership is its partners
        # and a changed one is a different house, which is what keeps 'Clark, Filer & Co.'
        # and 'A. Filer & Co.' apart. Where one of them names NONE, there is nothing to
        # compare and an empty set is not a contradiction: it is a printing that lost the
        # signature, which is the commonest thing a segmenter does to an advertisement.
        # Such a merge rests entirely on its stated rule, so the escape is not free — the
        # style has to be DECLARED a sign-name above, and that declaration is refused for
        # any house a claim ever signed with a proprietor.
        into_names, frm_names = partner_surnames(into, signs), partner_surnames(frm, signs)
        if into_names and frm_names and into_names != frm_names:
            problems.append("%s: the partner surnames differ (%s against %s) — this "
                            "project never merges those, with or without a rule, because "
                            "a partnership IS its partners and a changed one is a "
                            "different house"
                            % (label, sorted(into_names) or "none",
                               sorted(frm_names) or "none"))
            continue
        dst, src = businesses[a], businesses[b]
        if dst.get("street") and src.get("street") and \
                slug(dst["street"]) != slug(src["street"]):
            problems.append("%s: the papers put these in different streets (%r against "
                            "%r) — a firm that moved is documented by a removal notice, "
                            "which is a claim, not a merge"
                            % (label, dst["street"], src["street"]))
            continue
        businesses.pop(b)
        dst["mentions"].extend(src["mentions"])
        for who in src["proprietors"]:
            if who not in dst["proprietors"]:
                dst["proprietors"].append(who)
        for good in src["goods"]:
            if good not in dst["goods"]:
                dst["goods"].append(good)
        dst["contradicted_by"].extend(src["contradicted_by"])
        dst["opening_announced"].extend(src["opening_announced"])
        for reading in src["placement_readings"]:
            absorb_reading(dst, reading)
        # T-0412. A vendor notice usually mints its own key — "P. Pruyne" beside
        # "P. Pruyne & Co." — so the record of WHY that printing places nothing has to
        # survive the merge that joins them, or the judgement is lost at the one moment
        # it becomes about the firm the corpus actually keeps.
        for vp in src.get("vendor_placements") or []:
            dst.setdefault("vendor_placements", []).append(vp)
        for cd in src["evidence"]["copy_dates"]:
            if cd not in dst["evidence"]["copy_dates"]:
                dst["evidence"]["copy_dates"].append(cd)
        dst["evidence"]["first_issue"] = min(dst["evidence"]["first_issue"],
                                             src["evidence"]["first_issue"])
        dst["evidence"]["last_issue"] = max(dst["evidence"]["last_issue"],
                                            src["evidence"]["last_issue"])
        # NOTHING IS INVENTED AND NOTHING IS THROWN AWAY. Where one side is silent the
        # other's reading stands; where both speak, the merge keeps the one that can put
        # more of the firm on the ground, and every trade either side printed is kept in
        # `trade_variants` so the merge cannot quietly narrow what the papers said.
        dst["street"] = dst.get("street") or src.get("street")
        if placement_rank(src.get("placement")) > placement_rank(dst.get("placement")):
            dst["placement"] = src.get("placement")
        trades = {t for t in (dst.get("trade"), src.get("trade")) if t}
        trades |= set(dst.get("trade_variants") or []) | set(src.get("trade_variants") or [])
        dst["trade"] = dst.get("trade") or src.get("trade")
        if len(trades) > 1:
            dst["trade_variants"] = sorted(trades)
        dst.setdefault("merged", []).append({"from": frm, "merge_rule": why})

    # A PRINTING THAT OMITS THE ADDRESS DOES NOT HOLD THE HOUSE'S PLACEMENT (T-0440).
    #
    # The dict a house is minted into takes `placement` and `street` from WHICHEVER
    # CLAIM MINTS THE KEY — the earliest printing the corpus carries — and nothing
    # downstream of that ever revised it. `record_reading` keeps every later printing's
    # placement (T-0345), and a firm merge may raise the live one, but within a single
    # key the first printing won outright. So a house whose first advertisement ran
    # without an address, and which printed one afterwards, stood at `{"class": "none"}`
    # for good: `compile_register.resolve_anchor` is handed no anchor, the row reads
    # `unplaceable`, and its own printings say otherwise three lines below in the same
    # file. Clark, Filer & Co. is the case this was found on — silent on 1834-05-28,
    # then "their ware house on South water St. five [doors east] of the corner [of
    # Randolph st.]" on 1834-06-11, 1834-06-18 and 1834-07-02 — and 13 other houses of
    # the 206 were in the same position (tools/measure_placement_silence.py).
    #
    # WHAT THIS DECIDES, AND WHAT IT REFUSES TO. A printing that omits the address does
    # not contradict one that gives it; it simply did not repeat it, which is what a
    # standing advertisement does every other week. Preferring speech to silence is
    # therefore not a judgement about a house that MOVED, and this pass makes none: it
    # fires only where the live placement places nothing at all, and it takes the
    # EARLIEST placing reading — the same tie-break `absorb_reading` already applies
    # inside a reading, and the same one the mint applied, now asked of the first
    # printing that actually said something. Where two placing readings disagree about
    # the anchor, both are kept with their own dates exactly as before and the only
    # thing that may reorder them is the authored `anchor_changes` rule below, which
    # runs after this and overwrites what it decides. Nothing here upgrades a class,
    # invents an anchor, or touches a house whose live placement already places
    # something: a printed address is never overridden by another printed address.
    #
    # AND IT IS BOUNDED BY THE SCENE DATE, for the reason `anchor_changes` already is
    # and AGENTS.md rule 3 states generally: an address first printed after 1 July 1835
    # was not up on 1 July 1835, and a house is not placed in this town on the strength
    # of it. Jones, King & Co. is the case — silent through its 1834 printings and given
    # South Water Street on 1835-08-05 — and it stays silent here.
    scene_iso_placement = SCENE_DATE.isoformat()
    for biz in businesses.values():
        if placement_rank(biz.get("placement")) > 0:
            continue
        placing = [r for r in biz["placement_readings"]
                   if placement_rank(r.get("placement")) > 0
                   and r["first_issue"] <= scene_iso_placement]
        if not placing:
            continue
        first = min(placing, key=lambda r: (r["first_issue"], min(r["claims"])))
        biz["placement"] = first["placement"]
        biz["placement_from"] = {
            "rule": "T-0440: the minting printing gave no address, so the house is "
                    "placed by the earliest printing that did. A printing that omits "
                    "the address does not contradict one that gives it.",
            "first_issue": first["first_issue"],
            "claims": sorted(first["claims"]),
            "superseded": {"class": "none"},
        }
        # The street the same reading names, where the minting printing named none.
        # This is the reading's OWN `street` field and not a second inference: the
        # sentence that carries the offset carries the street it is measured along.
        street = (first["placement"] or {}).get("street")
        if street and not biz.get("street") and " and " not in street \
                and street != "unstated":
            biz["street"] = street
            biz["placement_from"]["street_from_reading"] = street

    # THE DATED ANCHOR CHANGE (T-0345). A firm merge unions two STYLES of one house.
    # This is the other thing two printings of one advertisement can differ about, and
    # it is not a spelling: Mason & Co.'s blacksmith notice runs under one copy date of
    # 26 November 1833, reads "on Main-street, nearly opposite Graves' Tavern" to
    # 1834-07-16, and from 1834-09-10 reads "on Main-street, opposite the Tremont House"
    # with the rest of the copy word for word unchanged. Nothing printed says WHICH
    # changed — the shop, or the name of the house across the street — and no
    # declaration here may decide it.
    #
    # What is DECLARED is only that two of a house's readings name two different
    # landmarks rather than two spellings of one. Everything else is COMPUTED from the
    # readings the claims carry: the weeks each anchor was printed between, the order
    # they were printed in, the gap the change is bracketed by, and which anchor is live
    # at the scene date. Seven guards, and each one is a way this could quietly assert
    # something the corpus does not say:
    #   1. the house has to be one the corpus compiles, or nobody can check the rule;
    #   2. two anchors at least — one anchor is not a change;
    #   3. every reading the declaration names has to be a string some printing of THIS
    #      house actually carries, matched verbatim against its own readings;
    #   4. EVERY reading of the house has to be claimed by exactly one anchor. A
    #      printing left out of the history is a printing silently dropped, which is the
    #      defect this whole mechanism exists to end;
    #   5. an anchor holding more than one reading is a GROUPING, which is a judgement,
    #      so it needs its own `why` naming the anchor verbatim;
    #   6. the windows may not OVERLAP. Two anchors printed in the same weeks are two
    #      standing placements and this ticket's actual complaint; a change is a change
    #      only where one anchor stops before the next starts;
    #   7. `cannot_say` has to be written down. A dated anchor change that says nothing
    #      about what the corpus leaves open has decided it in silence.
    scene_iso = SCENE_DATE.isoformat()
    for rule in identity.get("anchor_changes", []):
        bid = rule.get("business")
        groups = rule.get("anchors") or []
        why = (rule.get("rule") or "").strip()
        cannot = (rule.get("cannot_say") or "").strip()
        label = "identity.json anchor_change %r" % bid
        bkey = bid[len("business_"):] if (bid or "").startswith("business_") else bid
        if not bkey or bkey not in businesses:
            problems.append("%s: no business of that id is compiled — an anchor rule for "
                            "a house that is not in the corpus is a rule nobody can check"
                            % label)
            continue
        if len(groups) < 2:
            problems.append("%s: a change needs at least two anchors — one anchor is not "
                            "a change" % label)
            continue
        if not why:
            problems.append("%s: no rule — an unexplained anchor change is a compile "
                            "error, because a wrong reading of two printings is "
                            "invisible afterwards" % label)
            continue
        if not cannot:
            problems.append("%s: no `cannot_say` — a dated anchor change that does not "
                            "state what the corpus leaves open has decided it in silence"
                            % label)
            continue
        names = [g.get("name") for g in groups]
        if not all(names):
            problems.append("%s: every anchor needs a `name`" % label)
            continue
        unnamed = [n for n in names if n not in why]
        if unnamed:
            problems.append("%s: the rule must name %s verbatim, so the judgement can be "
                            "read back without the code"
                            % (label, ", ".join(repr(n) for n in unnamed)))
            continue
        biz = businesses[bkey]
        # T-0440. A reading that places NOTHING names no landmark, so it can neither be
        # claimed by an anchor group (guard 3 would refuse the name `null`) nor be left
        # out of one (guard 4 would call it a printing silently dropped). Before this,
        # any house whose advertisement ever ran without an address could not have an
        # anchor rule written for it AT ALL — the one mechanism that may order a house's
        # anchors was unreachable for exactly the houses whose placement most needed
        # ordering. Silence is still kept in `placement_readings` with its own dates;
        # what it may not do is take part in a judgement about which anchor is live.
        #
        # T-0773. One anchor STRING can be carried by more than one reading of the same
        # house, because a reading is grouped by its whole placement and not by its
        # anchor alone: G. Spring's "the corner of Franklin and South Water streets" is
        # read `relative` across seven printings from 1833-12-17 and `corner` once on
        # 1834-09-03, two readings under one name. Keyed one-to-one, the later of the two
        # overwrote the earlier and the rule's history lost seven claims and eleven
        # months of window WITHOUT tripping guard 4 — the drop was invisible to the very
        # guard that exists to catch it, because the anchor was still claimed. An anchor
        # therefore holds every reading printed under it, and a group takes all of them.
        held = {}
        for r in biz["placement_readings"]:
            if placement_rank(r.get("placement")) > 0:
                held.setdefault(r["anchor"], []).append(r)
        claimed, windows, bad = [], [], False
        for g in groups:
            readings = g.get("readings") or []
            if not readings:
                problems.append("%s: anchor %r claims no reading — an anchor nothing was "
                                "printed under places nothing" % (label, g.get("name")))
                bad = True
                break
            unknown = [r for r in readings if r not in held]
            if unknown:
                problems.append(
                    "%s: %s is not an anchor any printing of this house carries (it "
                    "reads %s) — an anchor rule may only order readings the corpus "
                    "already made"
                    % (label, ", ".join(repr(u) for u in unknown),
                       ", ".join(repr(a) for a in sorted(held, key=lambda x: x or ""))))
                bad = True
                break
            if len(readings) > 1 and g.get("name") not in (g.get("why") or ""):
                problems.append("%s: anchor %r groups %d readings and its `why` does not "
                                "name it verbatim — calling two printed anchors one "
                                "landmark is a judgement and it has to be written down"
                                % (label, g.get("name"), len(readings)))
                bad = True
                break
            claimed.extend(readings)
            rs = [one for r in readings for one in held[r]]
            windows.append({
                "name": g.get("name"),
                "why": (g.get("why") or "").strip() or None,
                "first_issue": min(r["first_issue"] for r in rs),
                "last_issue": max(r["last_issue"] for r in rs),
                "readings": sorted(
                    ({"anchor": r["anchor"], "class": r["class"],
                      "first_issue": r["first_issue"], "last_issue": r["last_issue"],
                      "claims": sorted(r["claims"]), "placement": r["placement"]}
                     for r in rs),
                    key=lambda r: (r["first_issue"], r["anchor"] or "")),
                "claims": sorted({c for r in rs for c in r["claims"]}),
                "placement": min(rs, key=lambda r: (r["first_issue"],
                                                    min(r["claims"])))["placement"],
            })
        if bad:
            continue
        if len(set(claimed)) != len(claimed):
            problems.append("%s: a reading is claimed by two anchors — one printing "
                            "names one landmark" % label)
            continue
        left = [a for a in held if a not in set(claimed)]
        if left:
            problems.append("%s: %s is printed for this house and no anchor claims it — "
                            "a reading left out of the history is a printing silently "
                            "dropped, which is what this mechanism exists to end"
                            % (label, ", ".join(repr(a) for a in sorted(left,
                                                                       key=lambda x: x or ""))))
            continue
        windows.sort(key=lambda w: (w["first_issue"], w["last_issue"], w["name"]))
        overlap = ["%r runs to %s and %r starts %s"
                   % (a["name"], a["last_issue"], b2["name"], b2["first_issue"])
                   for a, b2 in zip(windows, windows[1:])
                   if b2["first_issue"] <= a["last_issue"]]
        if overlap:
            problems.append("%s: %s — these anchors were printed in overlapping weeks, "
                            "which is two standing placements and not a change. A change "
                            "is a change only where one anchor stops before the next "
                            "starts." % (label, "; ".join(overlap)))
            continue
        live = windows[0]
        for w in windows:
            if w["first_issue"] <= scene_iso:
                live = w
        biz["placement"] = live["placement"]
        # T-0773. AND THE STREET GOES WITH IT. `street` is taken from whichever claim
        # MINTS the house, so a rule that moves the live anchor across town leaves the
        # street of the anchor it superseded behind — and `compile_register` adopts a
        # street face off that field, not off the placement. G. Spring's rule put his
        # office on Dearborn-street beside the Tremont House while the row went on
        # reading South Water Street, which is the frontage the ruling had just retired.
        # Only where the live reading names ONE street: a corner reading names two, and
        # a `street` field holding both is not a street this town can adopt against.
        live_street = (live["placement"] or {}).get("street")
        if live_street and " and " not in live_street:
            biz["street"] = live_street
        biz["anchor_change"] = {
            "rule": why,
            "cannot_say": cannot,
            "live_anchor": live["name"],
            "live_reason": "The last of these anchors first printed on or before the "
                           "scene date %s; this one was first printed %s."
                           % (scene_iso, live["first_issue"]),
            "changes": [{"from": a["name"], "to": b2["name"],
                         "after": a["last_issue"], "before": b2["first_issue"]}
                        for a, b2 in zip(windows, windows[1:])],
            "history": [{"anchor": w["name"], "why": w["why"],
                         "first_issue": w["first_issue"], "last_issue": w["last_issue"],
                         "readings": w["readings"], "claims": w["claims"],
                         "live_at_scene_date": w is live,
                         "placement": w["placement"]}
                        for w in windows],
        }
    # …AND THE FIRMS' REFUSAL (T-0399), which is the other half of the same judgement
    # and had nowhere to live until now. `firm_surnames()` groups the register on the
    # partner surname alone, so it puts together houses that are not one house — the two
    # Montgomerys, a namesake, an anchor mistaken for a partner — and a sweep that
    # merged on the name would have merged them. Before this, the only record of such a
    # judgement was the ABSENCE of a merge rule, which reads exactly like a group nobody
    # has looked at yet; the next sweep finds the group again and has to do the work
    # again. So a refusal is declared as explicitly as a merge, and held to the same
    # three disciplines: it names both spellings verbatim, it names the printings it
    # rests on, and it cannot outlive its pair — a refusal whose two styles a later
    # merge has already collapsed is a judgement nobody can check, and is an error.
    REFUSAL_KINDS = {
        # the papers show two different houses under one surname
        "two_houses",
        # one name, and no printing puts the two styles under one roof — the honest
        # answer is "not shown to be one", which is not the same as "shown to be two"
        "not_joined",
        # one house, and the papers put the two styles on different ground: a removal
        # or a succession, which is a claim and not a merge
        "different_ground",
    }
    merged_pairs = {frozenset((slug(r.get("into") or ""), slug(r.get("from") or "")))
                    for r in identity.get("firm_merges", [])}
    for rule in identity.get("refused_firm_merges", []):
        into, frm = rule.get("into"), rule.get("from")
        why = (rule.get("refused_because") or "").strip()
        kind = rule.get("kind")
        witnesses = rule.get("witnesses") or []
        label = "identity.json refused_firm_merge %r <- %r" % (into, frm)
        if not into or not frm:
            problems.append("%s: a refusal needs both `into` and `from`" % label)
            continue
        if not why:
            problems.append("%s: no refused_because — an unexplained refusal is worth no "
                            "more than no refusal at all, because the next sweep cannot "
                            "tell it from a group nobody has judged" % label)
            continue
        if into not in why or frm not in why:
            problems.append("%s: refused_because must name BOTH spellings verbatim, so "
                            "the judgement can be read back without the code" % label)
            continue
        if kind not in REFUSAL_KINDS:
            problems.append("%s: `kind` must be one of %s — the shape of a refusal is "
                            "part of what it says, and 'not shown to be one' is not the "
                            "same judgement as 'shown to be two'"
                            % (label, ", ".join(sorted(REFUSAL_KINDS))))
            continue
        if not witnesses:
            problems.append("%s: no `witnesses` — a refusal rests on printings exactly as "
                            "a merge does, and one that names none cannot be checked"
                            % label)
            continue
        a, b = slug(into), slug(frm)
        if a == b:
            problems.append("%s: a firm cannot be refused against itself" % label)
            continue
        if frozenset((a, b)) in merged_pairs:
            problems.append("%s: this pair is also declared in `firm_merges` — the file "
                            "cannot both join and hold apart the same two styles" % label)
            continue
        missing = [n for n, k in ((into, a), (frm, b)) if k not in businesses]
        if missing:
            problems.append("%s: %s is not a firm the compiled register carries — a "
                            "refusal that has outlived its pair is a judgement nobody can "
                            "check, and it will not be left to rot here"
                            % (label, ", ".join(repr(m) for m in missing)))
            continue
        for key, name in ((a, into), (b, frm)):
            businesses[key].setdefault("refused_merges", []).append(
                {"with": frm if key == a else into, "kind": kind,
                 "witnesses": list(witnesses), "refused_because": why})

    # THE PROPRIETORS' HALF (T-0337). Applied after the firm merges, because a firm
    # merge is what unions two houses' proprietor lists in the first place, and a pair
    # that needs adjudicating can be created by one.
    for rule in identity.get("proprietor_merges", []):
        bid, into, frm = rule.get("business"), rule.get("into"), rule.get("from")
        why = (rule.get("merge_rule") or "").strip()
        label = "identity.json proprietor_merge %r: %r <- %r" % (bid, into, frm)
        if not bid or not into or not frm:
            problems.append("%s: a proprietor merge needs `business`, `into` and `from`"
                            % label)
            continue
        if not why:
            problems.append("%s: no merge_rule — an unexplained merge is a compile error, "
                            "because a wrong one is invisible afterwards" % label)
            continue
        if into not in why or frm not in why:
            problems.append("%s: merge_rule must name BOTH spellings verbatim, so the "
                            "judgement can be read back without the code" % label)
            continue
        biz = businesses.get(bid[len("business_"):] if bid.startswith("business_") else bid)
        if biz is None:
            problems.append("%s: no business of that id is compiled — a proprietor rule "
                            "for a house that is not in the corpus is a rule nobody can "
                            "check" % label)
            continue
        missing = [n for n in (into, frm) if n not in (biz.get("proprietors") or [])]
        if missing:
            problems.append("%s: %s is not a proprietor this house carries — the rule has "
                            "gone stale, or it names a spelling no claim reads"
                            % (label, ", ".join(repr(m) for m in missing)))
            continue
        if surname(into) != surname(frm):
            problems.append("%s: the surnames differ (%r against %r) — a proprietor merge "
                            "may join two readings of one name and never two names"
                            % (label, surname(into), surname(frm)))
            continue
        biz["proprietors"] = [p for p in biz["proprietors"] if p != frm]
        biz.setdefault("proprietors_merged", []).append({"into": into, "from": frm,
                                                         "merge_rule": why})

    # …and the refusal. Every same-surname pair left standing in one house's proprietors
    # is either two people or one read twice, and the gate will not guess which.
    declared = {}
    for rule in identity.get("proprietor_distinctions", []):
        bid = rule.get("business")
        names = rule.get("names") or []
        label = "identity.json proprietor_distinction %r %s" % (bid, names)
        if not bid or len(names) != 2 or not all(names):
            problems.append("%s: a distinction needs a `business` and exactly two `names`"
                            % label)
            continue
        if not (rule.get("rule") or "").strip():
            problems.append("%s: no rule — declaring two men without saying how they are "
                            "told apart is the assertion this gate exists to refuse"
                            % label)
            continue
        key = bid[len("business_"):] if bid.startswith("business_") else bid
        if key not in businesses:
            problems.append("%s: no business of that id is compiled" % label)
            continue
        declared.setdefault(key, set()).add(frozenset(names))

    for key, biz in businesses.items():
        want = {frozenset(pair) for pair in proprietor_pairs(biz)}
        have = declared.get(key, set())
        for pair in sorted(want - have, key=lambda s: sorted(s)):
            a, b = sorted(pair)
            problems.append(
                "%s: %r and %r are one surname with different forenames, and nothing "
                "declares which they are. One house's proprietors are read printing by "
                "printing, so this is either two men or one man read twice — declare it "
                "in identity.json: `proprietor_merges` to join them, or "
                "`proprietor_distinctions` to hold them apart, with the reasoning."
                % (biz["id"], a, b))
        for pair in sorted(have - want, key=lambda s: sorted(s)):
            problems.append(
                "%s: the distinction declared for %s no longer answers anything — those "
                "two spellings are not both proprietors of this house any more. A "
                "declaration that has outlived its pair is a judgement nobody can check."
                % (biz["id"], sorted(pair)))

    for b in businesses.values():
        # Ruling 3, computed and never asserted: a documented business stands in the
        # 1835 town unless a claim contradicts it, and one whose last issue predates
        # 1835 stands on a survival liberty that has to be written down.
        b["built_at_scene_date"] = not b["contradicted_by"]
        last = date.fromisoformat(b["evidence"]["last_issue"])
        b["survival_liberty_required"] = b["built_at_scene_date"] and last.year < SCENE_DATE.year
        b["goods"].sort()
        b["mentions"].sort()
        b["opening_announced"].sort(key=lambda o: (o["iso"] or "", o["claim"]))
        b["evidence"]["copy_dates"].sort()
        for r in b["placement_readings"]:
            r["claims"].sort()
        b["placement_readings"].sort(
            key=lambda r: (r["first_issue"], r["anchor"] or "", r["class"] or ""))
        if b.get("vendor_placements"):
            b["vendor_placements"].sort(key=lambda v: (v["issue"], v["claim"]))
    for p in persons.values():
        p["mentions"].sort()
        p["variants"].sort(key=lambda v: (v["claim"], v["as_printed"] or ""))
        p["occupations"].sort()
        p["associated_places"].sort()
    for pl in places.values():
        pl["mentions"].sort()
        pl["variants"].sort(key=lambda v: (v["claim"], v["as_printed"] or ""))
        pl["associated_places"].sort()

    doc = {
        "schema": SCHEMA_VERSION,
        "generated_by": "tools/compile_gazetteer.py --build",
        "scene_date": SCENE_DATE.isoformat(),
        "compiled_from": [
            {"file": rel_to_repo(p), "sha256": sha256(p)}
            for p in sorted(files, key=lambda p: Path(p).name)
        ],
        "counts": {"claims": claim_count, "persons": len(persons),
                   "places": len(places), "businesses": len(businesses)},
        "persons": sorted(persons.values(), key=lambda p: p["id"]),
        "places": sorted(places.values(), key=lambda p: p["id"]),
        "businesses": sorted(businesses.values(), key=lambda b: b["id"]),
    }
    if not quiet:
        print("  ok    %d claim(s) → %d person(s), %d place(s), %d business(es)"
              % (claim_count, len(persons), len(places), len(businesses)))
    return doc, problems


def surname(name):
    """'Work, James Houston' → 'work'; 'Peter Cohen' → 'cohen'.

    Markup off first, for the same reason `initials` takes it off (T-0299) and for one
    more: the two halves of the refusal rule have to answer about the SAME name. While
    this slugged the markup and `initials` parsed it, `Charles Work[s]` and `Charles
    Works` were two surnames — so the rule did not fire — and `A. Beegle` and `[?]. Beegle`
    were one, so it did. Whether the policy protected a pair came down to which side of
    the name a bracket happened to fall on.
    """
    name = unmarked(name).strip()
    if "," in name:
        return slug(name.split(",", 1)[0])
    return slug(name.split()[-1]) if name.split() else ""


UNCERTAIN_PART = re.compile(r"\[uncertain:\s*(.*?)\]")

# An initial the printing does not read. It is a VALUE in the initials tuple, never a
# letter, so it is equal to itself and to nothing else — which is exactly the policy:
# an unread initial is not the same as a read one. `UNREAD_MARK` is its in-string form,
# carried through the bracket strip so the marker survives to the tokenizer.
UNREAD_MARK = "\x00"
UNREAD = "?"


def unmarked(name):
    """A normalized reading with the transcriber's markup taken off.

    `normalized` carries three marks and they are all ABOUT the reading, not part of
    the name: `[x]` around a letter the transcriber supplied for a recognition-class
    error, `[?]` where no letter could be supplied, and an `[uncertain: …]` wrapper
    where the printed form supports no reading at all. They belong in the stored
    reading — that is the honesty — and they do not belong in the name parse below,
    which is why this exists rather than being folded into `slug`.

    The `[uncertain: …]` wrapper is stripped wherever it stands, not only around the
    whole name: `Dani[e]l O. [uncertain: Robian]` wraps the surname alone, and leaving
    the word `uncertain` in the string made it a third forename.
    """
    name = UNCERTAIN_PART.sub(r"\1", name or "")
    name = name.replace("[?]", "")
    return re.sub(r"\[([^\]]*)\]", r"\1", name)


def initials(name):
    """The forename initials, in order — the half of a name the letter lists turn on.

    THE MARKUP IS NOT A WORD BOUNDARY, AND NEITHER IS A LETTER PYTHON HAS NOT HEARD OF
    (T-0299). This split on `[A-Za-z]+`, so `A[n]drew W. Borland` parsed as the four
    forenames A / n / drew / W and `[uncertain: Abey Blankinship]` parsed as `uncertain`
    and `Abey`; against the plain `Andrew W. Borland` of another printing that reads as
    two different people under one surname, and the identity policy then refuses the
    merge that would join them. Measured on the three printings of the 1 July 1834
    letter list: 120 of 206 correct merges were refused this way, none of them for a
    reason the policy is about. The same defect ate `Benjamın Swena`, whose OCR left a
    dotless ı that `[A-Za-z]` treats as a space.

    The policy itself is untouched and is the reason this is a parser fix rather than a
    loosening: `Cohen, P.` and `Cohen, J.` still carry different initials and still
    never merge, and so do `Lyman R. Lovell` and `Lyman B. Lovell`, `[H]enry Swartwout
    jr.` and `J[n]o. Swartwout jr.` — a bracketed letter is READ, so it counts.

    AN UNREAD `[?]` IS A POSITION, NOT AN ABSENCE (T-0397). `unmarked` DELETES the
    marker, which is right for a surname and wrong here, because deleting it hands the
    initial to whatever letter stood behind it. Every one of the seventeen `[?]`
    refusals on the 1 July 1834 list parsed wrongly, in three shapes:

      - a letter INVENTED from the rest of the forename — `[?]rah Fowler` read as `R.`,
        `[?]nn M. Gooding` as `N. M.`, `[?]saac Scarrett` as `S.`;
      - a POSITION collapsed — `[?]. M. Fish` read as `M.` in FIRST position, against
        `E. M. Fish`'s `E. M.`, so a middle initial was compared with a forename one;
      - an absence — `[?]. Beegle` read as no initial at all, which is the shape the
        ticket's own diagnosis assumed all seventeen had.

    Those readings then went into `identity.json` as the STATED reason for a refusal —
    "A. against R." — so a committed record asserted a letter no printing ever read.
    That is a provenance defect and it is what this repairs. `UNREAD` occupies the slot
    the marker stood in and equals no read letter, so the refusals all stand (the policy
    does not move: 177 merges and 29 refusals before and after) and both answers to the
    OPEN policy question are now expressible, because the parse can finally SAY which
    side is unread instead of guessing a letter for it.
    """
    name = UNCERTAIN_PART.sub(r"\1", name or "")
    # The marker becomes a sentinel BEFORE the generic bracket strip, so `[?]` is not
    # mistaken for a supplied letter, and it stays welded to the word it opens: the
    # first character of `[?]rah` is unread, and `[?]rah` is still ONE forename.
    name = re.sub(r"\[([^\]]*)\]", r"\1", name.replace("[?]", UNREAD_MARK)).strip()
    fore = name.split(",", 1)[1] if "," in name else " ".join(name.split()[:-1])
    words = re.findall(r"(?:%s|[^\W\d_])+" % re.escape(UNREAD_MARK), fore, re.UNICODE)
    return tuple(UNREAD if w[0] == UNREAD_MARK else w[0].lower() for w in words)


# --------------------------------------------------------------------------
# the firm's half of the identity policy (T-0304)

# What a partnership style says AFTER the partners: '& Co.', '& Son', 'Brothers'.
# These are not surnames and a firm's identity does not turn on them.
FIRM_SUFFIXES = {"co", "company", "son", "sons", "bro", "bros", "brother", "brothers"}


def firm_style(name):
    """A firm name with any trailing trade description cut away.

    'Collins & Caton, attorneys and counsellors at law' → 'Collins & Caton'.

    The tail is recognisable without a dictionary because of how the papers set type:
    names are capitalised and trades are not, so a comma followed by a LOWER-CASE word
    begins the trade and everything before it is the style. That is why 'Clark, Filer
    & Co.' keeps both its partners — 'Filer' is capitalised, so the comma is a partner
    separator and not the start of a trade.
    """
    name = re.sub(r"\s*\([^)]*\)", "", (name or "")).strip()
    return re.split(r",\s+(?=[a-z])", name, maxsplit=1)[0].strip().rstrip(",")


def firm_surnames(name):
    """The set of partner surnames a firm style carries.

    'J. L. Wilson & Co.' → {'wilson'} · 'Clark, Filer & Co.' → {'clark', 'filer'}.

    Split the style on the separators a partnership uses — '&', ',' and 'and' — and take
    the LAST word of each partner, which is the surname whether the forename was printed
    whole ('Giles Spring'), abbreviated ('Jno. L. Wilson') or dropped ('L. Wilson').
    """
    out = set()
    for seg in re.split(r"\s*(?:&|,|\band\b)\s*", firm_style(name)):
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z\u2019']*", seg)
                 if slug(w) not in FIRM_SUFFIXES]
        if words:
            out.add(slug(words[-1]))
    return out


def sign_name_index(identity):
    """`identity.json`'s `firm_sign_names`, as {style: the partner half of that style}.

    A SIGN-NAME is the shop's own name over its door — 'Chicago Wholesale and Retail Book
    & Stationary Store' — and `firm_style` cannot see one, because the heuristic it runs
    on is that partners are capitalised and trades are not, and a sign-name is a
    capitalised trade. Left alone, `firm_surnames` reads 'Book', 'Store' and 'Wholesale'
    as three partners and the guard then reports partner surnames that no printing ever
    carried. So the split is DECLARED, next to the merges it governs, and checked below.
    """
    return {d.get("style"): (d.get("partners") or "")
            for d in identity.get("firm_sign_names", []) if d.get("style")}


def partner_surnames(name, signs):
    """The partner surnames a style states, with any declared sign-name taken off it.

    'Russell & Clift, Chicago Book and Stationary Store' → {'clift', 'russell'}, because
    the declaration says the partner half is 'Russell & Clift'. A style declared to be a
    sign-name and nothing else states NO partner and returns the empty set — which is not
    a different partnership, only a printing that did not name one (see the guard).
    """
    return firm_surnames(signs.get(name, name)) if signs.get(name, name) else set()


# --------------------------------------------------------------------------
# the PROPRIETORS' half of the identity policy (T-0337)
#
# A firm's `proprietors` are the third place a name lives here, and until this ticket
# it was the only one with no rule at all. `identity.json.merges` governs gazetteer
# PERSONS and `firm_merges` governs business STYLES; a proprietor is neither — it is a
# string on a business record, put there by whichever claim read that printing. So one
# man read two ways became two proprietors of his own house and nothing could see it:
# `business_russell_clift` carried 'Benj. Clift' from the 1834-09-03 impression of the
# copartnership notice and '[H. H.] Clift' from the 1834-11-12 impression of the SAME
# notice, and neither the person policy nor the firm policy can reach across to say so.
#
# The rule here is the firm-side sibling of the person one, and it points the other way
# on purpose. For a person, same surname with different initials NEVER merges, silently
# and by default, because the letter lists are full of families. For two proprietors of
# ONE house the default cannot be silence either way: brothers really do trade together
# (William and Franklin Brewster sign one dissolution notice) and so does one man read
# twice. So the pair is REFUSED until `identity.json` says which it is —
# `proprietor_merges` to join them, `proprietor_distinctions` to hold them apart — and
# each declaration carries the reasoning, exactly as a merge rule does.


def firm_styled(name):
    """Is this proprietor string a firm's style rather than a person's name?

    `proprietors` carries both — a claim that reads only the signature 'JONES & KING.'
    records that as the proprietor, because it is what the paper printed. A style is
    not a person and the rule below is about people, so these are stepped over.
    """
    text = unmarked(name or "")
    if "&" in text or re.search(r"\band\b", text):
        return True
    words = [slug(w) for w in re.findall(r"[A-Za-z][A-Za-z\u2019']*", text)]
    return bool(words) and words[-1] in FIRM_SUFFIXES


def proprietor_pairs(business):
    """Every pair of this business's proprietors that one surname could be hiding in.

    Two person-styled proprietors, the same surname, and forename initials that are
    READ on both sides and disagree. Both sides must carry initials: a bare surname
    beside a full name ('Hubbard' beside 'Gurdon S. Hubbard') is the papers printing
    less, not a second man, and there is nothing there to adjudicate.
    """
    names = [n for n in (business.get("proprietors") or []) if not firm_styled(n)]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if not surname(a) or surname(a) != surname(b):
                continue
            ia, ib = initials(a), initials(b)
            if ia and ib and ia != ib:
                yield a, b


# --------------------------------------------------------------------------
# the placements a house was printed with, and their dates


def reading_key(placement):
    """Two printings carry ONE reading when they set the same class and anchor."""
    p = placement or {}
    return ((p.get("class") or ""), (p.get("anchor") or ""))


def absorb_reading(business, reading):
    """Fold a printing's placement into a house's readings, widening the window.

    The placement KEPT for a reading is the earliest printing's, so the offset text
    quoted beside it is the one the anchor was first set with. Ties break on the claim
    key, because this compile is re-derived and byte-compared by the gate.
    """
    for r in business["placement_readings"]:
        if reading_key(r["placement"]) != reading_key(reading["placement"]):
            continue
        if (reading["first_issue"], min(reading["claims"])) < (r["first_issue"],
                                                              min(r["claims"])):
            r["placement"] = reading["placement"]
        r["first_issue"] = min(r["first_issue"], reading["first_issue"])
        r["last_issue"] = max(r["last_issue"], reading["last_issue"])
        for c in reading["claims"]:
            if c not in r["claims"]:
                r["claims"].append(c)
        return
    business["placement_readings"].append({
        "anchor": (reading["placement"] or {}).get("anchor"),
        "class": (reading["placement"] or {}).get("class"),
        "first_issue": reading["first_issue"], "last_issue": reading["last_issue"],
        "claims": list(reading["claims"]), "placement": reading["placement"],
    })


def record_reading(business, placement, issue_date, key):
    absorb_reading(business, {"placement": placement or {}, "first_issue": issue_date,
                              "last_issue": issue_date, "claims": [key]})


def placement_rank(placement):
    """How much of the ground a placement can actually put a storefront on."""
    order = list(reversed(PLACEMENT_CLASSES))          # none < street_only < relative < corner
    cls = (placement or {}).get("class")
    return order.index(cls) if cls in order else -1


# --------------------------------------------------------------------------
# coverage: a range someone said they READ, checked against the register


def coverage_problems(coverage_doc, corpus_doc, files):
    """Every issue inside a DECLARED range must have an extraction file.

    A reading pass covers a range of issues, and the failure it is prone to is not a
    bad claim — the gate above catches those — but a MISSING issue: fourteen of fifteen
    read, and nothing anywhere says which one was skipped. Counting files does not
    answer it either, because the count that should have been is exactly the thing in
    question. So a pass declares its range here when it closes, and the register says
    what is inside it.

    Declaring is the act that makes the assertion; an undeclared issue is simply not
    read yet and is not a fault. What is a fault is declaring a range and leaving a
    hole in it.
    """
    problems = []
    have = {Path(f).stem for f in files}
    issues = corpus_doc.get("issues", [])
    for rng in coverage_doc.get("ranges", []):
        label = "coverage %r" % (rng.get("ticket") or rng.get("note") or "range")
        pub, first, last = rng.get("publication"), rng.get("from"), rng.get("to")
        if not (pub and first and last):
            problems.append("%s: a range needs publication, from and to" % label)
            continue
        try:
            date.fromisoformat(first), date.fromisoformat(last)
        except ValueError:
            problems.append("%s: from/to must be ISO dates" % label)
            continue
        inside = [i for i in issues
                  if i.get("publication") == pub and first <= i.get("date", "") <= last]
        if not inside:
            problems.append("%s: names no issue in corpus.json — a range covering "
                            "nothing is a range that was mistyped" % label)
            continue
        missing = sorted(i["id"] for i in inside if i["id"] not in have)
        if missing:
            problems.append("%s: declared read %s to %s, and %d of its %d issue(s) have "
                            "no extraction file: %s"
                            % (label, first, last, len(missing), len(inside),
                               ", ".join(missing)))
    return problems


# --------------------------------------------------------------------------
# check


def check(extracted=EXTRACTED, gazetteer=GAZETTEER, identity=IDENTITY, corpus=CORPUS,
          deposit=DEPOSIT, repo=REPO, coverage=COVERAGE, quiet=False):
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

            # T-0356's field, and every guard on it is a way a date could be invented.
            op = claim.get("announces_opening")
            if op is not None and not isinstance(op, dict):
                bad.append("%s %s: announces_opening is %r. It was a bare boolean on twenty "
                           "claims and no tool read it; it is now a reading — "
                           "{verbatim, dating, iso, note} — and the register excludes on "
                           "its date" % (at, key, op))
                op = None
            if op is not None:
                if claim.get("kind") not in ("business", "building"):
                    bad.append("%s %s: announces_opening on a %s claim — an opening is "
                               "something a HOUSE does, and only a business or building "
                               "claim has one to announce"
                               % (at, key, claim.get("kind")))
                phrase = op.get("verbatim")
                if not phrase:
                    bad.append("%s %s: announces_opening with no verbatim — the paper's own "
                               "words are the evidence" % (at, key))
                elif phrase not in (claim.get("normalized") or ""):
                    bad.append("%s %s: announces_opening.verbatim is not in the claim's "
                               "normalized reading, character for character" % (at, key))
                if not (op.get("note") or "").strip():
                    bad.append("%s %s: announces_opening with no note — the note says how "
                               "the date was READ, and a date with no reading behind it is "
                               "the invention this field exists to prevent" % (at, key))
                if op.get("dating") not in OPENING_DATINGS:
                    bad.append("%s %s: announces_opening.dating %r is not one of %s"
                               % (at, key, op.get("dating"), "/".join(OPENING_DATINGS)))
                if op.get("dating") == "undated":
                    if op.get("iso") is not None:
                        bad.append("%s %s: an `undated` opening carries a date (%r). The "
                                   "paper dated nothing; supplying a number here is the "
                                   "invention this field exists to prevent"
                                   % (at, key, op.get("iso")))
                else:
                    try:
                        date.fromisoformat(op.get("iso") or "")
                    except ValueError:
                        bad.append("%s %s: announces_opening.iso %r does not parse"
                                   % (at, key, op.get("iso")))
                if op.get("dating") == "effected":
                    if ad is None:
                        bad.append("%s %s: an `effected` opening is dated by the "
                                   "advertisement's own dateline, and this claim carries no "
                                   "ad_copy_date to take it from" % (at, key))
                    elif op.get("iso") != ad.get("iso"):
                        bad.append("%s %s: an `effected` opening is dated %r and the "
                                   "advertisement's dateline is %r — the dateline is the "
                                   "only date this reading may carry"
                                   % (at, key, op.get("iso"), ad.get("iso")))

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
                if loc.get("spans"):
                    bad.extend("%s %s: %s" % (at, key, p)
                               for p in span_problems(loc["spans"], used, None))
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
            spans = loc.get("spans")
            if spans is not None:
                sp_bad = span_problems(spans, used, lines)
                bad.extend("%s %s: %s" % (at, key, p) for p in sp_bad)
                if sp_bad:
                    continue
            want = quoted_text(lines, used, spans)
            if claim.get("quote") is not None and claim["quote"] != want:
                bad.append("%s %s: the quote is not what lines %s of the transcription "
                           "say. A quote is verbatim including its uncertainty brackets; "
                           "the smoothed reading belongs in `normalized`." % (at, key, used))
            else:
                checked_quotes += 1

    # THE RESOLVER CENSUS (T-0325). Three times now a marker dialect has been found only
    # because somebody sat down to READ the issues that speak it — T-0289's majority ruled
    # shape, T-0258's 1833 dash-column one, and the two here. Each time the reason nothing
    # caught it earlier was the same: `check` only opens the transcriptions its CLAIMS cite,
    # so an unread issue's dialect is not exercised by anything. This walks every artifact
    # in the corpus instead of every cited one, and refuses any readable transcription that
    # resolves no column at all. It costs one pass over the deposit and it turns "found when
    # read" into "found when the deposit lands".
    #
    # Unreadable is silent, not a failure: on `dev` the deposit is absent and that is the
    # green state (T-0275), exactly as it is for the quotes above.
    resolved = unreadable = 0
    for issue in corpus_doc.get("issues", []):
        for art in issue.get("artifacts", []):
            recorded = art.get("text_path")
            if not recorded:
                continue
            lines = text_lines(recorded, deposit, repo)
            if lines is None:
                unreadable += 1
                continue
            if column_starts(lines):
                resolved += 1
                continue
            why = UNSEGMENTED.get((issue["id"], art.get("role")))
            if why is None:
                bad.append("%s %s resolves NO column marker, so no claim can ever cite it "
                           "— either its transcription speaks an eighth dialect nothing "
                           "here has been shown, or it carries no column structure and "
                           "belongs in UNSEGMENTED with the reason" % (issue["id"], art.get("role")))

    coverage_doc = load_json(coverage) if Path(coverage).exists() else {"ranges": []}
    bad.extend(coverage_problems(coverage_doc, corpus_doc, files))

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

    for entry in doc["persons"] + doc.get("places", []) + doc["businesses"]:
        if not entry.get("mentions"):
            bad.append("%s has no mention — every entry is compiled FROM a claim, so an "
                       "entry with none cannot have come from one" % entry["id"])

    if not quiet:
        state = "present" if Path(deposit).exists() else "absent (this branch has no deposit)"
        print("  ok    %d extraction file(s), %d claim(s), deposit %s"
              % (len(files), len(seen_claims), state))
        print("  ok    %d quote(s) reassembled from the transcription and identical"
              % checked_quotes)
        print("  ok    %d person(s), %d place(s), %d business(es), compile deterministic "
              "and committed"
              % (len(doc["persons"]), len(doc.get("places", [])), len(doc["businesses"])))
        print("  ok    %d declared identity merge(s): %d person, %d firm, %d place, "
              "%d proprietor — each one carrying its reason"
              % (len(identity_doc.get("merges", []))
                 + len(identity_doc.get("firm_merges", []))
                 + len(identity_doc.get("place_merges", []))
                 + len(identity_doc.get("proprietor_merges", [])),
                 len(identity_doc.get("merges", [])),
                 len(identity_doc.get("firm_merges", [])),
                 len(identity_doc.get("place_merges", [])),
                 len(identity_doc.get("proprietor_merges", []))))
        print("  ok    %d name(s) declared a place rather than a person, each with its "
              "reason and none of them letter-list-only"
              % len(identity_doc.get("places", [])))
        print("  ok    %d house(s) hold two proprietors of one surname apart, each with "
              "the sentence that tells them apart"
              % len(identity_doc.get("proprietor_distinctions", [])))
        readings = sum(len(b.get("placement_readings") or []) for b in doc["businesses"])
        many = sum(1 for b in doc["businesses"]
                   if len(b.get("placement_readings") or []) > 1)
        print("  ok    %d placement reading(s) kept with their own dates, %d house(s) "
              "printed with more than one, %d whose anchor CHANGES on a date — every "
              "reading of those accounted for, the live one computed from the scene date"
              % (readings, many,
                 sum(1 for b in doc["businesses"] if b.get("anchor_change"))))
        print("  ok    %d firm group(s) refused rather than merged, each naming the "
              "printings the refusal rests on"
              % len(identity_doc.get("refused_firm_merges", [])))
        covered = sum(1 for i in corpus_doc.get("issues", [])
                      for r in coverage_doc.get("ranges", [])
                      if i.get("publication") == r.get("publication")
                      and r.get("from", "") <= i.get("date", "") <= r.get("to", ""))
        print("  ok    %d issue(s) inside %d declared coverage range(s), none missing"
              % (covered, len(coverage_doc.get("ranges", []))))
        print("  ok    %d transcription(s) resolve their columns, %d unreadable here, "
              "%d unsegmented by nature" % (resolved, unreadable, len(UNSEGMENTED)))
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
    cases = []                      # every broken-fixture case run below, counted rather
                                    # than asserted: the printed number was hand-kept and
                                    # stopped moving when cases were added (T-0337).
    corpus_doc = load_json(CORPUS)
    fixtures = sorted(EXTRACTED.glob("*.json"))
    base = load_json(fixtures[0]) if fixtures else None
    if base is None:
        print("FAIL: no extraction fixture to break", file=sys.stderr)
        return 1

    def run(mutate, want, label, identity=None):
        cases.append(label)
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
                        deposit=DEPOSIT, repo=REPO, coverage=Path(td) / "none.json",
                        quiet=True)
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

    # T-0356'S FIELD, and every guard on it is a way a date could be invented. Claim 7
    # of this fixture is S. B. Cobb's saddlery, a business claim carrying a dateline of
    # 8 June 1835, which is the shape every `effected` reading in the corpus has.
    COBB = 6

    def opening(d, **kw):
        c = d["claims"][COBB]
        rec = {"verbatim": c["normalized"][:40], "dating": "effected",
               "iso": (c.get("ad_copy_date") or {}).get("iso"),
               "note": "the reading, written down"}
        rec.update(kw)
        c["announces_opening"] = rec

    run(lambda d, i: opening(d), None, "an effected opening over the ad's own dateline")
    run(lambda d, i: opening(d, dating="stated", iso="1835-09-01"),
        None, "a stated opening naming its own date")
    run(lambda d, i: opening(d, dating="undated", iso=None),
        None, "an opening the printing dates nowhere")
    run(lambda d, i: d["claims"][COBB].update(announces_opening=True),
        "it is now a reading", "the bare boolean the field used to be")
    run(lambda d, i: opening(d, verbatim="he will open on the glorious Fourth"),
        "not in the claim's normalized reading",
        "an opening quoting words the paper does not carry")
    run(lambda d, i: opening(d, note="   "),
        "no note", "an opening with no reading behind its date")
    run(lambda d, i: opening(d, dating="rumoured"),
        "is not one of", "a dating outside the vocabulary")
    run(lambda d, i: opening(d, dating="stated", iso="the fourteenth"),
        "does not parse", "an opening date that is not a date")
    run(lambda d, i: opening(d, iso="1835-08-14"),
        "the dateline is the only date", "an effected opening dated off its own dateline")
    run(lambda d, i: (d["claims"][COBB].pop("ad_copy_date"), opening(d, iso="1835-06-08")),
        "carries no ad_copy_date", "an effected opening with no dateline to take")
    run(lambda d, i: opening(d, dating="undated", iso="1835-08-14"),
        "carries a date", "an undated opening given a number anyway")
    run(lambda d, i: (d["claims"][0].update(
            announces_opening={"verbatim": d["claims"][0]["normalized"][:20],
                               "dating": "undated", "iso": None, "note": "n"})),
        "an opening is something a HOUSE does",
        "an opening announced by a claim that is not about a house")

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

    # AND THE NAME PARSE THE POLICY RUNS ON (T-0299). The cases are the ones the three
    # printings of the 1 July 1834 letter list actually produced: markup inside a name and
    # an `[uncertain: …]` wrapper must not invent forenames, an OCR'd dotless ı must not
    # split one, and every genuine disagreement of initials — two read letters, a read
    # letter against an unread `[?]`, a present initial against an absent one — must still
    # refuse. A loosening here shows up as a failure in the SECOND list, which is why both
    # are asserted and not just the first.
    for a, b in (("A[n]drew W. Borland", "Andrew W. Borland"),
                 ("[uncertain: Abey Blankinship]", "Abey Blankinship"),
                 ("Benjam\u0131n Swena", "Benjamin Swena"),
                 ("Ch[a]s. L. Barry", "[C]h[a]s. L. Barry"),
                 ("Dani[e]l O. [uncertain: Robian]", "Daniel O. Robian"),
                 ("W[m]. C. Whittely", "Wm. C Whittely")):
        if surname(a) == surname(b) and initials(a) != initials(b):
            failures.append("the name parse: %r and %r read as different initials, and the "
                            "difference is the transcriber's markup" % (a, b))
    for a, b in (("Cohen, P.", "Cohen, J."),
                 ("Lyman R. Lovell", "Lyman B. Lovell"),
                 ("[H]enry Swartwout jr.", "J[n]o. Swartwout jr."),
                 ("Ann M. Gooding", "[?]nn M. Gooding"),
                 ("Samuel E. Toby", "Samuel. Toby")):
        if not (surname(a) == surname(b) and initials(a) != initials(b)):
            failures.append("the identity policy: %r and %r no longer refuse to merge, and "
                            "an initial is what separates them" % (a, b))

    # AND WHAT AN UNREAD INITIAL ACTUALLY READS AS (T-0397). The two loops above assert
    # only that a pair DIFFERS — and `Ann M. Gooding` / `[?]nn M. Gooding` did differ, for
    # the wrong reason: the parse read `N. M.` off the rest of the forename, and
    # identity.json then STATED that invented letter as the ground of the refusal. So this
    # asserts the VALUE and not the difference. All three shapes the 1 July 1834 list
    # produced are here, because each failed differently.
    for name, want in (("[?]rah Fowler", (UNREAD,)),           # a letter invented from the word
                       ("[?]saac Scarrett", (UNREAD,)),
                       ("[?]nn M. Gooding", (UNREAD, "m")),    # invented, and a position kept
                       ("[?]. M. Fish", (UNREAD, "m")),        # a position that used to collapse
                       ("[?]. [H]. Scott", (UNREAD, "h")),
                       ("[?]. Beegle", (UNREAD,)),             # the absence the ticket assumed
                       ("[?] Adkins", (UNREAD,)),
                       ("Ann M. Gooding", ("a", "m")),         # a read name is untouched
                       ("[uncertain: Abey Blankinship]", ("a",))):
        if initials(name) != want:
            failures.append("the name parse: %r reads as %r, and the printing gives %r"
                            % (name, initials(name), want))


    # THE FIRM'S HALF OF THE SAME POLICY (T-0304). Every case below is built by giving
    # the fixture's own Wilson advertisement a SECOND printing under another spelling,
    # which is the shape every firm merge in identity.json actually has.
    def variant(d, name, **biz):
        src = next(c for c in d["claims"]
                   if (c.get("business") or {}).get("name") == "L. Wilson & Co.")
        c = copy.deepcopy(src)
        c["id"] = "zz1"
        c["business"]["name"] = name
        c["business"].update(biz)
        d["claims"].append(c)

    def firm_rule(i, into, frm, why=None):
        i.setdefault("firm_merges", []).append({
            "into": into, "from": frm,
            "merge_rule": why if why is not None
            else "%s and %s are one house: the same advertisement, twice printed" % (into, frm)})

    run(lambda d, i: (variant(d, "Jno. Wilson & Co."), firm_rule(i, "L. Wilson & Co.", "Jno. Wilson & Co.")),
        None, "two printings of one firm, merged by a stated rule")
    run(lambda d, i: (variant(d, "Jno. Wilson & Co."),
                      i.setdefault("firm_merges", []).append(
                          {"into": "L. Wilson & Co.", "from": "Jno. Wilson & Co."})),
        "no merge_rule", "a firm merge with no stated reason")
    run(lambda d, i: (variant(d, "Jno. Wilson & Co."),
                      firm_rule(i, "L. Wilson & Co.", "Jno. Wilson & Co.", "they look alike")),
        "name BOTH spellings", "a firm merge rule that does not name what it merges")
    run(lambda d, i: firm_rule(i, "Goss & Cobb",
                               "S. B. Cobb, saddle, harness and trunk manufactory"),
        "the partner surnames differ", "a merge that would change who the partners are")
    run(lambda d, i: firm_rule(i, "L. Wilson & Co.", "Nobody & Co."),
        "not a firm any claim carries", "a firm merge rule for a house nobody claimed")
    run(lambda d, i: firm_rule(i, "L. Wilson & Co.", "L. Wilson & Co."),
        "cannot be merged into itself", "a firm merged into itself")
    def street_of(d, name, street):
        next(c for c in d["claims"]
             if (c.get("business") or {}).get("name") == name)["business"]["street"] = street

    run(lambda d, i: (street_of(d, "L. Wilson & Co.", "Dearborn Street"),
                      variant(d, "Jno. Wilson & Co.", street="Lake Street"),
                      firm_rule(i, "L. Wilson & Co.", "Jno. Wilson & Co.")),
        "different streets", "a firm merge across a street the papers contradict")

    # …AND THE REFUSAL (T-0399). Same fixture, same shape: the second printing is a
    # DIFFERENT house that happens to carry the partner surname, which is what
    # `firm_surnames()` cannot tell apart and what the sweep has to be able to write down.
    def firm_refusal(i, into, frm, why=None, kind="two_houses", witnesses=("the fixture",)):
        i.setdefault("refused_firm_merges", []).append({
            "into": into, "from": frm, "kind": kind, "witnesses": list(witnesses),
            "refused_because": why if why is not None
            else "%s and %s are two houses: one surname, two trades, no printing joining them"
                 % (into, frm)})

    run(lambda d, i: (variant(d, "Jno. Wilson & Co."), firm_refusal(i, "L. Wilson & Co.", "Jno. Wilson & Co.")),
        None, "two firm styles held apart by a stated refusal")
    run(lambda d, i: (variant(d, "Jno. Wilson & Co."),
                      firm_refusal(i, "L. Wilson & Co.", "Jno. Wilson & Co.", "")),
        "no refused_because", "a firm refusal that does not say why it refuses")
    run(lambda d, i: (variant(d, "Jno. Wilson & Co."),
                      firm_refusal(i, "L. Wilson & Co.", "Jno. Wilson & Co.", "they differ")),
        "name BOTH spellings", "a firm refusal that does not name what it holds apart")
    run(lambda d, i: (variant(d, "Jno. Wilson & Co."),
                      firm_refusal(i, "L. Wilson & Co.", "Jno. Wilson & Co.", kind="probably")),
        "`kind` must be one of", "a firm refusal whose kind is not one of the three")
    run(lambda d, i: (variant(d, "Jno. Wilson & Co."),
                      firm_refusal(i, "L. Wilson & Co.", "Jno. Wilson & Co.", witnesses=())),
        "no `witnesses`", "a firm refusal that rests on no printing")
    run(lambda d, i: firm_refusal(i, "L. Wilson & Co.", "Nobody & Co."),
        "outlived its pair", "a firm refusal for a house nobody claimed")
    run(lambda d, i: firm_refusal(i, "L. Wilson & Co.", "L. Wilson & Co."),
        "refused against itself", "a firm refused against itself")
    run(lambda d, i: (variant(d, "Jno. Wilson & Co."),
                      firm_rule(i, "L. Wilson & Co.", "Jno. Wilson & Co."),
                      firm_refusal(i, "L. Wilson & Co.", "Jno. Wilson & Co.")),
        "cannot both join and hold apart", "a pair both merged and refused")

    # THE SIGN-NAME ESCAPE AND ITS NEGATIVE CASES (T-0340). The guard above lets a style
    # that names NO partner merge into one that does; everything here is the price of
    # that, because a loosening nobody can fire is a loosening nobody can trust. The
    # FIRST case is the one that matters most: undeclared, a headline-only style is still
    # refused, so the escape cannot be taken by accident or by silence.
    def sign_decl(i, style, partners, sign, note="the self-test's own declaration"):
        i.setdefault("firm_sign_names", []).append(
            {"style": style, "partners": partners, "sign": sign, "note": note})

    run(lambda d, i: (variant(d, "Chicago Book and Stationary Store", proprietors=[]),
                      firm_rule(i, "L. Wilson & Co.", "Chicago Book and Stationary Store")),
        "the partner surnames differ",
        "a headline-only style merged with no sign-name declared")
    run(lambda d, i: (variant(d, "Chicago Book and Stationary Store", proprietors=[]),
                      sign_decl(i, "Chicago Book and Stationary Store", "",
                                "Chicago Book and Stationary Store"),
                      firm_rule(i, "L. Wilson & Co.", "Chicago Book and Stationary Store")),
        None, "a declared sign-name merged into the style that names the partners")
    run(lambda d, i: (variant(d, "Chicago Book and Stationary Store",
                              proprietors=["Ezekiel Book"]),
                      sign_decl(i, "Chicago Book and Stationary Store", "",
                                "Chicago Book and Stationary Store"),
                      firm_rule(i, "L. Wilson & Co.", "Chicago Book and Stationary Store")),
        "the claims sign it with",
        "a house declared to name no partner that a printing signs with one")
    run(lambda d, i: (variant(d, "Chicago Book and Stationary Store", proprietors=[]),
                      sign_decl(i, "Chicago Book and Stationary Store", "",
                                "Chicago Book Store")),
        "put the style back together verbatim",
        "a sign-name split that quietly drops a word of the style")
    run(lambda d, i: sign_decl(i, "Nobody & Co., Chicago Book Store", "Nobody & Co.",
                               "Chicago Book Store"),
        "a business that is not in the corpus",
        "a sign-name declaration for a house nobody claimed")
    run(lambda d, i: (variant(d, "Chicago Book and Stationary Store", proprietors=[]),
                      i.setdefault("firm_sign_names", []).append(
                          {"style": "Chicago Book and Stationary Store", "partners": "",
                           "sign": "Chicago Book and Stationary Store"})),
        "no note", "a sign-name declaration with no stated reason")
    # And a declaration cannot FORCE a merge: split the style honestly and the partners
    # it does name are compared exactly as before.
    run(lambda d, i: (variant(d, "Goss & Cobb, Chicago Book Store", proprietors=[]),
                      sign_decl(i, "Goss & Cobb, Chicago Book Store", "Goss & Cobb",
                                "Chicago Book Store"),
                      firm_rule(i, "L. Wilson & Co.", "Goss & Cobb, Chicago Book Store")),
        "the partner surnames differ",
        "a sign-name declaration used to smuggle two other partners in")

    # THE PROPRIETORS' HALF (T-0337). Every case is the shape the Russell & Clift pair
    # actually had: two readings of one house's partner, sitting in one `proprietors`
    # list, which neither the person policy nor the firm policy can reach.
    def props(d, name, *who):
        next(c for c in d["claims"]
             if (c.get("business") or {}).get("name") == name)["business"]["proprietors"] = list(who)

    def prop_merge(i, bid, into, frm, why=None):
        i.setdefault("proprietor_merges", []).append({
            "business": bid, "into": into, "from": frm,
            "merge_rule": why if why is not None
            else "%s and %s are one man: the same notice, twice printed" % (into, frm)})

    def prop_distinct(i, bid, a, b, why="two partners, both signing one notice"):
        i.setdefault("proprietor_distinctions", []).append(
            {"business": bid, "names": [a, b], "rule": why})

    WILSON = "business_l_wilson_co"
    run(lambda d, i: props(d, "L. Wilson & Co.", "Benj. Clift", "[H. H.] Clift"),
        "one surname with different forenames",
        "one house's proprietors read two ways, undeclared")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Benj. Clift", "[H. H.] Clift"),
                      prop_merge(i, WILSON, "Benj. Clift", "[H. H.] Clift")),
        None, "…and joined by a stated proprietor merge")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Benj. Clift", "[H. H.] Clift"),
                      prop_distinct(i, WILSON, "Benj. Clift", "[H. H.] Clift")),
        None, "…or held apart by a stated distinction")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Benj. Clift", "[H. H.] Clift"),
                      prop_distinct(i, WILSON, "Benj. Clift", "[H. H.] Clift", "")),
        "no rule", "a distinction that does not say how the two are told apart")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Benj. Clift", "[H. H.] Clift"),
                      i.setdefault("proprietor_merges", []).append(
                          {"business": WILSON, "into": "Benj. Clift", "from": "[H. H.] Clift"})),
        "no merge_rule", "a proprietor merge with no stated reason")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Benj. Clift", "[H. H.] Clift"),
                      prop_merge(i, WILSON, "Benj. Clift", "[H. H.] Clift", "they look alike")),
        "name BOTH spellings", "a proprietor merge rule that does not name what it merges")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Aaron Russell", "Benj. Clift"),
                      prop_merge(i, WILSON, "Aaron Russell", "Benj. Clift")),
        "a proprietor merge may join two readings of one name",
        "a proprietor merge across two different surnames")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Benj. Clift"),
                      prop_merge(i, WILSON, "Benj. Clift", "[H. H.] Clift")),
        "is not a proprietor this house carries", "a proprietor merge gone stale")
    run(lambda d, i: (props(d, "L. Wilson & Co.", "Benj. Clift"),
                      prop_distinct(i, WILSON, "Benj. Clift", "[H. H.] Clift")),
        "no longer answers anything", "a distinction whose pair has gone")
    run(lambda d, i: prop_merge(i, "business_nobody_at_all", "A. Nobody", "B. Nobody"),
        "no business of that id is compiled", "a proprietor rule for a house nobody claimed")
    # A BARE SURNAME IS NOT A SECOND MAN. 'Hubbard' beside 'Gurdon S. Hubbard' is the
    # papers printing less, and the gate must not send anyone to adjudicate it.
    run(lambda d, i: props(d, "L. Wilson & Co.", "Hubbard", "Gurdon S. Hubbard"),
        None, "a bare surname beside a full name is nothing to declare")
    # …and neither is a firm's own style, which `proprietors` carries wherever a claim
    # read only the signature.
    run(lambda d, i: props(d, "L. Wilson & Co.", "Jones & King", "Byram King"),
        None, "a firm style in the proprietors is not a person")

    # And the merge has to DO something: green is also what a merge that quietly did
    # nothing would look like, so the union is asserted on the compiled record itself.
    merged_fixture = copy.deepcopy(base)
    variant(merged_fixture, "Jno. Wilson & Co.")
    merged_fixture["claims"][-1]["business"]["goods"] = ["Window Sash"]
    merged_ident = {"merges": []}
    firm_rule(merged_ident, "L. Wilson & Co.", "Jno. Wilson & Co.")
    with tempfile.TemporaryDirectory() as td:
        ex = Path(td) / "extracted"
        ex.mkdir()
        (ex / ("%s.json" % merged_fixture["issue_id"])).write_text(
            json.dumps(merged_fixture, ensure_ascii=False), encoding="utf-8")
        doc, probs = compile_gazetteer(sorted(ex.glob("*.json")), merged_ident, corpus_doc)
    names = [b["name"] for b in doc["businesses"]]
    got = next((b for b in doc["businesses"] if b["name"] == "L. Wilson & Co."), None)
    if probs:
        failures.append("the union case did not compile clean: %r" % probs)
    elif "Jno. Wilson & Co." in names:
        failures.append("a declared firm merge left both spellings standing")
    elif got is None:
        failures.append("a declared firm merge lost the firm it merged into")
    elif len(got["mentions"]) != 2:
        failures.append("a firm merge did not carry the mentions across: %r" % got["mentions"])
    elif "Window Sash" not in got["goods"]:
        failures.append("a firm merge did not carry the goods across: %r" % got["goods"])
    elif not got.get("merged"):
        failures.append("a firm merge left no record of itself on the firm")


    # THE DATED ANCHOR CHANGE (T-0345). These run against compile_gazetteer directly
    # rather than through `run`, because a CHANGE needs two issues printed on different
    # days and `run` writes one extraction file. Two issues are taken from corpus.json
    # itself, earliest and latest, so the cases cannot rot into asserting a date the
    # corpus stopped carrying.
    dates = sorted((i.get("date"), i.get("id")) for i in corpus_doc.get("issues", [])
                   if i.get("date") and i.get("id"))
    scene_iso = SCENE_DATE.isoformat()
    early_id = dates[0][1]
    late_id = [i for d, i in dates if d <= scene_iso][-1]
    after_id = dates[-1][1]                     # the corpus runs past the scene date

    def anchor_docs(early_anchors, late_anchors):
        def doc_for(issue_id, anchors):
            return {"issue_id": issue_id, "claims": [
                {"id": "za%d" % n, "kind": "business", "reading": "transcription_mediated",
                 "business": {"name": "A. Smith & Co.", "trade": "blacksmith",
                              "street": "Lake Street",
                              "placement": {"class": "relative", "anchor": a,
                                            "offset_text": "opposite %s" % a}}}
                for n, a in enumerate(anchors)]}
        return [doc_for(early_id, early_anchors), doc_for(late_id, late_anchors)]

    def anchor_rule(groups, rule=None, cannot="the corpus does not say which moved",
                    business="business_a_smith_co"):
        names = [g["name"] for g in groups]
        return {"merges": [], "anchor_changes": [{
            "business": business, "anchors": groups,
            "rule": rule if rule is not None
            else "the anchor changes from %s" % " to ".join('"%s"' % n for n in names),
            "cannot_say": cannot}]}

    def run_anchor(docs, ident, want, label):
        cases.append(label)
        with tempfile.TemporaryDirectory() as td:
            ex = Path(td) / "extracted"
            ex.mkdir()
            for doc in docs:
                (ex / ("%s.json" % doc["issue_id"])).write_text(
                    json.dumps(doc, ensure_ascii=False), encoding="utf-8")
            out, probs = compile_gazetteer(sorted(ex.glob("*.json")), ident, corpus_doc)
        if want is None:
            if probs:
                failures.append("%s: expected a clean compile, got %r" % (label, probs))
            return out
        if not any(want in b for b in probs):
            failures.append("%s: expected a failure mentioning %r, got %r"
                            % (label, want, probs))
        return out

    GRAVES = {"name": "the tavern", "readings": ["the tavern", "the tavern, on Main-st"],
              "why": "two readings of the tavern, one sweeping the street in after it"}
    TREMONT = {"name": "the hotel", "readings": ["the hotel"]}

    out = run_anchor(anchor_docs(["the tavern", "the tavern, on Main-st"], ["the hotel"]),
                     anchor_rule([GRAVES, TREMONT]), None,
                     "an anchor that changes on a date, declared and dated")
    got = next((b for b in out["businesses"] if b["id"] == "business_a_smith_co"), None)
    if got is None:
        failures.append("the dated anchor case lost the house it was declared on")
    elif not got.get("anchor_change"):
        failures.append("a declared anchor change left no history on the house")
    elif got["anchor_change"]["live_anchor"] != "the hotel":
        failures.append("the anchor live at the scene date is computed as %r, and the "
                        "later printing is 'the hotel'" % got["anchor_change"]["live_anchor"])
    elif got["placement"]["anchor"] != "the hotel":
        failures.append("a dated anchor change left the house placed on the SUPERSEDED "
                        "reading %r" % got["placement"]["anchor"])
    elif [c["after"] for c in got["anchor_change"]["changes"]] != [dates[0][0]]:
        failures.append("the change is bracketed by %r and the earlier printing is %s"
                        % (got["anchor_change"]["changes"], dates[0][0]))
    elif len(got["placement_readings"]) != 3:
        failures.append("three printings, three readings kept, got %d"
                        % len(got["placement_readings"]))

    # …and the scene date is what decides which is live, not the order they were
    # printed in: an anchor first set AFTER 1 July 1835 was not up on 1 July 1835.
    out = run_anchor(
        [{"issue_id": early_id, "claims": [
            {"id": "za0", "business": {"name": "A. Smith & Co.", "trade": "blacksmith",
                                       "street": "Lake Street",
                                       "placement": {"class": "relative",
                                                     "anchor": "the tavern"}}}]},
         {"issue_id": after_id, "claims": [
             {"id": "za1", "business": {"name": "A. Smith & Co.", "trade": "blacksmith",
                                        "street": "Lake Street",
                                        "placement": {"class": "relative",
                                                      "anchor": "the hotel"}}}]}],
        anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}, TREMONT]),
        None, "an anchor first printed after the scene date")
    got = next((b for b in out["businesses"] if b["id"] == "business_a_smith_co"), None)
    if got and got["anchor_change"]["live_anchor"] != "the tavern":
        failures.append("an anchor first printed %s was made live at the scene date %s"
                        % (dates[-1][0], scene_iso))

    run_anchor(anchor_docs(["the tavern"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}, TREMONT],
                           rule=""),
               "no rule", "an anchor change with no stated reason")
    run_anchor(anchor_docs(["the tavern"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}, TREMONT],
                           rule="the anchor changed at some point"),
               "must name", "an anchor rule that does not name the anchors it orders")
    run_anchor(anchor_docs(["the tavern"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}, TREMONT],
                           cannot=""),
               "cannot_say", "a dated change that says nothing about what stays open")
    run_anchor(anchor_docs(["the tavern"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}, TREMONT],
                           business="business_nobody_at_all"),
               "no business of that id is compiled",
               "an anchor rule for a house nobody claimed")
    run_anchor(anchor_docs(["the tavern"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}]),
               "one anchor is not a change", "an anchor change with a single anchor")
    run_anchor(anchor_docs(["the tavern"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]},
                            {"name": "the hotel", "readings": ["the hotel", "the barn"]},
                            ]),
               "not an anchor any printing of this house carries",
               "an anchor rule naming a reading nobody printed")
    run_anchor(anchor_docs(["the tavern", "the tavern, on Main-st"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}, TREMONT]),
               "silently dropped", "a printing left out of the history")
    run_anchor(anchor_docs(["the tavern", "the tavern, on Main-st"], ["the hotel"]),
               anchor_rule([GRAVES, {"name": "the hotel",
                                     "readings": ["the hotel", "the tavern"],
                                     "why": "the hotel, twice"}]),
               "claimed by two anchors", "one printing naming two landmarks")
    run_anchor(anchor_docs(["the tavern", "the tavern, on Main-st"], ["the hotel"]),
               anchor_rule([dict(GRAVES, why="two readings, grouped"), TREMONT]),
               "is a judgement and it has to be written down",
               "two readings called one landmark on nobody's argument")
    run_anchor(anchor_docs(["the tavern", "the hotel"], ["the hotel"]),
               anchor_rule([{"name": "the tavern", "readings": ["the tavern"]}, TREMONT]),
               "overlapping weeks", "two anchors printed in the same weeks")

    # SILENCE DOES NOT HOLD A HOUSE'S PLACEMENT (T-0440). The mint takes `placement`
    # and `street` from the earliest printing, so a standing advertisement that ran
    # without an address in its first week and with one afterwards stood at
    # `{"class": "none"}` for good and read `unplaceable` in the register. Both halves
    # of the repair are asserted here: that a later printing's address is taken up, and
    # that a printed address is NEVER overridden by another printed address.
    def silent_then_placed(late_placement, early_placement=None):
        def doc_for(issue_id, placement):
            return {"issue_id": issue_id, "claims": [
                {"id": "zs0", "kind": "business", "reading": "transcription_mediated",
                 "business": {"name": "A. Smith & Co.", "trade": "blacksmith",
                              "placement": placement}}]}
        return [doc_for(early_id, early_placement or {"class": "none"}),
                doc_for(late_id, late_placement)]

    LATE = {"class": "relative", "anchor": "the hotel", "offset_text": "opposite the hotel",
            "street": "Lake Street"}
    out = run_anchor(silent_then_placed(LATE), {"merges": [], "anchor_changes": []}, None,
                     "a first printing with no address does not hold the placement")
    got = next((b for b in out["businesses"] if b["id"] == "business_a_smith_co"), None)
    if got is None:
        failures.append("the silent-printing case lost the house it was declared on")
    elif (got["placement"] or {}).get("anchor") != "the hotel":
        failures.append("a house silent in its first printing and placed in its second "
                        "is left placed by the silence: %r" % got["placement"])
    elif got.get("street") != "Lake Street":
        failures.append("the street the placing printing names was not taken up: %r"
                        % got.get("street"))
    elif not got.get("placement_from"):
        failures.append("a placement taken from a later printing left no record of "
                        "where it came from")
    elif len(got["placement_readings"]) != 2:
        failures.append("the silent printing was dropped rather than kept as a reading: "
                        "%d reading(s)" % len(got["placement_readings"]))

    # …and the other direction: an address that IS printed first stands, whatever a
    # later printing says. Reordering two printed addresses is `anchor_changes`' to
    # declare and this pass may never do it in silence.
    out = run_anchor(silent_then_placed(LATE, early_placement={
        "class": "street_only", "street": "South Water Street"}),
        {"merges": [], "anchor_changes": []}, None,
        "a printed address is not overridden by a later printed address")
    got = next((b for b in out["businesses"] if b["id"] == "business_a_smith_co"), None)
    if got and (got["placement"] or {}).get("class") != "street_only":
        failures.append("a house printed with an address in its first week was re-placed "
                        "by a later printing with no rule declaring the move: %r"
                        % got["placement"])
    if got and got.get("placement_from"):
        failures.append("the silence rule fired on a house that was never silent")

    # …and an address first printed AFTER the scene date does not place the house at the
    # scene date, which is the bound `anchor_changes` and AGENTS.md rule 3 already hold.
    # The SILENT printing has to be the one that MINTS the house, or this case tests the
    # mint rather than the pass — `compile_gazetteer` reads the extraction files in
    # filename order, so both ids are chosen off the corpus by that order and the
    # fixture asserts the ordering it depends on rather than assuming it.
    silent_id = min(i for d, i in dates if d <= scene_iso)
    placed_after_id = max((i for d, i in dates if d > scene_iso), default=None)
    if placed_after_id is None or silent_id >= placed_after_id:
        failures.append("the after-the-scene-date placement case cannot be built from "
                        "this corpus: %r does not sort before %r"
                        % (silent_id, placed_after_id))
    else:
        out = run_anchor([{"issue_id": silent_id, "claims": [
            {"id": "zs0", "kind": "business", "reading": "transcription_mediated",
             "business": {"name": "A. Smith & Co.", "trade": "blacksmith",
                          "placement": {"class": "none"}}}]},
            {"issue_id": placed_after_id, "claims": [
                {"id": "zs1", "kind": "business", "reading": "transcription_mediated",
                 "business": {"name": "A. Smith & Co.", "trade": "blacksmith",
                              "placement": LATE}}]}],
            {"merges": [], "anchor_changes": []}, None,
            "an address first printed after the scene date")
        got = next((b for b in out["businesses"] if b["id"] == "business_a_smith_co"),
                   None)
        if got and placement_rank(got.get("placement")) > 0:
            failures.append("an address first printed after the scene date %s placed "
                            "the house at it: %r" % (scene_iso, got["placement"]))

    # …and an anchor rule may now be written for a house one of whose printings gave no
    # address at all. Before T-0440 the `null` anchor of a silent printing could neither
    # be named by a group (guard 3) nor left out of one (guard 4), so the one mechanism
    # that may order a house's anchors was unreachable for exactly those houses.
    def three_printings(anchors):
        docs = silent_then_placed({"class": "relative", "anchor": anchors[1],
                                   "offset_text": "opposite %s" % anchors[1]})
        docs.append({"issue_id": after_id, "claims": [
            {"id": "zs1", "kind": "business", "reading": "transcription_mediated",
             "business": {"name": "A. Smith & Co.", "trade": "blacksmith",
                          "placement": {"class": "relative", "anchor": anchors[2],
                                        "offset_text": "opposite %s" % anchors[2]}}}]})
        return docs

    out = run_anchor(three_printings([None, "the tavern", "the hotel"]),
                     anchor_rule([{"name": "the tavern", "readings": ["the tavern"]},
                                  TREMONT]),
                     None, "an anchor rule on a house whose first printing was silent")
    got = next((b for b in out["businesses"] if b["id"] == "business_a_smith_co"), None)
    if got is None:
        failures.append("the silent-printing anchor-rule case lost its house")
    elif not got.get("anchor_change"):
        failures.append("a silent printing still blocks an anchor rule from being "
                        "written for the house")
    elif got["anchor_change"]["live_anchor"] != "the tavern":
        failures.append("the anchor live at the scene date is %r on a house whose only "
                        "later printing runs after it"
                        % got["anchor_change"]["live_anchor"])
    elif len(got["placement_readings"]) != 3:
        failures.append("the silent printing was dropped from the readings by the "
                        "anchor rule: %d kept" % len(got["placement_readings"]))

    # A NAME IS NOT ALWAYS A PERSON (T-0359), and the cases below are the ones the
    # Haddock's/Maddock's pair actually produced. Every guard here exists to stop the
    # place table becoming a hole in the families rule, so each is asserted from the
    # direction that would open one.
    def entity(d, name, claim_id="zp1", letter_list=False, occupations=None):
        c = copy.deepcopy(d["claims"][0])
        c["id"] = claim_id
        c["entities"] = [{"as_printed": name, "normalized": name,
                          "occupations": list(occupations or [])}]
        if letter_list:
            c["letter_list_only"] = True
        d["claims"].append(c)

    def place_rule(i, name, why=None, kind="tavern"):
        i.setdefault("places", []).append({
            "name": name, "kind": kind,
            "why": why if why is not None
            else "%s is a signboard the papers measure a lot from, not a man" % name})

    def place_merge(i, into, frm, why=None):
        i.setdefault("place_merges", []).append({
            "into": into, "from": frm,
            "merge_rule": why if why is not None
            else "%s and %s are one building, printed twice" % (into, frm)})

    run(lambda d, i: (entity(d, "Haddock's Tavern"),
                      entity(d, "Maddock's Tavern", claim_id="zp2"),
                      place_rule(i, "Haddock's Tavern"), place_rule(i, "Maddock's Tavern"),
                      place_merge(i, "Haddock's Tavern", "Maddock's Tavern")),
        None, "two spellings of one signboard, declared places and merged")
    run(lambda d, i: (entity(d, "Haddock's Tavern"),
                      i.setdefault("places", []).append({"name": "Haddock's Tavern"})),
        "no `why`", "a place declared with no reason")
    run(lambda d, i: (entity(d, "Haddock's Tavern"),
                      place_rule(i, "Haddock's Tavern", "it sounds like a building")),
        "name the place VERBATIM", "a place reason that does not name what it declares")
    run(lambda d, i: place_rule(i, "Nowhere Tavern"),
        "not a name any claim carries", "a place nobody claimed")
    run(lambda d, i: (entity(d, "Chester House", letter_list=True),
                      place_rule(i, "Chester House", kind="hotel")),
        "post-office letter list", "a letter-list name declared a building")
    run(lambda d, i: (entity(d, "Haddock's Tavern", occupations=["innkeeper"]),
                      place_rule(i, "Haddock's Tavern")),
        "carries an occupation", "a name a claim reads as a person, declared a place")

    # The families rule is not loosened, and these two say so from both sides: a place
    # merge cannot reach a name that was not declared, and once a name IS declared the
    # PERSON merge path cannot see it at all.
    run(lambda d, i: (entity(d, "Haddock's Tavern"),
                      entity(d, "Maddock's Tavern", claim_id="zp2"),
                      place_rule(i, "Haddock's Tavern"),
                      place_merge(i, "Haddock's Tavern", "Maddock's Tavern")),
        "not a DECLARED place", "a place merge reaching a name nobody declared a place")
    run(lambda d, i: (entity(d, "Haddock's Tavern"), place_rule(i, "Haddock's Tavern"),
                      i["merges"].append(
                          {"into": "W. L. Newberry", "from": "Haddock's Tavern",
                           "merge_rule": "W. L. Newberry and Haddock's Tavern, as people"})),
        "not a name any claim carries", "a declared place merged as if it were a person")
    run(lambda d, i: (entity(d, "Haddock's Tavern"), place_rule(i, "Haddock's Tavern"),
                      place_merge(i, "Haddock's Tavern", "Haddock's Tavern")),
        "cannot be merged into itself", "a place merged into itself")
    run(lambda d, i: (entity(d, "Haddock's Tavern"),
                      entity(d, "Maddock's Tavern", claim_id="zp2"),
                      place_rule(i, "Haddock's Tavern"), place_rule(i, "Maddock's Tavern"),
                      i.setdefault("place_merges", []).append(
                          {"into": "Haddock's Tavern", "from": "Maddock's Tavern"})),
        "no merge_rule", "a place merge with no stated reason")
    run(lambda d, i: i.setdefault("refused_places", []).append(
            {"name": "Chester House",
             "refused_because": "Chester House is a person: the surname is House"}),
        "not a name any claim carries as a person", "a refusal about a name nobody claimed")
    run(lambda d, i: (entity(d, "Haddock's Tavern"), place_rule(i, "Haddock's Tavern"),
                      i.setdefault("refused_places", []).append(
                          {"name": "Haddock's Tavern",
                           "refused_because": "Haddock's Tavern is a person after all"})),
        "DECLARED a place and refused", "a name both declared and refused in one file")

    # And the declaration has to DO something: green is also what a place table that
    # quietly changed nothing would look like, so the move and the union are asserted on
    # the compiled record itself.
    placed = copy.deepcopy(base)
    entity(placed, "Haddock's Tavern")
    entity(placed, "Maddock's Tavern", claim_id="zp2")
    placed_ident = {"merges": []}
    place_rule(placed_ident, "Haddock's Tavern")
    place_rule(placed_ident, "Maddock's Tavern")
    place_merge(placed_ident, "Haddock's Tavern", "Maddock's Tavern")
    with tempfile.TemporaryDirectory() as td:
        ex = Path(td) / "extracted"
        ex.mkdir()
        (ex / ("%s.json" % placed["issue_id"])).write_text(
            json.dumps(placed, ensure_ascii=False), encoding="utf-8")
        doc, probs = compile_gazetteer(sorted(ex.glob("*.json")), placed_ident, corpus_doc)
    person_names = [p["name"] for p in doc["persons"]]
    got = next((p for p in doc.get("places", []) if p["name"] == "Haddock's Tavern"), None)
    if probs:
        failures.append("the place case did not compile clean: %r" % probs)
    elif "Haddock's Tavern" in person_names or "Maddock's Tavern" in person_names:
        failures.append("a declared place is still standing in the persons table")
    elif got is None:
        failures.append("a declared place reached neither table")
    elif len(got["mentions"]) != 2:
        failures.append("a place merge did not carry the mentions across: %r" % got["mentions"])
    elif "letter_list_only" in got or "occupations" in got:
        failures.append("a place kept a field that only means something about a person: %r"
                        % sorted(got))
    elif not got.get("merged"):
        failures.append("a place merge left no record of itself on the place")
    elif doc["counts"].get("places") != 1:
        failures.append("the places count does not match the table: %r" % doc["counts"])

    # THE ASSERTIONS THAT NEED A TRANSCRIPTION TO READ, and they must fire on `dev`,
    # where the deposit is absent. So they are run against an issue whose text is
    # DERIVED and therefore committed — the American run — with the claim built out of
    # that file at run time, so the control case cannot drift as the corpus grows.
    backed = text_backed_fixture(corpus_doc)
    if backed is None:
        failures.append("no derived-text issue to build the text-backed cases from")
    else:
        def run_backed(mutate, want, label):
            cases.append(label)
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
                            deposit=DEPOSIT, repo=REPO,
                            coverage=Path(td) / "none.json", quiet=True)
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

        # T-0261's finer grain. The control narrows the backed claim to two character
        # ranges of its own line and quotes exactly those, so every case below is
        # unambiguously about `spans` and not about the line it sits in.
        n0 = backed["claims"][0]["locator"]["lines_of_claim"][0]
        whole = backed["claims"][0]["quote"]
        half = max(2, len(whole) // 2)

        def with_spans(d, spans, quote=None):
            d["claims"][0]["locator"]["spans"] = spans
            if quote is not None:
                d["claims"][0]["quote"] = quote

        run_backed(lambda d: with_spans(d, [{"line": n0, "from": 0, "to": 2},
                                            {"line": n0, "from": half, "to": half + 2}],
                                        whole[0:2] + "\n" + whole[half:half + 2]),
                   None, "a quote narrowed to two character ranges of its line")
        run_backed(lambda d: with_spans(d, [{"line": n0, "from": 0, "to": 2}], whole),
                   "not what lines", "a spans quote that still carries the whole line")
        run_backed(lambda d: with_spans(d, [{"line": n0 + 500000, "from": 0, "to": 2}]),
                   "lines_of_claim does not name",
                   "a span on a line the claim never claimed")
        run_backed(lambda d: with_spans(d, [{"line": n0, "from": 0, "to": 10 ** 7}]),
                   "is not inside a", "a span running past the end of its line")
        run_backed(lambda d: with_spans(d, [{"line": n0, "from": half, "to": half + 2},
                                            {"line": n0, "from": 0, "to": 2}]),
                   "reading order", "spans out of reading order")
        run_backed(lambda d: with_spans(d, [{"line": n0, "from": 0, "to": half + 2},
                                            {"line": n0, "from": half, "to": half + 4}]),
                   "overlap", "two spans quoting the same characters twice")
        run_backed(lambda d: (d["claims"][0]["locator"].update(
                       lines=[n0, n0 + 1], lines_of_claim=[n0, n0 + 1]),
                       with_spans(d, [{"line": n0, "from": 0, "to": 2}])),
                   "no span quotes any of it",
                   "a claimed line the spans never quote")

    # THE COVERAGE RANGE, which is the only assertion here about an issue that is NOT
    # in the tree. Every other case breaks something present; these break something by
    # its absence, which is the shape of the fault a reading pass actually has.
    def run_coverage(ranges, want, label):
        cases.append(label)
        with tempfile.TemporaryDirectory() as td:
            ex = Path(td) / "extracted"
            ex.mkdir()
            (ex / ("%s.json" % base["issue_id"])).write_text(
                json.dumps(base, ensure_ascii=False), encoding="utf-8")
            ip = Path(td) / "identity.json"
            ip.write_text(json.dumps({"merges": []}), encoding="utf-8")
            doc, _ = compile_gazetteer(sorted(ex.glob("*.json")), {"merges": []}, corpus_doc)
            gz = Path(td) / "gazetteer.json"
            gz.write_text(dumps(doc), encoding="utf-8")
            cov = Path(td) / "coverage.json"
            cov.write_text(json.dumps({"schema": 1, "ranges": ranges}), encoding="utf-8")
            bad = check(extracted=ex, gazetteer=gz, identity=ip, corpus=CORPUS,
                        deposit=DEPOSIT, repo=REPO, coverage=cov, quiet=True)
        if want is None:
            if bad:
                failures.append("%s: expected a clean run, got %r" % (label, bad))
        elif not any(want in b for b in bad):
            failures.append("%s: expected a failure mentioning %r, got %r"
                            % (label, want, bad))

    issue = issue_index(corpus_doc)[base["issue_id"]]
    run_coverage([], None, "no declared range at all")
    run_coverage([{"publication": issue["publication"], "from": issue["date"],
                   "to": issue["date"], "ticket": "self-test"}],
                 None, "a range covering exactly the issue that is present")
    run_coverage([{"publication": issue["publication"], "from": "1835-07-01",
                   "to": "1835-08-31", "ticket": "self-test"}],
                 "no extraction file",
                 "a range with issues in it that were never read")
    run_coverage([{"publication": issue["publication"], "from": issue["date"],
                   "ticket": "self-test"}],
                 "needs publication, from and to", "a range missing its end")
    run_coverage([{"publication": issue["publication"], "from": "1899-01-01",
                   "to": "1899-12-31", "ticket": "self-test"}],
                 "names no issue in corpus.json", "a range that covers nothing")
    run_coverage([{"publication": issue["publication"], "from": "the summer",
                   "to": "1835-08-31", "ticket": "self-test"}],
                 "must be ISO dates", "a range whose dates do not parse")

    # THE RULED MARKER DIALECTS, one case each plus a negative (T-0289). T-0257's pattern
    # matched only the bare `PDF PAGE` form, which is 90 of the deposit's 1,266 ruled
    # markers, and nothing on `dev` could see the gap because the deposit is not there to
    # read. A dialect added without a case here will be caught by this list failing to grow.
    for dialect in (
            "===== ISSUE PAGE 3 / PDF PAGE 19 / COLUMN 5 OF 6 =====",
            "===== ISSUE PAGE 3 / SOURCE PDF PAGE 19 / COLUMN 5 OF 6 =====",
            "===== ISSUE PAGE 3 / ORIGINAL PDF PAGE 19 / COLUMN 5 OF 6 ====="):
        m = COLUMN_MARKER.match(dialect)
        if not m or (int(m.group(1)), int(m.group(3))) != (3, 5):
            failures.append("the column marker %r does not resolve to page 3 column 5" % dialect)
    if COLUMN_MARKER.match("===== ISSUE PAGE 3 / COLUMN 5 OF 6 ====="):
        failures.append("the column marker pattern matched a line with no scan page")

    # THE FIFTH SHAPE, WHICH IS THE WHOLE OF 1833 (T-0258): a page banner in one of two
    # forms, then `--- Column k ---`. The bare banner names the SCAN page and not the
    # issue's, so it is resolved by ordinal — asserted here on two pages, because an
    # off-by-one that only shows on the second page is exactly what this would hide.
    dash = ["SOURCE PDF PAGE 5", "--- Column 1 ---", "a", "--- Column 2 ---", "b",
            "===== SOURCE PDF PAGE 6 / ISSUE PAGE 2 =====", "--- Column 1 ---", "c"]
    if column_starts(dash) != [(2, 1, 1), (4, 1, 2), (7, 2, 1)]:
        failures.append("the 1833 dash-column dialect does not resolve: a bare "
                        "`SOURCE PDF PAGE 5` banner must count as issue page 1 by ordinal, "
                        "and a ruled banner must be read for the page it states")
    if not DASH_COLUMN_HEADING.match("--- Column 4 ---"):
        failures.append("the dash-column heading `--- Column 4 ---` does not resolve")
    if BARE_PAGE_BANNER.match("===== SOURCE PDF PAGE 6 / ISSUE PAGE 2 ====="):
        failures.append("the bare page banner pattern swallowed a ruled banner, which "
                        "would resolve the issue page by ordinal instead of reading it")
    if column_starts(["--- Column 1 ---", "orphan"]):
        failures.append("a column before any page line was guessed at rather than skipped")

    # THE SIXTH SHAPE, WHICH IS THREE OF THE EIGHT DEMOCRATS OF EARLY 1835 (T-0298): page
    # and column on one bracketed line. Asserted on two pages for the same reason the
    # 1833 case is, and with the Extra's column-less prospectus line beside them, because
    # reading that one as column 1 is the only judgement in this dialect.
    bracket = ["[Source PDF page 9; newspaper page 1; column 1]", "a",
               "[Source PDF page 9; newspaper page 1; column 3]", "b",
               "[Source PDF page 10; newspaper page 2; column 1]", "c",
               "[Source PDF page 8; Extra page 4; single-column subscription prospectus]"]
    if column_starts(bracket) != [(1, 1, 1), (3, 1, 3), (5, 2, 1), (7, 4, 1)]:
        failures.append("the 1835 bracket dialect does not resolve: page and column are "
                        "both on the line, and a column-less `single-column` marker is "
                        "that page's column 1")
    if BRACKET_COLUMN.match("[uncertain: page 3; column 1]"):
        failures.append("the bracket column pattern matched a bracketed uncertainty note, "
                        "which would invent a column boundary inside an advertisement")

    # THE SEVENTH SHAPE, WHICH IS THE OTHER THREE (T-0298). The column rule names the SCAN
    # page, so it is resolved through the banner stating that page — asserted here with
    # the banners OUT of scan order, which is what tells the lookup apart from a
    # most-recent-banner rule that would pass on a tidy file and be wrong on a real one.
    printed = ["PRINTED PAGE 1 \u2014 SOURCE PDF PAGE 13", "--- SOURCE PDF PAGE 13, COLUMN 1 ---", "a",
               "PRINTED PAGE 2 \u2014 SOURCE PDF PAGE 14", "--- SOURCE PDF PAGE 13, COLUMN 2 ---", "b",
               "--- SOURCE PDF PAGE 14, COLUMN 1 ---", "c"]
    if column_starts(printed) != [(2, 1, 1), (5, 1, 2), (7, 2, 1)]:
        failures.append("the 1835 printed-page dialect does not resolve: a `--- SOURCE PDF "
                        "PAGE m, COLUMN k ---` rule takes its issue page from the banner "
                        "that states scan page m, not from the banner last passed")
    if column_starts(["--- SOURCE PDF PAGE 13, COLUMN 1 ---", "orphan"]):
        failures.append("a scan-page column rule with no banner naming its page was "
                        "guessed at rather than skipped")
    if BARE_PAGE_BANNER.match("PRINTED PAGE 1 \u2014 SOURCE PDF PAGE 13"):
        failures.append("the bare page banner pattern swallowed a printed-page banner, "
                        "which would resolve the issue page by ordinal instead of reading it")
    if DASH_COLUMN_HEADING.match("--- SOURCE PDF PAGE 13, COLUMN 1 ---"):
        failures.append("the 1833 dash-column heading swallowed a 1835 scan-page column "
                        "rule, which carries a page the 1833 shape does not")

    # A VENDOR'S FOR-SALE NOTICE PLACES NOTHING (T-0412), and the control beside it is
    # the whole of the rule: change one word of the role and the same corner places the
    # firm. Asserted on the compiled record, because a rule that silently changed
    # nothing would look exactly like a green run.
    def for_sale(role, claim_id="zv1", kind="building"):
        d = copy.deepcopy(base)
        c = copy.deepcopy(d["claims"][0])
        c["id"] = claim_id
        c["kind"] = kind
        c["entities"] = [{"as_printed": "P. PRUYNE", "normalized": "P. Pruyne",
                          "role": role, "occupations": []}]
        c["business"] = {"name": "Vendor Test & Co.",
                         "placement": {"class": "corner",
                                       "anchor": "Lasalle and Lake streets",
                                       "street": "Lasalle Street and Lake Street"},
                         "address_text": "the House on the corner of Lasalle and Lake"}
        d["claims"] = [c]
        with tempfile.TemporaryDirectory() as td:
            ex = Path(td) / "extracted"
            ex.mkdir()
            (ex / ("%s.json" % d["issue_id"])).write_text(
                json.dumps(d, ensure_ascii=False), encoding="utf-8")
            doc, probs = compile_gazetteer(sorted(ex.glob("*.json")), {"merges": []},
                                           corpus_doc)
        got = next((b for b in doc["businesses"] if b["name"] == "Vendor Test & Co."), None)
        return got, probs, claim_key(d["issue_id"], c)

    cases.append("a building notice signed by its vendor")
    sold, probs, sold_key = for_sale("vendor")
    if probs:
        failures.append("the vendor case did not compile clean: %r" % probs)
    elif sold is None:
        failures.append("the vendor case minted no business at all")
    elif placement_rank(sold["placement"]) > 0:
        failures.append("a vendor's for-sale notice placed the firm that signed it: %r"
                        % sold["placement"])
    elif any(placement_rank(r["placement"]) > 0 for r in sold["placement_readings"]):
        failures.append("a vendor's for-sale notice left a placing reading on the firm: %r"
                        % sold["placement_readings"])
    elif sold_key not in {c for r in sold["placement_readings"] for c in r["claims"]}:
        failures.append("the vendor printing was dropped out of the readings entirely — "
                        "it says nothing about the firm's ground, which is a silence and "
                        "not an absence")
    elif not sold.get("vendor_placements"):
        failures.append("a vendor's for-sale notice was silenced and not recorded, so "
                        "the judgement cannot be read back off the record")
    elif sold["vendor_placements"][0]["printed_placement"].get("anchor") \
            != "Lasalle and Lake streets":
        failures.append("the vendor record does not carry the corner the paper printed: %r"
                        % sold["vendor_placements"][0])

    cases.append("the same corner signed by an occupant")
    for role, kind, why in (("occupant", "building", "an occupant's building notice"),
                            ("vendor", "business", "a vendor role on a business claim")):
        cases.append(why)
        kept, probs, _ = for_sale(role, claim_id="zv2", kind=kind)
        if probs:
            failures.append("%s did not compile clean: %r" % (why, probs))
        elif kept is None or placement_rank(kept["placement"]) <= 0:
            failures.append("%s stopped placing the firm — T-0412 reaches only a "
                            "`building` claim signed by its vendor" % why)
        elif kept.get("vendor_placements"):
            failures.append("%s was recorded as a vendor notice" % why)

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
                    deposit=DEPOSIT, repo=REPO, coverage=Path(td) / "none.json",
                    quiet=True)
        if not any("hand-edited" in b for b in bad):
            failures.append("a hand-edit to gazetteer.json was not caught")
        gz.unlink()
        bad = check(extracted=ex, gazetteer=gz, identity=ip, corpus=CORPUS,
                    deposit=DEPOSIT, repo=REPO, coverage=Path(td) / "none.json",
                    quiet=True)
        if not any("is missing" in b for b in bad):
            failures.append("a missing gazetteer.json was not caught")

    if failures:
        for f in failures:
            print("FAIL: " + f, file=sys.stderr)
        return 1
    print("  ok    every gazetteer assertion fires when broken (%d cases), and all\n"
          "        seven marker dialects resolve" % len(cases))
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
