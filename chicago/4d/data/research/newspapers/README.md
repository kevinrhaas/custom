# The newspaper corpus — what is here, and how to cite out of it

`corpus.json` is the register. Eighty-six issues: **seventy-three** of the *Chicago
Democrat*, 1833-11-26 to 1835-08-26, and **thirteen** of the *Chicago American*,
1835-06-08 to 1835-08-29. The scene date sits inside both runs, and a Democrat was
printed on 1835-07-01.

Two source records carry the judgements — the traps, the owner's three rulings, the
uneven transcription quality, and what each publication may and may not be used for:

- `data/sources/chicago_democrat_1833_1835.json`
- `data/sources/chicago_american_1835.json`

`data/sources/chicago_democrat_1833_11_26.json` is the per-issue record for the first
issue and **stays senior to both** for that issue: it was verified against the page
images, and a scan read outranks a transcription read.

## Citing

A claim that cannot name its column cannot be made. Resolve the issue through
`corpus.json`, quote the transcription's uncertainty brackets as they stand, and cite:

> *Chicago Democrat*, 1835-07-01, Vol. II, No. 11, issue page 3, column 4 —
> `chicago/reference/newspapers/Transcriptions/Chicago_Democrat_1833-11_to_1835-08/Chicago_Democrat_1835-07-01_Vol2_No11_Transcription.txt`, lines 812-819.

Page and column come from the transcription's own column markers — and this file has now
been wrong about how many dialects there are **three times**. There are SEVEN, the last
two found by T-0325, and the count is now measured against every artifact in the corpus
rather than asserted. The sixty-six issues the deposit
delivered as committed `.txt` carry a RULED marker in one of three shapes:

    ===== ISSUE PAGE 4 / PDF PAGE 36 / COLUMN 5 OF 6 =====
    ===== ISSUE PAGE 4 / SOURCE PDF PAGE 36 / COLUMN 5 OF 6 =====
    ===== ISSUE PAGE 4 / ORIGINAL PDF PAGE 36 / COLUMN 5 OF 6 =====

and the twenty-three extracted here from `.docx` carry the same two facts as prose
headings, the page once and each column under it:

    Newspaper Page 1 — Source PDF Page 13
    Column 1

**AND THE WHOLE OF 1833 SPEAKS A FIFTH SHAPE, which is a third of T-0258's range.** The five
issues 1833-11-26 to 1833-12-24 separate the page from the column instead of ruling them onto
one line — a page banner, then a rule before each column:

    ===== SOURCE PDF PAGE 9 / ISSUE PAGE 1 =====      1833-12-10 .. 1833-12-24
    SOURCE PDF PAGE 1                                  1833-11-26, 1833-12-03
    --- Column 1 ---

Counted on 2026-08-28 over the thirty issues of Vol. I Nos. 1-30: **five** are dash-column,
**five** (1833-12-31 to 1834-01-28) are the prose pair, and the remaining **twenty** are
ruled. 121 column markers were invisible to the resolver, and — the same blind spot T-0289
recorded — `dev` could not tell, because the page/column assertion is skipped outright when
the text cannot be opened. The bare banner names the SCAN page and not the issue's (the
Democrat of 1833-12-03 opens at PDF page 5, because No. 1 occupies 1-4), so it is resolved
**by ordinal**: the first page banner of a transcription is issue page 1. That is the only
rule here not lifted verbatim off the line, it is a reading of the transcription's own stated
method — "assembled in printed page and column order" — and it is not used when the banner
states the issue page itself. The self-test carries a case per dialect plus three negatives.

**AND A SIXTH AND A SEVENTH SHAPE, WHICH ARE THE FIRST HALF OF 1835 — the last two, and
this is now measured rather than asserted (T-0325).** Six of the eight Democrats between
1835-01-21 and 1835-06-24 resolved to ZERO columns, so every claim citing them would have
failed the gate with *"the transcription carries no ISSUE PAGE / COLUMN marker"* and the
read of that range could not have landed at all. T-0298 had recorded three of them as
*"bare `=====` rules carrying no page or column at all"* and left open whether that was a
transcription defect. **It was not.** The rules are decoration around a page banner, and
every column carries its own rule naming the scan page:

    [Source PDF page 9; newspaper page 1; column 1]      1835-01-21, the 03-25 Extra, 05-20
    PRINTED PAGE 1 — SOURCE PDF PAGE 13                  1835-05-27, 06-04, 06-10
    --- SOURCE PDF PAGE 13, COLUMN 1 ---

46 bracket markers and 72 dash rules under 12 banners: **118 column markers invisible to a
resolver already corrected twice for exactly this.** The seventh dialect's column rule
states its own scan page, so it is resolved through the banner naming that page rather than
through the banner last passed — no ordinal, nothing counted. One bracket marker carries no
column number, `[Source PDF page 8; Extra page 4; single-column subscription prospectus]`,
and is read as that page's column 1 on the warrant of its own word and its file's header
line ("Extra pages 1–3 have 3 columns; page 4 is a single-column subscription prospectus").
That page is Calhoun's subscription list and it names people.

**Where the census now stands.** Every artifact in `corpus.json` was resolved before and
after the change on 2026-08-29: the six move, the other 83 do not. **One artifact of the
89 still resolves no column and it is not a resolver gap** — the `alternate` of 1833-11-26,
a prose reading transcription made from the page images, which segments nothing and names
its pages "SUPPLIED SCAN PAGE 1". There is no column marker in it to find, so it is not
citable at column level and a claim needing it must cite the `primary`, which is what
T-0308 read. That is a fact about the artifact, recorded here rather than left silent.

**The middle ruled shape is the majority and it was the one nobody had.** Counted across
the deposit on 2026-08-28 while reading July 1834 (T-0289): 1,176 of the 1,266 ruled column
markers say `SOURCE PDF PAGE`, 90 say the bare `PDF PAGE`, and four say `ORIGINAL PDF
PAGE`. T-0257's resolver matched only the bare form, so it could find a column marker in
NONE of the twenty-six issues of the second half of 1834. Nothing caught it because the
gate skips the page/column assertion outright when it cannot read the text, and on `dev`
it never can — a resolver that speaks no dialect and one that speaks all three are
indistinguishable on this branch. `tools/compile_gazetteer.py` now reads all four shapes
and its self-test carries a case per ruled dialect plus a negative.

**Where the deposit is not readable, run the gate against a copy of it.** `--deposit
<path>` re-roots deposit-held citations exactly as `newspaper_corpus.py` does, so a reading
pass working on `dev` can machine-check every quote it makes against the real text from
`main` before it opens its PR. `check.sh` on `dev` then counts those claims unresolved and
reports them, which is green.

## Where the text is, and why it is in two places

| | issues | text |
|---|---|---|
| the deposit carries a committed `.txt` | 66 | cited at its `chicago/reference/...` path, never copied |
| delivered as `.docx` only | 20 primaries + 3 alternates | extracted here to `text/`, and **committed** |

The deposit is the owner's archival deposit and this project reads it only. It was
committed to `main` on 2026-08-28, and for a week after that it was NOT on `dev`, where
this subtree is developed — so ten reading passes materialised a read-only copy from
`main` and machine-checked their quotes with `--check --deposit <path>`, which is why so
many `coverage.json` notes say so.

**IT IS ON `dev` NOW, and a reading pass no longer needs `--deposit` (found 2026-08-29,
T-0325).** The promotion back-merge carried `chicago/reference/` across, and every one of
the 178 recorded paths and sha256s in `corpus.json` resolves and matches on this branch —
checked file by file, not assumed. `tools/newspaper_corpus.py --check` says `deposit
present`, and the gate reassembles all 713 committed quotes here rather than counting them
unresolved. `--deposit` stays for the case it was built for: a branch or a checkout that
does not carry it. T-0275, which asks for exactly this back-merge, has not been closed and
should be looked at by whoever next reads its queue row rather than being done again.

The three states `tools/newspaper_corpus.py --check` reports are unchanged: deposit
**present** (every path resolved file by file), **absent** (reported, and green),
**partial** (always red — that state means damage).

## Quality is not uniform

The 1833, 1834 and January–July 1835 Democrat batches were reconciled against enlarged
page images with a second-reviewer pass. The August 1835 Democrat tail, the three `-2`
rebuilds and **the entire American run** are single-pass OCR. Where two runs cover one
issue the `-2` text is visibly worse; 1835-07-15 survives only as a `-2`, and
`corpus.json` says so on that entry. Weight a reading by the batch it came from —
`status`, `completeness` and `sole_witness_note` carry it.

## This is research, not payload

`tools/publish.sh` copies named subdirectories of `data/` and this is not one of them.
The gate asserts that nothing under `data/research/` has reached `site/chicago/4d/`,
so the corpus can grow without spending the published tree's size budget.

## Rebuilding

    tools/newspaper_corpus.py --build --deposit <path to Transcriptions>

Deterministic: the same deposit produces byte-identical `corpus.json` and `text/`.
`--deposit` exists because the deposit is on another branch; paths are always
*recorded* at their canonical `chicago/reference/...` home whatever `--deposit` says.

## Reading out of it — claims, and the gazetteer they compile into

`corpus.json` says where a passage IS. These say what was read out of it (T-0257).

| | |
|---|---|
| `extracted/<issue_id>.json` | one file per issue, holding `claims[]` — hand-authored |
| `identity.json` | the only place two differently-spelled names may become one person, or two firm styles one house |
| `coverage.json` | the ranges a reading pass has DECLARED it read, and the gate holds it to them |
| `gazetteer.json` | **generated** by `tools/compile_gazetteer.py --build` — never hand-edited |

    tools/compile_gazetteer.py --build       recompile the gazetteer
    tools/compile_gazetteer.py --check       the gate (in check.sh)
    tools/compile_gazetteer.py --self-test   its assertions still fire

**A declared range may not have a hole in it.** The failure a reading pass is prone to is
not a bad claim — the quote gate catches those — but a MISSING ISSUE: fourteen of fifteen
read, and nothing anywhere saying which one was skipped. Counting extraction files cannot
answer it, because the count that should have been is exactly the thing in question. So a
pass names the range it read in `coverage.json` and `--check` resolves that range against
`corpus.json` and refuses any issue inside it with no extraction file. Declaring is what
makes the assertion: an issue nobody has declared is simply not read yet and is not a
fault, and a range is only widened by the pass that widens the reading (T-0295).

**A claim quotes verbatim and normalizes beside it, never instead.** `quote` is the
transcription's own text including its uncertainty brackets; `normalized` is the reading
after OCR judgment — interleaved columns unshuffled, `rn/m`-class confusions corrected.
The gate reassembles `quote` out of the transcription line by line and refuses any claim
whose text differs by a character, so a smoothed quote fails rather than passing quietly.

**WHEN TWO PRINTINGS DISAGREE, COUNT THE PRINTINGS BEFORE YOU SEND FOR THE IMAGES
(T-0328).** A weekly's advertising is STANDING type: the same notice runs week after week,
and every week is a separate impression, separately scanned. So a disagreement between two
settings of one advertisement is rarely a two-witness problem — it is an n-witness problem
in which n has not been counted. D. Weaver's building on North Water street was read as
Lot 9 in one issue and Lot 2 in the next, and the reading pass filed a ticket for the page
images because "one of the two transcriptions is simply wrong". It ran FIVE times, from
1834-11-26 to 1834-12-24. Four of the five read Lot 2; the outlier's own line drops the t
out of `Norh`. No image was needed.

The method, and it is three greps: search the whole run for the advertiser's name, resolve
each hit's page and column, and read the settings side by side. It has now answered three
questions the ticket queue had assigned to the page images — the blacksmith's "opposite the
Tremont House" (T-0330), the axes that belonged to the ironmongers and not the booksellers,
and this lot number. **Nothing is amended to agree with anything**: every printing keeps its
own verbatim quote, the losing reading stays visible in `normalized`, and the winner is
declared in the notes with the tally that decided it.

Two cautions, both learned here. **The tally is over impressions, not over readings** — two
transcriptions of the SAME impression are one witness, and `corpus.json`'s `-2` rebuilds are
exactly that. And **a run of concordant settings does not make a scan trustworthy in
general**: the same five printings that agree on the lot number set the advertisement's copy
date as Nov. 12, Nov. 12, Nov. 13 and Nov. 19, so the digit that was decidable and the digit
that was not stood two lines apart in one column.

**Interleaving is the normal case.** The segmenter frequently alternates two physical
columns line by line, so one advertisement occupies a SUBSET of a line range with another
woven through it. `locator.lines` is the range cited; `locator.lines_of_claim` names the
lines the quote is built from, and the gate checks the subset lies inside the range.

**And it happens INSIDE a line too, which is what `locator.spans` is for (T-0261).** The
Democrat's transcriptions carry one line per printed line, so naming lines names an
advertisement. The American's do not: its densest advertising columns arrive as ONE line
of up to 11,361 characters carrying four separate advertisements and the segmenter's own
coordinate telemetry, so naming that line quotes seven other things. `spans` is the
character-level sibling of `lines_of_claim` — a list of `{line, from, to}` half-open
ranges — and when it is present the quote is those ranges joined by a newline instead of
those whole lines. Every range is still verbatim and still rebuilt from the file by the
gate; only the grain is finer. It is optional and additive: a claim without `spans`
behaves exactly as before, which is why the T-0257 fixture and the Democrat read needed no
edit. All 130 of the American's claims use it.

**Nor does the Democrat's own first issue, and SIX of T-0258's thirty do.** This count
has been corrected twice by reading — the two paragraphs below are the corrections, and
each names the sweep it refuted — and it stands at six issues carrying Chicago's own list:
**1834-01-14** and **1834-01-28** (the 1 January list, printed cut and then nearly whole,
T-0310), **1834-02-04**, **1834-03-04** (T-0312), and **1834-04-01** with its
**1834-04-08** reprint (the 1 April list, T-0313). The other twenty-four carry none of
Chicago's — the April Hennepin printings are another town's and mint nobody — so a reading
pass over 1833 and the first half of 1834 meets the epic's letter-list clause mostly by
demonstrating absence. Where a list IS there it is the census proxy and ruling 1 applies
in full.

**The fifth was found by READING and not by searching, and that is the lesson (T-0312).**
This file said four until March 1834 was read through, because a text sweep cannot match a
heading the segmenter has cut in half. The list of 1834-03-04 sits on page 4, and the crop
boundary runs down the middle of its printed column: `List of L` stands at the head of
column 2 and `etters` / `ost-Offiee at Chica-` / `34.` at the head of column 3. No search
for *list of letters*, *letters remaining* or *remaining in the post office* can hit a
heading that exists whole in neither column. **So sweep for the FRAGMENTS too** — `ist of L`,
`etters`, `ost-Off`, `advertis` — and expect a list to be split across two claims, one per
crop, the way `chicago_democrat_1834_03_04.json` c024 and c025 carry it. Its date line
survives only as `34.`, so WHICH return it is cannot be read and is not asserted; its
seventy-eight extracted names are a floor, cut on their left edge where January's were cut
on their right.

**THAT SWEEP WAS WRONG, AND READING APRIL 1834 IS HOW IT WAS FOUND OUT (T-0313).** It is
six of the thirty, not four, and the two it names for April are the wrong two. **1834-04-23
and 1834-04-30 carry the HENNEPIN list**, not Chicago's — as does 1834-04-16, which the sweep
missed as well — and out-of-county lists mint nobody here (T-0290, T-0292). Chicago's own
list of letters remaining on **1 April 1834**, over J. S. C. Hogan's signature, is printed
twice, in **1834-04-01** and **1834-04-08**, in the two issues the sweep passed over. The
reason a keyword sweep cannot find it is the reason a keyword sweep cannot be trusted on this
deposit: on 1834-04-01 the heading reads `SQA AINIG init` — that is `REMAINING` — and the
words *List of Letters* stand in the NEXT segmenter column, over the list's second half. So
every form of the heading this file lists was searched for, and every one of them returned
Hennepin. **Sweep for a list by reading the columns of the issues in the range, not by
searching them**; the eight issues of 1835 that only the deposit can open (T-0298) have never
been swept any other way.

**The Chicago American carries no post-office letter list.** Searched across all thirteen
issues for every form the Democrat uses — *list of letters*, *letters remaining*,
*remaining in the post office*, *uncalled for*, a signature ending *P. M.* — for exactly
one hit, and it is a list of State Bank of Illinois officers reprinted from the *Sangamon
Journal* (1835-06-27). The American's post-office notices are its hours and rules, signed
by the postmaster J. S. C. Hogan, and are extracted as `infrastructure`. The epic's
letter-list ruling has nothing to bite on in this paper; the census proxy is the
Democrat's.

**Nor does the Democrat carry one every month.** July 1834 (T-0289) and September 1834 (T-0291) were both swept for every form of the heading — *list of letters*, *letters remaining*, *remaining in the post office*, *uncalled for*, a signature ending *P. M.*, and the bare words *letter*, *postmaster* and *list* — and September's four issues carry none. The month's post-office matter is a reprinted Senate report, a Cumberland postmaster's letter about mail robbers, the Postmaster General's own Chicago-to-Green-Bay proposals (extracted as `infrastructure`) and a want-advertisement routing replies through the office. So the letter-list ruling has nothing to bite on there either, and `coverage.json` records the sweep rather than the silence — an absence a pass has looked for is evidence, an absence nobody looked for is a hole.

**`[…]` marks absence, `[word]` marks a supply.** Text the column edge cut away is a gap,
not an invitation. The worked fixture leaves *'a few doors below'* unsupplied for exactly
that reason and says where a fuller witness might be found.

**The owner's three rulings live in fields, not in prose.** `letter_list_only` on a person
(a listed name mints a resident candidate, and the weaker evidence stays distinguishable);
`reading` required on every claim (`transcription_mediated`, or `scan_verified` where a
scan was read and outranks it); and `built_at_scene_date` / `survival_liberty_required`
computed on a business — documented businesses stand in the 1835 town unless a claim
contradicts them, and one last seen before 1835 stands on a stated liberty.

**Identity never coalesces by accident.** The gazetteer is keyed on the whole normalized
name, so `Cohen, P.` and `Cohen, J.` are two people. A merge is declared in
`identity.json` with a `merge_rule` naming both spellings; same surname with different
initials never merges, rule or no rule.

**The first bulk merge pass is T-0299**: the list of letters remaining in the Post Office at
Chicago on 1 July 1834, which the Democrat printed three times — 1834-07-02, 1834-07-09 and
1834-07-16 — and which the segmenter cut differently each time, so 298 names had been
minting up to three people apiece. The three readings are aligned BY POSITION, because the
list is one ordered sequence that every printing carries in the same order; a pair is a
candidate only where the alignment puts the two readings at the same entry, never on
resemblance alone. **175 merges declared and 29 REFUSED**, the refusals recorded in
`refused_merges` beside them with the surname the two share and the initials that separate
them — the refusals are the evidence that the pass was a judgement and not a
de-duplication. The gazetteer went from 2,108 persons to 1,933. The file's `passes` block
states the method, the canonical-reading rule, and the two returns printed in the same
issues that are deliberately NOT part of this list (Plainfield and Juliet). Seventeen of
the twenty-nine refusals are an initial one printing could not read against the same
initial another prints whole. **Whether such a pair may merge is NOT settled here**: it is a
change to the identity policy and it is the owner's, and T-0392 carries the question with
both answers and their costs — no keeps eighteen duplicate persons the project's own best
witness resolves, yes needs a bound (same list, same entry, no competing letter).

`surname()` and `initials()` take the transcription's markup off before they parse (T-0299).
They did not, so `A[n]drew W. Borland` read as four forenames and `Benjamın Swena` as two,
and whether the policy protected a pair came down to which side of a name a bracket fell on.
The policy is unchanged; ten self-test cases hold both halves of that.

**AN UNREAD `[?]` IS A POSITION, NOT AN ABSENCE (T-0391).** Taking the markup off is right
for a surname and was wrong for a forename, because DELETING the `[?]` hands the initial to
whatever letter stood behind it. All seventeen `[?]` refusals above had been stated on such
a reading: seven named a letter invented from the rest of the forename (`[?]rah Fowler` as
`R.`, `[?]nn M. Gooding` as `N. M.`, `[?]saac Scarrett` as `S.`), six collapsed a middle
initial into first position (`[?]. M. Fish` as `M.` against `E. M. Fish`'s `E. M.`), and
four read no initial at all — which is the shape all seventeen were assumed to have. So a
committed record was asserting letters no printing carried. `initials()` now records the
marker as UNREAD, in the slot it was printed in, welded to the word it opens, and UNREAD is
equal to no letter; every `refused_because` states the reading the page carries and each
refusal carries its parsed `initials_read`. **Nothing merged or unmerged** — 177 declared
person merges and 29 refusals before and after, 2,634 persons either way, and `gazetteer.json`
and `register_1835.json` are byte-identical across the change. Nine self-test cases assert
the VALUE and not merely that a pair differs, which is what let `[?]nn M. Gooding` pass while
reading `N. M.`

**AND THE RULE HAS NO SIBLING FOR FIRMS, WHICH IS WHY ONE BOOKSHOP STANDS IN THREE PLACES.**
The Chicago Democrat's bookseller is `RUISAL & CLUPR,` in the December 1834 advertisement's
only legible heading, and T-0327 read the name off the firm's OTHER advertisement rather
than off that line: the copartnership notice dated `Chicago, Aug. 26, 1834` — Aaron
Russell of Boston and [—] Clift of Philadelphia, opening a store adjoining P. Carpenter's
drug establishment in Water-street — runs from 1834-08-27 to 1834-11-12 and is signed
legibly four times, `RUSSELL & CLIFT`. So the December claim's business name is now a
supply, `[RUSSELL & CLIFT]`, and the compiler folds it into `business_russell_clift` by
key, which is a corrected READING and not a merge. What the key cannot fold is the rest:
`business_chicago_wholesale_and_retail_book_stationary_store` is the 1834-08-27 printing of
that same notice, whose signature went with the woven half of the column, and
`business_russell_clift_chicago_book_and_stationary_store` is the firm's own 1835 card in
the *American*. Three keys, one house, and the evidence for it is a shared copy date and a
shared body of type — but joining them means DECLARING two names one firm, and that is
exactly what `identity.json` supplies for people and, as of T-0304, for firms as well:
`firm_merges`, below. The three keys stand apart until somebody declares them, because a
declaration cites its printings and nobody has yet written that one down (T-0337) — but the
place to write it now exists, and the alternative it replaces was a hand-merge, which makes
a gazetteer nobody can recompile.

**Firms have the same policy and a different discriminator** (T-0304). A business is keyed
on its whole name too, so five printings of one house are five businesses until something
says otherwise, and `firm_merges` is where that is said — same two rules, a `merge_rule`
naming both spellings verbatim. What changes is the guard. For a person a differing
forename initial is fatal, because the letter lists are full of families; a `& Co.` style
routinely elides or misprints the forename it trades under, so applying that rule to firms
would refuse every merge a firm needs. What survives is the SURNAME: the two styles must
carry the same set of partner surnames, with or without a rule, because a partnership is
its partners and a changed one is a different house — which is what keeps `Clark, Filer &
Co.` and `A. Filer & Co.` apart. The second guard is about the ground rather than the
name: two styles the papers put in different STREETS never merge, because a firm that
moved is documented by a removal notice, and a removal notice is a claim. A merge takes
the union of mentions, proprietors, goods and copy dates, the wider issue window, the
more specific placement, and every trade either side printed in `trade_variants` — it can
widen a record and it cannot narrow one.

The scene-date Democrat, `extracted/chicago_democrat_1835_07_01.json`, is both the worked
fixture (claims c001-c003, T-0257 — Peter Cohen and J. S. C. Hogan on South Water Street,
and one letter-list name) and the first issue read through (c004-c021, T-0295).

**And `extracted/chicago_democrat_1833_11_26.json` is the one issue where the scan outranks
the transcription in practice rather than in principle** (T-0308, the first piece of T-0258).
Vol. I No. 1 is the only issue in the corpus with a per-issue source record read off the page
images, `data/sources/chicago_democrat_1833_11_26.json`, and six of its thirty-three claims
carry `reading: scan_verified` because the record supplies type the transcription lost — the
schooner's master, the tavern keeper, Philo Carpenter's name, Kimball's address, Goss & Cobb's
address, the imprint. One claim runs the other way and is worth as much: the record warns that
*a* transcription of this issue read "C. & L. Harmon" for "C. & I. HARMON", and the deposit
transcription read here has the I, so the warning now attaches to a named artefact instead of
to transcriptions generally. Two advertisers the record does not enumerate — C. H. Chapman and
S. Foot — are added by the transcription pass, and three traps the record quarantines are
claimed by neither: the stock engraving over "Two Buildings to Let", the pencilled "S. W." in
the margin beside the imprint, and the estray notices, which are county filings from Du Page
and Walker's Grove and not Chicago.

**It is read from the deposit `primary`, not from the `-2` rebuild `dev` can open**, and
the reason is the letter list: the primary sets it legibly at name level and the alternate
does not. So its quotes are verified with

    tools/compile_gazetteer.py --check --deposit <a materialised deposit>

and the committed gate on `dev` reports them unresolved-but-green until T-0275 lands. The
segmenter cut each printed column in half and alternates the halves line by line, so nearly
every claim there is `interleaved`, and most bracketed supplies are read off the OTHER half
of the same printed lines — each claim's note names the lines they came from.

## `register_1835.json` — the work list (T-0262)

`gazetteer.json` is an index of what was PRINTED. It says nothing about what the model
should build. `tools/compile_register.py --build` turns it into the register the seeding
tickets read: for every business, whether it stood on 1 July 1835 and what the town has to
do about it; for every person, whether the town already holds them.

    tools/compile_register.py --build       recompile register_1835.json
    tools/compile_register.py --check       the gate (check.sh runs it)
    tools/compile_register.py --self-test   the gate's assertions still fire

**It is DERIVED, and the gate refuses a hand-edit** — the same contract `gazetteer.json` is
under, for the same reason: a hand-edited register is a place to promote a business into the
town without an argument, and T-0263 and T-0264 read it as if it were derived. Its inputs are
the gazetteer, `data/structures/`, `data/streets/1835.json` and `data/residents/`; change
those, not this.

**Four business actions.** `enrich_existing` — a committed building already carries this
house, and the row names the field it matched on and the exact text. `new_building` — nothing
committed carries it and the paper's own placement resolves: a corner of two platted streets,
a landmark that is a committed structure, or ONE hop through another documented business that
is. `street_only` — a platted street face and nothing narrower. `unplaceable` — no street the
model holds.

**Three person actions.** `enrich` (already in `data/residents/`, matched under the
gazetteer's own identity policy, imported so the two tools cannot drift), `replace_invented`
(a documented person of a trade the town invented a household for) and `new_resident`
(everybody else — owner ruling 1, a letter-list name is enough).

**Two exclusions, and the second is a proxy that says so.** A contradiction dated ON OR
BEFORE the scene date excludes; a LATER one is recorded (`dissolved_after_scene_date`) and
disobeyed, because a firm dissolved in August 1835 was demonstrably open in July. The second
is `first_evidence_after_scene_date`: T-0262 asked to exclude on an `announces_opening` field
the claim vocabulary does not have, and this is the derivable question that comes closest.
T-0356 is the field.
