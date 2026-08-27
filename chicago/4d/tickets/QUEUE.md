# QUEUE — top is next. Everything after the ticket id on a line is a label, not data.
# The owner owns this order. Reordered by an agent on 2026-08-23 on his explicit
# instruction: "put visible things first ... if there is some non visible ticket that
# will make a big difference or dependency then fine". Absent that instruction, agents
# still only APPEND (new) and REMOVE (done) — do not re-rank on your own judgement.
#
# The ordering rule, so it can be maintained rather than guessed at:
#   1. VISIBLE FIRST. AGENTS.md's test — when this merges, what is different in a
#      screenshot taken from the same spot? "See" means in the 3-D scene or on a card
#      a visitor opens. A gate, a metric, a source record and a refactor are not.
#   2. An INVISIBLE ticket outranks visible ones only when it BLOCKS them, and the
#      band it sits in has to say what it blocks.
#   3. Related work runs together, so a run can carry the context of the last one.
# The `# ---` band headers are comments; the parser reads only lines starting T-NNNN.

# --- BLOCKERS — small, and each one gates visible work below

# --- RED NOW — visible, and a gate is failing on it today

# --- THE TOWN AND ITS STREETS — visible
T-0028 — Build out the NEXT anonymous block (one per run)
T-0199 — The five South Water stores standing on a lot the roof schedule already dealt
T-0129 — The La Salle slough is dammed by a tongue of land where the street crosses it
T-0026 — The southern buildable ground and its schedule
T-0027 — How much of the public square was wet

# --- THE RIVER AND ITS WHARVES — visible
T-0059 — The generator half of the wharf layer: a river-wharf mode of pier_crib
T-0058 — A visitor can walk out along a wharf deck
T-0134 — The south bank at the Dearborn reach has no ground outside the platted street corridor

# --- THE FORT — visible, mostly small
T-0098 — Trees at the fort, which the plate puts in a mass east of the walls
T-0099 — The bank track from the fort's north gate down to the water
T-0137 — The fort's stacks are still roof-coloured, and its 1816 date fits neither chimney answer
T-0096 — Did the second Fort Dearborn carry a flagstaff, and can anything but a retrospective plate say so

# --- FABRIC AND WHAT THE BUILDINGS ARE MADE OF — visible
T-0126 — The openings-and-glazing half of the material sheet: one dark, one timber
T-0138 — The placeholders' brick chimney is a different brick from the archetypes'
T-0112 — Deal the anonymous roofs their own siding stocks, in their recipes
T-0022 — May the schedule deal log cabins to commercial frontage
T-0023 — The end rule is exhausted on the Randolph-Washington row
T-0032 — The six-roof civic target counts three that were never built

# --- WHAT GROWS, AND WHAT A PHONE SEES — visible
T-0034 — Raise the bloom, which has no bar left to raise it to
T-0031 — Where did the South Water timber belt stand
T-0157 — A phone draws the town with no antialiasing, so every edge T-0013 named crawls unresolved
T-0054 — Every liberty appended since L111 lands under the Resolved heading and compiles as resolved

# --- THE TRIANGLE BUDGET — invisible, but it governs how much can be added
T-0146 — Merge far chunks back into single draws
T-0147 — Re-lower the ceilings once the trims land
T-0089 — The 'light' scene-detail ceiling is breached, and it was breached before this run's geometry
T-0056 — The enclosure layer pays its full triangle cost at every scene-detail level

# --- MEASUREMENT, GATES AND PROVENANCE — invisible
T-0158 — The AO bake succeeds and the glTF export drops it: the shipped occlusion texture is uniformly black
T-0053 — A patched lit material silently inherits another layer's shader program
T-0162 — SWARD_VIEWPORT=mobile deals the same census as desktop: the viewport does not reach the ring sizes
T-0019 — Six forb layers ask for more plants than the lattice holds
T-0021 — Census what the residents' figures reach
T-0024 — May the face rule rank a store
T-0025 — Three records carry the standing constraint and say why nowhere
T-0037 — The liberties gate reads the whole Evidence panel, so a liberty saying 'Three of these' fails it
T-0055 — Hold the Kinzie-view plate as a source record
T-0136 — The eight owner-brief plates T-0075 could not identify: Andreas at page-image level, and two museum objects
T-0155 — The changelog stamper has the same after-publish trap the ticket tool just lost
T-0156 — The interior/silhouette discriminator counts edges internal to a layer as interior
T-0164 — The rule module that decides whether a mesh is built at all now sits inside the hash of what a mesh is built from
T-0030 — A queue card in Manager reading tickets.json
T-0170 — The desktop smoke's part 7 has 2 m 17 s of margin, and it is the one measured over the ceiling on another runner
T-0172 — The other three anonymous parcels still deal a retyped roof pitch, and none of them bounds an eave band by what the archetype can carry
T-0173 — The desktop smoke's part 4 and part 5 have under a minute of margin on the ceiling, and part 7 is over it
T-0180 — The bake opens a content PR on every run, because the build stamp it writes is always dirty
T-0181 — The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin was asserted rather than measured
T-0179 — Three families offer a shed roof their own ridge band cannot carry: C1, F1 and F4
T-0183 — The Market and South Water corner needs one control point, and the node rule may not be able to make it
T-0182 — The household layer's two Lake-face buildings stand on a hand-authored coordinate, not on the face they front
T-0185 — The plate draws the fort's pickets three times coarser than the model builds them
T-0187 — At light detail the mid and forb rings' outer ramps dither inside the verge
T-0186 — LIBERTIES.md has no merge driver and no duplicate check, so two branches that each append L-NNN merge clean
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0189 — A house on Washington is told it is 'one unit of the party-line river row'
T-0197 — Three of the fort image-accuracy table's eight rows were refuted in two days; audit the rest before building to them
T-0188 — Apply the core density standard to blk_randolph_market, the last core block below the bar off the South Water reach (successor to T-0143)
T-0208 — North Water Street runs inside the water mask for 477 m and draws no ribbon at all
