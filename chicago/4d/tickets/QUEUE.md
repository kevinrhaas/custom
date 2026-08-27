# QUEUE — top is next. Everything after the ticket id on a line is a label, not data.
# The owner owns this order. Reordered by an agent on 2026-08-27 on his explicit
# instruction: "reorder the queue and put items added to their correct category,
# again visible progress items first" — the second such instruction, after
# 2026-08-23's "put visible things first ... if there is some non visible ticket
# that will make a big difference or dependency then fine". Absent that
# instruction, agents still only APPEND (new) and REMOVE (done) — do not re-rank
# on your own judgement.
#
# The ordering rule, so it can be maintained rather than guessed at:
#   1. VISIBLE FIRST. AGENTS.md's test — when this merges, what is different in a
#      screenshot taken from the same spot? "See" means in the 3-D scene or on a card
#      a visitor opens. A gate, a metric, a source record and a refactor are not.
#   2. An INVISIBLE ticket outranks visible ones only when it BLOCKS them, and the
#      band it sits in has to say what it blocks.
#   3. Related work runs together, so a run can carry the context of the last one.
# The `# ---` band headers are comments; the parser reads only lines starting T-NNNN.
#
# Labels on these lines are regenerated from each ticket's own `title:` field. If a
# label and its ticket disagree, the ticket wins — one line was found mislabelled
# on 2026-08-27, damage from the `ticket.mjs restamp` bug that T-0217 records.

# --- BLOCKERS — small, and each one corrupts or blocks the work below

# --- THE TRIANGLE BUDGET — invisible, and it gates EVERY visible ticket that adds geometry
T-0229 — The full and balanced ceilings are raised on the owner's decision, and the raise expires with T-0223's timber cull
T-0147 — Re-lower the ceilings once the trims land
T-0056 — The enclosure layer pays its full triangle cost at every scene-detail level

# --- THE TOWN AND ITS STREETS — visible
T-0028 — Build out the NEXT anonymous block (one per run)
T-0240 — Randolph gets the street edge
T-0241 — Washington gets the street edge
T-0192 — The cross streets' own frontages get the street edge
T-0193 — blk_lake_clinton, the West Division block T-0069 refused
T-0194 — Hitching posts at the commercial frontages
T-0213 — Weight the trade families onto the business front
T-0182 — The household layer's two Lake-face buildings stand on a hand-authored coordinate, not on the face they front
T-0183 — The Market and South Water corner needs one control point, and the node rule may not be able to make it
T-0195 — Three South Water corner stores lap the cross street's corridor by 0.16-0.21 m, which the plat reconciliation could not reach
T-0196 — Four documented buildings still stand on Lake Street's plank walk, the same OSM-kerb fault the South Water repair answered
T-0221 — measure_street_frontage.layer_of reads a record's evidence layer off its filename, and misreads physicians_office

# --- THE RIVER, THE WHARVES AND THE GROUND — visible
T-0059 — The generator half of the wharf layer: a river-wharf mode of pier_crib
T-0134 — The south bank at the Dearborn reach has no ground outside the platted street corridor
T-0226 — North Water Street runs inside the water mask for 477 m and draws no ribbon at all
T-0219 — Finish the heightfield SOUTH to Madison Street, the plat's last tier

# --- THE FORT — visible, mostly small
T-0099 — The bank track from the fort's north gate down to the water
T-0137 — The fort's stacks are still roof-coloured, and its 1816 date fits neither chimney answer
T-0096 — Did the second Fort Dearborn carry a flagstaff, and can anything but a retrospective plate say so
T-0185 — The plate draws the fort's pickets three times coarser than the model builds them
T-0197 — Three of the fort image-accuracy table's eight rows were refuted in two days; audit the rest before building to them

# --- FABRIC AND WHAT THE BUILDINGS ARE MADE OF — visible
T-0138 — The placeholders' brick chimney is a different brick from the archetypes'
T-0212 — The one A5 roof still dealt a gable takes the shed its family gets everywhere else
T-0172 — The other three anonymous parcels still deal a retyped roof pitch, and none of them bounds an eave band by what the archetype can carry
T-0024 — May the face rule rank a store
T-0025 — Three records carry the standing constraint and say why nowhere
T-0021 — Census what the residents' figures reach

# --- WHAT GROWS, AND WHAT A PHONE SEES — visible
T-0209 — The bloom reaches 1.8 per cent of the ground the sward covers
T-0214 — Two flower-head archetypes truncate silently at their instance cap
T-0019 — Six forb layers ask for more plants than the lattice holds
T-0225 — The sward's drawn reach is measured off plants at two per cent coverage
T-0162 — SWARD_VIEWPORT=mobile deals the same census as desktop: the viewport does not reach the ring sizes

# --- MEASUREMENT, GATES AND PROVENANCE — invisible, and nothing below blocks the above
T-0227 — Is the AO bake actually too dark? Every figure that said so was wrong twice over
T-0211 — The other nine group rows are cross-checked against nothing
T-0224 — A critic baseline standing on the public square
T-0210 — The desktop smoke's stage 9 times out clicking the panel close, on an unmodified tree
T-0190 — A second street tier for the street edge, and the ceiling that refuses it
T-0164 — The rule module that decides whether a mesh is built at all now sits inside the hash of what a mesh is built from
T-0156 — The interior/silhouette discriminator counts edges internal to a layer as interior
T-0155 — The changelog stamper has the same after-publish trap the ticket tool just lost
T-0136 — The eight owner-brief plates T-0075 could not identify: Andreas at page-image level, and two museum objects
T-0055 — Hold the Kinzie-view plate as a source record
T-0053 — A patched lit material silently inherits another layer's shader program
T-0037 — The liberties gate reads the whole Evidence panel, so a liberty saying 'Three of these' fails it
T-0030 — A queue card in Manager reading tickets.json
T-0170 — The desktop smoke's part 7 has 2 m 17 s of margin, and it is the one measured over the ceiling on another runner
T-0173 — The desktop smoke's part 4 and part 5 have under a minute of margin on the ceiling, and part 7 is over it
T-0180 — The bake opens a content PR on every run, because the build stamp it writes is always dirty
T-0181 — The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin was asserted rather than measured

# --- PROBABLY ALREADY ANSWERED — verify, then withdraw. Not withdrawn by an agent.
T-0203 — The 'balanced' scene-detail ceiling is breached at Lake and Canal by 4,015 triangles
T-0218 — The 'balanced' scene-detail ceiling is breached at Lake and Canal, at both viewports

# --- NEWLY FILED — appended here by `ticket.mjs new`, which writes to the END of
# --- this file. NOT yet placed by the owner, and NOT part of the band above:
# --- these are new tickets, not tickets to withdraw.
T-0228 — Two wharf decks oversail the riverside plank walk, and the walk now meets a half-metre riser at their edge
T-0231 — T-0229's expiry was blocked on a flora ticket, so the raised ceilings would never have come down
T-0232 — The owner's production switch is a coin toss: one promotion in four never reaches a promotion step
T-0233 — Eight of seventeen dealt lots carry none of their run's own roofs, and nothing was measuring it
T-0234 — The account's GraphQL quota is exhausted while REST sits untouched, and a slice loses its PR to it
T-0235 — The unfiltered renderer smoke takes 55 minutes on the steward runner, and three tickets reason against a 30-minute cap
T-0236 — The loop's 10-minute heartbeat fires every one to four hours, and the gaps are widening
T-0238 — Two parallel slices took the same ticket, because the rule that ranks them is evaluated per-slice
T-0237 — The full ceiling has 1,145 triangles clear on the published mirror, twelve hours after T-0229 raised it
T-0239 — Nothing tests the party-line note's prose against the placement it describes
T-0242 — Two dooryard plantings are dealt onto blocked ground and refused at load, on dev
