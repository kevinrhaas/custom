# The three Main Branch sloughs — identified, and two of them built

**Investigated:** 2026-08-20 · **Ticket:** T-0005 (legacy K13) · **Epoch:** `e1834_harbor_cut` ·
**Owner's ask (twice):** "refer the 1833 map for the locations and terminus of the several
streams coming in."

## 1. What "three sloughs" is actually a citation to

The dossier line this ticket rests on — *"The 1830 Thompson plat area shows three sloughs off
the Main Branch and a 'bayou' near Wolf Point"* (`docs/research/01-terrain-hydrology.md`
§ 2.5) — cites Chicago Architecture History § 1.16, *Platting the Town of Chicago*. Checked
against the article itself: the figure whose caption reads **"The three sloughs off the Main
Branch are indicated"** is captioned *"Fort Dearborn and Environs, c. 1834 (Holland, Maps of
Chicago)"*, and that figure is a reproduction of the **Conley/Stelzer pictorial map of 1833
Chicago** — the same sheet this project holds as `conley_stelzer_1933`. The surviving
Thompson plat working copy (Wikimedia scan, ICHi-34284 lineage) is a schematic redrawing that
does not carry the watercourses. So the operative source for the three sloughs' courses and
termini is Conley/Stelzer, exactly as ROADMAP § S2e designated — with its ceiling
(`asset_use: orientation`, a 1933 reconstruction; positions reach `inferred` at best, nothing
is traced from it) — and Wright 1834, the sheet this terrain is fitted to, is the check for
the two mouths it draws.

## 2. The three, named

Read off the Leventhal IIIF scan of Conley/Stelzer (`commonwealth:0r96fm848`; north to the
right; town-grid regions at 4200,1650,700,450 and 4050,1900,800,650 of the 6660×4858 sheet),
with image→local mapping fitted on the street lines visible in each crop (La Salle at local
E +452, Clark +576, Dearborn +699, State +827; Washington N −390, Randolph −257, Lake −113,
South Water ≈ +5). Pictorial map, scale ≈ 1:5,450: readings are good to roughly 20–30 m.

| # | slough | mouth | course and terminus | state after T-0005 |
|---|---|---|---|---|
| 1 | **North-side slough** | main stem north bank near local E +190 | runs north out of the main stem, across Kinzie, ending at Michigan Street (Wright 1834, drafted band) | already carried — traced centreline `north_side_slough` in `hydrology.geojson`, carved by the generator |
| 2 | **La Salle Street slough** | Wright's traced south-shore re-entrant at E +462…+469 (`docs/RESEARCH/clark_reach_bulge_1834.md` § 4) | Conley/Stelzer: south up the west half of the La Salle–Clark block, washed as open water to about Lake Street, then a dark drain **terminating just north of Randolph** (head read at ≈ E +480–505, N −230±25) | **built** — spec swales `lasalle_slough_lower` + `lasalle_slough_upper`; the re-entrant now reaches its terminus |
| 3 | **State Street slough** (dossier zone 14) | Wright's traced re-entrant at E +850…+856 — "entered the river at the end of State Street" | chicagology_prefire273 documents the route (public-square pond → Tremont House site → foot of State); Conley/Stelzer draws the full winding course: head just east of Clark between Washington and Randolph, a mid-block Dearborn crossing ≈ N −190, then north-east under the State ridge toe | **built** — spec swales `state_slough_course` + `state_slough_mouth` |

No fourth watercourse enters the main stem on either sheet inside the modelled box. The
"bayou near Wolf Point" of the same dossier line is on the **branches** at the forks, not the
Main Branch, and is out of this ticket's scope.

## 3. The cross-check K13 asked for

*"Cross-check the State Street slough mouth the trace already carries at E +850…+856 against
dossier zone 14."* Zone 14's mouth, by the State Street ground control (State runs at about
local E +825…+838), is at E ≈ +827 at the bank; the traced re-entrant's deepest point is
(850.5, +8.2). That is a ~25 m offset, inside the combined tolerance of a pictorial route
statement and the sheet's georeferencing — the same magnitude `chicago_american_office.md`
measured for paper stretch on this quadrant — and the slough_log_bridge record already
reasons the crossing to "a little west of the mouth". Read as consistent: the traced notch
IS zone 14's mouth. The La Salle re-entrant (E +462…+469 against La Salle's platted
centreline at +452) and the north-side slough need no such reconciliation; each sits on its
own drawn feature.

## 4. Why the built form is a swale pair, not a below-datum channel

Zone 14's own row gives the thalweg as −1.5…−3.0 ft **below the adjacent plain**, i.e.
+0.5…+1.5 ft **above** the water datum: the documented slough is a damp drain in July, not a
canal. A `watercourses` entry cuts to a bed below datum and floods its whole course, which
would contradict the row it was built from. The spec's swale mechanism is already the
authored centreline-plus-half-width form (the form K13 asked for — a centreline, never a
traced boundary), so:

- the two inland courses are constant-depth swales whose beds land at +0.5…+1.1 ft against
  the committed division profiles (measured off the regenerated heightfield, not asserted);
- each slough's wet reach is a deeper entry: the La Salle mouth reach reads −0.4…−0.6 ft
  (standing backwater to about Lake Street, where Conley's wash turns from water to drain),
  and the State mouth reach is cut 6.2 ft against the State ridge toe so one connected pool
  runs from the traced notch, under the committed Slough Log Bridge deck (bed −1.8 ft;
  0.83 m deck; ~1.3 m clearance), to about N −60;
- where a deep entry meets its course entry the profiles overlap and the joint over-deepens
  (−5.0 ft at the State joint). The joint is under the pool, the water plane renders flat at
  Z = 0, and a bed under standing water is a modelling convenience here exactly as
  L31b records it for the river.

Both mouths END at the traced water: the generator's bank ramp takes the ground to Z = 0 on
the traced line, so the carved beds meet the river's own carved beds without either touching
the trace. The La Salle channel starts one cell SOUTH of the South Water corridor — Wright
draws the stream stopping at the street line, so the street crossed on fill or a culvert
nothing describes, and the corridor is left unbroken. The alignments thread every committed
structure: nearest footprint (recon_1835_south_c1_018) stands 9.1 m off the State centreline
against a 5 m half-width.

## 5. Zone 14's dating, carried over from the deferral record

Zone 14 graduated out of `data/terrain/1835_intown_water_dating.json` with this ticket. Its
dating argument, preserved: the scene commits `slough_log_bridge` standing on 1835-07-01,
whose source runs the crossing "until after 1840". A town does not build and maintain a log
crossing over dry ground, so the slough held water at the scene date on this project's own
committed reading — **inferred**, because the date arrives entirely through the thing built
over it. The standing contradiction that record named — "the scene draws the bridge and does
not draw what it crosses" — is what this ticket closes.

## 6. What is NOT built, and where it lives

- **The public-square pond (zone 15)** and **the Wells Street marsh (zone 17)** stay
  deferred and dated in the dating record: the slough drained both, but the pond's date and
  extent are one unsettled question and the marsh has no stated extent at all. The State
  slough's head therefore starts just east of Clark — where Conley draws it — and claims
  nothing about the ground it drained west of that street.
- **The Frog Pond (zone 16)**: unchanged, deferred, dated.
- The La Salle slough's head is a terminus reading from a 1933 reconstruction and nothing
  more; any period document locating the stream (a lot-survey note, a grading petition, a
  nuisance complaint) would replace it.
