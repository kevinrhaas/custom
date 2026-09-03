# Directories — entry by entry, structured, and crosswalked

**What lives here.** The 1839 Chicago directory, which this project cites today
from a web transcription and has never extracted, and its successors (T-0506).

**Shape: `claims`.** A directory reads like a list and is filed as claims for one
reason: the repository holds it as PROSE — a page of running text this project
commits and quotes from — and the verbatim gate binds any domain whose text is
committed here. A structured entry is then the claim's `normalized` reading, with
the printed line in `quote`, unedited, and `kind: person` or `kind: business`
according to what the entry is.

**A directory entry is three facts at once:** a name, a trade and an address. Keep
all three in `normalized`, keep the printed line whole in `quote`, and let the
crosswalk decide whether the name is a person this project already holds.

**1839 IS FOUR YEARS LATE.** The town in this reconstruction is the town of 1 July
1835. A directory of 1839 is evidence about 1839, and an address in it is not an
1835 address. Where it corroborates a person, say so in the crosswalk with the
rule written out; where it supplies a place, it supplies a 1839 place.

**Not a second-hand citation.** The current citation is to somebody else's
transcription of the directory. A reading made through that is
`transcription_mediated`; a reading made off the page image is `scan_verified` and
outranks it. Say which.

**Hand-authored:** `claims/`, `text/`, `coverage.json`, `crosswalk.json`.
**Generated:** nothing here yet; `data/research/domains.json` is, and is gated.

**Coverage.** Declare the PAGES read. A directory is finite and countable, which
makes an undeclared page an honest "not yet" and a declared empty one a fault.

**This is research, not payload.** Nothing under `data/research/` reaches
`site/chicago/4d/`.

---

## Norris's *General Directory ... of the City of Chicago for the Year 1844*

**Read for T-0566** (piece 1 of the owner's T-0555). The first Chicago directory,
and the largest single list of named Chicagoans this project has touched: **2,073
entries** off printed pages 21-65, of which 117 are the ADDENDA Norris set at the
back for "names accidentally omitted above."

**Which copy, and why not the owner's.** He named HathiTrust `chi.56111136`. That
copy sits behind a Cloudflare challenge no runner here can pass — the plain-text
view, the `ssd` reader and `imgsrv` all answer 403 with a challenge page. The
volume was read instead from the University of Illinois scan of the T. F. Bohan
republication of 1903, Internet Archive `generaldirectory19norr`, which is the
same 1844 text and is full-view public domain. That substitution is in the source
record, not only here.

**The structure is the indent.** Norris sets every entry flush left and turns the
long ones in about half an inch. `text/norris_1844_leaf_NNN.txt` keeps that: a
turned line carries two leading spaces, computed from the word coordinates of the
scan (`_djvu.xml`), and a line is judged turned when it starts more than 45/400 of
an inch right of the page's own margin — the MODE of that page's line starts, not
the minimum, because a speck in the gutter is one line and the body is fifty. On
leaves 40, 46 and 61 the speck is far enough left that a minimum would have made
the whole page look turned. Entry boundaries therefore survive the trip from image
to text and can be checked by eye against the page.

**What is generated here.** `claims/norris_1844_directory_entries.json` by
`tools/read_norris_1844.py --build`, and `norris_1844_crosswalk_1835.json` by
`tools/crosswalk_norris_1844.py`. Both have a `--check` that rebuilds and compares,
so a hand-edit is caught. The page text under `text/` is committed, hand-authored
in the sense that nothing regenerates it here, and is what the verbatim gate reads.

**The reading is `transcription_mediated`, all 2,073 of them.** This is
archive.org's OCR, machine-read and not checked against the image by eye. The
damage is left in every quote on purpose — `Win.` for `Wm.`, `ISickalls` for
`Nickalls`, `wi<jmaker` for `wigmaker` — because a tidied quote cannot be found
again. The repair, where one is safe, is in `normalized`, and `normalized` is best
effort: the split of one printed line into name / occupation / address is a
heuristic over inconsistent nineteenth-century punctuation, `as_printed` carries
the whole line, and the quote carries it unedited. Firm detection is the weakest
part of it — `Frink, Walker, & Co.` reads as a person because the comma falls
before the ampersand — and 65 entries are graded `kind: business` where the true
number is higher. T-0568 reads the Advertising Directory and will correct the
business side from the cards.

**1844 IS NINE YEARS LATE, and this is the whole discipline of the file.** Every
claim carries `describes_date: "1844"`. Nothing here is an 1835 fact. The one place
a name in this volume touches a person standing in the scene of 1 July 1835 is
`norris_1844_crosswalk_1835.json`, and it touches them as corroboration and as a
CANDIDATE enrichment: **48** of the 847 people in the residents layer meet exactly
one 1844 entry on the rule, **15** meet more than one and are left ambiguous, **4**
are contested — two 1835 people meeting the same 1844 line, at most one of whom is
the man printed — and **171** have their surname in the book under a different
initial and are refused outright, because a surname-only agreement is always a
refusal and Norris lists eleven Smiths. That file **changes no resident record**:
under the ratified ladder an 1844 listing alone never makes an 1835 resident, and
T-0569 is the ticket that spends the reading on the layers.

**What was not read** is named in `coverage.json`: the 1903 front matter, the
Description and Historical Sketch (T-0567), the Statistical Account (T-0567), the
Advertising Directory (T-0568) and Norris's own General Intelligence Agency card at
the foot of printed page 65. All of it is committed as page text, so those tickets
start from the text rather than from the network.
