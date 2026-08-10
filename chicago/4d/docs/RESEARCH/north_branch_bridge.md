# North Branch Bridge — research memo

**Record:** `data/structures/north_branch_bridge.json` · **Archetype:** `bridge_timber` ·
**Written:** 2026-08-10 · **Scene:** 1835 (target 1835-07-01)

Chicago's first bridge, and the first structure in this dataset that is not a building. It is
also the first record here whose dimensions come from evidence instead of from a placeholder,
which is worth stating plainly because every other footprint in `data/structures/` says in its
own note that its numbers are invented.

---

## 1. What the sources say

**Andreas, *History of Chicago* vol. I (1886), transcribed by chicagology on its Kinzie Street
Bridges page** (`chicagology_kinzie_bridge`):

> In the summer of 1832 Samuel Miller, the original possessor of the old ferry scow, built the
> first bridge over the North Branch. It was located near the southeast corner of Kinzie and
> Canal streets, in the vicinity of the present bridge of the Chicago & Northwestern Railroad
> Company. It was formed of stringers and only fitted for foot passengers. Even up to the summer
> of 1833 the structure was useless for teams.

The same page carries a tabulated chronology of the six Kinzie Street crossings whose first row
reads **Kinzie #1 · 1832 · 1839 · Wood, Fixed, Bent · Samuel Miller**. That table is the page's
own editorial apparatus, not Andreas, and it is treated as weaker than his prose.

**Charles Cleaver, recalled in the *Chicago Tribune* of 29 October 1893**
(`chicagology_prefire252`):

> Mr. Cleaver was authority for the statement that the first bridge across the North Branch of
> the river was built in the winter of 1831-32, and that the first bridge over the South Branch
> was built in the [winter] of 1832-33. The abutments were built of heavy logs in the shallow
> water near the banks. **These bridges were ten feet wide.** Mr. Cleaver remembered driving
> across the first bridge over the North Branch.

(The transcription's OCR is corrupt in two places — "heavy legs" for heavy logs, "in the beer of"
for in the winter of. Both are read through, and the fact that they had to be is itself a reason
not to build anything on a single word of this page.)

**The war-dance account of 18 August 1835** (`chicagology_lastwardance`) has a procession cross
"the North Branch bridge" and then move "south along West Water street (now Canal street), in
front of the 'Green Tree Tavern' and 'Wolf's Point Tavern' to the log raft bridge across the
south branch". Cited here for three narrow facts and nothing else: the bridge was standing six
and a half weeks after the scene date, it carried a crowd, and it landed on the west bank north
of the two taverns. **The subject of that page falls under the standing constraint in
`AGENTS.md`**, and nothing in this project depicts, stages or narrates it; the citation is about
timber.

---

## 2. Three disagreements, and how each was read

**The build date — Andreas's summer 1832 against Cleaver's winter 1831-32.** Adopted: 1832.
Cleaver did not reach Chicago until 23 October 1833, so his date is hearsay reported sixty years
after the fact, while Andreas is a compiler working over the town's records in the 1880s. It
makes no difference to a scene dated 1835-07-01 and is recorded because the next reader will
find both numbers.

**The capacity — "only fitted for foot passengers" against "remembered driving across".** Both
kept; neither discarded. Andreas's judgement is explicitly dated ("even up to the summer of
1833"), Cleaver's recollection is undated, and on 18 August 1835 the thing carried hundreds of
people at once. The reading adopted is that the bridge was rebuilt, widened or decked between
1833 and 1835 and **nothing reached says when or how**. The record's `stringer_count: 4` and its
full-width deck take the 1835 reading, and its note says that an 1833 scene would want the other
one. This is the single largest unknown about the structure and it is invisible in the model,
because a model shows one state.

**The pier type — Cleaver's heavy logs against the table's "Bent".** Adopted: `crib`, tagged
`inferred`. An eyewitness describing logs standing in shallow water is describing a crib; "Bent"
is a modern type-word applied down a column covering six bridges and a century. The inference
that matters is not the choice of word, though — it is the step from *abutments*, which Cleaver
describes, to *piers*, which nobody does. See §4.

---

## 3. Where it stands, and how the span was measured

The corner is documented and the coordinate is derived, so the position is tagged `inferred` —
the same rule the Green Tree's placement uses.

- Modern **Kinzie and Canal** intersection centre, from OpenStreetMap (three shared nodes, mean
  41.889068 N, -87.640156 W) = EPSG:26916 **E 446891.7, N 4637657.8**, local **N +262.0**. Kinzie
  Street is one of the streets that survives on its 1835 alignment, and it runs east-west, which
  is also this archetype's zero-rotation orientation.
- The deck centreline sits on that northing. Its ends sit where the **traced 1834 waterline**
  crosses it — west bank local **E −117.52**, east bank local **E −45.69** — read off
  `data/terrain/epochs/e1834_harbor_cut/river.geojson`, the same Wright 1834 segmentation the
  ground and the river are built from. **Span 71.83 m.** It agrees with the reach's drafted mean
  width of 72.9 m to about a metre, which is the check that the number is reading the map at this
  station rather than averaging it.
- The modern channel was deliberately not used. It is a dredged and walled successor; measuring
  against it would put an 1832 bridge's abutments on nineteenth-century engineering.

**The span overstates the clear span, and by an unknown amount.** Cleaver puts the abutments "in
the shallow water near the banks" — inside the drawn line — and nobody recorded how far inside.
Landing the deck exactly on the traced waterline was chosen because that line is the one thing
here that is evidence: the terrain surface crosses Z = 0 along it by construction, so the deck
ends where ground meets water. An inset would have been a second invention stacked on the first.
The carried uncertainty, ±20 m from the georeference, is larger than the difference being argued
about.

One thing the corner does **not** say: modern Canal Street at this northing lies **63 m west of
the traced 1834 west bank**. "The south-east corner of Kinzie and Canal" is where the approach
began, not where the bridge did. That is a fact about two streets, not an error bar.

---

## 4. What is invented

`docs/LIBERTIES.md` **L29**. Fifteen cribs stand in the river at the archetype's default 4.5 m
spacing over a 71.83 m span, and **no source describes the middle of this bridge at all**.
Something had to hold up seventy metres of log stringer, so intermediate supports are not the
invention; their number, spacing and form are. The default was kept rather than replaced with a
fresh number, because a new number would look like a finding.

It is also the invention the confidence view cannot show: the tint on a crib grades what a crib
*is*, not how many there were. A visitor sees a regular colonnade marching across the water and
reads it as a fact about the bridge.

Beyond that: the stringer scantlings, the puncheon deck pitch and the abutment fill are the
archetype's, unstated on the record, and the railing is deliberately absent — an absence argued
in `generators/archetypes/bridge_timber.py` and stated as `inferred` on the record, because a
railed deck reads as considered infrastructure and an unrailed one reads as a plank over water.

---

## 5. A correction to this project's own dossier

`docs/research/03-structures-north.md` §5 gives both branch bridges as "about 10 ft wide,
clearing the water by about 6 ft" and tags the pair `[DOC]`. **Only the width survives.** Ten
feet is Cleaver's and now has a source record. The six-foot clearance has none: the pages that
carry the width, the abutments, the stringers, the 1832 date and the 1839 replacement say
nothing about a height above the water, and a direct search of the same host for the phrasing
returns nothing.

The figure is kept — it is plausible for a stringer bridge on cribbed abutments in shallow water,
and it is the dossier's — but the record tags `clearance_m` **inferred**, and
`bridge_timber_params.py`'s docstring is corrected in the same slice so that the constant's name
stops asserting what it cannot show. Promote it if the page behind it is found.

---

## 6. Open threads, in the order worth pulling

1. **The 1834/1835 Wabansia and Kinzie's Addition plat** (Encyclopedia of Chicago item 10634; LoC
   g4104c.ct007620), in its state corrected 17 June 1835 — contemporaneous to within two weeks of
   the scene date, covering exactly this ground, and the one document that could show the
   crossing drawn.
2. **Andreas vol. I at page-image level**, where the prose transcribed above sits; the same
   unopened source that would settle Miller's house one bank away.
3. **What happened between 1833 and 1835.** A town that could build the 200-ft Dearborn Street
   drawbridge in 1834 did something to the crossing that was useless for teams in 1833. Trustee
   minutes are the likely home of it.
4. **The six-foot clearance.** Find the page, or downgrade the dossier's tag where it stands.
