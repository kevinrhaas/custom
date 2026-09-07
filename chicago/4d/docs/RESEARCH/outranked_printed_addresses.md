# A printed address outranked by a later printed address — the seven, ruled one by one

**Ticket:** T-0773 · **Records touched:** `data/research/newspapers/identity.json`
(`anchor_changes`) · **Tools:** `tools/measure_placement_silence.py`,
`tools/compile_gazetteer.py` § the dated anchor change ·
**Corpus:** `data/research/newspapers/extracted/` (the *Chicago Democrat*, 1833-11 to
1835-08; the *Chicago American*, 1835-06 to 1835-08)

T-0440 repaired the half of this population that is not a judgement — a house whose live
placement placed NOTHING while one of its own printings placed it, where silence does not
contradict speech. Thirteen houses were repaired by taking the earliest printing that said
something. This note is the other half: the houses whose live placement DOES place them and
which one of their own printings outranks. Preferring one printed address to another is a
statement about a house that moved or about copy that was reset, and the corpus rarely says
which, so the only instrument that may make it is the authored `anchor_changes` rule.

T-0773 listed seven. P. Pruyne & Co. left the list when T-0412 landed — the corner it
carried came off a building offered for sale by the firm and was never its own address —
so six were open when this pass ran. Each is ruled below. **One gained a rule, two were
already ruled elsewhere, two are the scene-date bound working, and one is deferred to the
ticket that owns it.** None was re-placed except through the authored rule, and the
compiler was not taught to prefer one printed address to another.

## What the report says now

`python3 tools/measure_placement_silence.py` counted all six on one line, "waiting on an
`anchor_changes` judgement". Only three of them were waiting on anything. The report now
separates the three populations, because a count that calls a settled house unsettled is
the kind of number a queue works from and should not have to correct:

| line | before | after |
|---|---:|---:|
| outranked, and waiting on an `anchor_changes` judgement | 6 | 3 |
| outranked, and the judgement has been WRITTEN | — | 1 |
| outranked only by a printing after 1835-07-01 | — | 2 |

The last two lines are not a weakening of the gate. `--check` still fails on exactly what
it failed on before — a house placed by a printing that gave no address — and the three
that are genuinely waiting are still named, still on one line, still counted.

---

## 1. G. Spring — RULED, and the placement moved

`business_g_spring`, `anchor_changes` written in `identity.json`.

Giles Spring, attorney and counsellor at law, advertised one card copy-dated **17 December
1833** through eleven printings from 1833-12-17 to 1834-11-26: *"OFFICE second door west
from the corner of Franklin and South Water streets."* From **1835-05-20** the paper carries
a different card, copy-dated **3 December 1834** — seven days after the last printing of the
old address — reading *"OFFICE, first door north from the Tre[mont] House, on
Dearborn-street"*, and it runs again on 1835-08-05.

These are two crossings of this town and not two spellings of one: Franklin and South Water
is at the west end of the business row, and the first Tremont House stands at the north-west
corner of Lake and Dearborn, some four blocks east. The identity merge of *Giles Spring* into
*G. Spring* already read both cards off the page and said the second one moves him; the rule
applies that reading to the placement rather than making a new judgement. The live placement
at the scene date of 1835-07-01 is now the Dearborn Street office.

**What the rule cannot say** is when — or whether — the office actually moved. The card that
first appears on 20 May 1835 was written five and a half months earlier, the deposit is not
the paper's whole run, and a lawyer taking a second set of rooms would read exactly like a
lawyer moving. The full `cannot_say` is on the rule; the earlier anchor is kept with its own
dates and its own eleven printings so a later pass can still tell the two cases apart.

The five readings of the Franklin corner are grouped as one landmark with its own `why`:
four spellings and one wreck of a line — *"PEHICE second door vcot from tho corner ee / of
Frankli s"* — which could only carry `the corner of Franklin [street]` with the second street
name lost to the type.

### The street had to go with it

A house's `street` is taken from whichever claim MINTS it, and `compile_register` adopts a
street face off that field rather than off the placement. So the first build of this rule
put Spring's office on Dearborn-street and left his row reading **South Water Street** — the
frontage the ruling had just retired, and the one the adoption pass would have set him on.
The street now follows the live reading wherever a rule names a single one; a corner reading
names two, and a `street` field holding both is not a street this town can adopt against, so
those are left alone. Matthias Mason & Co. is unaffected — its live reading names Main Street
and its row already did.

His register row is `street_only` on Dearborn Street rather than a building, because *"the
Tremont House"* resolves to nothing the committed town holds even though `tremont_house_1` is
in it. That is **T-0406**'s question — the Tremont House answering to the name the papers
print — and it is open with a branch on it. Nothing here touches it.

### The guard this rule broke first

Writing it exposed a defect in the mechanism. `anchor_changes` collected a house's readings
into a dict keyed by the anchor STRING, one reading per key — but a reading is grouped by its
whole placement, not by its anchor alone, and G. Spring is the one house in the corpus that
carries **one anchor string under two readings**: `the corner of Franklin and South Water
streets` is read `relative` across seven printings from 1833-12-17 and `corner` once on
1834-09-03. Keyed one-to-one, the later overwrote the earlier and the rule's history lost
seven claims and eleven months of window — and guard 4, the guard that exists to catch a
printing silently dropped, could not see it, because the anchor was still claimed. An anchor
now holds every reading printed under it. The Matthias Mason rule is unaffected: it has no
repeated anchor string, and neither does any other house.

### And the gate that then refused it

With all eleven printings visible, `compile_register.py` refused the rule outright: *"the
readings grouped under the anchor 'the corner of Franklin and South Water streets' resolve
to 2 different things in the committed town"* — a `corner` of Franklin and South Water, and
a `street` reach of South Water alone. That gate is right in principle and was wrong here,
for a reason worth writing down.

The reading it objected to is 1834-05-28, and what survives of that printing is *"[corne]r
[F]ra[n]klin and South W[at]er-str[ee]t"*. The word **of** went with the type, so
`resolve_anchor`'s corner pattern — which looks for "corner of X and Y" — does not match,
and all that resolves is the reach of South Water Street. It is the same corner, read
through a broken line.

`resolve_anchor`'s own docstring says a `street` resolution does not put a building on the
ground, and `ANCHOR_KIND_RANK` ranks it below everything that does; the anchor history
already resolves a group on its BEST reading for exactly this reason — *"'Graves' Tavern'
resolving where 'Graves' Tavern, on Main-street' does not is a fact about how much of the
sentence one reading pass swept into the field."* The gate nonetheless excused the reading
that swept in NOTHING (`unresolved`) and refused the one that swept in half. It now excuses
a `street` reach too — **but only where the placing resolution names that street.** A reach
the landmark does not name is still two places declared one landmark and still fails, and a
group that resolves to two different reaches and to nothing that places fails as well. Three
self-test cases, all firing.

## 2. J. K. Botsford — ALREADY RULED, by T-0324, and no rule may be written

`business_j_k_botsford` holds *"next door to Graves' Tavern"* (1834-02-18) and is outranked
by *"corner of Dearborn and Lake streets"*, printed from 1834-02-25 and unbroken to the end
of that year.

T-0324 read every printing of both and ruled: **the two addresses are one frontage.** Graves'
Tavern is the Mansion House, on the north side of Lake Street just east of Dearborn, and the
corner is the corner it stands on. A move was refuted outright. So no reordering is owed —
the outranking reading names the same ground the live one does.

No `anchor_changes` rule may be written here even if one were wanted, and the mechanism is
right to refuse it: the two anchors were printed in **overlapping weeks** — the tavern
reading runs 1834-02-18 to 1834-04-01, the corner reading starts 1834-02-25 — and guard 6
holds that a change is a change only where one anchor stops before the next starts.
Overlapping anchors are two standing descriptions of one house, which is exactly what T-0324
found this to be. See `docs/RESEARCH/botsford_graves_1834.md`.

## 3. Newberry & Dole — DEFERRED to T-0396, which owns the question

`business_newberry_dole` holds a `street_only` reading from 1834-03-04 and is outranked by
*"opposite to Fort Dearborn"* (1834-05-14).

T-0396 is open on this firm and asks something prior to its address: whether the partner is
Oliver Newberry or Walter L. Newberry, which the corpus reads one way in 1834 and the other
in 1835. T-0773 states plainly that it must not overtake that ticket, and the placement is
not ordered here. The reading is kept with its own date and the row stays on the waiting
line.

## 4. J. S. C. Hogan — WAITING, and the instrument is wrong rather than the evidence

`business_j_s_c_hogan` holds `{"class": "street_only", "anchor": null}` from a single
printing, 1834-03-25 c010, and is outranked by *"in South Water Street, one [door … of] the
Post Office"* — printed eight times from 1834-08-13 to **the scene date itself**, 1835-07-01.

Read the minting claim and the row dissolves. It is a two-line notice of three hundred cedar
posts under a scrap of song about fencing a garden: *"300 CEDAR POSTS, for sale che[ap] by J.
S. C. HOGAN. March [24]."* **It names no address at all.** The `street_only` class and the
`South Water Street` beside it come from the extraction's business-level `street` field,
supplied by a reader who knew where Hogan's store was, not from anything the advertisement
printed.

So this is T-0440's population — silence that does not contradict speech — wearing a
`street_only` mask, and it is invisible to that repair because the repair fires only where
the live rank is zero. Ordering these two readings needs no judgement about a house that
moved. What it needs is the compiler taught that a `street_only` naming no street and no
landmark places nothing, and T-0773 forbids teaching the compiler anything of the kind.
**Filed as its own ticket** rather than done here.

### T-0859 ruled it, and the row dissolved (2026-09-06)

The ticket filed here was taken up the same night and the answer is the one this section
predicted, with a count behind it.

**The ruling.** A `street_only` placement carrying neither a `street` nor an `anchor` names
no street, and puts a storefront on no more ground than `{"class": "none"}` does. It is a
statement about the PLACEMENT RECORD and not about the advertisement. `places_nothing()`
lives beside `placement_rank` in `compile_gazetteer.py` so the two cannot drift, and the
T-0440 repair now uses it on BOTH sides — a pass may not take up a reading it would itself
refuse to be held by. Nothing else changed: same earliest-placing tie-break, same scene-date
bound, same refusal to let one printed address override another.

**The count: twelve claims across eleven houses.** Four houses moved, and only four:

| house | before | after |
|---|---|---|
| `business_j_s_c_hogan` | `street_only` off the cedar posts | **`relative`, one door from the Post Office**, off eight printings to the scene date |
| `business_newberry_dole` | `street_only` naming no street | `relative`, *"opposite to Fort Dearborn"* — see below |
| `business_brewster_hogan_co` | `street_only` naming no street | `none` — the dissolution notice says *"at the old stand"* and no more |
| `business_david_carver` | `street_only` naming no street | `none` — the lumber notice says *"at his Store"* and no more |

The last two are the ruling paying its own way in the other direction: two houses stop being
placed on a street their own printings never named. Neither is re-placed, neither loses its
business-level `street`, and both read `unplaceable` in the register as they did before.

**Newberry & Dole is the one to argue with, and the argument is that this is not the
judgement §3 deferred.** Its `street_only` reading names no street; once that places
nothing, the firm has exactly ONE printing that places it, *"opposite to Fort Dearborn"*
(1834-05-14), and taking it is T-0440's ordinary rule — silence does not contradict
speech — applied as it is to twelve other houses. No printed address is preferred to
another, because there is only one. **T-0396's question is untouched**: it asks which
Newberry is the partner, and nothing here answers, prejudges or depends on that. The
register row is still `unplaceable` — *"Fort Dearborn"* resolves to nothing this row can
enrich — so the town does not move on it either.

**And the count turned up a defect the ruling does not fix.** Eight of the twelve notices DO
print a street in their own prose — *"a lot and Store[hous]e on South Water Street"*,
*"Dearborn-stree[t]"*, *"a shop, on Randolph street"* twice, *"at the corner of […] and
Canal streets"*, *"at his room on south water street"*, *"Montgomery's Auction Room, South
Water Street"* — and the reading pass put it in the claim's business-level `street` field
and left the placement empty. Nothing is mis-placed by it today, because
`compile_register` adopts a street face off that field; what is wrong is that the reading
does not say what the printing said. **T-0861** carries it.

**One thing written here was wrong and is corrected.** The compiler's own comment named
Jones, King & Co. as the house the scene-date bound holds — *"silent through its 1834
printings and given South Water Street on 1835-08-05"*. It is not: that 1835-08-05 notice
is a fire-insurance agency card printing no address at all, and the South Water Street
beside it is again the business-level field. The house is silent on both counts and the
bound is not what holds it. The bound is unchanged and still asserted, now on a fixture
rather than on a house that turned out not to be one.

## 5 and 6. Rockwell, and Samuel Lewis — NO JUDGEMENT IS OWED

Both are outranked only by a printing that ran **after the scene date**.

* `business_rockwell_cabinet_furniture_warehouse` is placed by 1835-06-27, *"Apply to […]
  ROCKWELL, [S]outh Wate[r street]"*, and outranked by 1835-07-04, *"[F]urniture a[t] the stand on
  S[outh] Water [s]tre[e]t, formerly occ[u]p[i]ed by Clark, [Fils?] [C]o."* — three days after the
  scene. The two do not even disagree: same street, and the later adds the stand.
* `business_samuel_lewis` is placed by 1835-07-22 and outranked by 1835-08-12, whose
  anchor is read `A. Garrett's Auction Room` off *"call at ita room pa South | ter street,
  (A. Gartetl's Auctiog Rowe)"* — **both** printings after the scene.

AGENTS.md rule 3 and the compiler's own scene bound say an address first printed after 1 July
1835 was not up on 1 July 1835. A rule preferring either of these later readings would place
a house on the strength of an advertisement that had not run yet, which no `anchor_changes`
rule may do — its live anchor is computed from the scene date for this exact reason. The
report now says so on its own line instead of counting them among the houses waiting for
someone to decide something.

---

**Links:** T-0773 · T-0440 (the silent half, repaired) · T-0345 (readings kept with their
own dates) · T-0324 · T-0396 · T-0407 · T-0412 · `tools/measure_placement_silence.py` ·
`tools/compile_gazetteer.py` § the dated anchor change.
