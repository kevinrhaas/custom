# The residents and households layer — the model

**Roadmap:** `docs/ROADMAP.md` § K1 · **Data:** `data/residents/` ·
**Gate:** `check_residents` in `tools/validate.py`, plus fourteen mint and ladder re-derivation
steps in `tools/check.sh` · **Scene date:** 1835-07-01

**This file is the MODEL. The measurement is
`docs/RESEARCH/residents-households-summary-2026-09.md`,** where every figure carries the
command that reproduces it. Rewritten under T-0517, because this dossier had gone a month
describing a layer of 72 households while the layer passed 1,300 — the reason the numbers now
live in a tool and not in prose.

---

## 1. What this layer is for

Chicago went from about 350 people in 1833 to **3,265 in the town census of November 1835**
(Andreas vol. 1, printed p. 180, archive.org scan p. 377), in **398 dwellings**.

The programme's argument is that the population and the buildings are the same problem seen
from opposite ends: *the population is what justifies the buildings*. A household that needs a
dwelling eventually becomes a structure record on the plat, archetyped, baked and graded.

**No human figures are drawn.** `docs/LIBERTIES.md` L1 and AGENTS.md stand: the scene ships
empty and accurate. This is a dataset layer feeding structures, the evidence panel and the
gate screen.

## 2. The two grading axes, and the vocabulary they share

`data/residents/index.json` is the manifest (a static host cannot be globbed) and
`data/residents/households/*.json` is one file per household. The manifest is a denormalised
copy; the record is authoritative and the validator fails the build on drift.

**There are two orthogonal axes. They use the same three words and they grade different
things** — that is the one thing about this layer that is easy to get wrong.

| axis | key | vocabulary | grades |
|---|---|---|---|
| resident evidence | `grade` (on a person) | `attested` / `inferred` / `reconstructed` | **the person** — how well the corpus supports them as a real named circa-1835 resident |
| attribute evidence | `confidence` (inside an attribute block) | `attested` / `inferred` / `reconstructed` | **one claim about them** — their trade, their arrival, where they live |

- **`attested`** — corroborated well enough that the project stands behind it.
- **`inferred`** — reasonably believed, and the `note` states the reasoning. Never optional.
- **`reconstructed`** — on an ATTRIBUTE, "not attested", which is the commonest state in the
  layer by a wide margin. On a PERSON it is reserved for an explicit later reconstruction pass
  and **is deliberately zero**: nobody in this layer is graded `reconstructed` today. The word
  validates so such a pass can be added without touching the schema.

`resident_subtype` is a second, narrower mark on a person: **`projected_resident`**, the
weakest evidence-based subset — a name the corpus prints once and places by nothing.

**Two retired words, and the reason they are named here.** The programme was renamed twice.
`recommended` was retired on 2026-08-13 and `tools/validate.py` rejects it *by name*, with a
message pointing at the rename, because a vocabulary that merely omits a word gets it back the
first time somebody copies an older file. The second rename replaced the earlier person-grade
words with the three above; `derived` is gone as a grade, and the first pass of the data used
it as an *attribute* confidence in 79 places, which is exactly the conflation the table above
exists to prevent.

**One remnant of that second rename is still in the data.** 39 households carry a
`source_pass` whose value is the pre-rename word for `attested`. It is a provenance label on
the mint that made the record, not a grade, and nothing reads it as one — but it is the last
place the old vocabulary survives, and it is filed as its own ticket rather than quietly
rewritten here.

## 3. How a household record is shaped

Every household carries `id`, `name`, `division`, `head`, `persons[]`, `review_required`,
`touches_removal`, `research_note`, and six **graded attribute blocks** — `arrival`,
`party_size_on_arrival`, `origin`, `reason_for_coming`, `lives_at`, `works_at` — plus
`present_on_scene_date`. Each block is `{value, confidence, sources[], note}` and an unattested
block says so in its note rather than being absent.

**The id families are gone.** Records were once minted into `hh_doc_`, `hh_placed_` and
`hh_ll_` prefixes; T-0638's rename left **every id a plain `hh_<surname>_<forename>`**, and the
mint that made a record is carried by the `source_pass` field instead — `letter_list`, `civic`,
`placed`, the legacy value in §2, or absent for the earliest hand-written records. A reader
looking for the old prefixes will not find them, and `data/residents/rename_map_t0638.json` is
the audit trail of the move.

**`persons[]`** carry `id`, `name`, `relationship`, `grade`, `occupation`, `sources[]`, `note`,
and then whatever has been read onto them: `resident_subtype`, `letter_list_only` with
`letter_list_returns[]`, `civic_mint`, `ladder_rule`, `sex`, `birth_year`,
`age_on_scene_date`, `resident_research`, `later_census`, and the evidence blocks in §5.

## 4. The gate that actually protects the scene

An arrival after 1835-07-01 is the population layer's version of the Saloon Building problem,
and it fails **silently**: a household record for a man who reached Chicago in September 1835
looks exactly like one for a man who reached it in 1832, and this layer licenses buildings.

Arrival values carry a **`precision`** — `day`, `month`, `season`, `year`, `not_later_than` —
because the sources give years far more often than days. The rule is **asymmetric on purpose**:

- the **earliest** day the value permits must not be after the scene date → **error**;
- a value whose **latest** day is after it → **warning**, because "1835" with no month is a
  real state of the evidence and not a mistake.

`not_later_than` exists because the commonest evidence of residence in this corpus is *an act
performed at Chicago on a date* — an advertisement placed, an office taken, a letter waiting at
the post office. That bounds an arrival from above and not at all from below, and calling it a
month precision would be a claim nobody made. It is now the precision on more than 95% of
households, which is the honest shape of the corpus and not a defect.

The exclusions half of the dataset is `index.json`'s **`researched_not_resident`**, and it is as
load-bearing as the households: people whose arrival is after the scene date, people the sources
place at Chicago but not as residents of the town, and people the project believes were here and
cannot cite. **William B. Ogden is there**, not written as a household, because the widely
repeated June 1835 arrival could not be traced to any source this project holds.

## 5. The evidence blocks, and the ladder that grades from them

A landed reading writes a block onto the person: `press_evidence`, `civic_evidence`,
`book_evidence`, `church_evidence`, `census_evidence`, `biographical_evidence`, and
`directories` on the household. Each entry names its `list`, its `as_read` string, its
`locator`, its `record_id`, the `describes_date`, its `source` and the ladder `rule` that fired
— so a grade can always be walked back to the printed line that produced it.

**The ladder is the mint precedence**, held in `index.json`'s `vocabulary.ladder_rules` and
re-derived by `check.sh` on every commit. In brief, strongest first:

| rung | grade | fires on |
|---|---|---|
| `G0` | not an 1835 resident | every appearance describes a date after the scene year |
| `G1a` | `attested` | the 1835 poll list **and** another independent source |
| `G1b` | `attested` | a contemporary record naming the person in Chicago — the 1833–1835 papers |
| `G1c` | `attested` | convergence: two independent in-window records from **different class families** |
| `G2a` | `inferred` | the 1835 poll list alone |
| `G2b` | `inferred` | an 1833/1834 poll, tax or muster list with another source |
| `G2c` | `inferred` | the St Cyr register 1833–1835 — a party to a marriage or burial in the window |
| `G2d` | `inferred` | Hubbard, Fergus or Norris naming a person the town already carries, with a trade or an address |
| `G2e` | `inferred` | a Chicago post-office letter list of 1833–1835 and nothing stronger |
| `G3` | `inferred` | a single appearance and nothing else → `projected_resident` |
| `G4` | `inferred` | two or more appearances, none of a class a rung above accepts → `projected_resident` |
| `G5` | — | **NO PROPOSAL.** The town already carries this person and every appearance the ladder can see is later than the scene year; it abstains rather than demote on evidence it has not read, and the row is listed as a conflict for the owner |

Two rungs are the ones to argue with. **`G1c` will not promote a letter list on its own** — a
letter list only counts *toward* convergence. **`G2e` grades a letter list down** rather than
reading "mail waiting at Chicago" as a contemporary record naming the person in the town; that
is the one reading put back to the owner, and it is why half this layer sits at
`projected_resident`. **`G5` is an abstention, not a zero** — it is the ladder refusing to act
outside what it has read.

## 6. The 1840 bridge rule

**1840 is LATER EVIDENCE and is never silently back-projected to 1835.** A person's
`later_census` block is explicitly an 1840 fact: it carries the year, the serial, the
transcribed and normalised head name, separate `name_confidence` and `identity_confidence`, the
`bridge_status`, the page and row, the source image, and the household's composition by age
band as the schedule prints it.

`bridge_status` is `validated` or `provisional`, and the distinction is the whole rule: a
provisional bridge is a proposed identity that has not been proved, and it licenses nothing
about 1835. What the bridge is *for* is composition — the schedules print how many people of
each sex and age band shared a roof, which is the only evidence in the corpus that can move
this layer off households of one (§ the summary, `--section size`).

## 7. The liberties this layer stands on

`docs/LIBERTIES.md` carries them in full; they are cited here because the layer cannot be read
honestly without them.

- **L205** — five corroborated men were seated on roofs the roof programme reconstructed. The
  men are real; the roofs are ours.
- **L206** — sixteen tradespeople whose trade the papers print are written as households of
  one. The trade is attested; **the household is the invention**.
- **L207** — twelve names from the post office's letter lists, written as households of one on
  the thinnest evidence this project accepts for a resident.
- **L211** — 101 businesses stand on 1 July 1835 because nothing says they closed.
- **L212** — nineteen businesses are seated on reconstructed roofs and no source puts them
  there.
- **L213** — four people the papers name with no trade, written as households of one on a
  residency test.
- **L214** — **the liberty of scale, and the largest in the project.** On 2026-08-30 the owner
  ruled that every name the post office's lists of uncalled-for letters yield, and the mint's
  refusals admit, joins the town. Nothing was invented and no confidence was upgraded: each of
  the 727 is printed by name at the issue and column its record cites. What changed is
  proportion — **a reader who counts this town's people is counting a post-office list.**
- **L216, L218 and L222** are the address side of the same programme: a later printed address
  used to position a business or a dwelling, and — at L222 — an attested lot-and-block notice
  re-dealing the roof beneath it.

## 8. The removal

Eight households carry `review_required: true`, and the validator makes `touches_removal` imply
it. They are the Owen, J. B. Beaubien, Madore Beaubien, Robinson, Caldwell, McKee, Porthier and
Kercheval records — the Indian agency's establishment, the families with Native kin, and the
Native households the sources name at Wolf Point.

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

## 9. Where the people were found

Ranked by yield. **The scan page is almost exactly `2 × printed page + 17`** across Andreas
vol. 1; verified on eleven quotations.

1. **The Chicago post office's letter lists**, in the `chicago_democrat_1833_1835` run — by
   volume the largest source in the layer by an order of magnitude, and the weakest per name
   (L214, and `G2e` above).
2. **`chicago_voter_lists_1833_1835_irad`** — the town's own lists of its own people, and the
   source with the highest match rate of anything read: a list a town made of its named
   inhabitants is what predicts yield.
3. **`andreas_1884_v1`, printed p. 132 (scan p. 281)** — "an imperfect list of the denizens of
   the town in the fall of 1833, not before named", about fifty names, most with a trade and an
   arrival year, plus the town's lawyers, physicians, churches, hotels and boarding houses. It
   is a retrospective of 1884: a YEAR off it is evidence, a MONTH is not.
4. **`andreas_1884_v1`, printed pp. 128 and 175–176** — the incorporation poll of 5 August 1833
   with all thirteen voters named, the twenty-eight electors of 10 August, and the officers of
   1833–1835. A man on those lists was in Chicago on that day.
5. **The directories — `fergus_chicago_directory_1839`, `_1843`, `norris_directory_1844`** —
   later than the scene and rich beyond anything else in the corpus, because they print a trade
   and very often a street beside each name.
6. **`st_cyr_register_ichr_v4`** — the parish register, a party to a marriage or burial inside
   the window.
7. **`chicago_american_1835`** — in the scene year rather than nineteen months before it.
8. **`chicago_democrat_1833_11_26`** — every advertiser a resident with a trade, six with an
   address; nineteen months before the scene date, in the town's fastest-changing period.

## 10. What this layer still has not done

- **The 1830 federal schedule has reached no card.** Chicago was enumerated in Peoria County;
  the schedule is read in `data/research/census_1830/` and not one ruling from it stands behind
  a person.
- **The directories' trades and addresses are adjudicated and unspent** — 187 people cite a
  directory for their identity and one cites one for their trade. This is the largest gap
  between what the project has read and what its town knows.
- **The enlisted garrison.** Fort Dearborn was an occupied post; the officers are written and
  no private soldier is, because no source in `data/sources/` names one. That needs a muster
  roll, not a guess.
- **The 1832 militia roll** (Andreas, scan p. 627) — about forty men of the settlement, several
  appearing nowhere else here.
- **The 1835 town election's date.** Andreas says only "in July, 1835", and the 1833 and 1834
  elections were both held on the 10th or 11th of August. **This project cannot say whether the
  board sitting on 1 July 1835 was Kinzie's or Hugunin's**, so the seven trustees of the 1835
  board are not written as households and no office-holding claim rests on it.
- **`docs/RESEARCH/residents_1835_inferred.md` is stale in the way this file was** — it
  describes an earlier state of the inferred layer. Named here so the next run finds it; T-0517
  deliberately did not rewrite it.

## 11. Buildings this layer discovered

The residents passes found positioned, described buildings with no structure record. In order
of strength:

1. **Rufus Brown's log boarding house** — fabric (log), use (a first-class boarding house),
   keeper (Mrs Rufus Brown, named as proprietor in her own right) and position ("the first
   building in the rear of this store", behind Peck's store at South Water and LaSalle).
2. **Russel Heacock's house on Monroe Street** — built in the *spring of 1835*, on the wrong
   lot, then *moved one block on rollers*. A dated, positioned, described dwelling.
3. **A third blacksmith shop** — Matthias Mason & Co., "Main-street, nearly opposite Graves'
   Tavern", self-reported in 1833. The `& Co.` says it employed more than one man.
4. **Dr Elijah Harmon's cabin of hewn logs** — the hewn-versus-round distinction K4 asks for.
5. **Dr Temple's building on Lake Street** — Caton's first law office *and* his bedroom, in the
   attic. Not the Temple Building at Franklin and South Water.
6. **John Wright's "two buildings to let"** — rental housing stock, otherwise invisible.
7. **A physician's office of any kind.** Eight doctors are named in the 1833 town and this
   dataset holds no doctor's office, apothecary's back room or hospital outside the fort.

## 12. A street name nobody else uses

Matthias Mason's own 1833 advertisement puts his smithy on **"Main-street"**, which appears
nowhere in `data/traces/street_control.json`, the Thompson plat module or either 1834 sheet.
Graves' Tavern is the log tavern at what became 84–86 Lake Street, so "Main-street" in November
1833 is very probably Lake Street under a colloquial name. **Recorded as a finding for the
streets layer, not acted on.**

## 13. The gates

- **`check_residents`** in `tools/validate.py` — schema, provenance, linkage and the scene-date
  gate over `data/residents/**`, tested in `tools/test_validate.py`.
- **The mint re-derivations**, one `check.sh` step each: the reconstructed residents' invented
  names, the corroborated residents on reconstructed roofs, the minted register residents, the
  residency-tested residents (`mint_placed_residents.py --check`), the letter-list mint
  (`mint_letter_list_residents.py`, with `--gate` proving what it may *not* do), the 75-person
  research cohort, the 375 reviewed residents, the letter-list cohort against the owner's
  ruling, the collision report, and the ladder's own two steps — the civic/church/press/book
  residents and the regrades.
- **`tools/town_census.py`** — the gate screen's town figures re-derive from the roofs and the
  residents; hand-edit `data/town_census.json` and `check.sh` says so.
- **`tools/export_resident_audit.py --check`** — the final audit still re-derives from the
  layer (T-0512).
- **`node tools/check_published_residents.mjs`** — the published mirror carries its source's
  value. `publish.sh` TRANSFORMS this layer rather than copying it, so this one is not optional.
- **`tools/residents_summary.py`** — not a gate. It reads and prints, and it refuses to run if
  its own domain table has fallen out of step with the layer.
