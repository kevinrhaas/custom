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
T-0191 — Randolph and Washington get the street edge
T-0192 — The cross streets' own frontages get the street edge
T-0193 — blk_lake_clinton, the West Division block T-0069 refused
T-0194 — Hitching posts at the commercial frontages
T-0129 — The La Salle slough is dammed by a tongue of land where the street crosses it

# --- THE RIVER AND ITS WHARVES — visible
T-0059 — The generator half of the wharf layer: a river-wharf mode of pier_crib
T-0058 — A visitor can walk out along a wharf deck
T-0134 — The south bank at the Dearborn reach has no ground outside the platted street corridor

# --- THE FORT — visible, mostly small
T-0099 — The bank track from the fort's north gate down to the water
T-0137 — The fort's stacks are still roof-coloured, and its 1816 date fits neither chimney answer
T-0096 — Did the second Fort Dearborn carry a flagstaff, and can anything but a retrospective plate say so

# --- FABRIC AND WHAT THE BUILDINGS ARE MADE OF — visible
T-0138 — The placeholders' brick chimney is a different brick from the archetypes'
T-0112 — Deal the anonymous roofs their own siding stocks, in their recipes

# --- WHAT GROWS, AND WHAT A PHONE SEES — visible
T-0031 — Where did the South Water timber belt stand

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
T-0183 — The Market and South Water corner needs one control point, and the node rule may not be able to make it
T-0182 — The household layer's two Lake-face buildings stand on a hand-authored coordinate, not on the face they front
T-0185 — The plate draws the fort's pickets three times coarser than the model builds them
T-0187 — At light detail the mid and forb rings' outer ramps dither inside the verge
T-0186 — LIBERTIES.md has no merge driver and no duplicate check, so two branches that each append L-NNN merge clean
T-0184 — Mitre the road ribbon's panel joints, so a bend stops opening a wedge of prairie
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0195 — Three South Water corner stores lap the cross street's corridor by 0.16-0.21 m, which the plat reconciliation could not reach
T-0196 — Four documented buildings still stand on Lake Street's plank walk, the same OSM-kerb fault the South Water repair answered
T-0197 — Three of the fort image-accuracy table's eight rows were refuted in two days; audit the rest before building to them
T-0188 — Apply the core density standard to blk_randolph_market, the last core block below the bar off the South Water reach (successor to T-0143)
T-0223 — The 'full' and 'balanced' ceilings are both breached on dev, with no parcel in flight that spends them
T-0221 — measure_street_frontage.layer_of reads a record's evidence layer off its filename, and misreads physicians_office
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports
T-0213 — Weight the trade families onto the business front
T-0212 — The one A5 roof still dealt a gable takes the shed its family gets everywhere else
T-0214 — Two flower-head archetypes truncate silently at their instance cap
T-0209 — The bloom reaches 1.8 per cent of the ground the sward covers
T-0211 — The other nine group rows are cross-checked against nothing
T-0208 — A party-line unit's card says its EAST wall is fixed by the WEST end of the run
T-0210 — The desktop smoke's stage 9 times out clicking the panel close, on an unmodified tree
T-0216 — dev has no standing smoke result of its own, so every branch re-derives dev's reds by hand
T-0217 — ticket.mjs restamp rewrites the WRONG queue line when the id it is repairing is the duplicated one
T-0224 — A critic baseline standing on the public square
T-0219 — Finish the heightfield SOUTH to Madison Street, the plat's last tier
T-0201 — docs/LIBERTIES.md ships committed Git conflict markers on dev and check.sh is green across them
T-0202 — SMOKE_STAGE=8-9 at desktop dies on PART 8's first click, on dev as well as on a branch
