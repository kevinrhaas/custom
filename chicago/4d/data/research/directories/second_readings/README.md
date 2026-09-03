# Second readings — directories

A page or a volume read INDEPENDENTLY of the reading committed in `../claims/`, kept whole so
that a disagreement between two readings of one printed book is a thing that can be examined
rather than a thing that was lost when the second PR merged. The idiom is
`../../census_1840/second_readings/`, and the rule is the same here: **nothing in this directory
is downstream of anything.** No record, claim, crosswalk or layer reads it. `../coverage.json`
declares that the check was made and this README says what it found.

A file here is superseded, not corrected. When a reconciliation lands in `../claims/`, say so
there and leave the comparison as it was made.

| file | what was read twice | by | committed reading | disagreement |
|---|---|---|---|---|
| `norris_1844_genealogytrails.json` | Norris's *General Directory ... of the City of Chicago for the Year 1844*, the directory proper and its addenda | Kim Torp for genealogytrails.com, published 2002, from a different copy | T-0566, PR #704, off the Internet Archive scan `generaldirectory19norr` | 2,065 of 2,073 entries matched; 1,190 identical, 808 agree, 67 differ, 8 in the archive reading alone and 5 in Kim Torp's alone |

---

## Norris 1844 against the Genealogy Trails transcription

**Read for T-0576** (piece 6 of 6 of the owner's T-0556), by
`tools/compare_norris_1844_readings.py --build`, which has a `--check` that rebuilds and
compares. It is a COMPARISON and not an import: it prefers neither reading, deletes nothing,
and writes no entry into `../claims/`.

**Why the second reading is worth a run.** These are two independent transcriptions of one
printed book, made by different hands from different copies — one machine (archive.org's OCR
of the University of Illinois scan of the 1903 Bohan republication), one human (typed from the
page, with the transcriber's own note that she kept spellings "as is", added the occasional
comma, and marked what she could not read with `(sic)` or `(?)`). Where two such readings
disagree is where the hard-to-read names live, and those are exactly the surnames a
reconstruction gets wrong.

**How they were matched.** Normalise (lowercase, `&` written out, everything outside `a-z 0-9`
and space dropped, spaces collapsed) and take the best `difflib` ratio, greedily and one to
one: pass 1 inside a block on the first three letters of the leading token, pass 2 sweeping
what is left against everything still unmatched — which is what recovers `ISickalls` for
Nickalls — and pass 3 pairing an entry left unmatched on each side when their first three
normalised tokens are the same string AND each is the only one left with that prefix. Pass 3
is what recovers the entries the archive OCR reduced to ditto marks: `Hough, R. M. " "`
against `Hough, R.M., res P. Kelsey's`. Requiring uniqueness on both sides is what keeps two
men of one name apart.

**Five wrapped lines.** The web page turns five long entries onto a second line, and in this
cache every one of those tails is the bare word `sts`. A line that does not begin with a
capital letter is joined back onto the entry above and the entry keeps both line numbers;
there is no other line in either page that begins lowercase.

**THE MATCH RATE IS 2,065 of 2,073 — 99.61%** of the archive reading, and 99.76% of Kim
Torp's 2,070. The addenda count agrees exactly: **117 in both**. Of the 2,065 matched pairs,
**1,190 are identical** once punctuation and case are set aside, **808 agree** at a ratio of
0.90 or better and **67 differ** below it.

**What the 808 "agree" pairs mostly are is abbreviation, not doubt.** Norris's compositor set
`street` in full where the Genealogy Trails page has `st`, `between` where it has `b` or
`bet`, `and` where it has `&`; and the archive scan carries a trailing `(See card)` — the
directory's own pointer at the advertising section — that Kim Torp did not transcribe. None of
that is a disagreement about who anybody was.

**The 67 that differ are where the reading is actually at risk**, and they divide three ways.
Most are OCR damage the human transcription repairs and this file now dates and names:
`Buticifit'ld` is Butterfield, `(JrisivoM` is Griswold, `Gilmorc. Win.` is Gilmore, Wm.,
`TJarnes` is Barnes, `Bolsford, 1.` is Botsford — and Kim Torp reads that last one
`Botsford, I. (or L.?)`, which is the honest answer to a letter neither reading can settle.
Some are a real difference of substance: the archive reads Isaac Cook at `corner of Franklin
and Randolph sts` and Kim Torp `corner of Franklin & Randolph & Washington sts`; the archive
reads James Fennerty at `Lake st. res Dearborn st` and Kim Torp at `100 Lake st`. And a
handful are places one reading lost text the other holds — `Adams, R. E. W, physician, corner
of Clark and Lake streets,-` breaks off where the other reading continues `house Clark st`.
**Neither is preferred. Both stand, verbatim, in the file.**

**The eight entries only the archive reading has**, and they are three different things.

*Two are OCR wreckage of a line Kim Torp prints plainly.* `Kobl>, Thus. P.` is her `Robb, Thos.
P., res J.B. Mitchell's` — the surname is damaged past the point where any rule here can pair
them, and it is left unpaired rather than paired by hand. `. -house Clark street (See card)` is
the tail of an entry whose head the scan lost. A third, `Bir/.zard. S. laborer, at S.
Jackson's`, is a surname NEITHER reading recovers: her page has no such entry at all.

*Five are entries her transcription does not carry.* `Cook, John, tailor, res Jefferson st.`;
`Dow, J. I. & Co. painters` (she has the man, `Dow, John I. of J.I. Dow & Co.`, and not the
firm's own line); `Jones, D. A. of D. A. & E. M. Jones` (she has the firm, `Jones, D.A. & E.M.,
chair and cabinet manufactory`, and not the partner's); `Taylor, Charles H. currier, at
Johonnett, Wells, & Co.'s` (she has the OTHER Taylor, Charles the merchant tailor, one line
above it in the book); and `Woodbury, A. J. clerk, at Bristol & Porter's house Monroe at`.

*And that last one leads to the sharpest disagreement in the file.* Directly beneath it the
archive scan reads `"Woodbnry. Hiram, clerk, at T. W. Salisbury's` where Kim Torp reads
`Woodbury, A.J., clerk, at T.W. Salisbury's`. Everything after the name agrees word for word;
the GIVEN NAME does not, and one of the two readings has taken the initials from the entry
above. That is a person the reconstruction would get wrong, found by the only method that can
find it.

**The five only Kim Torp has are all explained, and two of them are her page doubling
itself.** `Buchanan, Nelson` and `Buckley, Noah` are set twice within four lines of each
other, and `McHale, John` twice within two — and **the two copies do not agree**: one Buckley
is at `corner Lake & Wells sts` and the other at `corner Randolph & Wells st`, which is what
the archive reading has. The remaining line, `Nelson, Andrew, laborer, house N. Water at near
Franklin`, is not missing from the book at all: the archive OCR ran it onto the end of the
Myers entry above it, so `Myers, Peter, laborer, h Chicago avenue, Dutch Settlement. , Andrew,
laborer, house N. Water st near Franklin` is TWO entries in one claim. **That is a defect in
the committed reading that only a second reading could have found**, and it is written here
rather than fixed here, because `../claims/norris_1844_directory_entries.json` is generated and
a repair to it is a pass of its own.

**Near-duplicates within one reading are reported and never removed**, both sides, under
`near_duplicates_within_archive` and `near_duplicates_within_genealogytrails`. Four in Kim
Torp's page (the three doublings above, plus one that is not a doubling) and one in the
archive's. The one that is not: `Johnson, J. & A.` the grocers on Dearborn street and
`Johnson, J. & Co.` the barbers on Clark street are two different firms, they are in both
readings, and they are here only because they share their first three normalised tokens. The
section is a list of candidates for a human, not a verdict.

**Neither reading is scan-verified.** Both are `transcription_mediated` — one through a
machine, one through a typist — and where they disagree the printed page has not been
consulted. Settling one of these 67 needs the image, and this file is what tells a later run
which 67 lines are worth fetching it for.
