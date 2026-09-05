# T-0509 resident-research handoff — cohort 14 of 79

Frozen manifest: `chicago/4d/data/research/residents/pass_14_76_cohort.json` (76 people, not 79 —
T-0492 split the 228 remaining named residents 76/76/76 and the ticket's title kept the older number).

Reviewed **2026-09-05: 76/76 complete, 0 pending** — 18 corroborated, 11 corroborated in a later
volume only, 8 candidate identities retained unasserted, 39 documented no-corroboration outcomes.

## Artifacts

- `T-0509_resident_research.csv` — machine-readable export, one row per manifest person.
- `T-0509_resident_research_working.xlsx` — Residents, Candidates, Sources and Search_Log sheets.
- `sweep/` — the five stages that produced them, in order, with their own README.
- `chicago/4d/data/research/residents/pass_14_findings.json` — the authoritative outcome ledger.

## Method

The T-0510 method, unchanged. Exact name first, then justified initial and OCR variants, across: the
committed Chicago Democrat and Chicago American transcriptions and the newspaper identity ledger; the
town's 1833 tax list and its 1834 and 1835 poll lists (IRAD); the Illinois public-domain land tract
sales; the 1830 census of the Chicago precinct; the 1840 census heads; the St Cyr and St Mary
registers; Fergus 1839, Fergus 1843 and Norris 1844; **Fergus's Historical Series 26-29**; the Calumet
Club old-settler rolls; the Newberry genealogical index cards; and the Genealogy Trails transcriptions.

**Where the repository already holds a crosswalk verdict for a name, that verdict is quoted rather
than re-decided.** Thirteen earlier passes and the domain crosswalks have adjudicated most of these
surnames already, and re-deciding them from scratch would produce a second, unreconciled opinion.
What this pass adds on top is a **directed reading of Fergus 26-29 against all 76 names** — the 1843
Chicago Directory, its advertising pages, its fire-department and civic rolls, and Wentworth's
obituary lists — which the directory claim ledgers do not cover.

## The outcome rule

| outcome | means |
|---|---|
| `corroborated` | an agreement, forename for forename or initial for initial, with an independent source written **at or before** the scene year |
| `corroborated_enrichment` | the same agreement, but only in a volume printed **after** 1835: it enriches the biography and adds no 1835 attestation |
| `candidate_identity` | a plausible external identity with no date, place, occupation or kinship discriminator bridging it to the 1835 person |
| `no_corroboration` | the post-office lists and a documented refusal — a negative search, not evidence of absence |

## Where a later reading is written, and why it is not promoted

`tools/synthesize_resident_research.py` promotes canonical facts (occupation, arrival year, birth
year, family evidence) out of a completed row's `proposed_facts`, `evidence_for` and `summary`. So
this pass puts **contemporary** evidence in those fields and every **post-1835** volume reading in
`notes`, which the synthesizer does not read. Back-projecting a trade or an age across eight years is
T-0514/T-0515's decision under the ratified ladder, not this pass's, and the split is mechanical
rather than promised.

## What Fergus 26-29 gave up

Fourteen readings the directory claim ledgers do not hold, quoted as printed and recorded in each
person's `notes`. **Seven of them resolve an initial to a full given name**, which is what this
programme is short of:

- **E. L. Thrall** — "Thrall, E, L,, clerk, Charles Walker & Co." A man the corpus otherwise holds
  only as an initialled letter-list name now has a trade and an employer.
- **H. B. Clarke** is *Henry B. Clarke*, farmer, "Michigan ave, n.-e. cor 16th Street". The bracketed
  death year OCRs as **1840**, which a directory of 1843 could not have listed him alive for; the
  digit is recorded as printed and **not corrected**.
- **J. H. Collins** is *James H. Collins*, attorney of Butterfield & Collins, 15 Lake — "died,
  Ottawa, Ill., July 14, 1854, aged 50", so born about 1804.
- **Chas. H. Chapman** is *Charles H. Chapman*, "res Wells, bet Randolph and Washington", with Henry
  Chapman the tobacconist boarding in his house — an address **and** a household relation.
- **Richard J. Hamilton** is *Richard Jones Hamilton*, of Hamilton & Chamberlin, res 264 Michigan.
- **Stephen F. Gale** is *Stephen Francis Gale* of S. F. Gale & Co., 108 Dearborn, and the same
  volume's fire-department roll makes him First Assistant Engineer.
- **Dr William B. Egan** is printed "Egan, Wm. Bradshaw, physician, recorder, etc., 68 Clark".

**The address the owner's instruction asked for.** `harmon_charles_l` is carried by **two independent
printings in one volume**: the directory line "Harmon, Charles Loomis, dry goods and groceries, 145
South Water, s.-w. cor Clark, res Dearborn, bet Washington and Madison [died November 2, 1868, aged
59-4" and his own advertisement, "C. L. HARMON, commission merchant and wholesale grocer, corner
South-Water and Clark streets". A street number, a corner, a residence street and a birth date to
the month — a documented later address for a business the 1835 layer cannot place.

**The reading that settles a split this project already made.** The obituary list carries both
Elijah Wentworths on consecutive lines — "Wentworth, Elijah, died, St. Jo., Mich., Nov., 1863, aged
87" and "Wentworth, jr., Elijah, died, Galesburg, Ill., November 18, 1875, aged 72" — distinguishing
senior from junior exactly as this project's two person records do. That is an independent printing
of the *split*, not merely of the name; the senior was about fifty-nine at the scene date.

Also **Bennet Bailey**, carpenter, Dearborn, boarding with John Gray, dead 7 November 1881 at
70-11-7, so born about December 1810; **Daniel Elston**, "patent press brick maker, res North
Branch", where the repository already puts his brickyard; and **George Washington Dole** of "Newberry
& D.", alderman of the 6th ward — which names the firm and **still does not say which Newberry stood
in it**, the question T-0396 holds open.

Two readings were **truncated or empty and are recorded as such**: the obituary list's "King, By ram,
died" runs straight into the next name, so no date, place or age survives — the unusual forename is
the whole of the reading; and "Moore, Henry, died. Concord, Mass., after 1841, aged —" dates a death
only as *after 1841*, on one of the corpus's commonest name shapes.

## What it refused, and why the refusals matter

Two candidates were minted rather than merged. **J. Curtiss** has *two* rivals in one volume — James
Curtiss the State's attorney and ninth mayor, and J. W. Curtiss the gunsmith — and an 1835 record
carrying the initial alone cannot choose between an attorney and a gunsmith. **H. Crocker**'s only
initial-agreeing entry is Hans Crocker the lawyer, whose printed age puts birth about 1816: nineteen
at the scene date, and in Milwaukee thereafter.

Ten refusals are written down with the discriminator that decided them, because a documented negative
is the product here as much as a hit is. Four of them are **false positives a raw surname sweep
produces and a reading destroys**: every apparent `cook_rowland_i` hit is the *county* — "Dunlap of
Cook"; every `house_chester` hit is the building word — "Temperance House", "Tremont House"; every
`lewis_samuel` hit is the *forename* Lewis; and `clark_erastus` returns 115 apparent surname hits
without one "Erastus Clark", the forename appearing in the volume only behind Bowen and Williams.
The rest are initial-pair refusals — the volume prints Abel, Henry and Samuel Curtis Bennett and no
H. C.; J. S. and Luke Comstock and no H. H.; Samuel W. Goss and no O.; George M. Bostwick and no
E. B.; E. A., Ephraim T. and Hart L. Stewart and no R. — plus **Mrs. H. Sherman**, who carries no
forename at all and so cannot be tested against any of the five Shermans the volume prints.

## Limits

Candidate identities stay unasserted and surname similarity is a clue, never a resolution. Negative
searches are documented negatives, not proof of nonexistence. FamilySearch and Ancestry are
login-walled and are recorded as inaccessible rather than absent; HathiTrust page views return 403.
Nothing here changes a grade **by hand**. The grade movement in this PR is the synthesizer's own
mechanical consequence, at `tools/synthesize_resident_research.py:528`, of a letter-list person
having been reviewed — nine `inferred → attested`, **all nine inside this cohort and none outside
it**, which is the programme's design and what the thirteen earlier cohorts also did.

Cumulative reviewed total after T-0509: **873**. `letter_list_missing_research_row` was already
**0** when this branch was cut, so the measurable movement here is the 76 people who leave
`no_corroboration_yet` (558 → 482) for an adjudicated outcome.
