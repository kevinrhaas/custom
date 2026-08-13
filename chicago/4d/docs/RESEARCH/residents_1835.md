# The inferred-residents programme, phase one: the documented population

**Roadmap:** `docs/ROADMAP.md` § K1 · **Data:** `data/residents/` ·
**Gate:** `check_residents` in `tools/validate.py`, tested in `tools/test_validate.py` ·
**Scene date:** 1835-07-01

---

## 1. What this layer is for

Chicago went from about 350 people in 1833 to **3,265 in the town census of 1835**
(Andreas vol. 1, printed p. 180, archive.org scan p. 377). The same census counts **398
dwellings**. This dataset models 184 structures, of which 108 are anonymous inferred infill.

The programme's argument is that the two numbers are the same problem seen from opposite
ends: *the population is what justifies the buildings*. A household that needs a dwelling
eventually becomes a structure record on the plat, archetyped, baked and confidence-graded.
So the order of work is people first, then houses — and phase one, this one, is the
**documented and derived** layer that the inferred layer will later be reasoned from.

**No human figures are drawn.** `docs/LIBERTIES.md` L1 and AGENTS.md stand: v1 ships an empty,
accurate town. This is a dataset layer feeding structures and the evidence panel.

## 2. The schema, and the one thing about it that is easy to get wrong

`data/residents/index.json` is the manifest (a static host cannot be globbed) and
`data/residents/households/*.json` is one file per household. The shape mirrors
`data/flora/` and `data/fauna/`: denormalised copies in the manifest, the record
authoritative, the validator failing the build on drift.

**There are two orthogonal grading axes and they must not be conflated.**

| axis | key | vocabulary | what it grades |
|---|---|---|---|
| evidence | `confidence` | `documented` / `inferred` / `conjectural` | an **attribute** — the same contract as a roof pitch, checked by `check_attested` |
| reconstruction | `grade` | `documented` / `derived` / `inferred` | a **person** — how much of them is reconstructed |

- **`documented`** — a source names this person.
- **`derived`** — a real, named person whose details are partly reconstructed (their trade is
  attested and their household size is not; their forename comes from another record; their
  presence on the day is read across from a partnership).
- **`inferred`** — a hypothesised resident filling a demonstrable need of the town. **None
  exist in this dataset yet.** The vocabulary exists and validates so a later parcel can add
  them without touching the schema.

**Never `recommended`.** The programme was renamed on 2026-08-13. `tools/validate.py` rejects
that term *by name*, with a message pointing at the rename, because a vocabulary that merely
omits a word gets it back the first time somebody copies an older file. (One legacy filename
still carries it: `docs/RESEARCH/recommended_infill_1835.md`. Renaming it is a separate slice.)

The first pass of the data used `derived` as an *attribute* confidence in 79 places. That is
the conflation the table above exists to prevent, and it was caught by the validator on its
first run: an attribute reconstructed with stated reasoning is `inferred`, which the project's
confidence model already had a word for.

## 3. The gate that actually protects the scene

An arrival after 1835-07-01 is the population layer's version of the Saloon Building problem,
and it fails **silently**: a household record for a man who reached Chicago in September 1835
looks exactly like one for a man who reached it in 1832, and this layer licenses buildings.

Arrival values carry a **`precision`** — `day`, `month`, `season`, `year`, `not_later_than` —
because the sources give years far more often than days. Of 72 households: 43 year, 12
not_later_than, 6 day, 6 month, 5 season. The rule is **asymmetric on purpose**:

- the **earliest** day the value permits must not be after the scene date → **error**;
- a value whose **latest** day is after it → **warning**, because "1835" with no month is a
  real state of the evidence and not a mistake. Two households sit there (`hh_davis_john`,
  `hh_haddock_edward`) and both say so in their notes.

`not_later_than` exists because the commonest evidence of residence in this corpus is *an act
performed at Chicago on a date* — an advertisement placed, an office taken, a tavern licensed.
That bounds an arrival from above and not at all from below, and calling it a month precision
would be a claim nobody made.

## 4. Where the documented people are

Ranked by yield, after working Andreas vol. 1 end to end from the `_djvu.txt` and pinning
each quotation to a scan page through the archive.org `inside.php` index. **The scan page is
almost exactly `2 × printed page + 17`** across the whole volume; verified on eleven quotations.

1. **`andreas_1884_v1`, printed p. 132 (scan p. 281)** — *the motherlode*. "The following is
   an imperfect list of the denizens of the town in the fall of 1833, not before named",
   followed by about fifty names, most with a trade and an arrival year, plus, on the same and
   the facing page, the town's six lawyers, its eight physicians, its four churches with their
   pastors, its four hotels with their landlords and its boarding houses. **One page supplies a
   third of this parcel.** It is a retrospective of 1884: a YEAR off it is documented, a MONTH
   is not, and it says nothing whatever about 1835.
2. **`andreas_1884_v1`, printed pp. 128 and 175–176 (scan pp. 273, 367–369)** — the town's own
   election records. The incorporation poll of 5 August 1833 with all thirteen voters named;
   the enrolment of the twenty-eight electors of 10 August; the officers of 1833, 1834 and
   1835. A man on those lists was in Chicago on that day.
3. **`chicago_democrat_1833_11_26`** — the only contemporary Chicago document this project
   holds, and the only *tier-1* evidence of residence in it. Every advertiser is a documented
   resident with a trade, and six of them state an address. It is **nineteen months** before
   the scene date, in the town's fastest-changing period, so it is strong evidence of existence
   in November 1833 and weak evidence of survival to 1835.
4. **`andreas_1884_v1`, printed pp. 457–465 (scan pp. 933–955)** — the medical chapter, which
   is really a biographical dictionary: dates of birth, places of study, routes of migration
   and arrival dates for every physician and druggist, plus the resolution of "C. & I. Harmon"
   into Dr Elijah Harmon's two eldest sons.
5. **`andreas_1884_v1`, printed pp. 420–422 (scan pp. 857–867)** — the bar. Caton's arrival to
   the day, the first law office, and the only account in the corpus of what an educated
   newcomer did for money in the town's first summer (carried a surveyor's chain).
6. **The existing `data/structures/*.json` prose** — Asahel Pierce arriving from Vermont on
   8 October 1833, Silas B. Cobb, the Murphys, Ira Couch, T. O. Davis, Frederick Thomas.

**The single most valuable unfetched source is the `Chicago American` of 1835–36.** Andreas
quotes its advertisements by name and date throughout; every one is a documented resident with
a trade and often an address, *in the scene year* rather than nineteen months before it.

## 5. What phase one deliberately left undone

- **No inferred residents.** The vocabulary validates; the volume is the next phase's job.
- **The enlisted garrison.** Fort Dearborn was an occupied post; two officers are written and
  no private soldier is, because no source in `data/sources/` names one. That needs a muster
  roll, not a guess.
- **The 1832 militia roll** (Andreas, scan p. 627) — about forty men of the settlement, several
  appearing nowhere else here. A population census of the adult male settlement two years
  before the 1833 roster, unworked.
- **The 1835 town election's date.** Andreas says only "in July, 1835". The 1833 and 1834
  elections were both held on the 10th or 11th of August. **This project cannot say whether the
  board sitting on 1 July 1835 was Kinzie's or Hugunin's**, so the seven trustees of the 1835
  board are not written as households and no office-holding claim in the parcel rests on it.
- **William B. Ogden.** Named in K1 and *not written*, because the widely repeated June 1835
  arrival could not be traced to any source this project holds. Recorded as an open item in
  `index.json`'s `researched_not_resident` rather than cited to nothing.

## 6. Buildings this layer discovered

The residents pass found **documented, positioned, described buildings with no structure
record**. In order of strength:

1. **Rufus Brown's log boarding house** — fabric (log), use (a first-class boarding house),
   keeper (Mrs Rufus Brown, named as the proprietor in her own right) and position ("the first
   building in the rear of this store", i.e. behind Peck's store at South Water and LaSalle).
   That is more than several buildings already standing in this scene have.
2. **Russel Heacock's house on Monroe Street** — built in the *spring of 1835*, on the wrong
   lot, and then *moved one block on rollers*. A dated, positioned, described dwelling for the
   parcel's largest documented household (a wife and five sons, the youngest born there).
3. **A third blacksmith shop** — Matthias Mason & Co., "Main-street, nearly opposite Graves'
   Tavern", self-reported in 1833. The `& Co.` says it employed more than one man.
4. **Dr Elijah Harmon's cabin of hewn logs** — the hewn-versus-round distinction K4 asks for,
   attested.
5. **Dr Temple's building on Lake Street** — Caton's first law office *and* his bedroom, in the
   attic. Not the Temple Building at Franklin and South Water, which is a different building.
6. **John Wright's "two buildings to let"** — rental housing stock, otherwise invisible.
7. **A physician's office of any kind.** Eight doctors are documented in the 1833 town and this
   dataset holds no doctor's office, apothecary's back room or hospital outside the fort.

## 7. A street name nobody else uses

Matthias Mason's own 1833 advertisement puts his smithy on **"Main-street"**, which appears
nowhere in `data/traces/street_control.json`, the Thompson plat module or either 1834 sheet.
The cross-reference is usable: Graves' Tavern is the log tavern at what became 84–86 Lake
Street, so "Main-street" in November 1833 is very probably Lake Street under a colloquial name.
**Recorded as a finding for the streets layer, not acted on.**

## 8. The removal

Seven households carry `review_required: true` and `touches_removal: true`, and the validator
makes the second imply the first. They are the Owen, J. B. Beaubien, Madore Beaubien, Robinson,
Caldwell, McKee, Porthier and Kercheval records — the Indian agency's establishment, the
families with Native kin, and the two Native households the sources name at Wolf Point.

Two datings are held side by side and **not** averaged. Andreas puts the last assembly and the
march to the Missouri in **1836** under Captain Russell and Billy Caldwell;
`chicagology_lastwardance` puts the last great war dance at Chicago on **18 August 1835**;
AGENTS.md takes the 1835 dating as the project's standing constraint. **Under either, 1 July
1835 is before it**, so the scene date is unaffected and the disagreement is recorded rather
than resolved.

Shabbona is deliberately **not** a household: Andreas gives him a full notice and puts his
village on the Illinois and then at Shabbona Grove in De Kalb County. He is at Chicago
repeatedly and lives elsewhere — a distinction this dataset has to be able to make about a man
it would otherwise be tempting to include.

Nothing in this layer improvises Native presence, representation or depiction. It states what
named sources say about named people and stops.

## 9. Where phase one landed

72 households, 96 person entries — **76 documented, 20 derived, 0 inferred**. Five of the 96 are
placeholders that carry a *count* in their name for people a source counts and does not name
(an unnamed wife, "four children", "and family"); they say in their notes that they must not be
counted as individuals, so the named-person figure is 91.

**43 structures that previously had no named resident now have one**, and 24 households are
**not** recorded as certainly present on the scene date — which is the number this layer exists
to be able to state.
