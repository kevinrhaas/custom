# The public-square pond — where one document argues both ways

**Parcel T-E5(a)** (ROADMAP · LANE 3 GROUND) · written 2026-08-16 · **a dating, not a change to the ground**

`AGENTS.md`: *where sources disagree, record the disagreement here and pick the best-attested
reading with reasoning — never silently choose.* This is that record. Nothing in this parcel
models, moves or removes any water; the four in-town water features are still deferred to the
hydrology parcel exactly as they were. What changes is that each of them now states where it
stands on **1835-07-01**, and this one states that it does not know.

---

## 0. Headline

`data/terrain/epochs/e1834_harbor_cut/terrain_spec.json` defers four in-town water features
under one shared phrase — **"existence documented, geometry conjectural"**. Existence is a claim
about a *place*; a scene is a *date*. Nobody had asked the second question, and the four do not
answer it alike:

| dossier zone | feature | at 1835-07-01 | what dates it |
|---|---|---|---|
| 14 | The slough | **present** (inferred) | a structure this project already stands in the scene |
| 15 | **The public-square pond** | **not established** (inferred) | nothing — and the same document argues both ways |
| 16 | The Frog Pond, Lake & LaSalle | present (inferred) | a newspaper, one year late to the day |
| 17 | The Wells Street marsh | present (inferred) | the sentence that gives the slough gives what it drains |

Three of the four survive the question. The pond is the one that does not, and it is the one
T-E5 was opened about.

---

## 1. The sharpest thing here is not the pond

**The scene draws a bridge over a watercourse the scene does not contain.**

`data/sidecars/1835/slough_log_bridge.json` — *The Slough Log Bridge, Water Street* — is a
committed structure standing on 1835-07-01, and its own `documented_range` note quotes the
source running the crossing *"until after 1840"*. Zone 14, the slough it crosses, is deferred
and undrawn. A visitor walks onto a timber crossing laid over open prairie.

That is **not** an argument for cutting a channel. The slough's depth and width are conjectural
and parcel (c) still owns them — the deferral's reasoning is intact. It is an argument that the
four features were never on one footing, which is what a single shared phrase implied.

---

## 2. The disagreement, stated in full

One document — `chicagology_prefire273`, rung 2 — carries **both** of the following.

**FOR a pond at the scene date.** The slough sentence, transcribed at
`docs/research/01-terrain-hydrology.md` § 2.2, describes the stream *"which drained **the pond**
and the marsh extending up Wells Street, and in a winding course passed over the site of the
Tremont House and entered the river at the end of State Street"* — and adds that where Water
Street crossed it, a log bridge was needed **until after 1840**. That is a drainage system
described as a working feature of the town, and the pond is named inside it as the thing being
drained. Nothing in that sentence is in a remembered past tense.

**AGAINST.** Three things, and the deferral weighed none of them.

1. **The pond quotation dates nothing.** `docs/research/08-fauna.md` line 44 gives it verbatim:
   *"Our public Square [where the Court House and City Hall now stand] **was then** a pond, where
   the Indians had trapped the muskrat, and where the first settlers hunted ducks."* A past tense
   set against an 1857 present, with no *then* the sentence fixes. And
   `data/sources/chicagology_prefire273.json` identifies the document it transcribes as built on
   **Gurdon Hubbard's description of Chicago as he found it in 1818** and on **George Davis's 1832
   drawing** — *"This is a picture of Chicago, and of all that then composed it, as described to
   us by Gurdon S. Hubbard, Esq."* The document's own *then* is a generation before the scene.
2. **The dossier's own row says the wrong season.** `docs/research/01-terrain-hydrology.md`
   row 15 reads *"~1 city block, **seasonal**; bed +1.0 to +2.0; **water 0.5–2 ft deep in
   spring**"*. The scene date is **1 July**. The row states a season and the deferral read it as
   a scene. The same dossier's modelling rule 2 says the ponding is *"worst in spring"* and that
   summer 1835 is *"drier than the spring 'impassable' condition"* — while noting that ponds 15
   and 16 *"were still wet in July 1836"*, which is a statement about zone 16's newspaper and not
   about zone 15.
3. **This project already stands two county buildings on that block, before the scene date.**
   `data/sidecars/1835/estray_pen.json` — Chicago's **first public building** — on the square's
   south-west corner from **March 1832**, and `data/sidecars/1835/log_jail.json` on its
   north-west corner from the **fall of 1833**. A pound is not built in a pond.

---

## 3. The reading picked, and why it is not "the pond was not there"

**Not established.** Graded `inferred`, in `data/terrain/1835_intown_water_dating.json` zone 15.

The temptation is to read §2's three points as a refutation and strike the pond. That would be
wrong twice. It would discard the slough sentence, which is the same document and better placed
in time than the quotation is. And it would answer a question about *extent* with a claim about
*existence*.

Because the buildings do not refute a pond — **they bound one**. A pond covering the whole block
is refused by this project's own committed records. A pond covering *part* of the block is
untouched by them, and is exactly what T-E5's third question asked for: *"a wet part of the square
with the three public buildings clear of it — which is a claim about extent that no source
reached supports."*

So the date and the extent are **one question**, and neither is settled. That is the finding:
`existence documented, geometry conjectural` was true of a *place* and was being read as though
it were true of the *scene*, and the geometry it called conjectural is not a detail to be filled
in later — it is the thing that decides whether water stands under Chicago's first public
building.

**What T-E5 asked for, discharged.** Its fallback was *"if it cannot be made honestly, the honest
answer is a `docs/LIBERTIES.md` entry saying the square is drawn dry and why."* No liberty is owed
and none is taken: nothing was invented, no confidence moved up, and the square was **already**
drawn dry and already recorded as such in the deferral a visitor can read. What was missing was
the reason, and the reason is now in that same visitor-facing text.

---

## 4. What it cost downstream, which is the part nobody would have looked for

`data/fauna/zones/f04_marsh.json` rested **three claims** on the pond quotation as though it were
in-scene evidence, and one of them said so in as many words.

| claim | before | after |
|---|---|---|
| `ondatra_zibethicus.presence` | `attested`, sourced **only** to the pond quotation, noted as *"direct evidence of animals present in numbers at a named location inside the scene box"* | `attested`, carried by Andreas — *"ducks and muskrats in the marshes"* — with the limit stated |
| `anas_platyrhynchos.presence` | `attested`, sourced **only** to the pond quotation | `attested`, carried by Andreas, same limit |
| the zone note | *"the two documented anchors are both inside the platted grid"* | the two anchors are named as unequally dated, and both as unmodelled |

**No grade moved**, and that is deliberate rather than convenient. What carries `attested` is
Andreas's marshes, and the marshes he names *are* the habitat this zone plants — `z04_marsh`'s
extent is a **buffer of the mapped water**, the river-shore strip, and has never reached the
square. The animal is attested in the habitat the scene draws. It is no longer attested at a
named block the scene draws dry, and the notes now say which of those two things they mean.

---

## 5. What this parcel did NOT do

- It did not model, move or size any water. All four features remain deferred to parcel (c).
- It did not touch `docs/research/01-terrain-hydrology.md`, `08-fauna.md` or `02-flora.md`.
  Research dossiers are committed **verbatim** as citable inputs; disagreements with them belong
  here, which is why this file exists.
- It did not resolve the disagreement in §2. It recorded it and graded the result
  `not_established`, which is a different and more honest thing.
- It did not answer **how much** of the block was wet, and nothing here should be read as
  licensing a guess at it. That is `T-E5(b)`, and its first question is whether any source states
  an extent at all.
