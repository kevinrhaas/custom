# South Branch Bridge — research memo

Record: `data/structures/south_branch_raft_bridge.json` · Archetype: `bridge_timber`
Written 2026-08-11.

---

## 1. What this record is for

Chicago's second bridge: the crossing of the South Branch between Lake and Randolph
Streets, built in the winter of 1832-33 and still in use on 18 August 1835, six and a
half weeks after the scene date. It is the third of the town's three crossings to get a
record, after the North Branch bridge and before the Dearborn Street drawbridge.

## 2. The conflict this record exists to hold open

**Every retelling calls it a floating log raft. The only source that describes how it
was built says it was not.**

| reading | where it comes from |
|---|---|
| floating log raft | `docs/research/03-structures-north.md` §5, "Log floating raft bridge"; `chicagology_lastwardance`, "the log raft bridge across the south branch"; the archetype's own docstring until this record was written |
| fixed bridge on log abutments and two bents | `old_settlers_bridges_1883` — the statement Andreas prints at the foot of vol. 1 pp. 631-632, signed J. D. Caton, John Bates, Charles Cleaver and John Noble |

The 1883 statement is about **both** branch bridges in every sentence: "both bridges
were built on abutments and two 'bents'"; "the bents were of four heavy logs, resting
on the bottom, in deeper water"; "these bridges were about ten feet wide"; "these were
**both** wagon bridges, and were about six feet above the water, so that teams passed
under them on the ice freely."

A floating raft has no abutments, no bents resting on the bottom, no six feet of air
beneath it, and nothing passes under it on the ice.

**How it was settled.** By the rule the North Branch record arrived at the hard way —
it once chose an eyewitness over a table's type-word, was wrong, and was corrected when
the footnote under the prose turned out to be the settlers' own word. The test is not
which source is better known but which was in a position to know *the thing being
claimed*, and joinery is what a man who drove a team over a structure knows. Four men
who used these bridges describe fixed carpentry over their signatures. "Raft" is also a
very good description of what a low log bridge on two bents looks like from the bank,
and it is the kind of phrase that survives sixty years of retelling.

**What was not done:** the name was not changed. The structure id, the record name and
the `aka` list all keep the word, because that is what the sources call it and a record
that renamed itself would make its own evidence unfindable.

**What would reverse it:** any source putting a floating deck on the South Branch in the
1830s against the settlers' signatures, or a reading showing the South Branch sentences
in the 1883 footnote are a later interpolation. The right response would be a
`raft_timber` archetype, not a parameter on `bridge_timber`.

## 3. The span is measured, not chosen

Method, identical to the North Branch bridge's:

1. The modern Lake and Randolph centrelines were read from OpenStreetMap — Lake from
   Canal Street (GCP **G5**, already committed in `data/traces/gcp/wright_1834_gcps.json`,
   and the best-fitting control point in that set at 1.8 m residual) to Dearborn Street
   (node 27477597); Randolph from LaSalle Street (**G3**) to Dearborn Street
   (node 28290271). Both streets survive on their 1830s alignment.
2. The two centrelines lie **137.69 m** apart. The crossing line is drawn parallel to
   them through the midpoint of that separation, at local **N −177.2**.
3. Its ends are set where the traced 1834 waterlines cross it, off
   `data/terrain/epochs/e1834_harbor_cut/river.geojson`.

| | local E | local N |
|---|---|---|
| west bank | +6.86 | −178.07 |
| east bank | +62.82 | −178.36 |

**Span = 55.96 m = 183.6 ft.**

**Cross-check.** The same file's drafted mean width for the South Branch reach is
**57.3 m**. The measured crossing comes out 55.96 m — an agreement to 1.3 m, which is
the same agreement the North Branch bridge's 71.83 m makes against its own reach's
72.9 m. Two crossings measured the same way, each landing within a metre and a half of
its reach's independently drafted mean.

**Why the midpoint station.** The two sources pull opposite ways: §5 of dossier 03 says
"just north of the present Randolph street bridge", and the war-dance account says "near
Lake Street". The midpoint is the only station that prefers neither.

**The real error bar is the station, not the georeference.** This reach narrows fast.
The same method gives:

| station | span |
|---|---|
| Lake Street line | 74.38 m (244 ft) |
| midpoint (adopted) | 55.96 m (184 ft) |
| Randolph Street line | 46.79 m (154 ft) |

So a crossing anywhere in the band the sources allow is between about 47 and 74 m. The
recorded value is the middle of the *band*, not the middle of that range.

**What would narrow it.** `docs/ROADMAP.md` names the Conley/Stelzer 1933 reconstruction
(`conley_stelzer_1933`, tier 5, `asset_use: orientation`) as the sheet that draws the
bridges in place, and `docs/PROVENANCE.md` licenses a tier-5 map to carry a position to
`inferred`. It has **not** been read at this crossing's pixel by this parcel, and it is
the first thing to try.

## 4. What is documented, and it is more than for any other structure here

Nearly the whole form block: construction, width (10 ft), clearance (6 ft), abutments,
pier kind (bent), pier count (2) and deck kind (puncheon) are all `documented` from the
1883 statement, most of them corroborated by Cleaver's 1893 Tribune recollection
(`chicagology_prefire252`). The GLB comes out entirely at `_CONFIDENCE = 0.0`.

Two attributes are `inferred`:

- **`stringer_count: 4`** — the source gives the load (a wagon bridge, heavy log
  stringers, three spans of 18.7 m) and not the count. Four is the archetype's.
- **`railing: false`** — "without railings, for the first few years, after which guards,
  or railings, were added". Three years after the build, the natural reading covers the
  scene date. A dated addition falling before July 1835 would flip it.

## 5. The dates

**Opening, 1833-03-01.** Cleaver, in the *Tribune* of 29 October 1893: the first bridge
over the South Branch "was built in the [winter] of 1832-33". A winter is not a day, so
the range opens at the end of it. Cleaver did not reach Chicago until 23 October 1833,
so this is hearsay reported sixty years later — and it is the only date reached.

**The 1883 statement's South Branch dates are deliberately not cited.**
`data/sources/old_settlers_bridges_1883.json` records that the two archive.org scans of
that footnote *disagree* on them. A number two readings cannot agree on is not evidence.

**Close, 1835-08-18.** The last date any source reached puts the bridge in use. This is
the range of the *attestation*, not a claim that the bridge fell on 19 August. The North
Branch record could close in 1839 because a chronology table says so; no equivalent
exists for this crossing. Closing on the last attestation is the conservative error — a
later scene excludes the bridge and *reports* the exclusion, which is a visible question,
where a widened range would be an invisible answer.

## 6. What is not modelled

The approaches, at both ends, exactly as on the North Branch bridge (`docs/LIBERTIES.md`
L30, L38). The deck stands 2.22 m above the design water surface; the modelled ground at
both landings is the traced 1834 waterline, which is Z = 0 by construction; the highest
land anywhere in the 640 m terrain box reaches 1.31 m. The 1883 statement makes the gap
*harder* to leave rather than easier, because it calls these wagon bridges: a loaded team
reached the deck somehow and nobody wrote down how.

The two bents stand at the third points of the span, 18.65 m and 37.31 m from the west
landing, because that is what a builder would do. The letter locates them by depth — "in
deeper water" — which this project cannot use: it models no riverbed. Same admission as
L31 for the North Branch.
